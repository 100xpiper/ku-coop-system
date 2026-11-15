# -*- coding: utf-8 -*-
import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )
        page = await browser.new_page()
        
        dialog_messages = []
        page.on("dialog", lambda dialog: [dialog_messages.append(dialog.message), dialog.accept()])
        
        print("1. Loading dashboard.html?user=admin ...")
        await page.goto("http://localhost:8080/dashboard.html?user=admin", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        std_file = os.path.abspath("รายชื่อนิสิต(1).xlsx")
        
        # 1st Import (should succeed)
        print("2. First import of file ...")
        await page.locator("#admin-student-excel-file-input").set_input_files(std_file)
        await page.wait_for_timeout(1000)
        await page.locator("#admin-student-import-btn").click()
        await page.wait_for_timeout(1500)
        print("First import completed.")
        
        # Reload page so everything is fresh and students are now in customUsers
        print("3. Reloading page ...")
        await page.reload(wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # 2nd Import of SAME file (must detect duplicates!)
        print("4. Selecting SAME file again (should detect duplicates) ...")
        await page.locator("#admin-student-excel-file-input").set_input_files(std_file)
        await page.wait_for_timeout(1500)
        
        btn_text = await page.locator("#admin-student-import-btn-text").inner_text()
        btn_disabled = await page.locator("#admin-student-import-btn").is_disabled()
        pill_text = await page.locator("#admin-student-preview-sec-pills").inner_text()
        
        print(f"Button text: {btn_text}")
        print(f"Is Button disabled: {btn_disabled}")
        print(f"Warning pill text: {pill_text}")
        
        # Try to force-click import button
        print("5. Attempting to force-click import button ...")
        await page.evaluate("importStudentExcelFile()")
        await page.wait_for_timeout(1000)
        
        print(f"\nDialog messages recorded ({len(dialog_messages)}):")
        for m in dialog_messages:
            print("  Alert message:", m)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
