from playwright.async_api import async_playwright
from .network import ProxyRotator, FingerprintSpoofer

class HeadlessBrowser:
    def __init__(self, browser_type='chromium', proxy_rotator_config=None, fingerprint_spoofer_config=None):
        """
        Initializes the HeadlessBrowser.
        Args:
            browser_type (str): Type of browser to launch ('chromium', 'firefox', 'webkit').
            proxy_rotator_config (dict, optional): Configuration for ProxyRotator.
            fingerprint_spoofer_config (dict, optional): Configuration for FingerprintSpoofer.
        """
        self.playwright = None
        self.browser = None
        self.browser_type = browser_type.lower()
        self.proxy_rotator = None
        self.fingerprint_spoofer = None

        if self.browser_type not in ['chromium', 'firefox', 'webkit']:
            raise ValueError(f"Unsupported browser type: {browser_type}. Choose 'chromium', 'firefox', or 'webkit'.")

        if proxy_rotator_config:
            self.proxy_rotator = ProxyRotator(config=proxy_rotator_config)
        
        if fingerprint_spoofer_config:
            self.fingerprint_spoofer = FingerprintSpoofer(config=fingerprint_spoofer_config)

    async def __aenter__(self):
        """
        Asynchronous context manager entry point.
        Starts Playwright and launches the browser.
        """
        try:
            self.playwright = await async_playwright().start()
            
            launch_options = {}
            if self.proxy_rotator:
                proxy_settings = self.proxy_rotator.get_proxy()
                if proxy_settings:
                    # Example: launch_options['proxy'] = proxy_settings 
                    # The actual key and format depend on Playwright's proxy configuration.
                    # e.g., {'server': 'http://myproxy.com:3128', 'username': 'user', 'password': 'password'}
                    print(f"Placeholder: Would apply proxy settings: {proxy_settings}") # Placeholder
                    # launch_options['proxy'] = proxy_settings # Actual integration

            if self.fingerprint_spoofer:
                fp_args = self.fingerprint_spoofer.get_fingerprint_args()
                # Example: launch_options.update(fp_args)
                # fp_args could include 'user_agent', 'viewport', 'locale', etc.
                print(f"Placeholder: Would apply fingerprint args: {fp_args}") # Placeholder
                # launch_options.update(fp_args) # Actual integration

            if self.browser_type == 'chromium':
                self.browser = await self.playwright.chromium.launch(**launch_options)
            elif self.browser_type == 'firefox':
                self.browser = await self.playwright.firefox.launch(**launch_options)
            elif self.browser_type == 'webkit':
                self.browser = await self.playwright.webkit.launch(**launch_options)
            else:
                # This case should ideally be caught by the __init__ constructor,
                # but as a safeguard:
                await self.playwright.stop()
                raise ValueError(f"Unsupported browser type: {self.browser_type}")
            return self
        except Exception as e:
            # If playwright was started, ensure it's stopped on error
            if self.playwright:
                await self.playwright.stop()
            raise RuntimeError(f"Failed to start Playwright or launch browser: {e}")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Asynchronous context manager exit point.
        Closes the browser and stops Playwright.
        """
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def new_page(self, url: str, resolution: tuple = (1920, 1080)):
        """
        Creates a new browser page, sets its viewport, and navigates to a URL.
        Args:
            url (str): The URL to navigate to.
            resolution (tuple): A tuple (width, height) for the viewport size.
        Returns:
            playwright.async_api.Page: The created page object.
        """
        if not self.browser:
            raise RuntimeError("Browser is not launched. Use 'async with HeadlessBrowser() as browser:'")
        
        # Placeholder: page_options = {}
        # if self.fingerprint_spoofer:
        #     # This is a conceptual placement for page-specific fingerprinting.
        #     # Playwright allows setting things like user_agent, extra_http_headers, viewport, etc.
        #     # per context or per page.
        #     # page_specific_fp_args = self.fingerprint_spoofer.get_page_specific_fingerprint_args(url) # Hypothetical method
        #     # if page_specific_fp_args:
        #     #     page_options.update(page_specific_fp_args)
        #     #
        #     # If creating a new context:
        #     # context = await self.browser.new_context(**page_options)
        #     # page = await context.new_page()
        #     # Else, if applying to a page directly (some options might not be available here):
        #     # page = await self.browser.new_page(**page_options) # Check Playwright docs for what can be passed here
        #     print(f"Placeholder: Would consider page-specific fingerprint args for {url}")

        page = await self.browser.new_page() # Potentially with page_options if Playwright supports them here
        await page.set_viewport_size({'width': resolution[0], 'height': resolution[1]})
        # If extra_http_headers are part of fingerprint, they can be set here:
        # if self.fingerprint_spoofer and 'extra_http_headers' in page_options:
        #    await page.set_extra_http_headers(page_options['extra_http_headers'])
        await page.goto(url, wait_until='load')
        return page

    async def close_page(self, page):
        """
        Closes the given browser page.
        Args:
            page (playwright.async_api.Page): The page object to close.
        """
        if page:
            await page.close()

    async def capture_screenshot(self, url: str, output_path: str, resolution: tuple = (1920, 1080), screenshot_type: str = 'png', full_page: bool = False):
        """
        Navigates to a URL and captures a screenshot.
        Args:
            url (str): The URL to navigate to.
            output_path (str): The path to save the screenshot.
            resolution (tuple): A tuple (width, height) for the viewport size.
            screenshot_type (str): Type of screenshot ('png' or 'jpeg'). Defaults to 'png'.
            full_page (bool): Whether to capture the full scrollable page. Defaults to False.
        """
        if not self.browser:
            raise RuntimeError("Browser is not launched. Use 'async with HeadlessBrowser() as browser:'")
        
        if screenshot_type not in ['png', 'jpeg']:
            raise ValueError("Unsupported screenshot type. Choose 'png' or 'jpeg'.")

        page = None
        try:
            page = await self.new_page(url, resolution)
            await page.screenshot(path=output_path, type=screenshot_type, full_page=full_page)
        except Exception as e:
            # Log or handle the exception appropriately
            # For now, re-raising to make it visible to the caller
            raise RuntimeError(f"Failed to capture screenshot for {url}: {e}")
        finally:
            if page:
                await self.close_page(page)

    async def extract_html(self, url: str, resolution: tuple = (1920, 1080)):
        """
        Navigates to a URL and extracts its HTML content after JavaScript execution.
        Args:
            url (str): The URL to navigate to.
            resolution (tuple): A tuple (width, height) for the viewport size.
        Returns:
            str: The extracted HTML content.
        """
        if not self.browser:
            raise RuntimeError("Browser is not launched. Use 'async with HeadlessBrowser() as browser:'")

        page = None
        html_content = ""
        try:
            page = await self.new_page(url, resolution)
            html_content = await page.content()
        except Exception as e:
            # Log or handle the exception appropriately
            # For now, re-raising to make it visible to the caller
            raise RuntimeError(f"Failed to extract HTML from {url}: {e}")
        finally:
            if page:
                await self.close_page(page)
        return html_content

    async def get_cookies(self, url: str, resolution: tuple = (1920, 1080)):
        """
        Navigates to a URL and retrieves cookies from the page's context.
        Args:
            url (str): The URL to navigate to (cookies are typically domain-specific).
            resolution (tuple): A tuple (width, height) for the viewport size.
        Returns:
            list: A list of cookie dictionaries.
        """
        if not self.browser:
            raise RuntimeError("Browser is not launched. Use 'async with HeadlessBrowser() as browser:'")

        page = None
        cookies = []
        try:
            page = await self.new_page(url, resolution)
            cookies = await page.context.cookies()
        except Exception as e:
            raise RuntimeError(f"Failed to get cookies from {url}: {e}")
        finally:
            if page:
                await self.close_page(page)
        return cookies

    async def set_cookies(self, url: str, cookies: list, resolution: tuple = (1920, 1080)):
        """
        Navigates to a URL and sets cookies in the page's context.
        Args:
            url (str): The URL to navigate to (cookies are typically domain-specific).
            cookies (list): A list of cookie dictionaries to set.
            resolution (tuple): A tuple (width, height) for the viewport size.
        """
        if not self.browser:
            raise RuntimeError("Browser is not launched. Use 'async with HeadlessBrowser() as browser:'")

        page = None
        try:
            page = await self.new_page(url, resolution)
            await page.context.add_cookies(cookies)
        except Exception as e:
            raise RuntimeError(f"Failed to set cookies for {url}: {e}")
        finally:
            if page:
                await self.close_page(page)
        # Optionally, return True or some status
        return True

# Example usage (for testing purposes, will not be part of the final file for this subtask)
# async def main():
#     print("Starting browser...")
#     try:
#         async with HeadlessBrowser(browser_type='chromium') as browser_manager:
#             print("Browser manager created. Opening new page...")
#             # page = await browser_manager.new_page("http://example.com")
#             # print(f"Page title: {await page.title()}")
#             # await browser_manager.close_page(page)
#             # print("Page closed.")
#             await browser_manager.capture_screenshot("http://example.com", "example.png")
#             print("Screenshot captured for example.com")
#             await browser_manager.capture_screenshot("https://playwright.dev/python", "playwright_python.jpeg", screenshot_type='jpeg', full_page=True)
#             print("Full page screenshot captured for playwright.dev/python")
#
#             html = await browser_manager.extract_html("http://example.com")
#             print(f"Extracted HTML from example.com (first 100 chars): {html[:100]}")
#
#             # Cookie example (using a site that sets cookies)
#             cookie_url = "https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending"
#             await browser_manager.capture_screenshot(cookie_url, "cookie_site_before.png")
#             initial_cookies = await browser_manager.get_cookies(cookie_url)
#             print(f"Initial cookies from {cookie_url}: {initial_cookies}")
#
#             # Example of setting a cookie
#             # Note: Cookie domains are strict. This cookie might not be 'settable' for example.com
#             # depending on its domain/path attributes. For a real test, use a site you control.
#             my_cookies = [{'name': 'TestCookie', 'value': 'TestValue', 'domain': '.example.com', 'path': '/'}]
#             await browser_manager.set_cookies("http://example.com", my_cookies)
#             # To verify, you'd typically navigate to a page on example.com and check if the cookie is sent.
#             # Or use get_cookies on an example.com URL.
#             # For this example, we'll just print a success message.
#             print(f"Attempted to set cookies for example.com.")
#             # cookies_after_set = await browser_manager.get_cookies("http://example.com")
#             # print(f"Cookies from example.com after setting: {cookies_after_set}")


#         print("Browser manager exited.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     import asyncio
#     # Ensure playwright browsers are installed
#     # import os
#     # os.system("playwright install") # This should be done once, not in every run.
#     asyncio.run(main())
