# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HTML layout for admin-card-import and student preview container
old_import_grid = '<div id="admin-card-import" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">'
new_import_grid = '<div id="admin-card-import" style="display: flex; flex-direction: column; gap: 16px; width: 100%;">'

if old_import_grid in content:
    content = content.replace(old_import_grid, new_import_grid)
    print("Updated #admin-card-import to full width flex layout.")

# Find student import section card
sec_import_start = content.find('<!-- นำเข้าข้อมูลนิสิตสหกิจศึกษา (Student Import Card) -->')
sec_reset_start = content.find('<!-- จัดการลบ / รีเซ็ตข้อมูลรายชื่อนิสิต -->')

if sec_import_start != -1 and sec_reset_start != -1:
    new_student_section_html = '''<!-- นำเข้าข้อมูลนิสิตสหกิจศึกษา (Student Import Card - Full Width Large Preview) -->
                        <section class="section-card" style="border: 1.5px solid #16a34a; background-color: #f0fdf4; border-radius: 12px; padding: 20px; margin: 0; width: 100%; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                            <div class="section-header" style="margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                                <div class="section-title" style="color: #15803d; display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 14px;">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><polyline points="16 11 18 13 22 9"/></svg>
                                    <span>นำเข้าข้อมูลนิสิตสหกิจศึกษา (.xlsx / .csv)</span>
                                </div>
                                <span class="status-badge badge-success" style="font-size: 11px;">ระบบจัดการบัญชีนิสิต</span>
                            </div>
                            <div style="font-size: 12px; color: #166534; margin-bottom: 14px; line-height: 1.5;">
                                อัปโหลดไฟล์สเปรดชีตรายชื่อนิสิตเพื่อสร้างบัญชีผู้ใช้ จัดกลุ่มหมู่เรียนอัตโนมัติ ผูกอาจารย์ที่ปรึกษา และบันทึกพิกัดสถานประกอบการลงฐานข้อมูล
                            </div>

                            <!-- Dropzone อัปโหลดไฟล์ -->
                            <div style="background: #ffffff; border: 2px dashed #86efac; border-radius: 10px; padding: 18px; text-align: center; margin-bottom: 14px; transition: all 0.2s ease; cursor: pointer;">
                                <input type="file" id="admin-student-excel-file-input" accept=".xlsx, .xls, .csv" style="display: none;" onchange="handleStudentExcelSelected(event)">
                                <label for="admin-student-excel-file-input" style="cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 8px;">
                                    <div style="font-size: 13px; font-weight: 700; color: #15803d; display: flex; align-items: center; gap: 8px;" id="excel-student-file-name-label">
                                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                                        คลิกเพื่อเลือกไฟล์ Excel รายชื่อนิสิต (.xlsx / .csv)
                                    </div>
                                    <div style="font-size: 11px; color: var(--text-muted); max-width: 650px; line-height: 1.4;">
                                        คอลัมน์มาตรฐานที่รองรับ: รหัสนิสิต, คำนำหน้านาม, ชื่อ - นามสกุล, หมู่เรียน (เช่น 700, 800), อาจารย์ที่ปรึกษา, ชื่อสถานประกอบการ, พิกัด GPS, อีเมลมหาวิทยาลัย
                                    </div>
                                </label>
                            </div>

                            <!-- กรอบแสดงผล Preview ขนาดใหญ่ (กว้างเต็มจอ ชัดเจนทั้งก่อนและหลังนำเข้า) -->
                            <div id="admin-student-preview-container" style="display: none; background: #ffffff; border: 1.5px solid #86efac; border-radius: 10px; padding: 16px; margin-bottom: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
                                    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                                        <div id="admin-student-preview-title" style="font-size: 13.5px; font-weight: 700; color: #166534; display: flex; align-items: center; gap: 6px;">
                                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                                            <span id="admin-student-preview-title-text">พรีวิวข้อมูลในไฟล์ Excel:</span>
                                        </div>
                                        <span id="admin-student-preview-count-badge" class="badge" style="background: #dcfce7; color: #15803d; font-size: 11px; padding: 3px 10px; border-radius: 12px; font-weight: 700;">0 รายการ</span>
                                        <span id="admin-student-preview-status-tag" class="badge" style="background: #fef3c7; color: #b45309; font-size: 11px; padding: 3px 10px; border-radius: 12px; font-weight: 700;">ก่อนนำเข้า (รอการยืนยัน)</span>
                                    </div>
                                    <div style="display: flex; align-items: center; gap: 8px;">
                                        <button type="button" id="btn-admin-preview-clear" onclick="clearAdminStudentFile()" style="border: 1px solid #fecaca; background: #fff5f5; color: #ef4444; font-size: 11px; padding: 5px 12px; border-radius: 6px; cursor: pointer; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">
                                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                                            เปลี่ยนไฟล์ / ล้าง
                                        </button>
                                    </div>
                                </div>

                                <!-- สรุปจำนวนคนตามหมู่เรียน -->
                                <div id="admin-student-preview-sec-pills" style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px;"></div>

                                <!-- ตารางพรีวิวขนาดใหญ่ กว้างเต็มจอ ความสูง 420px เห็นข้อมูลชัดเจน -->
                                <div style="max-height: 420px; overflow-y: auto; overflow-x: auto; border: 1.5px solid #cbd5e1; border-radius: 8px; background: #ffffff;">
                                    <table style="width: 100%; border-collapse: collapse; font-size: 12px; min-width: 860px;">
                                        <thead>
                                            <tr style="background: #f1f5f9; border-bottom: 2px solid #cbd5e1; color: #334155; position: sticky; top: 0; z-index: 2;">
                                                <th style="padding: 10px 12px; text-align: left; width: 60px;">ลำดับ</th>
                                                <th style="padding: 10px 12px; text-align: left; width: 120px;">รหัสนิสิต</th>
                                                <th style="padding: 10px 12px; text-align: left; width: 180px;">ชื่อ - นามสกุล</th>
                                                <th style="padding: 10px 12px; text-align: center; width: 110px;">หมู่เรียน</th>
                                                <th style="padding: 10px 12px; text-align: left; width: 150px;">อาจารย์ที่ปรึกษา</th>
                                                <th style="padding: 10px 12px; text-align: left;">สถานประกอบการ</th>
                                                <th style="padding: 10px 12px; text-align: center; width: 140px;">พิกัด GPS</th>
                                                <th style="padding: 10px 12px; text-align: center; width: 110px;">สถานะ</th>
                                            </tr>
                                        </thead>
                                        <tbody id="admin-student-preview-tbody">
                                        </tbody>
                                    </table>
                                </div>

                                <!-- กล่องแจ้งเตือนหลังนำเข้าสำเร็จ -->
                                <div id="admin-student-post-notice" style="display: none; background: #ecfdf5; border: 1.5px solid #a7f3d0; border-radius: 8px; padding: 12px 16px; margin-top: 14px; font-size: 12px; color: #047857;">
                                    <div style="font-weight: 700; margin-bottom: 3px; display: flex; align-items: center; gap: 6px; font-size: 13px;">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                                        นำเข้ารายชื่อนิสิตสำเร็จและบันทึกเข้าสู่ระบบเรียบร้อยแล้ว
                                    </div>
                                    <div style="line-height: 1.4;">ข้อมูลทั้งหมดถูกบันทึกลงในระบบเรียบร้อย สามารถตรวจสอบข้อมูลบัญชีผู้ใช้ (รหัสผ่านแรกเข้า: รหัสนิสิต) และพิกัดสถานประกอบการที่นำเข้าได้จากตารางด้านบนนี้ทันที</div>
                                </div>
                            </div>

                            <!-- ปุ่มดำเนินการ -->
                            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                                <button type="button" id="admin-student-import-btn" class="btn-primary" style="flex: 1; min-width: 220px; background-color: #16a34a; padding: 12px; font-size: 12.5px; font-weight: 700; opacity: 0.6; cursor: not-allowed; border-radius: 8px; display: flex; align-items: center; justify-content: center; gap: 6px;" disabled onclick="importStudentExcelFile()">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                                    <span id="admin-student-import-btn-text">นำเข้ารายชื่อนิสิตเข้าสู่ระบบ</span>
                                </button>
                                <button type="button" class="btn-primary" style="background-color: #ffffff; color: #166534; border: 1.5px solid #bbf7d0; padding: 12px 18px; font-size: 12px; font-weight: 700; border-radius: 8px; display: flex; align-items: center; justify-content: center; gap: 6px;" onclick="downloadStudentExcelTemplate()">
                                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                                    <span>ดาวน์โหลดแม่แบบไฟล์นิสิต (.xlsx)</span>
                                </button>
                            </div>
                        </section>\n\n                        '''
    content = content[:sec_import_start] + new_student_section_html + content[sec_reset_start:]
    print("Updated student import section HTML successfully.")

# 2. Update JavaScript functions for Pre and Post Preview
old_render_preview = 'function renderAdminStudentPreImportPreview() {'
idx_rp = content.find(old_render_preview)
old_import_func = 'function importStudentExcelFile() {'
idx_imp = content.find(old_import_func)

# We will replace renderAdminStudentPreImportPreview and importStudentExcelFile
new_js_logic = '''function renderAdminStudentPreImportPreview(isPostImport = false, postImportList = null) {
            const previewContainer = document.getElementById('admin-student-preview-container');
            const countBadge = document.getElementById('admin-student-preview-count-badge');
            const statusTag = document.getElementById('admin-student-preview-status-tag');
            const titleText = document.getElementById('admin-student-preview-title-text');
            const secPills = document.getElementById('admin-student-preview-sec-pills');
            const tbody = document.getElementById('admin-student-preview-tbody');
            const importBtn = document.getElementById('admin-student-import-btn');
            const importBtnText = document.getElementById('admin-student-import-btn-text');
            const postNotice = document.getElementById('admin-student-post-notice');

            const rowsToDisplay = isPostImport && Array.isArray(postImportList) 
                ? postImportList 
                : adminParsedStudentRows;

            if (!rowsToDisplay || rowsToDisplay.length === 0) {
                if (previewContainer) previewContainer.style.display = 'none';
                return;
            }

            if (previewContainer) {
                previewContainer.style.display = 'block';
                previewContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }

            if (countBadge) countBadge.textContent = `${rowsToDisplay.length} รายการ`;

            if (isPostImport) {
                // ==============================================================
                // POST-IMPORT STATE (หลังเพิ่มไฟล์เข้าไป)
                // ==============================================================
                if (titleText) titleText.textContent = 'พรีวิวผลลัพธ์รายชื่อนิสิตที่นำเข้าล่าสุด:';
                if (statusTag) {
                    statusTag.textContent = 'นำเข้าสำเร็จแล้ว (พร้อมใช้งาน)';
                    statusTag.style.backgroundColor = '#dcfce7';
                    statusTag.style.color = '#15803d';
                }
                if (postNotice) postNotice.style.display = 'block';

                if (importBtn) {
                    importBtn.disabled = false;
                    importBtn.style.opacity = '1';
                    importBtn.style.cursor = 'pointer';
                    importBtn.style.backgroundColor = '#0284c7';
                    if (importBtnText) importBtnText.textContent = 'นำเข้าไฟล์ Excel อื่นเพิ่มเติม';
                    importBtn.onclick = function() {
                        clearAdminStudentFile();
                        const fileInput = document.getElementById('admin-student-excel-file-input');
                        if (fileInput) fileInput.click();
                    };
                }
            } else {
                // ==============================================================
                // PRE-IMPORT STATE (ก่อนเพิ่มไฟล์เข้าไป)
                // ==============================================================
                if (titleText) titleText.textContent = 'พรีวิวข้อมูลในไฟล์ Excel ก่อนยืนยันนำเข้า:';
                if (statusTag) {
                    statusTag.textContent = 'ก่อนนำเข้า (รอการยืนยัน)';
                    statusTag.style.backgroundColor = '#fef3c7';
                    statusTag.style.color = '#b45309';
                }
                if (postNotice) postNotice.style.display = 'none';

                if (importBtn) {
                    importBtn.disabled = false;
                    importBtn.style.opacity = '1';
                    importBtn.style.cursor = 'pointer';
                    importBtn.style.backgroundColor = '#16a34a';
                    if (importBtnText) importBtnText.textContent = `ยืนยันนำเข้ารายชื่อนิสิต (${rowsToDisplay.length} รายการ) เข้าสู่ระบบ`;
                    importBtn.onclick = importStudentExcelFile;
                }
            }

            // Summary pills by section
            const secCounts = {};
            rowsToDisplay.forEach(row => {
                let sec = 'หมู่ 700';
                if (isPostImport) {
                    sec = row.section || 'หมู่ 700';
                } else {
                    const sectionVal = findRowValue(row, ['หมู่เรียน', 'หมู่เรียนที่รับผิดชอบ', 'หมู่', 'Section', 'section']);
                    sec = sectionVal ? (sectionVal.includes('หมู่') ? sectionVal : `หมู่ ${sectionVal}`) : 'หมู่ 700';
                }
                secCounts[sec] = (secCounts[sec] || 0) + 1;
            });

            if (secPills) {
                secPills.innerHTML = Object.entries(secCounts).map(([sec, count]) => `
                    <span style="background: #ecfdf5; color: #047857; border: 1.5px solid #a7f3d0; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;">
                        ${sec}: ${count} คน
                    </span>
                `).join('');
            }

            // Full table render of all rows
            if (tbody) {
                tbody.innerHTML = '';
                rowsToDisplay.forEach((row, idx) => {
                    let studentId, fullName, sec, advisorVal, company, coords, statusBadge;

                    if (isPostImport) {
                        studentId = row.student_id || row.id || `STD_${idx+1}`;
                        fullName = row.name || 'นิสิต';
                        sec = row.section || 'หมู่ 700';
                        advisorVal = row.advisor || row.advisor_name || '-';
                        company = row.company || row.company_name || '-';
                        coords = (row.company_lat && row.company_lng) ? `${row.company_lat}, ${row.company_lng}` : (row.coords || '-');
                        statusBadge = '<span class="status-badge badge-success" style="font-size: 10.5px;">นำเข้าสำเร็จ</span>';
                    } else {
                        studentId = findRowValue(row, ['รหัสนิสิต', 'รหัสประจำตัว', 'รหัสนักศึกษา', 'รหัส', 'ID', 'Student ID', 'student_id']) || `STD_${idx+1}`;
                        const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname']);
                        const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']);
                        fullName = title ? `${title} ${name}`.trim() : (name || 'นิสิต');
                        const sectionVal = findRowValue(row, ['หมู่เรียน', 'หมู่เรียนที่รับผิดชอบ', 'หมู่', 'Section', 'section']);
                        sec = sectionVal ? (sectionVal.includes('หมู่') ? sectionVal : `หมู่ ${sectionVal}`) : 'หมู่ 700';
                        advisorVal = findRowValue(row, ['อาจารย์ที่ปรึกษา', 'อาจารย์นิเทศ', 'อาจารย์', 'Advisor', 'advisor']) || '-';
                        company = findRowValue(row, ['ชื่อสถานประกอบการ', 'สถานประกอบการ', 'Company', 'company']) || '-';
                        coords = findRowValue(row, ['พิกัด', 'พิกัด GPS', 'GPS', 'Location']) || '-';
                        statusBadge = '<span style="background: #fef3c7; color: #b45309; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 10.5px;">รอการบันทึก</span>';
                    }

                    const tr = document.createElement('tr');
                    tr.style.borderBottom = '1px solid #f1f5f9';
                    tr.style.backgroundColor = (idx % 2 === 0) ? '#ffffff' : '#f8fafc';
                    tr.innerHTML = `
                        <td style="padding: 8px 12px; color: #64748b; font-weight: 600;">${idx + 1}</td>
                        <td style="padding: 8px 12px; font-weight: 700; font-family: monospace; color: #1e293b;">${studentId}</td>
                        <td style="padding: 8px 12px; font-weight: 600; color: #0f172a;">${fullName}</td>
                        <td style="padding: 8px 12px; text-align: center;"><span style="background: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">${sec}</span></td>
                        <td style="padding: 8px 12px; color: #475569;">${advisorVal}</td>
                        <td style="padding: 8px 12px; color: #334155; font-weight: 500;">${company}</td>
                        <td style="padding: 8px 12px; text-align: center; font-family: monospace; font-size: 11px; color: #166534;">${coords}</td>
                        <td style="padding: 8px 12px; text-align: center;">${statusBadge}</td>
                    `;
                    tbody.appendChild(tr);
                });
            }
        }

        function clearAdminStudentFile() {
            selectedStudentExcelFile = null;
            adminParsedStudentRows = [];

            const input = document.getElementById('admin-student-excel-file-input');
            if (input) input.value = '';

            const label = document.getElementById('excel-student-file-name-label');
            if (label) {
                label.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg> คลิกเพื่อเลือกไฟล์ Excel รายชื่อนิสิต (.xlsx / .csv)`;
                const parentBox = label.closest('div');
                if (parentBox) {
                    parentBox.style.backgroundColor = '#ffffff';
                    parentBox.style.border = '2px dashed #86efac';
                }
            }

            const previewContainer = document.getElementById('admin-student-preview-container');
            if (previewContainer) previewContainer.style.display = 'none';

            const importBtn = document.getElementById('admin-student-import-btn');
            const importBtnText = document.getElementById('admin-student-import-btn-text');
            if (importBtn) {
                importBtn.disabled = true;
                importBtn.style.opacity = '0.6';
                importBtn.style.cursor = 'not-allowed';
                importBtn.style.backgroundColor = '#16a34a';
                if (importBtnText) importBtnText.textContent = 'นำเข้ารายชื่อนิสิตเข้าสู่ระบบ';
                importBtn.onclick = importStudentExcelFile;
            }
        }

        function importStudentExcelFile() {
            if (!selectedStudentExcelFile && (!adminParsedStudentRows || adminParsedStudentRows.length === 0)) {
                alert('กรุณาคลิกเลือกไฟล์ Excel รายชื่อนิสิต (.xlsx / .csv) ก่อนกดนำเข้าข้อมูล');
                return;
            }

            const jsonRows = adminParsedStudentRows;
            if (!jsonRows || jsonRows.length === 0) {
                alert('ไม่พบข้อมูลรายชื่อในไฟล์ Excel ที่เลือก');
                return;
            }

            const importBtn = document.getElementById('admin-student-import-btn');
            const importBtnText = document.getElementById('admin-student-import-btn-text');
            if (importBtnText) importBtnText.textContent = 'กำลังนำเข้าข้อมูลลงสู่ระบบ...';
            if (importBtn) importBtn.disabled = true;

            setTimeout(async () => {
                try {
                    let importedCount = 0;
                    const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                    const importedStudentsList = [];
                    const sectionsCountMap = {};

                    for (const row of jsonRows) {
                        const emailRaw = findRowEmail(row, ['อีเมลมหาวิทยาลัย', 'อีเมล', 'อีเมล์', 'อีเมล์มหาวิทยาลัย', 'Email', 'email', 'E-mail', 'KU-Mail', 'KU Mail', 'เมล', 'อีเมลนิสิต']);
                        if (!emailRaw) continue;
                        const email = String(emailRaw).trim().toLowerCase();
                        if (!email) continue;

                        const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname']);
                        const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']);
                        const fullName = title ? `${title} ${name}`.trim() : (name || 'นิสิตสหกิจศึกษา');
                        const studentId = findRowValue(row, ['รหัสนิสิต', 'รหัสประจำตัว', 'รหัสนักศึกษา', 'รหัส', 'ID', 'Student ID', 'StudentID', 'student_id']);
                        const yearVal = findRowValue(row, ['ชั้นปี', 'ชั้น', 'Year', 'year']);
                        const deptVal = findRowValue(row, ['ภาควิชา', 'สาขาวิชา', 'ภาค', 'Department', 'dept']);
                        const curriculumVal = findRowValue(row, ['หลักสูตร', 'Curriculum', 'program']);
                        const sectionVal = findRowValue(row, ['หมู่เรียน', 'หมู่เรียนที่รับผิดชอบ', 'หมู่', 'Section', 'section']);
                        const section = sectionVal ? (sectionVal.includes('หมู่') ? sectionVal : `หมู่ ${sectionVal}`) : 'หมู่ 700';
                        const company = findRowValue(row, ['ชื่อสถานประกอบการ', 'สถานประกอบการ', 'Company', 'company']);
                        const advisorVal = findRowValue(row, ['อาจารย์ที่ปรึกษา', 'อาจารย์นิเทศ', 'อาจารย์', 'อาจารย์ผู้ดูแล', 'Advisor', 'advisor', 'ที่ปรึกษา']);
                        const semesterRaw = findRowValue(row, ['ภาคการศึกษา', 'ภาคเรียน', 'เทอม', 'Semester', 'semester', 'Term', 'term']);
                        let semester = semesterRaw || 'ภาคต้น 2569';
                        if (semester === '69' || semester === '2569') {
                            semester = 'ภาคต้น 2569';
                        }
                        const phoneVal = findRowValue(row, ['เบอร์โทรศัพท์', 'เบอร์โทร', 'เบอร์', 'โทร', 'Phone', 'Tel', 'tel']);
                        
                        // Parse coordinates
                        const locationCoord = findRowValue(row, ['พิกัด', 'พิกัด GPS', 'GPS', 'Location', 'พิกัดจีพีเอส']);
                        let lat = null;
                        let lng = null;
                        if (locationCoord) {
                            if (locationCoord.includes(',')) {
                                const parts = locationCoord.split(',');
                                if (parts.length >= 2) {
                                    lat = parseFloat(parts[0].trim());
                                    lng = parseFloat(parts[1].trim());
                                }
                            } else if (!isNaN(parseFloat(locationCoord))) {
                                lat = parseFloat(locationCoord.trim());
                            }
                        }

                        const passRaw = findRowValue(row, ['รหัสผ่านชั่วคราว', 'รหัสผ่าน', 'Password', 'pass']);
                        const pass = passRaw || studentId || '123456';

                        const userObj = {
                            id: studentId || email.split('@')[0],
                            student_id: studentId || email.split('@')[0],
                            name: fullName,
                            email: email,
                            password: pass,
                            password_hash: pass,
                            role: 'student',
                            year: yearVal || '4',
                            department: deptVal || 'วิทยาการคอมพิวเตอร์',
                            curriculum: curriculumVal || (section.includes('800') ? 'ภาคพิเศษ' : 'ภาคปกติ'),
                            section: section,
                            company_name: company,
                            company_lat: lat || null,
                            company_lng: lng || null,
                            advisor_name: advisorVal || '',
                            semester: semester,
                            phone: phoneVal || '',
                            status: 'approved',
                            first_login: true,
                            password_changed: false
                        };

                        customUsers[email] = userObj;

                        if (typeof supabaseClient !== 'undefined' && supabaseClient) {
                            try {
                                await supabaseClient.from('users').upsert([{
                                    email: email,
                                    password_hash: pass,
                                    full_name: fullName,
                                    role: 'student',
                                    status: 'approved'
                                }], { onConflict: 'email' });

                                if (studentId) {
                                    const studentData = {
                                        student_id: studentId,
                                        email: email,
                                        full_name: fullName,
                                        section: section,
                                        company_name: company,
                                        doc_status: 'รอตรวจ',
                                        supervision_status: 'รอนิเทศ'
                                    };
                                    if (advisorVal) studentData.advisor_name = advisorVal;
                                    if (lat) studentData.company_lat = lat;
                                    if (lng) studentData.company_lng = lng;

                                    await supabaseClient.from('students').upsert([studentData], { onConflict: 'student_id' });
                                }
                            } catch (err) {
                                console.warn("Supabase upsert notice:", err.message);
                            }
                        }

                        importedCount++;
                        sectionsCountMap[section] = (sectionsCountMap[section] || 0) + 1;
                        importedStudentsList.push({
                            id: studentId || email.split('@')[0],
                            student_id: studentId || email.split('@')[0],
                            name: fullName,
                            email: email,
                            section: section,
                            company: company || '-',
                            company_name: company || '-',
                            company_lat: lat,
                            company_lng: lng,
                            coords: (lat && lng) ? `${lat}, ${lng}` : '-',
                            advisor: advisorVal || '-',
                            initialPassword: pass,
                            status: 'approved'
                        });
                    }

                    localStorage.setItem('customUsers', JSON.stringify(customUsers));
                    renderAdminUsersTable();
                    updateAdvisorStats();

                    // RENDER POST-IMPORT PREVIEW IMMEDIATELY! (เห็นทั้งก่อนและหลังนำเข้า)
                    renderAdminStudentPreImportPreview(true, importedStudentsList);

                    // Also trigger the post-add modal
                    showPostAddPreviewModal({
                        title: 'นำเข้ารายชื่อนิสิตเข้าสู่ระบบสำเร็จเรียบร้อย',
                        roleTitle: 'ผู้ดูแลระบบ (Admin)',
                        source: 'admin_file',
                        students: importedStudentsList,
                        sectionsCountMap: sectionsCountMap,
                        emailSent: false
                    });

                } catch (err) {
                    console.error("Import processing error:", err);
                    alert('เกิดข้อผิดพลาดในการนำเข้าข้อมูล: ' + err.message);
                    if (importBtn) importBtn.disabled = false;
                }
            }, 50);
        }
'''

# Find where renderAdminStudentPreImportPreview begins and where clearAdminAdvisorFile begins
idx_start = content.find('function renderAdminStudentPreImportPreview() {')
idx_next = content.find('function clearAdminAdvisorFile()')

if idx_start != -1 and idx_next != -1:
    content = content[:idx_start] + new_js_logic + '\n\n        ' + content[idx_next:]
    print("Replaced Excel import JS functions with enhanced Pre/Post preview logic.")

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved dashboard.html successfully.")

