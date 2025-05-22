# Rendering Engine Module

## Purpose

The `rendering_engine` module provides capabilities to render web pages using a headless browser (via Playwright), capture screenshots, extract HTML content, and manage cookies. It is designed to be a foundational component for web automation and data extraction tasks that require full browser rendering capabilities.

## Features

*   **Playwright-Based:** Leverages Playwright for robust headless browser automation, supporting Chromium, Firefox, and WebKit.
*   **Screenshot Capture:** Capture full or partial page screenshots in PNG or JPEG format.
*   **HTML Extraction:** Extract HTML content after JavaScript execution.
*   **Cookie Management:** Get and set cookies for web pages.
*   **Asynchronous API:** Designed for asynchronous operations using `async/await`.
*   **Extensibility (Placeholders):** Includes placeholder components for future integration of:
    *   Proxy rotation (`ProxyRotator`)
    *   Browser fingerprint spoofing (`FingerprintSpoofer`)

## Setup

1.  **Install Dependencies:**
    Navigate to the project root directory (the parent directory of `rendering_engine`) and run:
    ```bash
    pip install -r requirements.txt
    ```
    This will install Playwright and any other necessary Python packages.

2.  **Install Playwright Browsers:**
    After installing the Python package, you need to download the browser binaries for Playwright:
    ```bash
    playwright install
    ```
    You can also install specific browsers (e.g., `playwright install chromium`).

## Basic Usage

The primary interface to the rendering engine is the `HeadlessBrowser` class found in `rendering_engine.core.browser`.

Here's a brief example of how to use it:

```python
import asyncio
from rendering_engine.core.browser import HeadlessBrowser # Assuming project root is in PYTHONPATH

async def run_browser_tasks():
    async with HeadlessBrowser(browser_type='chromium') as browser:
        # Capture a screenshot
        await browser.capture_screenshot('http://example.com', 'output/example.png')
        print("Captured screenshot of example.com")

        # Extract HTML
        html = await browser.extract_html('http://example.com')
        print(f"HTML from example.com (first 100 chars): {html[:100]}...")

        # Get cookies
        cookies = await browser.get_cookies('https://httpbin.org/cookies/set?test=value')
        print(f"Cookies from httpbin: {cookies}")

if __name__ == "__main__":
    # Create an 'output' directory if it doesn't exist
    import os
    if not os.path.exists("output"):
        os.makedirs("output")
    
    asyncio.run(run_browser_tasks())
```

For a more detailed demonstration, see the `example.py` script located within the `rendering_engine` directory. You can run it from the project root using:
```bash
python -m rendering_engine.example
```
Or, if `rendering_engine` is in your `PYTHONPATH`, you might be able to run it directly:
```bash
python rendering_engine/example.py
```
Ensure the `output` directory exists in the context where the script is run (or is created by the script, as `example.py` does).

## Directory Structure

*   `core/`: Contains the main logic of the rendering engine.
    *   `browser.py`: Defines the `HeadlessBrowser` class for browser interactions.
    *   `network.py`: Contains placeholder classes for network-related functionalities like proxy rotation (`ProxyRotator`) and fingerprint spoofing (`FingerprintSpoofer`).
    *   `__init__.py`: Makes `core` a Python package.
*   `utils/`: Intended for utility functions and helper classes (currently empty).
    *   `__init__.py`: Makes `utils` a Python package.
*   `example.py`: A script demonstrating common use cases of the `HeadlessBrowser`.
*   `README.md`: This file.
*   `__init__.py`: Makes `rendering_engine` a Python package.

---

This module is under development. Advanced features and error handling will be improved over time.
