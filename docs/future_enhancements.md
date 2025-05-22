# Future Enhancements for Vision-Web-Scraper

This document outlines planned future enhancements and conceptual approaches for advanced features, based on the project's long-term goals.

## 1. Real-Time Price Tracking

**Goal:** Automatically track price changes for specific products across various e-commerce sites and notify users or trigger actions.

**Conceptual Approach:**

*   **Product Watchlist:**
    *   A system (database table or dedicated service) to manage a list of product URLs that need to be tracked.
    *   Users or other systems can add/remove URLs from this list.
*   **Scheduled Scraping:**
    *   A job scheduler (e.g., Celery, Apache Airflow, Kubernetes CronJobs, or a simpler Go-based scheduler) will periodically trigger scraping tasks for URLs in the watchlist.
    *   The frequency of scraping can be configurable per product or globally.
*   **Data Storage & Comparison:**
    *   Extracted product data (especially price, currency, and timestamp) will be stored in a time-series friendly way (e.g., a dedicated table in PostgreSQL with product ID, price, timestamp, or a time-series database like InfluxDB/TimescaleDB).
    *   The Neo4j graph can also store price history as properties or related nodes.
    *   After each scrape, the new price is compared against the previously recorded price for that product.
*   **Change Detection & Notification:**
    *   If a price change (or stock status change) is detected:
        *   The change is logged.
        *   A notification system is triggered. This could involve:
            *   Sending emails to subscribed users.
            *   Sending webhooks to external services.
            *   Pushing messages to a WebSocket for real-time dashboard updates.
            *   Creating alerts in a monitoring system.
*   **Backend Logic:**
    *   The `backend` service would need new endpoints or internal logic to manage watchlists and process price history.
    *   The `parser` might need to be enhanced to reliably extract stock availability if that's also to be tracked.

## 2. Anti-Bot Evasion Measures

**Goal:** Improve the scraper's ability to access web pages that are protected by anti-bot technologies.

**Conceptual Approach:**

*   **Rotating Proxies:**
    *   Integrate with third-party proxy services (e.g., Bright Data, Oxylabs, Smartproxy) or set up a custom proxy rotation mechanism.
    *   The `renderer` service (Playwright) would need to be configured to use these proxies for outgoing requests.
    *   Proxy selection could be random, round-robin, or based on proxy health/performance.
*   **User-Agent Randomization:**
    *   Maintain a list of common and valid browser user-agent strings.
    *   The `renderer` service should rotate user-agents for each request or session.
*   **Headless Browser Fingerprint Management:**
    *   Headless browsers can sometimes be detected. Techniques to mitigate this include:
        *   Using Playwright Stealth or similar plugins (if available and effective).
        *   Customizing browser launch arguments to mimic normal browser behavior.
        *   Ensuring JavaScript properties (like `navigator.webdriver`) are not easily identifiable as automated.
*   **CAPTCHA Solving Services:**
    *   For sites with CAPTCHAs, integrate with CAPTCHA solving services (e.g., 2Captcha, Anti-CAPTCHA).
    *   This would involve:
        *   Detecting when a CAPTCHA is presented (this can be complex).
        *   Sending the CAPTCHA challenge (image, site key) to the solving service.
        *   Receiving the solution and submitting it to the website.
    *   This adds cost and complexity.
*   **Rate Limiting & Polite Scraping:**
    *   Implement configurable delays between requests to the same domain to avoid overwhelming servers.
    *   Respect `robots.txt` where appropriate (though for specific data extraction, this might be selectively bypassed if terms of service allow).
*   **Session Management:**
    *   For sites requiring logins or multi-step interactions, manage browser sessions (cookies, local storage) effectively.
*   **Retry Mechanisms & Error Handling:**
    *   Implement robust retry logic for failed requests, possibly with backoff strategies and proxy rotation on failure.

## 3. Scalability Considerations

*   **Distributed Task Queues:** Use message queues (e.g., RabbitMQ, Kafka, Redis Streams) to manage scraping jobs, allowing multiple `renderer` and `cv_service` instances to process tasks in parallel.
*   **Autoscaling:** Design services to be horizontally scalable. Container orchestration platforms like Kubernetes can manage autoscaling based on load.
*   **Optimized CV Models:** Use efficient CV models and consider hardware acceleration (GPUs) for the `cv_service` if performance is critical.
*   **Database Optimization:** Ensure the database (Neo4j, PostgreSQL, etc.) is optimized for the expected read/write load.
