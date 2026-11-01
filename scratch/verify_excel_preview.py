import asyncio
from playwright.async_api import async_playwright
import os
import shutil

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Create a standard desktop browser viewport (1280x800) matching user's screen
        page = await browser.new_page(viewport={"width": 1280, "height": 850})
        
        # Navigate to admin dashboard
        await page.goto("http://localhost:8080/dashboard.html?user=admin&page=sec-admin-dash", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # Switch to the Import Excel section by clicking the navigation or triggering showSection
        await page.evaluate("""() => {
            if (typeof showSection === 'function') {
                showSection('sec-admin-dash');
            }
            // Scroll to the excel import card
            const el = document.getElementById('admin-card-import');
            if (el) el.scrollIntoView();
        }""")
        await page.wait_for_timeout(500)
        
        # Test 1: Simulate selecting an Excel file (Pre-import Preview)
        await page.evaluate("""() => {
            window.adminParsedStudentRows = [
                {
                    'รหัสนิสิต': '6521655305',
                    'คำนำหน้านาม': 'นาย',
                    'ชื่อ - นามสกุล': 'พชร ศิริวัฒน์',
                    'อีเมลมหาวิทยาลัย': 'phachara.s@ku.th',
                    'หมู่เรียน': '800 (ภาคพิเศษ)',
                    'อาจารย์ที่ปรึกษา': 'อาจารย์ สมจิต มั่งมี',
                    'ชื่อสถานประกอบการ': 'บริษัท กสท โทรคมนาคม จำกัด (มหาชน)',
                    'พิกัด GPS': '13.8821, 100.5841'
                },
                {
                    'รหัสนิสิต': '6521655313',
                    'คำนำหน้านาม': 'นางสาว',
                    'ชื่อ - นามสกุล': 'กนกวรรณ รัตนวิชัย',
                    'อีเมลมหาวิทยาลัย': 'kanokwan.r@ku.th',
                    'หมู่เรียน': '800 (ภาคพิเศษ)',
                    'อาจารย์ที่ปรึกษา': 'อาจารย์ สมจิต มั่งมี',
                    'ชื่อสถานประกอบการ': 'บริษัท อโกด้า เซอร์วิสเซส จำกัด',
                    'พิกัด GPS': '13.7462, 100.5348'
                },
                {
                    'รหัสนิสิต': '6521650012',
                    'คำนำหน้านาม': 'นาย',
                    'ชื่อ - นามสกุล': 'ธนกฤต แสงสว่าง',
                    'อีเมลมหาวิทยาลัย': 'thanakrit.s@ku.th',
                    'หมู่เรียน': '700 (ภาคปกติ)',
                    'อาจารย์ที่ปรึกษา': 'อาจารย์ นิเทศ สหกิจ',
                    'ชื่อสถานประกอบการ': 'บริษัท บลูบิค กรุ๊ป จำกัด (มหาชน)',
                    'พิกัด GPS': '13.7234, 100.5289'
                },
                {
                    'รหัสนิสิต': '6521650045',
                    'คำนำหน้านาม': 'นางสาว',
                    'ชื่อ - นามสกุล': 'พิมพ์พิชชา วงศ์สุวรรณ',
                    'อีเมลมหาวิทยาลัย': 'pimpitcha.w@ku.th',
                    'หมู่เรียน': '700 (ภาคปกติ)',
                    'อาจารย์ที่ปรึกษา': 'อาจารย์ นิเทศ สหกิจ',
                    'ชื่อสถานประกอบการ': 'ธนาคารไทยพาณิชย์ จำกัด (มหาชน)',
                    'พิกัด GPS': '13.8279, 100.5652'
                }
            ];
            
            // Set file label mock
            const label = document.getElementById('excel-student-file-name-label');
            if (label) {
                label.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> เลือกไฟล์แล้ว: <strong>รายชื่อนิสิตสหกิจ_2569.xlsx</strong> (78.3 KB)';
                const p = label.closest('div');
                if (p) {
                    p.style.backgroundColor = '#dcfce7';
                    p.style.border = '1.5px solid #22c55e';
                }
            }
            
            // Render PRE-IMPORT PREVIEW
            renderAdminStudentPreImportPreview(false);
        }""")
        await page.wait_for_timeout(1000)
        
        # Verify Pre-import DOM assertions
        pre_info = await page.evaluate("""() => {
            const container = document.getElementById('admin-student-preview-container');
            const statusTag = document.getElementById('admin-student-preview-status-tag');
            const countBadge = document.getElementById('admin-student-preview-count-badge');
            const btn = document.getElementById('admin-student-import-btn');
            const btnText = document.getElementById('admin-student-import-btn-text');
            const rows = document.querySelectorAll('#admin-student-preview-tbody tr');
            const rect = container ? container.getBoundingClientRect() : null;
            
            return {
                visible: container && window.getComputedStyle(container).display !== 'none',
                width: rect ? rect.width : 0,
                statusText: statusTag ? statusTag.textContent : '',
                countText: countBadge ? countBadge.textContent : '',
                btnDisabled: btn ? btn.disabled : true,
                btnText: btnText ? btnText.textContent : '',
                rowCount: rows.length
            };
        }""")
        print("Pre-import Verification:", pre_info)
        assert pre_info["visible"] is True, "Preview container should be visible"
        assert "ก่อนนำเข้า" in pre_info["statusText"], f"Expected 'ก่อนนำเข้า' in statusText, got {pre_info['statusText']}"
        assert "4 รายการ" in pre_info["countText"], "Expected '4 รายการ' in countText"
        assert pre_info["rowCount"] == 4, f"Expected 4 rows, got {pre_info['rowCount']}"
        assert pre_info["width"] > 600, f"Expected container width > 600px, got {pre_info['width']}"
        
        os.makedirs("screenshots", exist_ok=True)
        await page.screenshot(path="screenshots/17_admin_excel_preview_pre_import.png", full_page=False)
        print("Saved screenshots/17_admin_excel_preview_pre_import.png")
        
        # Test 2: Simulate POST-IMPORT PREVIEW (after adding the file)
        await page.evaluate("""() => {
            const samplePostList = [
                {
                    id: '6521655305',
                    student_id: '6521655305',
                    name: 'นาย พชร ศิริวัฒน์',
                    email: 'phachara.s@ku.th',
                    section: 'หมู่ 800 (ภาคพิเศษ)',
                    company: 'บริษัท กสท โทรคมนาคม จำกัด (มหาชน)',
                    company_lat: 13.8821,
                    company_lng: 100.5841,
                    coords: '13.8821, 100.5841',
                    advisor: 'อาจารย์ สมจิต มั่งมี',
                    initialPassword: '6521655305',
                    status: 'approved'
                },
                {
                    id: '6521655313',
                    student_id: '6521655313',
                    name: 'นางสาว กนกวรรณ รัตนวิชัย',
                    email: 'kanokwan.r@ku.th',
                    section: 'หมู่ 800 (ภาคพิเศษ)',
                    company: 'บริษัท อโกด้า เซอร์วิสเซส จำกัด',
                    company_lat: 13.7462,
                    company_lng: 100.5348,
                    coords: '13.7462, 100.5348',
                    advisor: 'อาจารย์ สมจิต มั่งมี',
                    initialPassword: '6521655313',
                    status: 'approved'
                },
                {
                    id: '6521650012',
                    student_id: '6521650012',
                    name: 'นาย ธนกฤต แสงสว่าง',
                    email: 'thanakrit.s@ku.th',
                    section: 'หมู่ 700 (ภาคปกติ)',
                    company: 'บริษัท บลูบิค กรุ๊ป จำกัด (มหาชน)',
                    company_lat: 13.7234,
                    company_lng: 100.5289,
                    coords: '13.7234, 100.5289',
                    advisor: 'อาจารย์ นิเทศ สหกิจ',
                    initialPassword: '6521650012',
                    status: 'approved'
                },
                {
                    id: '6521650045',
                    student_id: '6521650045',
                    name: 'นางสาว พิมพ์พิชชา วงศ์สุวรรณ',
                    email: 'pimpitcha.w@ku.th',
                    section: 'หมู่ 700 (ภาคปกติ)',
                    company: 'ธนาคารไทยพาณิชย์ จำกัด (มหาชน)',
                    company_lat: 13.8279,
                    company_lng: 100.5652,
                    coords: '13.8279, 100.5652',
                    advisor: 'อาจารย์ นิเทศ สหกิจ',
                    initialPassword: '6521650045',
                    status: 'approved'
                }
            ];
            
            // Render POST-IMPORT PREVIEW
            renderAdminStudentPreImportPreview(true, samplePostList);
        }""")
        await page.wait_for_timeout(1000)
        
        # Verify Post-import DOM assertions
        post_info = await page.evaluate("""() => {
            const container = document.getElementById('admin-student-preview-container');
            const statusTag = document.getElementById('admin-student-preview-status-tag');
            const notice = document.getElementById('admin-student-post-notice');
            const rows = document.querySelectorAll('#admin-student-preview-tbody tr');
            
            return {
                visible: container && window.getComputedStyle(container).display !== 'none',
                statusText: statusTag ? statusTag.textContent : '',
                noticeVisible: notice && window.getComputedStyle(notice).display !== 'none',
                rowCount: rows.length
            };
        }""")
        print("Post-import Verification:", post_info)
        assert post_info["visible"] is True, "Preview container should still be visible after import"
        assert "นำเข้าสำเร็จแล้ว" in post_info["statusText"], f"Expected 'นำเข้าสำเร็จแล้ว' in statusText, got {post_info['statusText']}"
        assert post_info["noticeVisible"] is True, "Post-import notice banner should be visible"
        assert post_info["rowCount"] == 4, f"Expected 4 rows, got {post_info['rowCount']}"
        
        await page.screenshot(path="screenshots/18_admin_excel_preview_post_import.png", full_page=False)
        print("Saved screenshots/18_admin_excel_preview_post_import.png")
        
        # Copy to brain screenshots directory
        brain_dir = r"C:\Users\PER\.gemini\antigravity\brain\ddb60d44-47b2-4e84-bca5-28d119fdaf51\screenshots"
        os.makedirs(brain_dir, exist_ok=True)
        shutil.copy("screenshots/17_admin_excel_preview_pre_import.png", os.path.join(brain_dir, "17_admin_excel_preview_pre_import.png"))
        shutil.copy("screenshots/18_admin_excel_preview_post_import.png", os.path.join(brain_dir, "18_admin_excel_preview_post_import.png"))
        print("Copied screenshots to artifact directory.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

