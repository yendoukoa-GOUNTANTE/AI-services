import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.set_default_timeout(60000)

        try:
            print("Navigating to frontend...")
            await page.goto("http://localhost:5173")

            # Wait for content
            await page.wait_for_selector("text=Official Services")
            print("Page loaded.")

            # Search for Twilio
            print("Searching for Twilio...")
            search_input = page.get_by_placeholder("Search for agents, roles, or domains...")
            await search_input.fill("Twilio")
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(2000)

            # Scroll down
            await page.evaluate("window.scrollTo(0, 1000)")
            await page.wait_for_timeout(1000)
            await page.screenshot(path="twilio_search_final.png")

            # Click Twilio Architect (corrected name from Strategist in App.tsx)
            print("Opening Twilio modal...")
            await page.click("text=Twilio Architect")
            await page.wait_for_timeout(2000)
            await page.screenshot(path="twilio_modal_final.png")

            print("Verification finished.")

        except Exception as e:
            print(f"Error: {e}")
            await page.screenshot(path="twilio_error.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
