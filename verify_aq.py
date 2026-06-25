import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Marketplace frontend URL
        url = "http://localhost:5173"

        try:
            await page.goto(url)
            await page.wait_for_timeout(3000)

            # Search for Airtable
            search_input = page.get_by_placeholder("Search for agents, roles, or domains...")
            await search_input.fill("Airtable")
            await page.wait_for_timeout(2000)
            await page.screenshot(path="v_airtable.png")
            print("Captured v_airtable.png")

            # Search for QuickBooks
            await search_input.fill("")
            await search_input.fill("QuickBooks")
            await page.wait_for_timeout(2000)
            await page.screenshot(path="v_quickbooks.png")
            print("Captured v_quickbooks.png")

        except Exception as e:
            print(f"Error during verification: {e}")
            await page.screenshot(path="v_error_aq.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
