# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = "const targetModal = urlParams.get('modal');"
assert target in content, "targetModal line not found"

hook_code = '''const targetModal = urlParams.get('modal');

            // Quick verification hook for Excel import pre/post preview
            if (urlParams.get('test_pre_import') === '1') {
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
                const lbl = document.getElementById('excel-student-file-name-label');
                if (lbl) {
                    lbl.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> เลือกไฟล์แล้ว: <strong>รายชื่อนิสิตสหกิจ_2569.xlsx</strong> (78.3 KB)`;
                    if (lbl.parentElement) {
                        lbl.parentElement.style.backgroundColor = '#dcfce7';
                        lbl.parentElement.style.border = '1.5px solid #22c55e';
                    }
                }
                setTimeout(() => {
                    renderAdminStudentPreImportPreview(false);
                    const previewCard = document.getElementById('admin-student-preview-container');
                    if (previewCard) previewCard.scrollIntoView();
                }, 100);
            } else if (urlParams.get('test_post_import') === '1') {
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
                const lbl = document.getElementById('excel-student-file-name-label');
                if (lbl) {
                    lbl.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> นำเข้าไฟล์แล้ว: <strong>รายชื่อนิสิตสหกิจ_2569.xlsx</strong> (4 รายการ)`;
                    if (lbl.parentElement) {
                        lbl.parentElement.style.backgroundColor = '#dcfce7';
                        lbl.parentElement.style.border = '1.5px solid #22c55e';
                    }
                }
                setTimeout(() => {
                    renderAdminStudentPreImportPreview(true, samplePostList);
                    const previewCard = document.getElementById('admin-student-preview-container');
                    if (previewCard) previewCard.scrollIntoView();
                }, 100);
            }'''

content = content.replace(target, hook_code, 1)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added test query parameter hooks to dashboard.html successfully.")

