const playwright = require('playwright');

async function renderPage(url) {
  // Launch a browser instance (Chromium by default)
  const browser = await playwright.chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Navigate to the given URL
    await page.goto(url, { waitUntil: 'networkidle' }); // Wait for network to be idle

    // Take a screenshot
    const screenshotPath = 'screenshot.png';
    await page.screenshot({ path: screenshotPath });

    // Extract page content
    const html = await page.content();

    return { html: html, screenshotPath: screenshotPath };
  } finally {
    // Ensure browser is closed even if errors occur
    await browser.close();
  }
}

module.exports = { renderPage };

// Simple test call
if (require.main === module) {
  (async () => {
    try {
      console.log('Testing renderPage with https://example.com...');
      const result = await renderPage('https://example.com');
      console.log(`HTML content length: ${result.html.length}`);
      console.log(`Screenshot saved to: ${result.screenshotPath}`);

      // Verify screenshot existence (optional, for more robust testing)
      const fs = require('fs');
      if (fs.existsSync(result.screenshotPath)) {
        console.log('Screenshot file successfully created.');
      } else {
        console.error('Error: Screenshot file not found!');
      }
    } catch (error) {
      console.error('Error during test run:', error);
    }
  })();
}
