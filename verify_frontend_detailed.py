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

            # Accept cookies if present
            try:
                await page.click("text=Accept All", timeout=5000)
                print("Cookies accepted.")
            except:
                print("Cookie banner not found or already accepted.")

            # Search and verify Flutterwave
            print("Verifying Flutterwave...")
            search_input = page.get_by_placeholder("Search for agents, roles, or domains...")
            await search_input.fill("Flutterwave")
            await page.wait_for_timeout(1000)

            # Click the card
            await page.click("text=Flutterwave Specialist")
            await page.wait_for_timeout(2000)
            await page.screenshot(path="v_flutterwave_modal.png")

            # Close modal
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(1000)

            # Search and verify Twilio
            print("Verifying Twilio...")
            await search_input.fill("")
            await search_input.fill("Twilio")
            await page.wait_for_timeout(1000)

            # Click the card
            await page.click("text=Twilio Strategist")
            await page.wait_for_timeout(2000)
            await page.screenshot(path="v_twilio_modal.png")

            # Check for Messaging Channel toggle in Twilio modal
            print("Checking for Messaging Channel toggle...")
            has_toggle = await page.is_visible("text=Messaging Channel")
            print(f"Messaging Channel toggle visible: {has_toggle}")

            print("Verification finished.")

        except Exception as e:
            print(f"Error: {e}")
            await page.screenshot(path="v_error.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
