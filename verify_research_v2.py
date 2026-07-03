import asyncio
from playwright.async_api import async_playwright
import os
import subprocess
import time

async def verify():
    # Start the backend
    backend = subprocess.Popen(["python3", "app.py"], env={**os.environ, "ALLOW_INTERNAL_AGENTS": "true"})
    time.sleep(5)

    # Start the frontend
    frontend = subprocess.Popen(["npm", "run", "dev"], cwd="marketplace-frontend", env={**os.environ, "PORT": "5173"})
    time.sleep(10)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto("http://localhost:5173")

            # Check for Research category
            await page.wait_for_selector("text=Research")
            print("Found Research category")

            # Click Research category
            await page.click("text=Research")

            # Verify specific agents
            await page.wait_for_selector("text=Dataset Architect")
            print("Found Dataset Architect agent")

            await page.wait_for_selector("text=AI Training Strategist")
            print("Found AI Training Strategist agent")

            await page.wait_for_selector("text=Open Dataset Explorer")
            print("Found Open Dataset Explorer agent")

            # Take a screenshot
            await page.screenshot(path="research_results_v2.png")
            print("Screenshot saved to research_results_v2.png")

        except Exception as e:
            print(f"Verification failed: {e}")
            await page.screenshot(path="verification_error.png")
        finally:
            await browser.close()
            backend.terminate()
            frontend.terminate()

if __name__ == "__main__":
    asyncio.run(verify())
