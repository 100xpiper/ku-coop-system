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
        
        init_stds = await page.locator("#admin-users-table-container table tbody tr").count()
        init_total = await page.locator("#admin-total-std").inner_text()
        print(f"Initial students count in table: {init_stds} (Stat total: {init_total})")
        
        # Test 1: Upload fresh student list
        std_file = os.path.abspath("รายชื่อนิสิต(1).xlsx")
        print(f"\n2. Uploading fresh student file: {std_file} ...")
        await page.locator("#admin-student-excel-file-input").set_input_files(std_file)
        await page.wait_for_timeout(1000)
        
        btn_text_1 = await page.locator("#admin-student-import-btn-text").inner_text()
        print(f"Button 1 text: {btn_text_1}")
        
        # Click import
        await page.locator("#admin-student-import-btn").click()
        await page.wait_for_timeout(1500)
        
        # Check table count and stats
        stds_after_1 = await page.locator("#admin-users-table-container table tbody tr").count()
        stat_total = await page.locator("#admin-total-std").inner_text()
        print(f"Students count after import 1: {stds_after_1} (Stat card total: {stat_total})")
        
        # Test 2: Try to upload the SAME file again (Duplicate test!)
        print("\n3. Testing duplicate upload of the same file ...")
        await page.locator("#admin-student-excel-file-input").set_input_files(std_file)
        await page.wait_for_timeout(1000)
        
        btn_text_2 = await page.locator("#admin-student-import-btn-text").inner_text()
        btn_disabled = await page.locator("#admin-student-import-btn").is_disabled()
        print(f"Button 2 text: {btn_text_2}")
        print(f"Button 2 is disabled: {btn_disabled}")
        
        # Check if preview shows red warning
        pill_text = await page.locator("#admin-student-preview-sec-pills").inner_text()
        print(f"Warning pill text: {pill_text[:80]}...")
        
        print("\nDialog messages recorded:")
        for m in dialog_messages:
            print("  [Alert]", m[:60] + "...")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
