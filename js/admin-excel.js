// ==========================================================================
// admin-excel.js - โมดูลนำเข้าข้อมูลสเปรดชีต Excel และระบบพรีวิวขนาดใหญ่ 100%
// โครงงาน: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================
// เริ่มต้นรีเซ็ตและตรวจสอบข้อมูลแคชของระบบนิเทศ
if (!localStorage.getItem('app_cache_initialized')) {
    localStorage.removeItem('systemAppointments');
    localStorage.removeItem('submittedDocs');
    localStorage.setItem('app_cache_initialized', 'true');
}

let selectedStudentExcelFile = null;
let selectedAdvisorExcelFile = null;
let adminParsedStudentRows = [];
let currentImportedFileType = 'student'; // 'student' หรือ 'advisor'

function detectIsAdvisorFile(rows, fileName = '') {
    const lowerName = String(fileName || '').toLowerCase();
    if (lowerName.includes('อาจารย์') || lowerName.includes('advisor')) {
        return true;
    }
    if (!rows || rows.length === 0) return false;
    const firstRow = rows[0];
    const keys = Object.keys(firstRow).map(k => String(k).trim());

    const hasAdvisorSec = keys.some(k => k.includes('หมู่เรียนที่รับผิดชอบ') || k.includes('รับผิดชอบ'));
    const hasStudentSpecific = keys.some(k => k.includes('รหัสนิสิต') || k.includes('สถานประกอบการ') || k.includes('พิกัด'));

    if (hasAdvisorSec && !hasStudentSpecific) return true;

    const prefix = String(findRowValue(firstRow, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']) || '').trim();
    if (prefix.includes('อาจารย์') || prefix.includes('ผศ.') || prefix.includes('รศ.') || prefix.includes('ดร.')) {
        if (!hasStudentSpecific) return true;
    }

    return false;
}

function normalizeCleanSection(val, defaultSec = 'หมู่ 700') {
    if (!val) return defaultSec;
    let s = String(val).replace(/\s*\(ภาคปกติ\)|\s*\(ภาคพิเศษ\)|\s*\(ปกติ\)|\s*\(พิเศษ\)|ภาคปกติ|ภาคพิเศษ/g, '').trim();
    if (!s) return defaultSec;
    return s.includes('หมู่') ? s : `หมู่ ${s}`;
}

function handleStudentExcelSelected(event) {
    const file = event.target.files && event.target.files[0];
    if (!file) return;

    const ext = file.name.split('.').pop().toLowerCase();
    if (!['xlsx', 'xls', 'csv'].includes(ext)) {
        alert('กรุณาเลือกไฟล์สเปรดชีต Excel (.xlsx, .xls) หรือ CSV (.csv) เท่านั้น');
        return;
    }

    selectedStudentExcelFile = file;
    const label = document.getElementById('excel-student-file-name-label');
    if (label) {
        const sizeKb = (file.size / 1024).toFixed(1);
        label.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> เลือกไฟล์แล้ว: <strong>${file.name}</strong> (${sizeKb} KB)`;
        const parentBox = label.closest('div');
        if (parentBox) {
            parentBox.style.backgroundColor = '#dcfce7';
            parentBox.style.border = '1.5px solid #22c55e';
        }
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        try {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
            const jsonRows = XLSX.utils.sheet_to_json(firstSheet);

            if (!jsonRows || jsonRows.length === 0) {
                alert('ไม่พบข้อมูลรายชื่อในไฟล์ที่เลือก');
                clearAdminStudentFile();
                return;
            }

            adminParsedStudentRows = jsonRows;
            currentImportedFileType = detectIsAdvisorFile(jsonRows, file.name) ? 'advisor' : 'student';
            renderAdminStudentPreImportPreview();
        } catch (err) {
            console.error("Admin file read error:", err);
            alert('เกิดข้อผิดพลาดในการอ่านไฟล์สเปรดชีต กรุณาตรวจสอบรูปแบบไฟล์');
            clearAdminStudentFile();
        }
    };
    reader.readAsArrayBuffer(file);
}

function clearAdminStudentFile() {
    selectedStudentExcelFile = null;
    adminParsedStudentRows = [];
    currentImportedFileType = 'student';

    const input = document.getElementById('admin-student-excel-file-input');
    if (input) input.value = '';

    const label = document.getElementById('excel-student-file-name-label');
    if (label) {
        label.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg> คลิกเพื่อเลือกไฟล์ Excel รายชื่อนิสิต, อาจารย์ (.xlsx / .csv)`;
        const parentBox = label.closest('div');
        if (parentBox) {
            parentBox.style.backgroundColor = '#ffffff';
            parentBox.style.border = '1.5px dashed #86efac';
        }
    }

    const previewContainer = document.getElementById('admin-student-preview-container');
    if (previewContainer) previewContainer.style.display = 'none';

    const dupAlert = document.getElementById('admin-student-preview-dup-alert');
    if (dupAlert) {
        dupAlert.style.display = 'none';
        dupAlert.innerHTML = '';
    }

    const importBtn = document.getElementById('admin-student-import-btn');
    if (importBtn) {
        importBtn.disabled = true;
        importBtn.style.opacity = '0.6';
        importBtn.style.cursor = 'not-allowed';
        importBtn.style.backgroundColor = '#16a34a';
        const importBtnText = document.getElementById('admin-student-import-btn-text');
        if (importBtnText) {
            importBtnText.textContent = 'นำเข้ารายชื่อนิสิต, อาจารย์เข้าสู่ระบบ';
        } else {
            importBtn.textContent = 'นำเข้ารายชื่อเข้าสู่ระบบ';
        }
    }
}

function renderAdminStudentPreImportPreview(isPostImport = false, postImportList = null) {
    const previewContainer = document.getElementById('admin-student-preview-container');
    const countBadge = document.getElementById('admin-student-preview-count-badge');
    const statusTag = document.getElementById('admin-student-preview-status-tag');
    const titleText = document.getElementById('admin-student-preview-title-text');
    const secPills = document.getElementById('admin-student-preview-sec-pills');
    const dupAlertBox = document.getElementById('admin-student-preview-dup-alert');
    const tbody = document.getElementById('admin-student-preview-tbody');
    const importBtn = document.getElementById('admin-student-import-btn');
    const importBtnText = document.getElementById('admin-student-import-btn-text');
    const postNotice = document.getElementById('admin-student-post-notice');

    const rawRows = (typeof adminParsedStudentRows !== 'undefined' && adminParsedStudentRows && adminParsedStudentRows.length > 0)
        ? adminParsedStudentRows
        : (window.adminParsedStudentRows || []);
    const rowsToDisplay = isPostImport && Array.isArray(postImportList)
        ? postImportList
        : rawRows;

    if (!rowsToDisplay || rowsToDisplay.length === 0) {
        if (previewContainer) previewContainer.style.display = 'none';
        return;
    }

    if (previewContainer) {
        previewContainer.style.display = 'block';
        previewContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    if (countBadge) countBadge.textContent = `${rowsToDisplay.length} รายการ`;

    // อัปเดตหัวตารางพรีวิวตามประเภทไฟล์
    const thead = document.querySelector('#admin-student-preview-container table thead');
    if (thead) {
        if (currentImportedFileType === 'advisor') {
            thead.innerHTML = `
                        <tr style="background: #f1f5f9; border-bottom: 2px solid #cbd5e1; color: #334155; position: sticky; top: 0; z-index: 2;">
                            <th style="padding: 10px 12px; text-align: center; width: 55px;">ลำดับ</th>
                            <th style="padding: 10px 12px; text-align: left; width: 120px;">รหัสอาจารย์</th>
                            <th style="padding: 10px 12px; text-align: left; width: 220px;">ชื่อ - นามสกุล</th>
                            <th style="padding: 10px 12px; text-align: center; width: 150px;">หมู่เรียนที่รับผิดชอบ</th>
                            <th style="padding: 10px 12px; text-align: left; width: 180px;">อีเมลมหาวิทยาลัย</th>
                            <th style="padding: 10px 12px; text-align: center; width: 130px;">เบอร์โทรศัพท์</th>
                            <th style="padding: 10px 12px; text-align: center; width: 100px;">บทบาท</th>
                        </tr>
                    `;
        } else {
            thead.innerHTML = `
                        <tr style="background: #f1f5f9; border-bottom: 2px solid #cbd5e1; color: #334155; position: sticky; top: 0; z-index: 2;">
                            <th style="padding: 10px 12px; text-align: center; width: 55px;">ลำดับ</th>
                            <th style="padding: 10px 12px; text-align: left; width: 120px;">รหัสนิสิต</th>
                            <th style="padding: 10px 12px; text-align: left; width: 180px;">ชื่อ - นามสกุล</th>
                            <th style="padding: 10px 12px; text-align: center; width: 100px;">หมู่เรียน</th>
                            <th style="padding: 10px 12px; text-align: left; width: 150px;">อาจารย์ที่ปรึกษา</th>
                            <th style="padding: 10px 12px; text-align: left;">สถานประกอบการ</th>
                            <th style="padding: 10px 12px; text-align: center; width: 140px;">พิกัด GPS</th>
                        </tr>
                    `;
        }
    }

    if (isPostImport) {
        // ==============================================================
        // POST-IMPORT STATE (หลังเพิ่มไฟล์เข้าไป)
        // ==============================================================
        if (titleText) {
            titleText.textContent = (currentImportedFileType === 'advisor')
                ? 'พรีวิวผลลัพธ์รายชื่ออาจารย์ที่นำเข้าล่าสุด:'
                : 'พรีวิวผลลัพธ์รายชื่อนิสิต, อาจารย์ที่นำเข้าล่าสุด:';
        }
        if (statusTag) {
            statusTag.textContent = 'นำเข้าสำเร็จแล้ว (พร้อมใช้งาน)';
            statusTag.style.background = '#dcfce7';
            statusTag.style.color = '#15803d';
        }
        if (postNotice) {
            postNotice.style.display = 'block';
            if (currentImportedFileType === 'advisor') {
                postNotice.innerHTML = `
                            <div style="font-weight: 700; margin-bottom: 3px; display: flex; align-items: center; gap: 6px; font-size: 13px;">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                                นำเข้ารายชื่ออาจารย์นิเทศสำเร็จและบันทึกเข้าสู่ระบบเรียบร้อยแล้ว
                            </div>
                            <div style="line-height: 1.4;">ข้อมูลอาจารย์ถูกจัดเก็บเข้าสู่ระบบและพร้อมใช้งานในแท็บ "รายชื่ออาจารย์ (Advisors)" ด้านบนทันที</div>
                        `;
            } else {
                postNotice.innerHTML = `
                            <div style="font-weight: 700; margin-bottom: 3px; display: flex; align-items: center; gap: 6px; font-size: 13px;">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                                นำเข้ารายชื่อนิสิต, อาจารย์สำเร็จและบันทึกเข้าสู่ระบบเรียบร้อยแล้ว
                            </div>
                            <div style="line-height: 1.4;">ข้อมูลทั้งหมดถูกบันทึกลงในระบบเรียบร้อย สามารถตรวจสอบข้อมูลบัญชีผู้ใช้ (รหัสผ่านแรกเข้า: 123456) และพิกัดสถานประกอบการที่นำเข้าได้จากตารางด้านบนนี้ทันที</div>
                        `;
            }
        }

        if (importBtn) {
            importBtn.disabled = true;
            importBtn.style.opacity = '0.7';
            importBtn.style.cursor = 'default';
            importBtn.style.backgroundColor = '#059669';
            if (importBtnText) {
                importBtnText.textContent = (currentImportedFileType === 'advisor')
                    ? `นำเข้ารายชื่ออาจารย์สำเร็จ (${rowsToDisplay.length} ท่าน) บันทึกในระบบแล้ว`
                    : `นำเข้ารายชื่อสำเร็จ (${rowsToDisplay.length} รายการ) บันทึกในระบบแล้ว`;
            }
        }

        if (secPills) {
            if (currentImportedFileType === 'advisor') {
                secPills.innerHTML = `
                            <span style="background: #dcfce7; color: #166534; border: 1px solid #86efac; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;">
                                อาจารย์นิเทศ: ${rowsToDisplay.length} ท่าน
                            </span>
                        `;
            } else {
                const secCounts = {};
                rowsToDisplay.forEach(item => {
                    const sec = item.section || 'หมู่ 700';
                    secCounts[sec] = (secCounts[sec] || 0) + 1;
                });
                secPills.innerHTML = Object.entries(secCounts).map(([sec, count]) => `
                            <span style="background: #dcfce7; color: #166534; border: 1px solid #86efac; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;">
                                ${sec}: ${count} คน
                            </span>
                        `).join('');
            }
        }

        if (tbody) {
            tbody.innerHTML = '';
            if (currentImportedFileType === 'advisor') {
                rowsToDisplay.forEach((item, idx) => {
                    const tr = document.createElement('tr');
                    tr.style.borderBottom = '1px solid #e2e8f0';
                    tr.style.backgroundColor = (idx % 2 === 0) ? '#ffffff' : '#f8fafc';
                    tr.innerHTML = `
                                <td style="padding: 10px 12px; text-align: center; color: #64748b; font-weight: 600;">${idx + 1}</td>
                                <td style="padding: 10px 12px; font-weight: 700; color: #1e40af;">${item.id || item.advisor_id || '-'}</td>
                                <td style="padding: 10px 12px; font-weight: 600; color: #0f172a;">${item.name || '-'}</td>
                                <td style="padding: 10px 12px; text-align: center;">
                                    <span style="background: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">${item.section || 'ไม่ระบุ'}</span>
                                </td>
                                <td style="padding: 10px 12px; color: #059669; font-weight: 600;">${item.email || '-'}</td>
                                <td style="padding: 10px 12px; text-align: center; color: #475569;">${item.phone || '-'}</td>
                                <td style="padding: 10px 12px; text-align: center;">
                                    <span class="status-badge badge-success" style="font-size: 10.5px;">อาจารย์นิเทศ</span>
                                </td>
                            `;
                    tbody.appendChild(tr);
                });
            } else {
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
                                    <div style="display: flex; flex-direction: column; gap: 3px; align-items: center;">
                                        <span style="background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">
                                            ${item.section || 'หมู่ 700'}
                                        </span>
                                        <span style="background: #eff6ff; color: #1d4ed8; padding: 1px 6px; border-radius: 4px; font-size: 9.5px; font-weight: 600;">
                                            ${item.semester || 'ภาคต้น 2569'}
                                        </span>
                                    </div>
                                </td>
                                <td style="padding: 10px 12px; color: #334155; font-size: 11.5px;">${item.advisor || '-'}</td>
                                <td style="padding: 10px 12px; color: #1e293b; font-size: 11.5px; font-weight: 500;">${item.company || item.company_name || '-'}</td>
                                <td style="padding: 10px 12px; text-align: center;">${coordsBadge}</td>
                            `;
                    tbody.appendChild(tr);
                });
            }
        }

    } else {
        // ==============================================================
        // PRE-IMPORT STATE (ก่อนเพิ่มไฟล์ / รอการยืนยัน)
        // ==============================================================
        if (titleText) {
            titleText.textContent = (currentImportedFileType === 'advisor')
                ? 'พรีวิวข้อมูลรายชื่ออาจารย์ในไฟล์ Excel:'
                : 'พรีวิวข้อมูลในไฟล์ Excel:';
        }
        if (statusTag) {
            statusTag.style.display = 'none';
        }
        if (postNotice) postNotice.style.display = 'none';

        // ==============================================================
        // ตรวจสอบข้อมูลซ้ำในขั้นตอนพรีวิวก่อนยืนยัน (ระบุตัวบุคคลและสาเหตุชัดเจน)
        // ==============================================================
        const customUsersCheckPre = JSON.parse(localStorage.getItem('customUsers') || '{}');
        const existingStudentKeysPre = new Map(); // key -> { id, name, email, role }
        const existingStudentsPre = (typeof getAllSystemStudents === 'function') ? getAllSystemStudents() : [];
        existingStudentsPre.forEach(s => {
            const entry = {
                id: s.id || s.student_id || '',
                name: s.name || s.fullname || 'นิสิตในระบบ',
                email: s.email || '',
                role: 'student'
            };
            if (s.id) existingStudentKeysPre.set(String(s.id).trim().toLowerCase(), entry);
            if (s.student_id) existingStudentKeysPre.set(String(s.student_id).trim().toLowerCase(), entry);
            if (s.email) existingStudentKeysPre.set(String(s.email).trim().toLowerCase(), entry);
        });
        Object.values(customUsersCheckPre).forEach(u => {
            if (u && u.role === 'student') {
                const entry = {
                    id: u.id || u.student_id || '',
                    name: u.name || 'นิสิตในระบบ',
                    email: u.email || '',
                    role: 'student'
                };
                if (u.id) existingStudentKeysPre.set(String(u.id).trim().toLowerCase(), entry);
                if (u.student_id) existingStudentKeysPre.set(String(u.student_id).trim().toLowerCase(), entry);
                if (u.email) existingStudentKeysPre.set(String(u.email).trim().toLowerCase(), entry);
            }
        });

        const existingAdvisorKeysPre = new Map();
        const defaultAdvisors = [
            { id: 'ADV001', name: 'อาจารย์ สมชาย แจ่มใส', email: 'somchai.j@ku.th' },
            { id: 'ADV002', name: 'อาจารย์ สมหญิง รักเรียน', email: 'somying.r@ku.th' },
            { id: 'ADV003', name: 'อาจารย์ สมจิต มั่งมี', email: 'somjit.m@ku.th' }
        ];
        defaultAdvisors.forEach(a => {
            const entry = { id: a.id, name: a.name, email: a.email, role: 'advisor' };
            existingAdvisorKeysPre.set(String(a.id).trim().toLowerCase(), entry);
            existingAdvisorKeysPre.set(String(a.email).trim().toLowerCase(), entry);
        });
        Object.values(customUsersCheckPre).forEach(u => {
            if (u && u.role === 'advisor') {
                const entry = {
                    id: u.id || u.advisor_id || '',
                    name: u.name || 'อาจารย์ในระบบ',
                    email: u.email || '',
                    role: 'advisor'
                };
                if (u.id) existingAdvisorKeysPre.set(String(u.id).trim().toLowerCase(), entry);
                if (u.advisor_id) existingAdvisorKeysPre.set(String(u.advisor_id).trim().toLowerCase(), entry);
                if (u.email) existingAdvisorKeysPre.set(String(u.email).trim().toLowerCase(), entry);
            }
        });

        const rowAnalysis = [];
        const duplicateItems = [];
        const seenKeysPre = new Map(); // key -> row index (1-based)

        rowsToDisplay.forEach((row, idx) => {
            const rowIdx = idx + 1;
            const emailRaw = findRowEmail(row, ['อีเมลมหาวิทยาลัย', 'อีเมล', 'อีเมล์', 'Email', 'email', 'E-mail', 'KU-Mail', 'KU Mail', 'เมล']);
            const email = emailRaw ? String(emailRaw).trim().toLowerCase() : '';

            let isDup = false;
            let dupReason = '';
            let targetId = '';
            let targetName = '';

            if (currentImportedFileType === 'advisor') {
                const advId = findRowValue(row, ['รหัสประจำตัว', 'รหัสอาจารย์', 'รหัส', 'ID', 'advisor_id']) || `ADV_${rowIdx}`;
                const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name']);
                const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']);
                targetName = title ? `${title} ${name}`.trim() : (name || 'อาจารย์นิเทศ');
                targetId = advId;
                const keyId = advId ? String(advId).trim().toLowerCase() : '';

                if (keyId && existingAdvisorKeysPre.has(keyId)) {
                    isDup = true;
                    dupReason = `รหัสอาจารย์ "${advId}" มีอยู่ในระบบแล้ว`;
                } else if (email && existingAdvisorKeysPre.has(email)) {
                    isDup = true;
                    dupReason = `อีเมล "${email}" มีอยู่ในระบบแล้ว`;
                } else if (keyId && seenKeysPre.has(keyId)) {
                    isDup = true;
                    dupReason = `รหัสซ้ำกับแถวที่ ${seenKeysPre.get(keyId)} ในไฟล์นี้`;
                } else if (email && seenKeysPre.has(email)) {
                    isDup = true;
                    dupReason = `อีเมลซ้ำกับแถวที่ ${seenKeysPre.get(email)} ในไฟล์นี้`;
                }

                if (keyId && !seenKeysPre.has(keyId)) seenKeysPre.set(keyId, rowIdx);
                if (email && !seenKeysPre.has(email)) seenKeysPre.set(email, rowIdx);
            } else {
                const stdId = findRowValue(row, ['รหัสนิสิต', 'รหัสประจำตัว', 'รหัสนักศึกษา', 'รหัส', 'ID', 'Student ID', 'student_id']) || `STD_${rowIdx}`;
                const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname']);
                const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']);
                targetName = title ? `${title} ${name}`.trim() : (name || 'นิสิต');
                targetId = stdId;
                const keyId = stdId ? String(stdId).trim().toLowerCase() : '';

                if (keyId && existingStudentKeysPre.has(keyId)) {
                    isDup = true;
                    dupReason = `รหัสนิสิต "${stdId}" มีอยู่ในระบบแล้ว`;
                } else if (email && existingStudentKeysPre.has(email)) {
                    isDup = true;
                    dupReason = `อีเมล "${email}" มีอยู่ในระบบแล้ว`;
                } else if (keyId && seenKeysPre.has(keyId)) {
                    isDup = true;
                    dupReason = `รหัสนิสิตซ้ำกับแถวที่ ${seenKeysPre.get(keyId)} ในไฟล์นี้`;
                } else if (email && seenKeysPre.has(email)) {
                    isDup = true;
                    dupReason = `อีเมลซ้ำกับแถวที่ ${seenKeysPre.get(email)} ในไฟล์นี้`;
                }

                if (keyId && !seenKeysPre.has(keyId)) seenKeysPre.set(keyId, rowIdx);
                if (email && !seenKeysPre.has(email)) seenKeysPre.set(email, rowIdx);
            }

            if (isDup) {
                duplicateItems.push({
                    index: rowIdx,
                    id: targetId,
                    name: targetName,
                    email: email || '-',
                    reason: dupReason
                });
            }

            rowAnalysis.push({
                index: rowIdx,
                isDup: isDup,
                dupReason: dupReason
            });
        });

        // จัดการสถานะปุ่มนำเข้า และกล่องแจ้งเตือนรายการซ้ำ
        if (duplicateItems.length > 0) {
            if (importBtn) {
                importBtn.disabled = true;
                importBtn.style.opacity = '0.75';
                importBtn.style.cursor = 'not-allowed';
                importBtn.style.backgroundColor = '#dc2626';
                if (importBtnText) {
                    if (duplicateItems.length === 1) {
                        importBtnText.textContent = `↑ ไม่สามารถนำเข้าได้: พบข้อมูลซ้ำ (${duplicateItems[0].name})`;
                    } else if (duplicateItems.length === 2) {
                        importBtnText.textContent = `↑ ไม่สามารถนำเข้าได้: พบข้อมูลซ้ำ (${duplicateItems[0].name}, ${duplicateItems[1].name})`;
                    } else {
                        importBtnText.textContent = `↑ ไม่สามารถนำเข้าได้: พบข้อมูลซ้ำกับในระบบ (${duplicateItems.length} รายการ)`;
                    }
                }
            }

            if (dupAlertBox) {
                dupAlertBox.style.display = 'block';
                dupAlertBox.innerHTML = `
                    <div style="background: #fef2f2; border: 1.5px solid #f87171; border-radius: 8px; padding: 12px 16px; color: #991b1b; box-shadow: 0 2px 6px rgba(220, 38, 38, 0.08);">
                        <div style="font-weight: 700; font-size: 13px; display: flex; align-items: center; gap: 8px; margin-bottom: 6px; color: #b91c1c;">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                            <span>ไม่สามารถนำเข้าได้: พบข้อมูลซ้ำกับในระบบทั้งหมด ${duplicateItems.length} รายการ (แถวสีแดงในตาราง)</span>
                        </div>
                        <div style="font-size: 12px; line-height: 1.6; margin-left: 26px;">
                            <div style="font-weight: 600; margin-bottom: 4px; color: #7f1d1d;">รายชื่อและเหตุผลที่พบข้อมูลซ้ำ:</div>
                            <ul style="margin: 0; padding-left: 20px;">
                                ${duplicateItems.map(d => `
                                    <li style="margin-bottom: 4px;">
                                        <strong>แถวที่ ${d.index}: ${d.name}</strong> 
                                        (รหัส: <code style="background: #fee2e2; padding: 1px 4px; border-radius: 3px; font-weight: 600;">${d.id}</code>, อีเมล: ${d.email})
                                        &mdash; <span style="color: #dc2626; font-weight: 700;">${d.reason}</span>
                                    </li>
                                `).join('')}
                            </ul>
                            <div style="margin-top: 8px; color: #991b1b; font-size: 11.5px; border-top: 1px dashed #fca5a5; padding-top: 6px;">
                                💡 <strong>คำแนะนำ:</strong> กรุณาลบแถวที่มีข้อมูลซ้ำออกจากไฟล์ Excel หรือแก้ไขรหัส/อีเมลให้ถูกต้อง จากนั้นกดปุ่ม "เปลี่ยนไฟล์ / ล้าง" แล้วเลือกไฟล์ใหม่อีกครั้ง
                            </div>
                        </div>
                    </div>
                `;
            }
        } else {
            if (dupAlertBox) {
                dupAlertBox.style.display = 'none';
                dupAlertBox.innerHTML = '';
            }
            if (importBtn) {
                importBtn.disabled = false;
                importBtn.style.opacity = '1';
                importBtn.style.cursor = 'pointer';
                importBtn.style.backgroundColor = '#16a34a';
                if (importBtnText) {
                    importBtnText.textContent = (currentImportedFileType === 'advisor')
                        ? `ยืนยันนำเข้ารายชื่ออาจารย์ (${rowsToDisplay.length} ท่าน) เข้าสู่ระบบ`
                        : `ยืนยันนำเข้ารายชื่อนิสิต, อาจารย์ (${rowsToDisplay.length} รายการ) เข้าสู่ระบบ`;
                }
            }
        }

        if (secPills) {
            if (currentImportedFileType === 'advisor') {
                secPills.innerHTML = `
                            <span style="background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;">
                                พบข้อมูลอาจารย์นิเทศ: ${rowsToDisplay.length} ท่าน
                            </span>
                        `;
            } else {
                const secCounts = {};
                const semCounts = {};
                rowsToDisplay.forEach(row => {
                    const sectionVal = findRowValue(row, ['หมู่เรียน', 'หมู่เรียนที่รับผิดชอบ', 'หมู่', 'Section', 'section']);
                    const sec = normalizeCleanSection(sectionVal, 'หมู่ 700');
                    secCounts[sec] = (secCounts[sec] || 0) + 1;

                    const rowSem = formatCombinedSemester(
                        findRowValue(row, ['ภาคการศึกษา', 'ภาคเรียน', 'ภาค', 'เทอม', 'Semester', 'semester', 'Term', 'term']),
                        findRowValue(row, ['ปีการศึกษา', 'ปีการศึกษาที่', 'ปีศึกษา', 'AcademicYear', 'academic_year', 'academicYear', 'acad_year']),
                        'ภาคต้น 2569'
                    );
                    semCounts[rowSem] = (semCounts[rowSem] || 0) + 1;
                });
                const secBadges = Object.entries(secCounts).map(([sec, count]) => `
                            <span style="background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;">
                                ${sec}: ${count} คน
                            </span>
                        `).join('');
                const semBadges = Object.entries(semCounts).map(([sem, count]) => `
                            <span style="background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;">
                                ภาคการศึกษา: ${sem} (${count} คน)
                            </span>
                        `).join('');
                secPills.innerHTML = secBadges + semBadges;
            }
        }

        if (tbody) {
            tbody.innerHTML = '';
            if (currentImportedFileType === 'advisor') {
                rowsToDisplay.forEach((row, idx) => {
                    const analysis = rowAnalysis[idx] || { isDup: false, dupReason: '' };
                    const advId = findRowValue(row, ['รหัสประจำตัว', 'รหัสอาจารย์', 'รหัส', 'ID', 'advisor_id']) || `ADV_${idx + 1}`;
                    const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name']);
                    const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']);
                    const fullName = title ? `${title} ${name}`.trim() : (name || 'อาจารย์นิเทศ');
                    const emailVal = findRowEmail(row, ['อีเมลมหาวิทยาลัย', 'อีเมล', 'Email', 'KU-Mail']) || '-';
                    let secVal = findRowValue(row, ['หมู่เรียนที่รับผิดชอบ', 'หมู่เรียน', 'Section']) || '700, 800';
                    if (!secVal.includes('หมู่') && (secVal.includes('700') || secVal.includes('800'))) {
                        const parts = secVal.split(',').map(s => s.trim().replace(/[^0-9]/g, ''));
                        secVal = parts.map(p => `หมู่ ${p}`).join(', ');
                    }
                    const phoneVal = findRowValue(row, ['เบอร์โทรศัพท์', 'เบอร์โทร', 'Phone', 'Tel']) || '-';

                    const tr = document.createElement('tr');
                    tr.style.borderBottom = '1px solid #e2e8f0';
                    if (analysis.isDup) {
                        tr.style.backgroundColor = '#fef2f2';
                        tr.style.borderLeft = '4px solid #ef4444';
                    } else {
                        tr.style.backgroundColor = (idx % 2 === 0) ? '#ffffff' : '#f8fafc';
                        tr.style.borderLeft = '4px solid transparent';
                    }

                    const idDisplay = analysis.isDup
                        ? `<div><span style="color: #dc2626; font-weight: 800;">${advId}</span> <span style="background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; padding: 1px 5px; border-radius: 4px; font-size: 9.5px; font-weight: 700;">ซ้ำ</span></div>`
                        : `<span style="color: #1e40af; font-weight: 700;">${advId}</span>`;

                    const dupBadgeOrReady = analysis.isDup
                        ? `<div style="margin-top: 4px;">
                                <span style="background: #fee2e2; color: #b91c1c; border: 1px solid #f87171; padding: 2px 8px; border-radius: 4px; font-size: 10.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                                    ซ้ำในระบบ: ${analysis.dupReason}
                                </span>
                           </div>`
                        : `<div style="margin-top: 3px;">
                                <span style="background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; padding: 1px 6px; border-radius: 4px; font-size: 9.5px; font-weight: 600; display: inline-flex; align-items: center; gap: 3px;">
                                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                                    พร้อมนำเข้า
                                </span>
                           </div>`;

                    tr.innerHTML = `
                                <td style="padding: 10px 12px; text-align: center; color: #64748b; font-weight: 600;">${idx + 1}</td>
                                <td style="padding: 10px 12px;">${idDisplay}</td>
                                <td style="padding: 10px 12px; font-weight: 600; color: #0f172a;">
                                    <div>${fullName}</div>
                                    ${dupBadgeOrReady}
                                </td>
                                <td style="padding: 10px 12px; text-align: center;">
                                    <span style="background: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">${secVal}</span>
                                </td>
                                <td style="padding: 10px 12px; color: ${analysis.isDup ? '#dc2626' : '#059669'}; font-weight: 600;">${emailVal}</td>
                                <td style="padding: 10px 12px; text-align: center; color: #475569;">${phoneVal}</td>
                                <td style="padding: 10px 12px; text-align: center;">
                                    <span class="status-badge ${analysis.isDup ? 'badge-danger' : 'badge-success'}" style="font-size: 10.5px;">${analysis.isDup ? 'ข้อมูลซ้ำ' : 'อาจารย์นิเทศ'}</span>
                                </td>
                            `;
                    tbody.appendChild(tr);
                });
            } else {
                rowsToDisplay.forEach((row, idx) => {
                    const analysis = rowAnalysis[idx] || { isDup: false, dupReason: '' };
                    const studentId = findRowValue(row, ['รหัสนิสิต', 'รหัสประจำตัว', 'รหัสนักศึกษา', 'รหัส', 'ID', 'Student ID', 'student_id']) || `STD_${idx + 1}`;
                    const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname']);
                    const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']);
                    const fullName = title ? `${title} ${name}`.trim() : (name || 'นิสิต');
                    const emailVal = findRowEmail(row, ['อีเมลมหาวิทยาลัย', 'อีเมล', 'อีเมล์', 'Email', 'email', 'E-mail', 'KU-Mail']) || `${studentId}@ku.th`;
                    const sectionVal = findRowValue(row, ['หมู่เรียน', 'หมู่เรียนที่รับผิดชอบ', 'หมู่', 'Section', 'section']);
                    const sec = normalizeCleanSection(sectionVal, 'หมู่ 700');
                    const advisorVal = findRowValue(row, ['อาจารย์ที่ปรึกษา', 'อาจารย์ที่ปึกษา', 'อาจารย์นิเทศ', 'อาจารย์', 'Advisor', 'advisor', 'ที่ปรึกษา', 'ที่ปึกษา']) || '-';
                    const company = findRowValue(row, ['ชื่อสถานประกอบการ', 'สถานประกอบการ', 'Company', 'company']) || '-';

                    const rowSem = formatCombinedSemester(
                        findRowValue(row, ['ภาคการศึกษา', 'ภาคเรียน', 'ภาค', 'เทอม', 'Semester', 'semester', 'Term', 'term']),
                        findRowValue(row, ['ปีการศึกษา', 'ปีการศึกษาที่', 'ปีศึกษา', 'AcademicYear', 'academic_year', 'academicYear', 'acad_year']),
                        'ภาคต้น 2569'
                    );

                    const locationCoord = findRowValue(row, ['พิกัด', 'พิกัด GPS', 'GPS', 'Location', 'พิกัดจีพีเอส']);
                    let coordsBadge = `<span style="color: #94a3b8; font-size: 11px;">-</span>`;
                    if (locationCoord) {
                        coordsBadge = `<span style="background: #f1f5f9; color: #475569; padding: 3px 8px; border-radius: 4px; font-family: monospace; font-size: 11px; font-weight: 600;">${locationCoord}</span>`;
                    }

                    const tr = document.createElement('tr');
                    tr.style.borderBottom = '1px solid #e2e8f0';
                    if (analysis.isDup) {
                        tr.style.backgroundColor = '#fef2f2';
                        tr.style.borderLeft = '4px solid #ef4444';
                    } else {
                        tr.style.backgroundColor = (idx % 2 === 0) ? '#ffffff' : '#f8fafc';
                        tr.style.borderLeft = '4px solid transparent';
                    }

                    const idDisplay = analysis.isDup
                        ? `<div><span style="color: #dc2626; font-weight: 800;">${studentId}</span> <span style="background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; padding: 1px 5px; border-radius: 4px; font-size: 9.5px; font-weight: 700;">ซ้ำ</span></div>`
                        : `<span style="color: #0f172a; font-weight: 700;">${studentId}</span>`;

                    const dupBadgeOrReady = analysis.isDup
                        ? `<div style="margin-top: 4px;">
                                <span style="background: #fee2e2; color: #b91c1c; border: 1px solid #f87171; padding: 2px 8px; border-radius: 4px; font-size: 10.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                                    ซ้ำในระบบ: ${analysis.dupReason}
                                </span>
                           </div>`
                        : `<div style="margin-top: 3px;">
                                <span style="background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; padding: 1px 6px; border-radius: 4px; font-size: 9.5px; font-weight: 600; display: inline-flex; align-items: center; gap: 3px;">
                                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                                    พร้อมนำเข้า
                                </span>
                           </div>`;

                    tr.innerHTML = `
                                <td style="padding: 10px 12px; text-align: center; color: #64748b; font-weight: 600;">${idx + 1}</td>
                                <td style="padding: 10px 12px;">${idDisplay}</td>
                                <td style="padding: 10px 12px; font-weight: 600; color: #1e293b;">
                                    <div>${fullName}</div>
                                    <div style="font-size: 10.5px; color: ${analysis.isDup ? '#dc2626' : '#64748b'};">${emailVal}</div>
                                    ${dupBadgeOrReady}
                                </td>
                                <td style="padding: 10px 12px; text-align: center;">
                                    <div style="display: flex; flex-direction: column; gap: 3px; align-items: center;">
                                        <span style="background: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">
                                            ${sec}
                                        </span>
                                        <span style="background: #eff6ff; color: #1d4ed8; padding: 1px 6px; border-radius: 4px; font-size: 9.5px; font-weight: 600;">
                                            ${rowSem}
                                        </span>
                                    </div>
                                </td>
                                <td style="padding: 10px 12px; color: #334155; font-size: 11.5px;">${advisorVal}</td>
                                <td style="padding: 10px 12px; color: #1e293b; font-size: 11.5px; font-weight: 500;">${company}</td>
                                <td style="padding: 10px 12px; text-align: center;">${coordsBadge}</td>
                            `;
                    tbody.appendChild(tr);
                });
            }
        }
    }
}

function handleAdvisorExcelSelected(event) {
    const file = event.target.files[0];
    if (file) {
        selectedAdvisorExcelFile = file;
        const label = document.getElementById('excel-advisor-file-name-label');
        if (label) {
            label.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> เลือกไฟล์รายชื่ออาจารย์แล้ว: ` + file.name;
            label.parentElement.style.backgroundColor = '#dbeafe';
            label.parentElement.style.border = '1.5px solid #3b82f6';
        }
    }
}

function formatCombinedSemester(termVal, yearVal, fallback = 'ภาคต้น 2569') {
    let rawTerm = String(termVal || '').trim();
    let rawYear = String(yearVal || '').trim();

    if (rawYear) {
        const yMatch = rawYear.match(/\d{2,4}/);
        if (yMatch) {
            let y = yMatch[0];
            if (y.length === 2) y = '25' + y;
            rawYear = y;
        }
    }

    if (!rawYear && rawTerm) {
        const yInTerm = rawTerm.match(/25\d{2}|\b[56]\d\b/);
        if (yInTerm) {
            let y = yInTerm[0];
            if (y.length === 2) y = '25' + y;
            rawYear = y;
            rawTerm = rawTerm.replace(yInTerm[0], '').trim();
        }
    }

    let normalizedTerm = '';
    const lowerTerm = rawTerm.toLowerCase();
    if (lowerTerm.includes('ปลาย') || lowerTerm === '2' || lowerTerm.includes('second')) {
        normalizedTerm = 'ภาคปลาย';
    } else if (lowerTerm.includes('ต้น') || lowerTerm === '1' || lowerTerm.includes('first')) {
        normalizedTerm = 'ภาคต้น';
    } else if (lowerTerm.includes('ฤดูร้อน') || lowerTerm.includes('ซัมเมอร์') || lowerTerm === '3' || lowerTerm.includes('summer')) {
        normalizedTerm = 'ภาคฤดูร้อน';
    } else if (rawTerm) {
        normalizedTerm = rawTerm.startsWith('ภาค') ? rawTerm : `ภาค${rawTerm}`;
    }

    if (normalizedTerm && rawYear) {
        return `${normalizedTerm} ${rawYear}`;
    }
    if (normalizedTerm) {
        return `${normalizedTerm} 2569`;
    }
    if (rawYear) {
        return `ภาคต้น ${rawYear}`;
    }
    return fallback;
}

function findRowValue(row, possibleKeys) {
    if (!row) return '';
    const rowKeys = Object.keys(row);
    for (const key of possibleKeys) {
        if (row[key] !== undefined && row[key] !== null && String(row[key]).trim() !== '') {
            return String(row[key]).trim();
        }
        const normKey = key.toLowerCase().replace(/[\s\-_]/g, '').replace(/์/g, '');
        const matchedKey = rowKeys.find(k => k.toLowerCase().replace(/[\s\-_]/g, '').replace(/์/g, '') === normKey);
        if (matchedKey && row[matchedKey] !== undefined && row[matchedKey] !== null && String(row[matchedKey]).trim() !== '') {
            return String(row[matchedKey]).trim();
        }
    }
    return '';
}

function findRowEmail(row, possibleKeys) {
    const val = findRowValue(row, possibleKeys);
    if (val && val.includes('@')) {
        return val.trim();
    }
    if (row) {
        for (const k of Object.keys(row)) {
            const cellVal = String(row[k] || '').trim();
            if (cellVal.includes('@') && cellVal.includes('.')) {
                return cellVal;
            }
        }
    }
    return val || '';
}

// ===================================================================
// UNIVERSAL POST-ADDITION PREVIEW MODAL LOGIC (ADMIN & ADVISOR)
// ===================================================================
let postAddPreviewStudentsList = [];

function showPostAddPreviewModal(options = {}) {
    const {
        title = 'เพิ่ม / นำเข้ารายชื่อนิสิต, อาจารย์สำเร็จเรียบร้อย',
        roleTitle = 'ผู้ดูแลระบบ',
        source = 'admin_file',
        students = [],
        sectionsCountMap = {},
        emailSent = false
    } = options;

    postAddPreviewStudentsList = Array.isArray(students) ? students : [];

    const titleEl = document.getElementById('post-add-preview-title');
    if (titleEl) titleEl.textContent = title;

    const roleBadge = document.getElementById('post-add-badge-role');
    if (roleBadge) roleBadge.textContent = `บทบาท: ${roleTitle}`;

    const modeBadge = document.getElementById('post-add-badge-mode');
    if (modeBadge) {
        if (source === 'admin_file') modeBadge.textContent = 'วิธี: นำเข้าไฟล์ Excel (Admin)';
        else if (source === 'advisor_file') modeBadge.textContent = 'วิธี: นำเข้าไฟล์ Excel (อาจารย์)';
        else modeBadge.textContent = 'วิธี: บันทึกข้อมูลรายบุคคล';
    }

    const timeBadge = document.getElementById('post-add-badge-time');
    if (timeBadge) {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        const dateStr = now.toLocaleDateString('th-TH', { day: 'numeric', month: 'short', year: 'numeric' });
        timeBadge.textContent = `เวลาบันทึก: ${dateStr} ${timeStr}`;
    }

    const countStat = document.getElementById('post-add-stat-count');
    if (countStat) countStat.textContent = `${postAddPreviewStudentsList.length} คน`;

    const secStat = document.getElementById('post-add-stat-sections');
    if (secStat) {
        const entries = Object.entries(sectionsCountMap);
        if (entries.length > 0) {
            secStat.innerHTML = entries.map(([s, c]) => `${s}: <strong>${c}</strong> คน`).join('<br>');
        } else {
            secStat.textContent = '-';
        }
    }

    const authStat = document.getElementById('post-add-stat-auth');
    if (authStat) {
        authStat.innerHTML = 'รหัสผ่านแรกเข้า:<br><strong style="color: #15803d; font-family: monospace;">123456</strong>';
    }

    const searchInput = document.getElementById('post-add-search-input');
    if (searchInput) searchInput.value = '';

    const emailNotice = document.getElementById('post-add-email-notice');
    const emailNoticeText = document.getElementById('post-add-email-notice-text');
    if (emailNotice) {
        if (emailSent) {
            emailNotice.style.display = 'flex';
            emailNotice.style.background = '#f0fdf4';
            emailNotice.style.borderColor = '#bbf7d0';
            emailNotice.style.color = '#15803d';
            if (emailNoticeText) emailNoticeText.textContent = 'ระบบได้ส่งอีเมลแจ้งแรกเข้าใช้งาน (รหัสผ่านแรกเข้า: 123456) ไปยังอีเมลเคยูของนิสิตเรียบร้อยแล้ว';
        } else {
            emailNotice.style.display = 'flex';
            emailNotice.style.background = '#f8fafc';
            emailNotice.style.borderColor = '#e2e8f0';
            emailNotice.style.color = '#475569';
            if (emailNoticeText) emailNoticeText.textContent = 'นิสิตสามารถเข้าสู่ระบบครั้งแรกได้ทันทีโดยใช้อีเมลเคยู / รหัสนิสิต และรหัสผ่านแรกเข้า 123456';
        }
    }

    renderPostAddPreviewTable();
    openModal('modal-post-add-preview');
}

function renderPostAddPreviewTable(query = '') {
    const tbody = document.getElementById('post-add-preview-tbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    const q = (query || '').trim().toLowerCase();
    const filtered = (postAddPreviewStudentsList || []).filter(s => {
        if (!q) return true;
        const id = (s.id || s.student_id || '').toLowerCase();
        const name = (s.name || '').toLowerCase();
        const email = (s.email || '').toLowerCase();
        const sec = (s.section || '').toLowerCase();
        const company = (s.company || s.company_name || '').toLowerCase();
        return id.includes(q) || name.includes(q) || email.includes(q) || sec.includes(q) || company.includes(q);
    });

    if (filtered.length === 0) {
        tbody.innerHTML = `
                    <tr>
                        <td colspan="6" style="padding: 16px; text-align: center; color: #94a3b8; font-size: 11px;">
                            ไม่พบข้อมูลนิสิตที่ตรงกับคำค้นหา
                        </td>
                    </tr>
                `;
        return;
    }

    filtered.forEach((s, idx) => {
        const id = s.id || s.student_id || '-';
        const name = s.name || '-';
        const email = s.email || '-';
        const sec = s.section || 'หมู่ 700';
        const company = s.company || s.company_name || '-';

        const tr = document.createElement('tr');
        tr.style.borderBottom = '1px solid #f1f5f9';
        tr.style.backgroundColor = idx % 2 === 0 ? '#ffffff' : '#fcfcfd';
        tr.innerHTML = `
                    <td style="padding: 6px 8px; font-weight: 700; color: #0f172a; font-family: monospace;">${id}</td>
                    <td style="padding: 6px 8px; color: #1e293b; font-weight: 600;">${name}</td>
                    <td style="padding: 6px 8px; color: #0284c7;">${email}</td>
                    <td style="padding: 6px 8px;"><span style="background: #ecfdf5; color: #047857; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 10px;">${sec}</span></td>
                    <td style="padding: 6px 8px; color: #475569; max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${company}</td>
                    <td style="padding: 6px 8px; text-align: center;"><span style="background: #dcfce7; color: #15803d; padding: 2px 6px; border-radius: 10px; font-weight: 600; font-size: 9.5px;">พร้อมใช้งาน</span></td>
                `;
        tbody.appendChild(tr);
    });
}

function filterPostAddPreviewTable(query) {
    renderPostAddPreviewTable(query);
}

function goToStudentList() {
    closeModal('modal-post-add-preview');
    if (typeof switchAdvisorClassroomTab === 'function') {
        switchAdvisorClassroomTab('students');
    }
    const adminTable = document.getElementById('admin-users-table');
    if (adminTable && adminTable.offsetParent !== null) {
        adminTable.scrollIntoView({ behavior: 'smooth' });
    }
    const stdTable = document.getElementById('advisor-student-table-container');
    if (stdTable && stdTable.offsetParent !== null) {
        stdTable.scrollIntoView({ behavior: 'smooth' });
    }
}

function importStudentExcelFile() {
    if (!selectedStudentExcelFile) {
        alert('กรุณาคลิกเลือกไฟล์ Excel รายชื่อนิสิต, อาจารย์ (.xlsx / .csv) ก่อนกดนำเข้าข้อมูล');
        return;
    }

    const reader = new FileReader();
    reader.onload = async function (e) {
        try {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            const firstSheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[firstSheetName];
            const jsonRows = XLSX.utils.sheet_to_json(worksheet);

            if (!jsonRows || jsonRows.length === 0) {
                alert('ไม่พบข้อมูลรายชื่อในไฟล์ Excel ที่เลือก');
                return;
            }

            const isAdvisor = (currentImportedFileType === 'advisor') || detectIsAdvisorFile(jsonRows, selectedStudentExcelFile ? selectedStudentExcelFile.name : '');

            // ==============================================================
            // STRICT DUPLICATE CHECK (ตรวจสอบข้อมูลซ้ำกับในระบบก่อนนำเข้า)
            // ==============================================================
            const customUsersCheck = JSON.parse(localStorage.getItem('customUsers') || '{}');
            const existingStudents = (typeof getAllSystemStudents === 'function') ? getAllSystemStudents() : [];
            const existingStudentKeys = new Set();
            existingStudents.forEach(s => {
                if (s.id) existingStudentKeys.add(String(s.id).trim().toLowerCase());
                if (s.student_id) existingStudentKeys.add(String(s.student_id).trim().toLowerCase());
                if (s.email) existingStudentKeys.add(String(s.email).trim().toLowerCase());
            });
            Object.values(customUsersCheck).forEach(u => {
                if (u && u.role === 'student') {
                    if (u.id) existingStudentKeys.add(String(u.id).trim().toLowerCase());
                    if (u.student_id) existingStudentKeys.add(String(u.student_id).trim().toLowerCase());
                    if (u.email) existingStudentKeys.add(String(u.email).trim().toLowerCase());
                }
            });

            const existingAdvisorKeys = new Set();
            const defaultAdvisorsList = [
                { id: 'ADV001', name: 'อาจารย์ สมชาย แจ่มใส', email: 'somchai.j@ku.th' },
                { id: 'ADV002', name: 'อาจารย์ สมหญิง รักเรียน', email: 'somying.r@ku.th' },
                { id: 'ADV003', name: 'อาจารย์ สมจิต มั่งมี', email: 'somjit.m@ku.th' }
            ];
            defaultAdvisorsList.forEach(a => {
                existingAdvisorKeys.add(String(a.id).trim().toLowerCase());
                existingAdvisorKeys.add(String(a.email).trim().toLowerCase());
            });
            Object.values(customUsersCheck).forEach(u => {
                if (u && u.role === 'advisor') {
                    if (u.id) existingAdvisorKeys.add(String(u.id).trim().toLowerCase());
                    if (u.advisor_id) existingAdvisorKeys.add(String(u.advisor_id).trim().toLowerCase());
                    if (u.email) existingAdvisorKeys.add(String(u.email).trim().toLowerCase());
                }
            });

            const duplicates = [];
            const seenInBatch = new Set();

            for (let idx = 0; idx < jsonRows.length; idx++) {
                const row = jsonRows[idx];
                const emailRaw = findRowEmail(row, ['อีเมลมหาวิทยาลัย', 'อีเมล', 'อีเมล์', 'Email', 'email', 'E-mail', 'KU-Mail', 'KU Mail', 'เมล']);
                const email = emailRaw ? String(emailRaw).trim().toLowerCase() : '';

                if (isAdvisor) {
                    const advId = findRowValue(row, ['รหัสประจำตัว', 'รหัสอาจารย์', 'รหัส', 'ID', 'Advisor ID', 'advisor_id']);
                    const advName = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname']) || 'อาจารย์';

                    const keyId = advId ? String(advId).trim().toLowerCase() : '';
                    if (keyId && (existingAdvisorKeys.has(keyId) || seenInBatch.has(keyId))) {
                        duplicates.push(`รหัสอาจารย์ ${advId}: ${advName} (มีอยู่ในระบบแล้ว)`);
                    } else if (email && (existingAdvisorKeys.has(email) || seenInBatch.has(email))) {
                        duplicates.push(`อีเมล ${email}: ${advName} (มีอยู่ในระบบแล้ว)`);
                    }
                    if (keyId) seenInBatch.add(keyId);
                    if (email) seenInBatch.add(email);
                } else {
                    const studentId = findRowValue(row, ['รหัสนิสิต', 'รหัสประจำตัว', 'รหัสนักศึกษา', 'รหัส', 'ID', 'Student ID', 'StudentID', 'student_id']);
                    const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname']) || 'นิสิต';

                    const keyId = studentId ? String(studentId).trim().toLowerCase() : '';
                    if (keyId && (existingStudentKeys.has(keyId) || seenInBatch.has(keyId))) {
                        duplicates.push(`รหัสนิสิต ${studentId}: ${name} (มีอยู่ในระบบแล้ว)`);
                    } else if (email && (existingStudentKeys.has(email) || seenInBatch.has(email))) {
                        duplicates.push(`อีเมล ${email}: ${name} (มีอยู่ในระบบแล้ว)`);
                    }
                    if (keyId) seenInBatch.add(keyId);
                    if (email) seenInBatch.add(email);
                }
            }

            if (duplicates.length > 0) {
                const maxShow = 5;
                const dupListText = duplicates.slice(0, maxShow).map((d, i) => `${i + 1}. ${d}`).join('\n');
                const moreCount = duplicates.length > maxShow ? `\n...และรายการอื่นๆ อีก ${duplicates.length - maxShow} รายการ` : '';
                alert(`พบข้อมูลซ้ำกับที่มีอยู่ในระบบแล้ว ไม่สามารถเพิ่มได้!\n\nรายชื่อที่ซ้ำ (${duplicates.length} รายการ):\n${dupListText}${moreCount}\n\nระบบปฏิเสธการนำเข้า กรุณาแก้ไขไฟล์หรือเลือกไฟล์ใหม่`);
                clearAdminStudentFile();
                return;
            }

            if (isAdvisor) {
                let importedCount = 0;
                const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                const importedAdvisorsList = [];

                for (let idx = 0; idx < jsonRows.length; idx++) {
                    const row = jsonRows[idx];
                    const emailRaw = findRowEmail(row, ['อีเมลมหาวิทยาลัย', 'อีเมล', 'อีเมล์', 'อีเมล์มหาวิทยาลัย', 'Email', 'email', 'E-mail', 'KU-Mail', 'KU Mail', 'เมล', 'อีเมลอาจารย์']);
                    if (!emailRaw) continue;
                    const email = String(emailRaw).trim().toLowerCase();
                    if (!email) continue;

                    const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname', 'อาจารย์']);
                    const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']);
                    const fullName = (title ? `${title} ` : '') + (name || 'อาจารย์');

                    const advisorId = findRowValue(row, ['รหัสประจำตัว', 'รหัสอาจารย์', 'รหัส', 'ID', 'Advisor ID', 'advisor_id']) || email.split('@')[0];
                    const sectionVal = findRowValue(row, ['หมู่เรียนที่รับผิดชอบ', 'หมู่เรียน', 'หมู่', 'Section', 'sections']) || '700, 800';
                    const phoneVal = findRowValue(row, ['เบอร์โทรศัพท์', 'เบอร์โทร', 'โทร', 'Phone', 'Tel']) || '';
                    const pass = findRowValue(row, ['รหัสผ่านชั่วคราว', 'รหัสผ่าน', 'Password', 'password']) || advisorId;

                    const advObj = {
                        id: advisorId,
                        advisor_id: advisorId,
                        name: fullName,
                        email: email,
                        password: pass,
                        password_hash: pass,
                        role: 'advisor',
                        section: sectionVal,
                        phone: phoneVal,
                        status: 'approved',
                        first_login: true,
                        password_changed: false
                    };

                customUsers[email] = advObj;
                customUsers[advisorId.toLowerCase()] = advObj;
                importedCount++;
                importedAdvisorsList.push(advObj);
            }

            localStorage.setItem('customUsers', JSON.stringify(customUsers));

            // สลับไปยังแท็บอาจารย์ทันที
            if (typeof switchAdminUserTab === 'function') {
                switchAdminUserTab('advisor');
            } else if (typeof renderAdminUsersTable === 'function') {
                renderAdminUsersTable();
            }
            if (typeof updateAdvisorStats === 'function') {
                updateAdvisorStats();
            }

            renderAdminStudentPreImportPreview(true, importedAdvisorsList);

            alert(`นำเข้ารายชื่ออาจารย์นิเทศสำเร็จจำนวน ${importedCount} ท่านเรียบร้อยแล้ว!\n\nระบบได้สลับไปยังแท็บ "รายชื่ออาจารย์ (Advisors)" เพื่อแสดงผลข้อมูลทันที`);
            return;
        }

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
            const section = normalizeCleanSection(sectionVal, 'หมู่ 700');
            const company = findRowValue(row, ['ชื่อสถานประกอบการ', 'สถานประกอบการ', 'Company', 'company']);
            const advisorVal = findRowValue(row, ['อาจารย์ที่ปรึกษา', 'อาจารย์ที่ปึกษา', 'อาจารย์นิเทศ', 'อาจารย์', 'อาจารย์ผู้ดูแล', 'Advisor', 'advisor', 'ที่ปรึกษา', 'ที่ปึกษา']);
            const semester = formatCombinedSemester(
                findRowValue(row, ['ภาคการศึกษา', 'ภาคเรียน', 'ภาค', 'เทอม', 'Semester', 'semester', 'Term', 'term']),
                findRowValue(row, ['ปีการศึกษา', 'ปีการศึกษาที่', 'ปีศึกษา', 'AcademicYear', 'academic_year', 'academicYear', 'acad_year']),
                'ภาคต้น 2569'
            );
            const phoneVal = findRowValue(row, ['เบอร์โทรศัพท์', 'เบอร์โทร', 'เบอร์', 'โทร', 'Phone', 'Tel', 'tel']);

            // อ่านพิกัดแบบรวม (เช่น "14.076948, 100.601234" หรือตัวเลขพิกัด)
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
            const pass = passRaw || '123456';

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
                curriculum: curriculumVal || '',
                section: section,
                company_name: company,
                company: company,
                company_lat: lat || null,
                company_lng: lng || null,
                advisor_name: advisorVal ? (advisorVal.startsWith('อาจารย์') || advisorVal.startsWith('อ.') ? advisorVal : `อาจารย์ ${advisorVal}`.trim()) : '',
                advisor: advisorVal ? (advisorVal.startsWith('อาจารย์') || advisorVal.startsWith('อ.') ? advisorVal : `อาจารย์ ${advisorVal}`.trim()) : '',
                semester: semester,
                phone: phoneVal || '',
                status: 'approved',
                first_login: true,
                password_changed: false,
                otp_forward_email: 'wongsapat.u@ku.th'
            };

            customUsers[email] = userObj;
            if (studentId) customUsers[studentId] = userObj;
            if (email.includes('@')) customUsers[email.split('@')[0]] = userObj;
                // ปลดล็อกออกจาก deletedStudentIds เมื่อมีการนำเข้าใหม่
                try {
                    let dIds = JSON.parse(localStorage.getItem('deletedStudentIds') || '[]');
                    const sid = String(userObj.student_id || userObj.id || '').trim();
                    dIds = dIds.filter(x => x !== sid && x !== email.toLowerCase());
                    localStorage.setItem('deletedStudentIds', JSON.stringify(dIds));
                } catch(e) {}

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
                semester: semester,
                company: company || '-',
                advisor: advisorVal || '-',
                initialPassword: pass,
                status: 'approved'
            });
        }

        localStorage.setItem('customUsers', JSON.stringify(customUsers));

        // สลับไปยังแท็บนิสิตทันที
        if (typeof switchAdminUserTab === 'function') {
            switchAdminUserTab('student');
        }

        // แสดงข้อมูลนิสิตปี 2569 ทั้งหมด (ทั้ง 29 คนเดิม และ 3 คนใหม่ที่เพิ่มเข้าไป)
        if (typeof onAdminSemesterChange === 'function') {
            onAdminSemesterChange('all_2569');
        } else {
            renderAdminUsersTable();
            updateAdvisorStats();
        }

        // RENDER POST-IMPORT PREVIEW (เห็นทั้งก่อนและหลังเพิ่มไฟล์เข้าไป)
        renderAdminStudentPreImportPreview(true, importedStudentsList);

        // Open Post-Addition Preview Modal!
        showPostAddPreviewModal({
            title: 'นำเข้ารายชื่อนิสิต, อาจารย์เข้าสู่ระบบสำเร็จ',
            roleTitle: 'ผู้ดูแลระบบ (Admin)',
            source: 'admin_file',
            students: importedStudentsList,
            sectionsCountMap: sectionsCountMap,
            emailSent: false
        });

    } catch (err) {
        console.error("Student Excel import error:", err);
        alert('เกิดข้อผิดพลาดในการอ่านไฟล์ Excel รายชื่อนิสิต, อาจารย์ กรุณาตรวจสอบรูปแบบไฟล์แล้วลองใหม่อีกครั้ง');
    }
};
reader.readAsArrayBuffer(selectedStudentExcelFile);
}

function importAdvisorExcelFile() {
    if (!selectedAdvisorExcelFile) {
        alert('กรุณาคลิกเลือกไฟล์ Excel รายชื่ออาจารย์ (.xlsx) ก่อนกดนำเข้าข้อมูล');
        return;
    }

    const reader = new FileReader();
    reader.onload = async function (e) {
        try {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            const firstSheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[firstSheetName];
            const jsonRows = XLSX.utils.sheet_to_json(worksheet);

            if (!jsonRows || jsonRows.length === 0) {
                alert('ไม่พบข้อมูลรายชื่อในไฟล์ Excel ที่เลือก');
                return;
            }

            let importedCount = 0;
            const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');

            for (const row of jsonRows) {
                const emailRaw = findRowEmail(row, ['อีเมลมหาวิทยาลัย', 'อีเมล', 'อีเมล์', 'อีเมล์มหาวิทยาลัย', 'Email', 'email', 'E-mail', 'KU-Mail', 'KU Mail', 'เมล', 'อีเมลอาจารย์']);
                if (!emailRaw) continue;
                const email = String(emailRaw).trim().toLowerCase();
                if (!email) continue;

                const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname', 'อาจารย์']);
                const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']);
                const fullName = title ? `${title} ${name}`.trim() : (name || 'อาจารย์นิเทศ');
                const advisorId = findRowValue(row, ['รหัสประจำตัว', 'รหัสอาจารย์', 'รหัสบุคลากร', 'รหัส', 'ID', 'Advisor ID', 'advisor_id', 'Code']);
                const section = findRowValue(row, ['หมู่เรียนที่รับผิดชอบ', 'หมู่เรียน', 'หมู่', 'Section', 'section']);
                const passRaw = findRowValue(row, ['รหัสผ่านชั่วคราว', 'รหัสผ่าน', 'Password', 'pass', 'Passwordชั่วคราว']);
                const pass = passRaw || 'Asd1234';

                const userObj = {
                    id: advisorId || email.split('@')[0],
                    advisor_id: advisorId || email.split('@')[0],
                    name: fullName,
                    email: email,
                    password: pass,
                    password_hash: pass,
                    role: 'advisor',
                    section: section || 'หมู่ 700, หมู่ 800',
                    status: 'approved',
                    first_login: true,
                    password_changed: false,
                    otp_forward_email: 'wongsapat.u@ku.th'
                };

                customUsers[email] = userObj;
                // ปลดล็อกออกจาก deletedStudentIds เมื่อมีการนำเข้าใหม่
                try {
                    let dIds = JSON.parse(localStorage.getItem('deletedStudentIds') || '[]');
                    const sid = String(userObj.student_id || userObj.id || '').trim();
                    dIds = dIds.filter(x => x !== sid && x !== email.toLowerCase());
                    localStorage.setItem('deletedStudentIds', JSON.stringify(dIds));
                } catch(e) {}

                if (typeof supabaseClient !== 'undefined' && supabaseClient) {
                    try {
                        await supabaseClient.from('users').upsert([{
                            email: email,
                            password_hash: pass,
                            full_name: fullName,
                            role: 'advisor',
                            status: 'approved'
                        }], { onConflict: 'email' });

                        if (advisorId) {
                            const secArr = section.replace(/หมู่/g, '').split(/[,/]/).map(s => s.trim()).filter(Boolean);
                            await supabaseClient.from('advisors').upsert([{
                                advisor_id: advisorId,
                                email: email,
                                full_name: fullName,
                                section: section,
                                responsible_sections: secArr
                            }], { onConflict: 'advisor_id' });
                        }
                    } catch (err) {
                        console.warn("Supabase upsert notice:", err.message);
                    }
                }
                importedCount++;
            }

            localStorage.setItem('customUsers', JSON.stringify(customUsers));
            renderAdminUsersTable();
            updateAdvisorStats();
            alert(`นำเข้าข้อมูลอาจารย์นิเทศเข้าสู่ระบบเรียบร้อยแล้วจำนวน ${importedCount} ท่าน!\n\nบัญชีอาจารย์พร้อมเข้าสู่ระบบได้ทันที:\n• ชื่อผู้ใช้งาน: อีเมลมหาวิทยาลัย (@ku.th) หรือ รหัสประจำตัวอาจารย์\n• รหัสผ่านเริ่มต้น: ${jsonRows.some(r => findRowValue(r, ['รหัสผ่านชั่วคราว', 'รหัสผ่าน', 'Password'])) ? 'รหัสผ่านในไฟล์ Excel' : 'รหัสประจำตัวอาจารย์ หรือ "1234"'}`);
            const label = document.getElementById('excel-advisor-file-name-label');
            if (label) {
                label.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg> คลิกเพื่อเลือกไฟล์ Excel รายชื่ออาจารย์ (.xlsx)`;
            }
            selectedAdvisorExcelFile = null;

        } catch (err) {
            console.error("Advisor Excel import error:", err);
            alert('เกิดข้อผิดพลาดในการอ่านไฟล์ Excel รายชื่ออาจารย์ กรุณาตรวจสอบรูปแบบไฟล์แล้วลองใหม่อีกครั้ง');
        }
    };
    reader.readAsArrayBuffer(selectedAdvisorExcelFile);
}

function downloadStudentExcelTemplate() {
    const studentSample = [
        {
            "รหัสนิสิต": "6521655442",
            "คำนำหน้านาม": "นาย",
            "ชื่อ - นามสกุล": "วงศพัทธ์ อุเทน",
            "ชั้นปี": "4",
            "ภาควิชา": "วิทยาการคอมพิวเตอร์",
            "หลักสูตร": "",
            "หมู่เรียน": "800",
            "อาจารย์ที่ปรึกษา": "อ. สมชาย แจ่มใส",
            "ภาคการศึกษา": "ปลาย",
            "ปีการศึกษา": "69",
            "อีเมลมหาวิทยาลัย": "wongsapat.u@ku.th",
            "เบอร์โทรศัพท์": "0948783020",
            "ชื่อสถานประกอบการ": "สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.)",
            "พิกัด": "14.0769486193, 100.601234",
            "รหัสผ่านชั่วคราว": "123456"
        },
        {
            "รหัสนิสิต": "6512345678",
            "คำนำหน้านาม": "นาง",
            "ชื่อ - นามสกุล": "สมหญิง แจ่มใส",
            "ชั้นปี": "4",
            "ภาควิชา": "วิทยาการคอมพิวเตอร์",
            "หลักสูตร": "",
            "หมู่เรียน": "800",
            "อาจารย์ที่ปรึกษา": "อ. สมชาย แจ่มใส",
            "ภาคการศึกษา": "ปลาย",
            "ปีการศึกษา": "69",
            "อีเมลมหาวิทยาลัย": "somying.j@ku.th",
            "เบอร์โทรศัพท์": "0989199992",
            "ชื่อสถานประกอบการ": "กสิกร บิซิเนส เทคโนโลยี กรุ๊ป",
            "พิกัด": "13.9106379573, 100.569612",
            "รหัสผ่านชั่วคราว": "123456"
        },
        {
            "รหัสนิสิต": "6666666666",
            "คำนำหน้านาม": "นาย",
            "ชื่อ - นามสกุล": "จิตดี มีเงิน",
            "ชั้นปี": "4",
            "ภาควิชา": "วิทยาการคอมพิวเตอร์",
            "หลักสูตร": "",
            "หมู่เรียน": "800",
            "อาจารย์ที่ปรึกษา": "อ. สมชาย แจ่มใส",
            "ภาคการศึกษา": "ปลาย",
            "ปีการศึกษา": "69",
            "อีเมลมหาวิทยาลัย": "jitdee.m@ku.th",
            "เบอร์โทรศัพท์": "0911111111",
            "ชื่อสถานประกอบการ": "กรุงเทพ",
            "พิกัด": "15.4123465232, 100.456789",
            "รหัสผ่านชั่วคราว": "123456"
        }
    ];
    const wb = XLSX.utils.book_new();
    const wsStudent = XLSX.utils.json_to_sheet(studentSample);
    XLSX.utils.book_append_sheet(wb, wsStudent, "รายชื่อนิสิต");
    XLSX.writeFile(wb, "Student_Import_Template.xlsx");
}

function downloadAdvisorExcelTemplate() {
    const advisorSample = [
        {
            "รหัสประจำตัว": "Q1171",
            "คำนำหน้านาม": "อาจารย์",
            "ชื่อ - นามสกุล": "ปรวี วงศ์สวัสดิ์สุริยะ",
            "หมู่เรียนที่รับผิดชอบ": "700, 800",
            "อีเมลมหาวิทยาลัย": "poravee.w@ku.th",
            "เบอร์โทรศัพท์": "034-300481 ถึง 4 ต่อ 7320",
            "รหัสผ่านชั่วคราว": "564879"
        }
    ];
    const wb = XLSX.utils.book_new();
    const wsAdvisor = XLSX.utils.json_to_sheet(advisorSample);
    XLSX.utils.book_append_sheet(wb, wsAdvisor, "รายชื่ออาจารย์");
    XLSX.writeFile(wb, "Advisor_Import_Template.xlsx");
}

function clearImportedUsersByRole(roleTarget) {
    const roleTitle = roleTarget === 'student' ? 'นิสิตสหกิจศึกษา' : 'อาจารย์นิเทศ';
    if (confirm(`คุณต้องการลบ/รีเซ็ตรายชื่อ "${roleTitle}" ทั้งหมดออกจากระบบใช่หรือไม่?\n\n(บัญชีในประเภทอื่นๆ จะไม่ได้รับผลกระทบ)`)) {
        const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
        const updatedUsers = {};
        Object.keys(customUsers).forEach(email => {
            const u = customUsers[email];
            if (u.role !== roleTarget) {
                updatedUsers[email] = u;
            }
        });
        localStorage.setItem('customUsers', JSON.stringify(updatedUsers));
        alert(`ลบ/รีเซ็ตรายชื่อ "${roleTitle}" ทั้งหมดเรียบร้อยแล้ว!`);
        location.reload();
    }
}

function clearAllImportedSystemUsers() {
    if (confirm('คุณต้องการลบ/รีเซ็ตรายชื่อผู้ใช้งานทั้งหมด (นิสิตและอาจารย์) ที่เคยอัปโหลดค้างไว้ออกจากระบบใช่หรือไม่?\n\n(บัญชีแอดมินยังคงอยู่ปกติ และจะไม่มีนิสิต/อาจารย์คนใดเข้าใช้ได้จนกว่าจะอัปโหลดไฟล์ Excel ใหม่)')) {
        localStorage.removeItem('customUsers');
        alert('ล้างข้อมูลรายชื่อผู้ใช้งานในระบบเรียบร้อยแล้ว!\n\nปัจจุบันในระบบจะเหลือเฉพาะบัญชีผู้ดูแลระบบ (Admin) เท่านั้น');
        location.reload();
    }
}
