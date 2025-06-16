from typing import Tuple
from playwright.async_api import (
    async_playwright,
    TimeoutError,
    Error as PlaywrightError,
)
from models.marketplace import Marketplace


async def scrape_product_data(
    marketplace: Marketplace, product_name: str
) -> Tuple[str, str, str]:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
        )
        page = await context.new_page()
        search_url = f"{marketplace.base_search_url}{product_name.replace(' ', '+')}"
        try:
            await page.goto(search_url, timeout=10000)
        except PlaywrightError as exc:
            await browser.close()
            raise RuntimeError(f"{marketplace.name} is not reachable: {exc}")

        # Check if product exists
        try:
            await page.wait_for_selector(marketplace.product_selector, timeout=5000)
            if not await page.locator(marketplace.product_selector).count():
                await browser.close()
                raise RuntimeError(f"No product found on {marketplace.name}")
        except TimeoutError:
            await browser.close()
            raise RuntimeError(
                f"Selector error: {marketplace.product_selector} on {marketplace.name}"
            )

        # Extract product title
        try:
            await page.wait_for_selector(marketplace.title_selector, timeout=5000)
            title = await page.locator(marketplace.title_selector).first.inner_text()
            if not title or not title.strip():
                await browser.close()
                raise RuntimeError(f"Title not found on {marketplace.name}")
        except (TimeoutError, PlaywrightError):
            await browser.close()
            raise RuntimeError(
                f"Title selector failed: {marketplace.title_selector} on {marketplace.name}"
            )

        # Extract price
        try:
            await page.wait_for_selector(marketplace.price_selector, timeout=5000)
            price = await page.locator(marketplace.price_selector).first.inner_text()
            if not price or not price.strip():
                await browser.close()
                raise RuntimeError(f"Price not found on {marketplace.name}")
        except (TimeoutError, PlaywrightError):
            await browser.close()
            raise RuntimeError(
                f"Price selector failed: {marketplace.price_selector} on {marketplace.name}"
            )

        # Extract product URL
        try:
            await page.wait_for_selector(marketplace.link_selector, timeout=5000)
            link = await page.locator(marketplace.link_selector).first.get_attribute(
                "href"
            )
            if not link or not link.strip():
                await browser.close()
                raise RuntimeError(f"URL not found on {marketplace.name}")
        except (TimeoutError, PlaywrightError):
            await browser.close()
            raise RuntimeError(
                f"URL selector failed: {marketplace.link_selector} on {marketplace.name}"
            )

        await browser.close()
        return title, price, link
