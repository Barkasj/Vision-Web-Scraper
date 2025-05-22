import asyncio
import os
# When running this example script from the root of the project (e.g., `python rendering_engine/example.py`),
# the following import should work if the Python path is set up correctly or if `rendering_engine` is a package.
# If `rendering_engine` is intended to be installed or used as a module in a larger project,
# this might become `from rendering_engine.core.browser import HeadlessBrowser`.
# For direct script execution from project root, assuming `PYTHONPATH` includes the project root:
from core.browser import HeadlessBrowser

async def main():
    # Ensure 'output' directory exists within 'rendering_engine'
    output_dir = "output" 
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Initialize HeadlessBrowser
    # Using chromium by default. You can try 'firefox' or 'webkit' if installed.
    print("Initializing HeadlessBrowser with Chromium...")
    async with HeadlessBrowser(browser_type='chromium') as browser:
        print("HeadlessBrowser initialized.")

        # --- Example 1: Capture a screenshot ---
        screenshot_url = 'http://example.com'
        screenshot_path = os.path.join(output_dir, "example_screenshot.png")
        print(f"\nAttempting to capture screenshot of '{screenshot_url}' to {screenshot_path}...")
        try:
            await browser.capture_screenshot(screenshot_url, screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            if not os.path.exists(screenshot_path) or os.path.getsize(screenshot_path) == 0:
                print(f"Warning: Screenshot file at {screenshot_path} is missing or empty.")
            else:
                print(f"Screenshot file at {screenshot_path} exists and is not empty.")

        except Exception as e:
            print(f"Error capturing screenshot for {screenshot_url}: {e}")

        # --- Example 2: Extract HTML ---
        html_url = 'http://example.com'
        print(f"\nAttempting to extract HTML from '{html_url}'...")
        try:
            html_content = await browser.extract_html(html_url)
            print(f"Extracted HTML from {html_url} (first 200 chars):")
            print(html_content[:200] + "...")
        except Exception as e:
            print(f"Error extracting HTML from {html_url}: {e}")

        # --- Example 3: Get cookies ---
        # example.com might not set many interesting cookies.
        # Using a site known for setting cookies for demonstration.
        # httpbin.org is good for this.
        cookie_url = 'https://httpbin.org/cookies/set?mycookie=myvalue&anothercookie=anothervalue'
        print(f"\nAttempting to get cookies from '{cookie_url}'...")
        try:
            # First, visit the page to ensure cookies are set by the server
            await browser.extract_html(cookie_url) # visit the page first
            # Then, get the cookies from the context
            cookies = await browser.get_cookies(cookie_url)
            print(f"Cookies from {cookie_url}:")
            if cookies:
                for cookie in cookies:
                    print(f"  - {cookie.get('name')}: {cookie.get('value')}")
            else:
                print("  No cookies found.")
        except Exception as e:
            print(f"Error getting cookies from {cookie_url}: {e}")
        
        # --- Example 4: Set Cookies (and then get them) ---
        # This example demonstrates setting cookies and then retrieving them.
        # We'll set cookies for httpbin.org/cookies, then navigate to it and check.
        set_cookie_url = 'https://httpbin.org/cookies'
        custom_cookies = [
            {'name': 'MyCustomCookie', 'value': 'SetByPlaywright', 'domain': 'httpbin.org', 'path': '/'},
            {'name': 'AnotherCustom', 'value': 'SuperValue', 'domain': 'httpbin.org', 'path': '/cookies'}
        ]
        print(f"\nAttempting to set cookies for '{set_cookie_url}' and then retrieve them...")
        try:
            # Set cookies
            await browser.set_cookies(set_cookie_url, custom_cookies) # Using the URL for context, cookies have domain
            print(f"  Custom cookies presumably set for domain related to {set_cookie_url}.")

            # Navigate to the page and retrieve HTML (to see if cookies are reflected, though httpbin shows them in JSON)
            html_after_set = await browser.extract_html(set_cookie_url)
            print(f"  HTML from {set_cookie_url} after setting cookies (first 300 chars):")
            print(html_after_set[:300] + "...")
            
            # Get cookies again to verify
            cookies_after_set = await browser.get_cookies(set_cookie_url)
            print(f"  Cookies from {set_cookie_url} after attempting to set custom ones:")
            found_custom = False
            if cookies_after_set:
                for cookie in cookies_after_set:
                    print(f"    - {cookie.get('name')}: {cookie.get('value')}")
                    if cookie.get('name') in ['MyCustomCookie', 'AnotherCustom']:
                        found_custom = True
                if found_custom:
                    print("  Successfully retrieved custom set cookies.")
                else:
                    print("  Custom set cookies were not found in the retrieved list.")
            else:
                print("  No cookies found after setting.")
        except Exception as e:
            print(f"Error in set/get cookies example for {set_cookie_url}: {e}")

    print("\nExample script finished.")

if __name__ == "__main__":
    # This setup assumes the script is run from the project's root directory
    # (i.e., the directory containing the `rendering_engine` folder and `requirements.txt`)
    # To make imports work correctly, ensure your PYTHONPATH includes the project root,
    # or run as a module: `python -m rendering_engine.example`
    
    # Add project root to Python path for direct execution
    import sys
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Now the import `from core.browser import HeadlessBrowser` (or potentially `from rendering_engine.core.browser ...`)
    # should work when this script is executed directly.
    # The example file itself is inside `rendering_engine`, so `from core.browser...` is appropriate
    # if the `rendering_engine` directory itself is treated as a path root for its internal modules.
    # However, standard practice would be to run from project root and use `from rendering_engine.core.browser ...`
    # The current import `from core.browser import HeadlessBrowser` implies that `rendering_engine` is in PYTHONPATH
    # or the script is run from within `rendering_engine` with `..` added to path for `core`.
    
    # The following adjustment ensures that `from core.browser import HeadlessBrowser` works
    # when `example.py` is run from *within* the `rendering_engine` directory
    # or when `rendering_engine` directory is in PYTHONPATH.
    # If running `python rendering_engine/example.py` from the project root,
    # the `sys.path.insert(0, project_root)` above helps.
    # If the script is run as `python example.py` from *inside* `rendering_engine`, this works:
    if os.path.basename(os.getcwd()) == "rendering_engine":
        sys.path.insert(0, os.path.abspath('..')) # Add parent dir to path to find `rendering_engine` package
        from core.browser import HeadlessBrowser # This will work
    else: # Assuming run from project root as `python rendering_engine/example.py`
        # The original import `from core.browser import HeadlessBrowser` will fail unless
        # `rendering_engine` itself is in PYTHONPATH.
        # The sys.path modification earlier should allow `from rendering_engine.core.browser import HeadlessBrowser`
        # Let's adjust the import to be robust for execution from project root.
        try:
            from core.browser import HeadlessBrowser # Works if rendering_engine is in PYTHONPATH or running from inside it
        except ModuleNotFoundError:
            from rendering_engine.core.browser import HeadlessBrowser # Works if running from project root with root in PYTHONPATH

    print("Starting asyncio event loop for main()...")
    asyncio.run(main())
