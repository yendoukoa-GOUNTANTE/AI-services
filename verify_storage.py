import asyncio
from playwright.async_api import async_playwright
import os

async def verify_file_storage():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to the app
        await page.goto("http://localhost:3000")
        await page.wait_for_selector("text=AI Specialist Marketplace")

        # Register/Login
        await page.click("nav >> text=Login / Register")
        await page.wait_for_selector("h3:has-text('Join Yendoukoa AI')")
        await page.fill('input[placeholder="Choose a username"]', "testuser_file_2")
        # Click the register button inside the modal
        await page.click('form >> button:has-text("Register")')

        # Wait for dashboard/user info
        await page.wait_for_selector("text=testuser_file_2")

        # Switch to dashboard
        await page.click("text=Dashboard")

        # Verify File Storage section
        await page.wait_for_selector("text=File Storage Specialist")

        # Switch back to marketplace and generate something
        await page.click("text=Marketplace")
        await page.click('text=Website Developer >> xpath=.. >> text=Use Now')
        await page.fill('textarea', "My test website")
        await page.click('button:has-text("Run Service")')

        # Wait for response and save
        await page.wait_for_selector("text=Save to Storage", timeout=60000)

        # Accept alert
        page.on("dialog", lambda dialog: dialog.accept())
        await page.click("text=Save to Storage")

        # Check dashboard again
        await page.click("text=Dashboard")
        await page.wait_for_selector("text=Website_Developer_")

        # Screenshot
        await page.screenshot(path="verification/file_storage_verify.png")
        print(await page.content()); print("Verification screenshot saved to verification/file_storage_verify.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_file_storage())
