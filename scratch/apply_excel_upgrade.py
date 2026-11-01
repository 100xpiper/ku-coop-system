# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Replace HTML section card (lines ~2919 to 2983)
card_start = -1
card_end = -1
for i, line in enumerate(lines):
    if '<!-- นำเข้าข้อมูลนิสิตสหกิจศึกษา (Student Import Card)' in line:
        card_start = i
    if card_start != -1 and '<!-- การลบ/รีเซ็ตข้อมูลผู้ใช้งานแยกประเภท -->' in line:
        card_end = i
        break

print(f'HTML card range: {card_start+1} to {card_end}')

new_card_html = '''                        <!-- นำเข้าข้อมูลนิสิตสหกิจศึกษา (Student Import Card - Full Width Large Preview) -->
                        <section class="section-card" style="border: 1.5px solid #16a34a; background-color: #f0fdf4; border-radius: 14px; padding: 20px; margin: 0; width: 100%; box-shadow: 0 4px 12px rgba(22, 163, 74, 0.08);">
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
                                            <span id="admin-student-preview-title-text">พรีวิวข้อมูลในไฟล์ Excel ก่อนยืนยันนำเข้า:</span>
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
                                                <th style="padding: 10px 12px; text-align: center; width: 55px;">ลำดับ</th>
                                                <th style="padding: 10px 12px; text-align: left; width: 120px;">รหัสนิสิต</th>
                                                <th style="padding: 10px 12px; text-align: left; width: 180px;">ชื่อ - นามสกุล</th>
                                                <th style="padding: 10px 12px; text-align: center; width: 100px;">หมู่เรียน</th>
                                                <th style="padding: 10px 12px; text-align: left; width: 150px;">อาจารย์ที่ปรึกษา</th>
                                                <th style="padding: 10px 12px; text-align: left;">สถานประกอบการ</th>
                                                <th style="padding: 10px 12px; text-align: center; width: 140px;">พิกัด GPS</th>
                                                <th style="padding: 10px 12px; text-align: center; width: 120px;">สถานะ</th>
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
                        </section>\n\n'''

if card_start != -1 and card_end != -1:
    lines = lines[:card_start] + [new_card_html] + lines[card_end:]

# 2. Replace renderAdminStudentPreImportPreview (lines ~111 to 183)
idx_rp_start = -1
idx_rp_end = -1
for i, line in enumerate(lines):
    if 'function renderAdminStudentPreImportPreview()' in line:
        idx_rp_start = i
    if idx_rp_start != -1 and 'function handleAdvisorExcelSelected(event)' in line:
        idx_rp_end = i
        break

print(f'renderAdminStudentPreImportPreview range: {idx_rp_start+1} to {idx_rp_end}')

new_rp_js = '''        function renderAdminStudentPreImportPreview(isPostImport = false, postImportList = null) {
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
                    statusTag.style.background = '#dcfce7';
                    statusTag.style.color = '#15803d';
                }
                if (postNotice) postNotice.style.display = 'block';

                if (importBtn) {
                    importBtn.disabled = true;
                    importBtn.style.opacity = '0.7';
                    importBtn.style.cursor = 'default';
                    importBtn.style.backgroundColor = '#059669';
                    if (importBtnText) {
                        importBtnText.textContent = `นำเข้ารายชื่อสำเร็จ (${rowsToDisplay.length} รายการ) บันทึกในระบบแล้ว`;
                    }
                }

                // สรุปหมู่เรียน
                const secCounts = {};
                rowsToDisplay.forEach(item => {
                    const sec = item.section || 'หมู่ 700';
                    secCounts[sec] = (secCounts[sec] || 0) + 1;
                });
                if (secPills) {
                    secPills.innerHTML = Object.entries(secCounts).map(([sec, count]) => `
                        <span style="background: #dcfce7; color: #166534; border: 1px solid #86efac; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;">
                            ${sec}: ${count} คน
                        </span>
                    `).join('');
                }

                if (tbody) {
                    tbody.innerHTML = '';
                    rowsToDisplay.forEach((item, idx) => {
                        const tr = document.createElement('tr');
                        tr.style.borderBottom = '1px solid #e2e8f0';
                        tr.style.backgroundColor = (idx % 2 === 0) ? '#ffffff' : '#f8fafc';
                        
                        const latVal = item.company_lat || '';
                        const lngVal = item.company_lng || '';
                        let coordsBadge = `<span style="color: #94a3b8; font-size: 11px;">-</span>`;
                        if (latVal && lngVal) {
                            const latNum = parseFloat(latVal);
                            const lngNum = parseFloat(lngVal);
                            coordsBadge = `<span style="background: #e0f2fe; color: #0284c7; padding: 3px 8px; border-radius: 4px; font-family: monospace; font-size: 11px; font-weight: 600;">${latNum.toFixed(4)}, ${lngNum.toFixed(4)}</span>`;
                        } else if (item.coords && item.coords !== '-') {
                            coordsBadge = `<span style="background: #e0f2fe; color: #0284c7; padding: 3px 8px; border-radius: 4px; font-family: monospace; font-size: 11px; font-weight: 600;">${item.coords}</span>`;
                        }

                        tr.innerHTML = `
                            <td style="padding: 10px 12px; text-align: center; color: #64748b; font-weight: 600;">${idx + 1}</td>
                            <td style="padding: 10px 12px; font-weight: 700; color: #0f172a;">${item.student_id || item.id || '-'}</td>
                            <td style="padding: 10px 12px; font-weight: 600; color: #1e293b;">
                                <div>${item.name || '-'}</div>
                                <div style="font-size: 10.5px; color: #64748b;">${item.email || ''}</div>
                            </td>
                            <td style="padding: 10px 12px; text-align: center;">
                                <span style="background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">
                                    ${item.section || 'หมู่ 700'}
                                </span>
                            </td>
                            <td style="padding: 10px 12px; color: #334155; font-size: 11.5px;">${item.advisor || '-'}</td>
                            <td style="padding: 10px 12px; color: #1e293b; font-size: 11.5px; font-weight: 500;">${item.company || item.company_name || '-'}</td>
                            <td style="padding: 10px 12px; text-align: center;">${coordsBadge}</td>
                            <td style="padding: 10px 12px; text-align: center;">
                                <span style="background: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 12px; font-weight: 700; font-size: 11px; display: inline-flex; align-items: center; gap: 4px;">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                                    พร้อมใช้งาน
                                </span>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                }

            } else {
                // ==============================================================
                // PRE-IMPORT STATE (ก่อนเพิ่มไฟล์ / รอการยืนยัน)
                // ==============================================================
                if (titleText) titleText.textContent = 'พรีวิวข้อมูลในไฟล์ Excel ก่อนยืนยันนำเข้า:';
                if (statusTag) {
                    statusTag.textContent = 'ก่อนนำเข้า (รอการยืนยัน)';
                    statusTag.style.background = '#fef3c7';
                    statusTag.style.color = '#b45309';
                }
                if (postNotice) postNotice.style.display = 'none';

                if (importBtn) {
                    importBtn.disabled = false;
                    importBtn.style.opacity = '1';
                    importBtn.style.cursor = 'pointer';
                    importBtn.style.backgroundColor = '#16a34a';
                    if (importBtnText) {
                        importBtnText.textContent = `ยืนยันนำเข้ารายชื่อนิสิต (${rowsToDisplay.length} รายการ) เข้าสู่ระบบ`;
                    }
                }

                // สรุปหมู่เรียน
                const secCounts = {};
                rowsToDisplay.forEach(row => {
                    const sectionVal = findRowValue(row, ['หมู่เรียน', 'หมู่เรียนที่รับผิดชอบ', 'หมู่', 'Section', 'section']);
                    const sec = sectionVal ? (sectionVal.includes('หมู่') ? sectionVal : `หมู่ ${sectionVal}`) : 'หมู่ 700';
                    secCounts[sec] = (secCounts[sec] || 0) + 1;
                });
                if (secPills) {
                    secPills.innerHTML = Object.entries(secCounts).map(([sec, count]) => `
                        <span style="background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;">
                            ${sec}: ${count} คน
                        </span>
                    `).join('');
                }

                if (tbody) {
                    tbody.innerHTML = '';
                    rowsToDisplay.forEach((row, idx) => {
                        const studentId = findRowValue(row, ['รหัสนิสิต', 'รหัสประจำตัว', 'รหัสนักศึกษา', 'รหัส', 'ID', 'Student ID', 'student_id']) || `STD_${idx+1}`;
                        const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname']);
                        const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']);
                        const fullName = title ? `${title} ${name}`.trim() : (name || 'นิสิต');
                        const emailVal = findRowEmail(row, ['อีเมลมหาวิทยาลัย', 'อีเมล', 'อีเมล์', 'Email', 'email', 'E-mail', 'KU-Mail']) || `${studentId}@ku.th`;
                        const sectionVal = findRowValue(row, ['หมู่เรียน', 'หมู่เรียนที่รับผิดชอบ', 'หมู่', 'Section', 'section']);
                        const sec = sectionVal ? (sectionVal.includes('หมู่') ? sectionVal : `หมู่ ${sectionVal}`) : 'หมู่ 700';
                        const advisorVal = findRowValue(row, ['อาจารย์ที่ปรึกษา', 'อาจารย์นิเทศ', 'อาจารย์', 'Advisor', 'advisor']) || '-';
                        const company = findRowValue(row, ['ชื่อสถานประกอบการ', 'สถานประกอบการ', 'Company', 'company']) || '-';
                        
                        const locationCoord = findRowValue(row, ['พิกัด', 'พิกัด GPS', 'GPS', 'Location', 'พิกัดจีพีเอส']);
                        let coordsBadge = `<span style="color: #94a3b8; font-size: 11px;">-</span>`;
                        if (locationCoord) {
                            coordsBadge = `<span style="background: #f1f5f9; color: #475569; padding: 3px 8px; border-radius: 4px; font-family: monospace; font-size: 11px; font-weight: 600;">${locationCoord}</span>`;
                        }

                        const tr = document.createElement('tr');
                        tr.style.borderBottom = '1px solid #e2e8f0';
                        tr.style.backgroundColor = (idx % 2 === 0) ? '#ffffff' : '#f8fafc';
                        tr.innerHTML = `
                            <td style="padding: 10px 12px; text-align: center; color: #64748b; font-weight: 600;">${idx + 1}</td>
                            <td style="padding: 10px 12px; font-weight: 700; color: #0f172a;">${studentId}</td>
                            <td style="padding: 10px 12px; font-weight: 600; color: #1e293b;">
                                <div>${fullName}</div>
                                <div style="font-size: 10.5px; color: #64748b;">${emailVal}</div>
                            </td>
                            <td style="padding: 10px 12px; text-align: center;">
                                <span style="background: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">
                                    ${sec}
                                </span>
                            </td>
                            <td style="padding: 10px 12px; color: #334155; font-size: 11.5px;">${advisorVal}</td>
                            <td style="padding: 10px 12px; color: #1e293b; font-size: 11.5px; font-weight: 500;">${company}</td>
                            <td style="padding: 10px 12px; text-align: center;">${coordsBadge}</td>
                            <td style="padding: 10px 12px; text-align: center;">
                                <span style="background: #fef3c7; color: #b45309; padding: 3px 8px; border-radius: 12px; font-weight: 700; font-size: 11px;">
                                    รอการยืนยัน
                                </span>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            }
        }\n\n'''

if idx_rp_start != -1 and idx_rp_end != -1:
    lines = lines[:idx_rp_start] + [new_rp_js] + lines[idx_rp_end:]

# 3. Update importStudentExcelFile to not call clearAdminStudentFile() and instead render post-import preview
content = "".join(lines)

old_finish_pattern = '''                    localStorage.setItem('customUsers', JSON.stringify(customUsers));
                    renderAdminUsersTable();
                    updateAdvisorStats();
                    clearAdminStudentFile();

                    // Open Post-Addition Preview Modal!'''

new_finish_pattern = '''                    localStorage.setItem('customUsers', JSON.stringify(customUsers));
                    renderAdminUsersTable();
                    updateAdvisorStats();

                    // RENDER POST-IMPORT PREVIEW (เห็นทั้งก่อนและหลังเพิ่มไฟล์เข้าไป)
                    renderAdminStudentPreImportPreview(true, importedStudentsList);

                    // Open Post-Addition Preview Modal!'''

if old_finish_pattern in content:
    content = content.replace(old_finish_pattern, new_finish_pattern)
    print("Replaced clearAdminStudentFile with post-import preview call in importStudentExcelFile.")
else:
    pos_fn = content.find('function importStudentExcelFile()')
    pos_clear = content.find('clearAdminStudentFile();', pos_fn)
    pos_modal = content.find('showPostAddPreviewModal', pos_fn)
    if pos_clear != -1 and pos_modal != -1 and pos_clear < pos_modal:
        content = content[:pos_clear] + 'renderAdminStudentPreImportPreview(true, importedStudentsList);' + content[pos_clear + len('clearAdminStudentFile();'):]
        print("Replaced clearAdminStudentFile with renderAdminStudentPreImportPreview(true, importedStudentsList).")

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved dashboard.html successfully.")

