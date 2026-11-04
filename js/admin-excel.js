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
            reader.onload = function(e) {
                try {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: 'array' });
                    const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
                    const jsonRows = XLSX.utils.sheet_to_json(firstSheet);

                    if (!jsonRows || jsonRows.length === 0) {
                        alert('ไม่พบข้อมูลรายชื่อนิสิตในไฟล์ที่เลือก');
                        clearAdminStudentFile();
                        return;
                    }

                    adminParsedStudentRows = jsonRows;
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

            const input = document.getElementById('admin-student-excel-file-input');
            if (input) input.value = '';

            const label = document.getElementById('excel-student-file-name-label');
            if (label) {
                label.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg> คลิกเพื่อเลือกไฟล์ Excel รายชื่อนิสิต (.xlsx / .csv)`;
                const parentBox = label.closest('div');
                if (parentBox) {
                    parentBox.style.backgroundColor = '#ffffff';
                    parentBox.style.border = '1.5px dashed #86efac';
                }
            }

            const previewContainer = document.getElementById('admin-student-preview-container');
            if (previewContainer) previewContainer.style.display = 'none';

            const importBtn = document.getElementById('admin-student-import-btn');
            if (importBtn) {
                importBtn.disabled = true;
                importBtn.style.opacity = '0.6';
                importBtn.style.cursor = 'not-allowed';
                importBtn.textContent = 'นำเข้ารายชื่อนิสิตเข้าสู่ระบบ';
            }
        }

        function renderAdminStudentPreImportPreview(isPostImport = false, postImportList = null) {
            const previewContainer = document.getElementById('admin-student-preview-container');
            const countBadge = document.getElementById('admin-student-preview-count-badge');
            const statusTag = document.getElementById('admin-student-preview-status-tag');
            const titleText = document.getElementById('admin-student-preview-title-text');
            const secPills = document.getElementById('admin-student-preview-sec-pills');
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
                        `;
                        tbody.appendChild(tr);
                    });
                }

            } else {
                // ==============================================================
                // PRE-IMPORT STATE (ก่อนเพิ่มไฟล์ / รอการยืนยัน)
                // ==============================================================
                if (titleText) titleText.textContent = 'พรีวิวข้อมูลในไฟล์ Excel:';
                if (statusTag) {
                    statusTag.style.display = 'none';
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
                        `;
                        tbody.appendChild(tr);
                    });
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
                title = 'เพิ่ม / นำเข้ารายชื่อนิสิตสำเร็จเรียบร้อย',
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
                authStat.innerHTML = 'รหัสผ่านแรกเข้า:<br><strong style="color: #15803d; font-family: monospace;">รหัสนิสิต</strong>';
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
                    if (emailNoticeText) emailNoticeText.textContent = 'ระบบได้ส่งอีเมลแจ้งแรกเข้าใช้งาน (รหัสนิสิต) ไปยังอีเมลเคยูของนิสิตเรียบร้อยแล้ว';
                } else {
                    emailNotice.style.display = 'flex';
                    emailNotice.style.background = '#f8fafc';
                    emailNotice.style.borderColor = '#e2e8f0';
                    emailNotice.style.color = '#475569';
                    if (emailNoticeText) emailNoticeText.textContent = 'นิสิตสามารถเข้าสู่ระบบครั้งแรกได้ทันทีโดยใช้อีเมลเคยู / รหัสนิสิต และรหัสผ่านแรกเข้า (รหัสนิสิต)';
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
                alert('กรุณาคลิกเลือกไฟล์ Excel รายชื่อนิสิต (.xlsx / .csv) ก่อนกดนำเข้าข้อมูล');
                return;
            }

            const reader = new FileReader();
            reader.onload = async function(e) {
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
                            advisor: advisorVal || '-',
                            initialPassword: pass,
                            status: 'approved'
                        });
                    }

                    localStorage.setItem('customUsers', JSON.stringify(customUsers));
                    renderAdminUsersTable();
                    updateAdvisorStats();

                    // RENDER POST-IMPORT PREVIEW (เห็นทั้งก่อนและหลังเพิ่มไฟล์เข้าไป)
                    renderAdminStudentPreImportPreview(true, importedStudentsList);

                    // Open Post-Addition Preview Modal!
                    showPostAddPreviewModal({
                        title: 'นำเข้ารายชื่อนิสิตเข้าสู่ระบบสำเร็จ',
                        roleTitle: 'ผู้ดูแลระบบ (Admin)',
                        source: 'admin_file',
                        students: importedStudentsList,
                        sectionsCountMap: sectionsCountMap,
                        emailSent: false
                    });

                } catch (err) {
                    console.error("Student Excel import error:", err);
                    alert('เกิดข้อผิดพลาดในการอ่านไฟล์ Excel รายชื่อนิสิต กรุณาตรวจสอบรูปแบบไฟล์แล้วลองใหม่อีกครั้ง');
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
            reader.onload = async function(e) {
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
                            password_changed: false
                        };

                        customUsers[email] = userObj;

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
                                    await supabaseClient.from('advisors').upsert([{
                                        advisor_id: advisorId,
                                        email: email,
                                        full_name: fullName,
                                        section: section
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
                    "หลักสูตร": "ภาคพิเศษ",
                    "หมู่เรียน": "800",
                    "อาจารย์ที่ปรึกษา": "อ. สมชาย แจ่มใส",
                    "ภาคการศึกษา": "69",
                    "อีเมลมหาวิทยาลัย": "wongsapat.u@ku.th",
                    "เบอร์โทรศัพท์": "0948783020",
                    "ชื่อสถานประกอบการ": "สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช)",
                    "พิกัด": "14.0769486193, 100.601234",
                    "รหัสผ่านชั่วคราว": "123456"
                },
                {
                    "รหัสนิสิต": "6512345678",
                    "คำนำหน้านาม": "นาง",
                    "ชื่อ - นามสกุล": "สมหญิง แจ่มใส",
                    "ชั้นปี": "4",
                    "ภาควิชา": "วิทยาการคอมพิวเตอร์",
                    "หลักสูตร": "ภาคพิเศษ",
                    "หมู่เรียน": "800",
                    "อาจารย์ที่ปรึกษา": "อ. สมชาย แจ่มใส",
                    "ภาคการศึกษา": "69",
                    "อีเมลมหาวิทยาลัย": "somying.j@ku.th",
                    "เบอร์โทรศัพท์": "089199992",
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
                    "หลักสูตร": "ภาคปกติ",
                    "หมู่เรียน": "800",
                    "อาจารย์ที่ปรึกษา": "อ. สมชาย แจ่มใส",
                    "ภาคการศึกษา": "69",
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
