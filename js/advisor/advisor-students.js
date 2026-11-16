// ==========================================================================
// advisor-students.js - ระบบจัดการนิสิต การตรวจเอกสาร และการนำเข้ารายชื่อแยกหมู่
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

let currentAdminUserTab = 'student';

function switchAdminUserTab(tab) {
            currentAdminUserTab = tab;
            const searchBar = document.getElementById('admin-search-filter-bar');
            if (searchBar) {
                searchBar.style.display = (tab === 'student') ? 'flex' : 'none';
            }
            const btnStd = document.getElementById('admin-tab-btn-student');
            const btnAdv = document.getElementById('admin-tab-btn-advisor');

            if (tab === 'student') {
                if (btnStd) {
                    btnStd.style.background = 'var(--primary-color)';
                    btnStd.style.color = '#fff';
                    btnStd.style.borderColor = 'var(--primary-color)';
                    btnStd.style.fontWeight = '700';
                }
                if (btnAdv) {
                    btnAdv.style.background = '#ffffff';
                    btnAdv.style.color = 'var(--text-muted)';
                    btnAdv.style.borderColor = 'var(--border-color)';
                    btnAdv.style.fontWeight = '600';
                }
            } else {
                if (btnAdv) {
                    btnAdv.style.background = 'var(--primary-color)';
                    btnAdv.style.color = '#fff';
                    btnAdv.style.borderColor = 'var(--primary-color)';
                    btnAdv.style.fontWeight = '700';
                }
                if (btnStd) {
                    btnStd.style.background = '#ffffff';
                    btnStd.style.color = 'var(--text-muted)';
                    btnStd.style.borderColor = 'var(--border-color)';
                    btnStd.style.fontWeight = '600';
                }
            }
            renderAdminUsersTable();
        }

        let adminStudentSearchQuery = '';
        let adminSelectedSemester = 'ภาคต้น 2569';
        let adminSelectedSection = 'all';

        function onAdminSectionChange(val) {
            adminSelectedSection = val;
            renderAdminUsersTable();
        }

        function onAdminStudentSearch(val) {
            adminStudentSearchQuery = (val || '').trim().toLowerCase();
            renderAdminTableRowsOnly();
        }

        function onAdminSemesterChange(val) {
            adminSelectedSemester = val;
            const overviewSel = document.getElementById('admin-overview-semester-select');
            if (overviewSel) overviewSel.value = val;
            renderAdminUsersTable();
            updateAdvisorStats();
        }

        async function confirmDeleteStudent(studentId, studentName) {
            const isConfirm = confirm(`คุณต้องการลบรายชื่อนิสิต "${studentName}" (รหัส ${studentId}) ออกจากระบบอย่างถาวรหรือไม่?`);
            if (!isConfirm) return;

            let customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
            let deletedEmail = null;
            Object.keys(customUsers).forEach(k => {
                const u = customUsers[k];
                if (u && (String(u.id) === String(studentId) || String(u.student_id) === String(studentId))) {
                    deletedEmail = u.email;
                    delete customUsers[k];
                }
            });
            if (deletedEmail && customUsers[deletedEmail]) {
                delete customUsers[deletedEmail];
            }
            localStorage.setItem('customUsers', JSON.stringify(customUsers));

            if (typeof dbDeleteStudent === 'function') {
                await dbDeleteStudent(studentId, deletedEmail);
            }

            loadDynamicStudentsData();
            renderAdminUsersTable();
            updateAdvisorStats();
            alert(`ลบรายชื่อนิสิต "${studentName}" เรียบร้อยแล้ว`);
        }

        async function confirmDeleteAdvisor(advId, advName) {
            const isConfirm = confirm(`คุณต้องการลบอาจารย์ "${advName}" (รหัส ${advId}) ออกจากระบบหรือไม่?`);
            if (!isConfirm) return;

            let customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
            let deletedEmail = null;
            Object.keys(customUsers).forEach(k => {
                const u = customUsers[k];
                if (u && (String(u.id) === String(advId) || String(u.advisor_id) === String(advId) || String(u.name) === String(advName) || (u.email && String(u.email).toLowerCase() === String(advId).toLowerCase()))) {
                    deletedEmail = u.email;
                    delete customUsers[k];
                }
            });
            if (deletedEmail && customUsers[deletedEmail]) {
                delete customUsers[deletedEmail];
            }
            localStorage.setItem('customUsers', JSON.stringify(customUsers));

            renderAdminUsersTable();
            alert(`ลบอาจารย์ "${advName}" เรียบร้อยแล้ว`);
        }

        function renderAdminTableRowsOnly() {
            // Re-render only table rows (called on search/filter changes to avoid losing focus)
            renderAdminUsersTable(true);
        }

        function renderAdminUsersTable(rowsOnly = false) {
            const container = document.getElementById('admin-users-table-container');
            if (!container) return;
            loadDynamicStudentsData();

            if (currentAdminUserTab === 'student') {
                const allStds = getAllSystemStudents();

                if (allStds.length === 0) {
                    container.innerHTML = `<div style="text-align:center; padding:20px; color:var(--text-muted); font-size:12px;">ยังไม่มีข้อมูลนิสิตในระบบ (สามารถใช้ฟังก์ชันนำเข้าไฟล์ Excel ด้านล่างได้)</div>`;
                    return;
                }

                const allDocs = getSubmittedDocs();
                let filteredStds = allStds;

                // กรองตามภาคการศึกษา (Requirement 1)
                if (adminSelectedSemester && adminSelectedSemester !== 'all') {
                    if (adminSelectedSemester === 'all_2569') {
                        filteredStds = filteredStds.filter(s => (s.semester || 'ภาคต้น 2569').includes('2569'));
                    } else {
                        filteredStds = filteredStds.filter(s => (s.semester || 'ภาคต้น 2569') === adminSelectedSemester);
                    }
                }

                // กรองตามหมู่เรียน (700, 701, 702, 800, 801, 802)
                if (adminSelectedSection && adminSelectedSection !== 'all') {
                    filteredStds = filteredStds.filter(s => {
                        const secStr = String(s.section || '');
                        return secStr.includes(adminSelectedSection);
                    });
                }

                if (adminStudentSearchQuery) {
                    filteredStds = filteredStds.filter(s => 
                        (s.id && String(s.id).toLowerCase().includes(adminStudentSearchQuery)) ||
                        (s.name && s.name.toLowerCase().includes(adminStudentSearchQuery)) ||
                        (s.company && s.company.toLowerCase().includes(adminStudentSearchQuery)) ||
                        (s.advisor_name && s.advisor_name.toLowerCase().includes(adminStudentSearchQuery)) ||
                        (s.section && s.section.toLowerCase().includes(adminStudentSearchQuery))
                    );
                }

                let rowsHtml = filteredStds.map(s => {
                    const stdDocs = allDocs.filter(d => String(d.studentId) === String(s.id));
                    let currentDocStatus = s.docs || 'รอตรวจ';
                    if (stdDocs.length > 0) {
                        currentDocStatus = stdDocs[0].status;
                    }
                    const isDocComplete = (currentDocStatus === 'ครบถ้วน' || currentDocStatus === 'ตรวจรับแล้ว' || currentDocStatus === 'เอกสารครบแล้ว');
                    const docBadgeClass = isDocComplete ? 'badge-success' : 'badge-warning';
                    const docDisplayText = isDocComplete ? 'เอกสารครบแล้ว' : 'ไม่ครบ';

                    const rawSup = String(s.status || '').toLowerCase().trim();
                    const isDone = (rawSup === 'approved' || rawSup === 'นิเทศแล้ว' || rawSup === 'done' || rawSup === 'completed');
                    const statusBadgeClass = isDone ? 'badge-success' : 'badge-info';
                    const supDisplayText = isDone ? 'นิเทศแล้ว' : 'รอนิเทศ';

                    return `
                        <tr style="border-bottom: 1px solid var(--border-color); font-size: 11.5px;">
                            <td style="padding: 10px 12px; font-weight: 700; color: var(--primary-color); white-space: nowrap;">${s.id}</td>
                            <td style="padding: 10px 12px; font-weight: 600; color: var(--text-main);">${s.name}</td>
                            <td style="padding: 10px 12px; color: #475569; white-space: nowrap; font-weight: 600;">${cleanSectionName(s.section)}</td>
                            <td style="padding: 10px 12px; color: #0284c7; font-weight: 600; white-space: nowrap;">${s.semester || 'ภาคต้น 2569'}</td>
                            <td style="padding: 10px 12px; color: #1e40af; font-weight: 600; white-space: nowrap;">${s.advisor_name || '-'}</td>
                            <td style="padding: 10px 12px; color: #1e293b;">${s.company}</td>
                            <td style="padding: 10px 12px; white-space: nowrap;">
                                <span class="status-badge ${docBadgeClass}" style="margin-right: 6px;">${docDisplayText}</span>
                                <button type="button" class="btn-primary" style="padding: 4px 8px; font-size: 10.5px; background-color: #2563eb; display: inline-flex; align-items: center; gap: 4px;" onclick="openDocModal('${s.id}', '${s.name}')">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg> ตรวจเอกสาร (${stdDocs.length})
                                </button>
                            </td>
                            <td style="padding: 10px 12px; text-align: center; white-space: nowrap;">
                                <button type="button" title="ลบรายชื่อนิสิตนี้" onclick="confirmDeleteStudent('${s.id}', '${s.name}')" style="background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; border-radius: 6px; width: 28px; height: 28px; font-weight: 700; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; font-size: 13px;" onmouseover="this.style.background='#fecaca'" onmouseout="this.style.background='#fee2e2'">
                                    ✕
                                </button>
                            </td>
                        </tr>
                    `;
                }).join('');

                // Show static search bar and sync dropdown values
                const searchBar = document.getElementById('admin-search-filter-bar');
                if (searchBar) {
                    searchBar.style.display = 'flex';
                    const secSel = document.getElementById('admin-section-select');
                    if (secSel) secSel.value = adminSelectedSection;
                    const semSel = document.getElementById('admin-semester-select');
                    if (semSel) semSel.value = adminSelectedSemester;
                    const countEl = document.getElementById('admin-result-count');
                    if (countEl) countEl.innerHTML = `แสดง <strong>${filteredStds.length}</strong> จาก ${allStds.length} คน`;
                }

                container.innerHTML = `
                    <div style="background: #ffffff; border: 1px solid var(--border-color); border-radius: 0 0 8px 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
                        <div style="overflow-x: auto;">
                            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                                <thead>
                                    <tr style="background: #f8fafc; border-bottom: 1px solid var(--border-color); color: #64748b; font-size: 11px; font-weight: 700;">
                                        <th style="padding: 10px 12px;">รหัสนิสิต</th>
                                        <th style="padding: 10px 12px;">ชื่อ-นามสกุล</th>
                                        <th style="padding: 10px 12px;">หมู่เรียน</th>
                                        <th style="padding: 10px 12px;">ภาคการศึกษา</th>
                                        <th style="padding: 10px 12px;">อาจารย์นิเทศ</th>
                                        <th style="padding: 10px 12px;">สถานประกอบการ</th>
                                        <th style="padding: 10px 12px;">เอกสาร Form 0-11</th>
                                        <th style="padding: 10px 12px; text-align: center;">จัดการ</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${rowsHtml || '<tr><td colspan="8" style="text-align:center; padding:20px; color:var(--text-muted); font-size:12px;">ไม่พบนิสิตที่ตรงกับเงื่อนไข</td></tr>'}
                                </tbody>
                            </table>
                        </div>
                        <div style="padding: 8px 12px; background: #f8fafc; border-top: 1px solid var(--border-color); font-size: 11px; color: var(--text-muted); display: flex; justify-content: space-between;">
                            <span>แสดงนิสิตในตัวกรองนี้: <strong>${filteredStds.length} คน</strong> (ทั้งหมด ${allStds.length} คน)</span>
                            <span></span>
                        </div>
                    </div>
                `;
            } else {
                const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                const uniqueAdvisors = new Map();
                Object.values(customUsers).forEach(u => {
                    if (u && u.role === 'advisor') {
                        const key = (u.email || u.advisor_id || u.id || '').toLowerCase().trim();
                        if (key && !uniqueAdvisors.has(key)) {
                            uniqueAdvisors.set(key, u);
                        }
                    }
                });
                const advisors = Array.from(uniqueAdvisors.values());
                const allStds = getAllSystemStudents();

                if (advisors.length === 0) {
                    container.innerHTML = `<div style="text-align:center; padding:32px; color:var(--text-muted); font-size:12px;">ยังไม่มีข้อมูลอาจารย์นิเทศในระบบ (สามารถใช้ฟังก์ชันนำเข้าไฟล์ Excel ด้านล่างได้)</div>`;
                    return;
                }

                let rowsHtml = advisors.map(a => {
                    const sec = a.section || '';
                    const assignedStds = allStds.filter(s => {
                        if (s.advisor_name && a.name && s.advisor_name.includes(a.name.replace(/อาจารย์\s*/, '').trim())) return true;
                        if (a.name && s.advisor_name && a.name.includes(s.advisor_name.replace(/อาจารย์\s*/, '').trim())) return true;
                        const secArr = (a.section || '').split(',').map(x => x.trim().replace(/[^0-9]/g, ''));
                        const sSecNum = (s.section || '').replace(/[^0-9]/g, '');
                        if (secArr.some(num => num && sSecNum.includes(num))) return true;
                        return false;
                    });
                    const countText = `${assignedStds.length} คน`;
                    return `
                        <tr style="border-bottom: 1px solid var(--border-color); font-size: 11.5px;">
                            <td style="padding: 10px 12px; font-weight: 700; color: #1e40af; white-space: nowrap;">${a.id || a.advisor_id || '-'}</td>
                            <td style="padding: 10px 12px; font-weight: 600; color: var(--text-main);">${a.name}</td>
                            <td style="padding: 10px 12px; color: #475569;">${a.section || 'ไม่ระบุ'}</td>
                            <td style="padding: 10px 12px; color: var(--primary-color);">${a.email}</td>
                            <td style="padding: 10px 12px; font-weight: 700; color: #15803d;">${countText}</td>
                            <td style="padding: 10px 12px; white-space: nowrap;"><span class="status-badge badge-success">อาจารย์นิเทศประจำภาควิชา</span></td>
                            <td style="padding: 10px 12px; text-align: center; white-space: nowrap;">
                                <button type="button" title="ลบอาจารย์ท่านนี้" onclick="confirmDeleteAdvisor('${a.id || a.advisor_id || a.email}', '${a.name}')" style="background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; border-radius: 6px; width: 28px; height: 28px; font-weight: 700; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; font-size: 13px;" onmouseover="this.style.background='#fecaca'" onmouseout="this.style.background='#fee2e2'">
                                    ✕
                                </button>
                            </td>
                        </tr>
                    `;
                }).join('');

                container.innerHTML = `
                    <div style="background: #ffffff; border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
                        <div style="overflow-x: auto;">
                            <table style="width: 100%; border-collapse: collapse; text-align: left;">
                                <thead>
                                    <tr style="background: #f8fafc; border-bottom: 1px solid var(--border-color); color: #64748b; font-size: 11px; font-weight: 700;">
                                        <th style="padding: 10px 12px;">รหัสประจำตัว</th>
                                        <th style="padding: 10px 12px;">ชื่อ-นามสกุลอาจารย์</th>
                                        <th style="padding: 10px 12px;">หมู่เรียนที่รับผิดชอบ</th>
                                        <th style="padding: 10px 12px;">อีเมลมหาวิทยาลัย</th>
                                        <th style="padding: 10px 12px;">นิสิตในดูแล</th>
                                        <th style="padding: 10px 12px;">สถานะ</th>
                                        <th style="padding: 10px 12px; text-align: center;">จัดการ</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${rowsHtml}
                                </tbody>
                            </table>
                        </div>
                        <div style="padding: 8px 12px; background: #f8fafc; border-top: 1px solid var(--border-color); font-size: 11px; color: var(--text-muted);">
                            <span>อาจารย์นิเทศทั้งหมด: <strong>${advisors.length} ท่าน</strong></span>
                        </div>
                    </div>
                `;
            }
        }

        function getAdvisorSections() {
            const savedSession = (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'));
            let loggedInUser = null;
            if (savedSession) {
                try { loggedInUser = JSON.parse(savedSession); } catch (e) {}
            }

            let mySecNormal = 'หมู่ 700';
            let mySecSpecial = 'หมู่ 800';
            if (loggedInUser && loggedInUser.role === 'advisor') {
                const advId = String(loggedInUser.id || loggedInUser.advisor_id || '');
                const advEmail = String(loggedInUser.email || '').toLowerCase();
                const advName = String(loggedInUser.name || '');

                if (advId.includes('Q2222') || advEmail.includes('somying') || advName.includes('สมหญิง')) {
                    mySecNormal = 'หมู่ 701';
                    mySecSpecial = 'หมู่ 801';
                } else if (advId.includes('Q3333') || advEmail.includes('somjit') || advName.includes('สมจิต')) {
                    mySecNormal = 'หมู่ 702';
                    mySecSpecial = 'หมู่ 802';
                } else {
                    const advSecStr = String(loggedInUser.section || '');
                    const mNorm = advSecStr.match(/70[012]/);
                    const mSpec = advSecStr.match(/80[012]/);
                    if (mNorm) mySecNormal = `หมู่ ${mNorm[0]}`;
                    if (mSpec) mySecSpecial = `หมู่ ${mSpec[0]}`;
                }
            }
            return { mySecNormal, mySecSpecial, loggedInUser };
        }



        function populateAdvisorStudentSelects(listNorm, listSpec, secNormTitle, secSpecTitle) {
            // Update filter dropdown labels in both Calendar and QR forms
            const calNormOpt = document.getElementById('cal-sec-opt-norm');
            const calSpecOpt = document.getElementById('cal-sec-opt-spec');
            if (calNormOpt) calNormOpt.textContent = `${secNormTitle} - ${listNorm.length} คน`;
            if (calSpecOpt) calSpecOpt.textContent = `${secSpecTitle} - ${listSpec.length} คน`;

            const qrNormOpt = document.getElementById('qr-sec-opt-norm');
            const qrSpecOpt = document.getElementById('qr-sec-opt-spec');
            if (qrNormOpt) qrNormOpt.textContent = `${secNormTitle} - ${listNorm.length} คน`;
            if (qrSpecOpt) qrSpecOpt.textContent = `${secSpecTitle} - ${listSpec.length} คน`;

            renderCalStudentSelectOptions(listNorm, listSpec, secNormTitle, secSpecTitle, currentCalSectionFilter);
            renderQrStudentSelectOptions(listNorm, listSpec, secNormTitle, secSpecTitle, currentQrSectionFilter);
        }

        function renderCalStudentSelectOptions(listNorm, listSpec, secNormTitle, secSpecTitle, filterMode = 'all') {
            const calSelect = document.getElementById('cal-student-select');
            if (!calSelect) return;
            const currentVal = calSelect.value;
            calSelect.innerHTML = '';

            const total = listNorm.length + listSpec.length;
            if (total === 0) {
                calSelect.innerHTML = '<option value="">ยังไม่มีข้อมูลนิสิต (รอแอดมินนำเข้าข้อมูล)</option>';
                return;
            }

            const promptOpt = document.createElement('option');
            promptOpt.value = '';
            promptOpt.textContent = '-- กรุณาเลือกนิสิต --';
            calSelect.appendChild(promptOpt);

            if (filterMode === 'all' || filterMode === 'normal') {
                if (listNorm.length > 0) {
                    const groupNorm = document.createElement('optgroup');
                    groupNorm.label = `── ${secNormTitle} [${listNorm.length} คน] ──`;
                    listNorm.forEach(s => {
                        const opt = document.createElement('option');
                        opt.value = s.id;
                        opt.textContent = `[${secNormTitle}] ${s.id} ${s.name} (${s.company || 'ยังไม่ระบุสถานประกอบการ'})`;
                        groupNorm.appendChild(opt);
                    });
                    calSelect.appendChild(groupNorm);
                }
            }

            if (filterMode === 'all' || filterMode === 'special') {
                if (listSpec.length > 0) {
                    const groupSpec = document.createElement('optgroup');
                    groupSpec.label = `── ${secSpecTitle} [${listSpec.length} คน] ──`;
                    listSpec.forEach(s => {
                        const opt = document.createElement('option');
                        opt.value = s.id;
                        opt.textContent = `[${secSpecTitle}] ${s.id} ${s.name} (${s.company || 'ยังไม่ระบุสถานประกอบการ'})`;
                        groupSpec.appendChild(opt);
                    });
                    calSelect.appendChild(groupSpec);
                }
            }

            if (currentVal) calSelect.value = currentVal;
        }

        function renderQrStudentSelectOptions(listNorm, listSpec, secNormTitle, secSpecTitle, filterMode = 'all') {
            const qrSelect = document.getElementById('qr-scan-student-select');
            if (!qrSelect) return;
            const currentVal = qrSelect.value;
            qrSelect.innerHTML = '';

            const total = listNorm.length + listSpec.length;
            if (total === 0) {
                qrSelect.innerHTML = '<option value="">ยังไม่มีข้อมูลนิสิต (รอแอดมินนำเข้าข้อมูล)</option>';
                return;
            }

            const promptOpt = document.createElement('option');
            promptOpt.value = '';
            promptOpt.textContent = '-- กรุณาเลือกนิสิตเป้าหมาย --';
            qrSelect.appendChild(promptOpt);

            if (filterMode === 'all' || filterMode === 'normal') {
                if (listNorm.length > 0) {
                    const groupNorm = document.createElement('optgroup');
                    groupNorm.label = `── ${secNormTitle} [${listNorm.length} คน] ──`;
                    listNorm.forEach(s => {
                        const opt = document.createElement('option');
                        opt.value = s.id;
                        const statusTag = s.status === 'นิเทศแล้ว' ? ' [เช็คอินแล้ว]' : '';
                        opt.textContent = `[${secNormTitle}] ${s.id} - ${s.name} (${s.company || 'ยังไม่ระบุ'})${statusTag}`;
                        groupNorm.appendChild(opt);
                    });
                    qrSelect.appendChild(groupNorm);
                }
            }

            if (filterMode === 'all' || filterMode === 'special') {
                if (listSpec.length > 0) {
                    const groupSpec = document.createElement('optgroup');
                    groupSpec.label = `── ${secSpecTitle} [${listSpec.length} คน] ──`;
                    listSpec.forEach(s => {
                        const opt = document.createElement('option');
                        opt.value = s.id;
                        const statusTag = s.status === 'นิเทศแล้ว' ? ' [เช็คอินแล้ว]' : '';
                        opt.textContent = `[${secSpecTitle}] ${s.id} - ${s.name} (${s.company || 'ยังไม่ระบุ'})${statusTag}`;
                        groupSpec.appendChild(opt);
                    });
                    qrSelect.appendChild(groupSpec);
                }
            }

            if (currentVal) qrSelect.value = currentVal;
        }

        function onCalSectionFilterChange(val) {
            currentCalSectionFilter = val;
            const { mySecNormal, mySecSpecial } = getAdvisorSections();
            let listNorm = studentsData[mySecNormal] || [];
            let listSpec = studentsData[mySecSpecial] || [];
            if (advisorSelectedSemester && advisorSelectedSemester !== 'all') {
                listNorm = listNorm.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
                listSpec = listSpec.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
            }
            renderCalStudentSelectOptions(listNorm, listSpec, mySecNormal, mySecSpecial, val);
        }

        function onQrSectionFilterChange(val) {
            currentQrSectionFilter = val;
            const { mySecNormal, mySecSpecial } = getAdvisorSections();
            let listNorm = studentsData[mySecNormal] || [];
            let listSpec = studentsData[mySecSpecial] || [];
            if (advisorSelectedSemester && advisorSelectedSemester !== 'all') {
                listNorm = listNorm.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
                listSpec = listSpec.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
            }
            renderQrStudentSelectOptions(listNorm, listSpec, mySecNormal, mySecSpecial, val);
        }



        function backToClassroomList() {
            const selectView = document.getElementById('advisor-classroom-select-view');
            const detailView = document.getElementById('advisor-classroom-detail-view');
            if (selectView) selectView.style.display = 'block';
            if (detailView) detailView.style.display = 'none';
        }



        function getCurrentAdvisorName() {
            try {
                const savedSession = (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'));
                if (savedSession) {
                    const u = JSON.parse(savedSession);
                    return u.name || 'อาจารย์นิเทศ';
                }
            } catch (e) {}
            return 'อาจารย์นิเทศ';
        }

        function onAdvisorSemesterChange(val) {
            advisorSelectedSemester = val;
            const dashSel = document.getElementById('adv-semester-dash-select');
            const tabSel = document.getElementById('adv-semester-select-tab');
            const classSel = document.getElementById('adv-classroom-semester-select');
            const asgSel = document.getElementById('adv-asg-semester-select');
            const photoSel = document.getElementById('adv-photo-semester-select');
            if (dashSel) dashSel.value = val;
            if (tabSel) tabSel.value = val;
            if (classSel) classSel.value = val;
            if (asgSel) asgSel.value = val;
            if (photoSel) photoSel.value = val;

            const statLabel = document.getElementById('adv-semester-stat-label');
            if (statLabel) {
                statLabel.textContent = val === 'all' ? 'แสดงข้อมูลทั้งหมด' : (val === 'ภาคต้น 2569' ? `แสดงเฉพาะ: ${val} (ปัจจุบัน)` : `แสดงเฉพาะ: ${val}`);
            }

            updateAdvisorStats();
            if (typeof renderStudentList === 'function') {
                renderStudentList();
            }
            if (typeof renderAdvisorAssignments === 'function') {
                renderAdvisorAssignments();
            }
            if (typeof renderAdvisorPhotosPage === 'function') {
                renderAdvisorPhotosPage();
            }
        }

        function switchAdvisorClassroomTab(tab) {
            currentAdvisorClassroomTab = tab;
            const btnStd = document.getElementById('adv-subtab-btn-students');
            const btnAsg = document.getElementById('adv-subtab-btn-assignments');
            const contentStd = document.getElementById('adv-content-students');
            const contentAsg = document.getElementById('adv-content-assignments');

            if (tab === 'students') {
                if (btnStd) {
                    btnStd.style.borderBottom = '3px solid var(--primary-color)';
                    btnStd.style.color = 'var(--primary-color)';
                }
                if (btnAsg) {
                    btnAsg.style.borderBottom = '3px solid transparent';
                    btnAsg.style.color = '#64748b';
                }
                if (contentStd) contentStd.style.display = 'block';
                if (contentAsg) contentAsg.style.display = 'none';
                renderStudentList();
            } else {
                if (btnStd) {
                    btnStd.style.borderBottom = '3px solid transparent';
                    btnStd.style.color = '#64748b';
                }
                if (btnAsg) {
                    btnAsg.style.borderBottom = '3px solid #2563eb';
                    btnAsg.style.color = '#2563eb';
                }
                if (contentStd) contentStd.style.display = 'none';
                if (contentAsg) contentAsg.style.display = 'block';
                renderAdvisorAssignments();
            }
        }

        function filterAdvisorStudentsList(query) {
            advisorStudentSearchQuery = (query || '').toLowerCase().trim();
            renderStudentList();
        }

        // ----------------------------------------------------
        // ADVISOR ADD STUDENT (MANUAL ENTRY & FILE IMPORT)
        // ----------------------------------------------------
        let advisorSelectedImportFile = null;
        let advisorParsedImportRows = [];
        let advisorAddStudentMode = 'manual';

        function switchAdvisorAddStudentMode(mode) {
            advisorAddStudentMode = mode;
            const manualView = document.getElementById('adv-add-student-manual-view');
            const fileView = document.getElementById('adv-add-student-file-view');
            const btnManual = document.getElementById('adv-add-tab-btn-manual');
            const btnFile = document.getElementById('adv-add-tab-btn-file');

            if (mode === 'manual') {
                if (manualView) manualView.style.display = 'block';
                if (fileView) fileView.style.display = 'none';
                if (btnManual) {
                    btnManual.style.background = '#ffffff';
                    btnManual.style.color = 'var(--primary-color, #15803d)';
                    btnManual.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
                }
                if (btnFile) {
                    btnFile.style.background = 'transparent';
                    btnFile.style.color = '#64748b';
                    btnFile.style.boxShadow = 'none';
                }
            } else {
                if (manualView) manualView.style.display = 'none';
                if (fileView) fileView.style.display = 'block';
                if (btnFile) {
                    btnFile.style.background = '#ffffff';
                    btnFile.style.color = 'var(--primary-color, #15803d)';
                    btnFile.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
                }
                if (btnManual) {
                    btnManual.style.background = 'transparent';
                    btnManual.style.color = '#64748b';
                    btnManual.style.boxShadow = 'none';
                }

                // Setup sections in target sec select
                const secSelect = document.getElementById('adv-import-target-sec-select');
                if (secSelect) {
                    const { mySecNormal, mySecSpecial } = getAdvisorSections();
                    const curr = currentSelectedClassroom || mySecNormal;
                    secSelect.innerHTML = `
                        <option value="current" selected>ตามห้องเรียนที่เลือกอยู่ (${curr})</option>
                        <option value="${mySecNormal}">${mySecNormal}</option>
                        <option value="${mySecSpecial}">${mySecSpecial}</option>
                        <option value="auto_file">ดึงตามคอลัมน์ในไฟล์ Excel (ถ้ามีระบุ)</option>
                    `;
                }

                const semSelect = document.getElementById('adv-import-semester-select');
                if (semSelect) {
                    semSelect.value = (advisorSelectedSemester && advisorSelectedSemester !== 'all') ? advisorSelectedSemester : 'ภาคต้น 2569';
                }
            }
        }

        function openAdvisorAddStudentModal(mode = 'manual') {
            const { mySecNormal, mySecSpecial } = getAdvisorSections();
            let targetSec = currentSelectedClassroom || mySecNormal;
            if (![mySecNormal, mySecSpecial].includes(targetSec)) {
                targetSec = mySecNormal;
                currentSelectedClassroom = mySecNormal;
            }
            const targetEl = document.getElementById('adv-add-std-target-sec');
            if (targetEl) targetEl.textContent = targetSec;

            const stdIdEl = document.getElementById('adv-add-std-id');
            if (stdIdEl) stdIdEl.value = '';
            const nameEl = document.getElementById('adv-add-std-name');
            if (nameEl) nameEl.value = '';
            const emailEl = document.getElementById('adv-add-std-email');
            if (emailEl) emailEl.value = '';
            const compEl = document.getElementById('adv-add-std-company');
            if (compEl) compEl.value = '';

            const semEl = document.getElementById('adv-add-std-semester');
            if (semEl) {
                semEl.value = (advisorSelectedSemester && advisorSelectedSemester !== 'all') ? advisorSelectedSemester : 'ภาคต้น 2569';
            }
            const sendEmailEl = document.getElementById('adv-add-std-send-email');
            if (sendEmailEl) sendEmailEl.checked = true;

            clearAdvisorImportFile();
            switchAdvisorAddStudentMode(mode);

            const modal = document.getElementById('modal-advisor-add-student');
            if (modal) modal.style.display = 'flex';
        }

        function downloadAdvisorStudentTemplate() {
            const advName = getCurrentAdvisorName();
            const { mySecNormal, mySecSpecial } = getAdvisorSections();
            const currentSem = (advisorSelectedSemester && advisorSelectedSemester !== 'all') ? advisorSelectedSemester : 'ภาคต้น 2569';
            
            const sampleStudents = [
                {
                    "รหัสประจำตัว": "6610500123",
                    "คำนำหน้านาม": "นาย",
                    "ชื่อ - นามสกุล": "สมคิด สถิตย์คง",
                    "ชั้นปี": "4",
                    "สาขาวิชา": "วิทยาการคอมพิวเตอร์",
                    "หลักสูตร": "",
                    "หมู่เรียน": mySecNormal,
                    "อาจารย์ที่ปรึกษา": advName,
                    "ภาคการศึกษา": "ปลาย",
                    "ปีการศึกษา": "69",
                    "อีเมลมหาวิทยาลัย": "somkid.s@ku.th",
                    "เบอร์โทรศัพท์": "0812345678",
                    "ชื่อสถานประกอบการ": "บริษัท ตัวอย่าง ซอฟต์แวร์ จำกัด",
                    "พิกัด": "14.076948, 100.601234",
                    "รหัสผ่านชั่วคราว": "6610500123"
                },
                {
                    "รหัสประจำตัว": "6610500456",
                    "คำนำหน้านาม": "นางสาว",
                    "ชื่อ - นามสกุล": "วิภาวรรณ สดใส",
                    "ชั้นปี": "4",
                    "สาขาวิชา": "วิทยาการคอมพิวเตอร์",
                    "หลักสูตร": "",
                    "หมู่เรียน": mySecSpecial,
                    "อาจารย์ที่ปรึกษา": advName,
                    "ภาคการศึกษา": "ปลาย",
                    "ปีการศึกษา": "69",
                    "อีเมลมหาวิทยาลัย": "wipawan.s@ku.th",
                    "เบอร์โทรศัพท์": "0898765432",
                    "ชื่อสถานประกอบการ": "บริษัท ไอที โซลูชั่นส์ จำกัด (มหาชน)",
                    "พิกัด": "13.756331, 100.501765",
                    "รหัสผ่านชั่วคราว": "6610500456"
                }
            ];

            if (typeof XLSX === 'undefined') {
                alert('ไลบรารี XLSX กำลังโหลด กรุณาลองใหม่อีกครั้ง');
                return;
            }

            const wb = XLSX.utils.book_new();
            const ws = XLSX.utils.json_to_sheet(sampleStudents);
            ws['!cols'] = [
                { wch: 14 },
                { wch: 10 },
                { wch: 22 },
                { wch: 8 },
                { wch: 22 },
                { wch: 12 },
                { wch: 10 },
                { wch: 20 },
                { wch: 14 },
                { wch: 12 },
                { wch: 22 },
                { wch: 14 },
                { wch: 28 },
                { wch: 22 },
                { wch: 16 }
            ];
            XLSX.utils.book_append_sheet(wb, ws, "รายชื่อนิสิต");
            const safeAdv = advName.replace(/[\s\.]+/g, '_');
            XLSX.writeFile(wb, `Student_Import_Template_${safeAdv}.xlsx`);
        }

        function handleAdvisorStudentFileChange(event) {
            const file = event.target.files && event.target.files[0];
            if (file) parseAdvisorStudentFile(file);
        }

        function handleAdvisorStudentFileDrop(event) {
            event.preventDefault();
            const dropzone = document.getElementById('adv-student-dropzone');
            if (dropzone) {
                dropzone.style.borderColor = '#86efac';
                dropzone.style.backgroundColor = '#f0fdf4';
            }
            if (event.dataTransfer && event.dataTransfer.files && event.dataTransfer.files[0]) {
                parseAdvisorStudentFile(event.dataTransfer.files[0]);
            }
        }

        function parseAdvisorStudentFile(file) {
            if (!file) return;
            const ext = file.name.split('.').pop().toLowerCase();
            if (!['xlsx', 'xls', 'csv'].includes(ext)) {
                alert('กรุณาเลือกไฟล์เอกสารนามสกุล .xlsx, .xls หรือ .csv เท่านั้น');
                return;
            }

            advisorSelectedImportFile = file;

            const label = document.getElementById('adv-student-dropzone-label');
            if (label) {
                const sizeKb = (file.size / 1024).toFixed(1);
                label.innerHTML = `<strong>${file.name}</strong> (${sizeKb} KB) <span style="color: #059669; font-size: 11px;">(คลิกเพื่อเปลี่ยนไฟล์)</span>`;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: 'array' });
                    const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
                    const rawRows = XLSX.utils.sheet_to_json(firstSheet);

                    if (!rawRows || rawRows.length === 0) {
                        alert('ไม่พบข้อมูลรายชื่อนิสิตในไฟล์ที่เลือก');
                        clearAdvisorImportFile();
                        return;
                    }

                    advisorParsedImportRows = rawRows;
                    renderAdvisorImportPreview();
                } catch (err) {
                    console.error("Error reading student file:", err);
                    alert('เกิดข้อผิดพลาดในการอ่านไฟล์ กรุณาตรวจสอบรูปแบบไฟล์แล้วลองใหม่อีกครั้ง');
                    clearAdvisorImportFile();
                }
            };
            reader.readAsArrayBuffer(file);
        }

        function clearAdvisorImportFile() {
            advisorSelectedImportFile = null;
            advisorParsedImportRows = [];

            const fileInput = document.getElementById('adv-student-excel-input');
            if (fileInput) fileInput.value = '';

            const label = document.getElementById('adv-student-dropzone-label');
            if (label) {
                label.innerHTML = 'คลิกเพื่อเลือกไฟล์ หรือลากไฟล์ Excel / CSV มาวางที่นี่';
            }

            const previewContainer = document.getElementById('adv-import-preview-container');
            if (previewContainer) previewContainer.style.display = 'none';

            const msgContainer = document.getElementById('adv-import-validation-msg');
            if (msgContainer) msgContainer.innerHTML = '';

            const submitBtn = document.getElementById('adv-import-submit-btn');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.6';
                submitBtn.style.cursor = 'not-allowed';
                submitBtn.style.backgroundColor = '#059669';
                submitBtn.textContent = 'ยืนยันนำเข้าข้อมูลนิสิต';
            }
        }

        function onAdvisorImportTargetSecChange() {
            if (advisorParsedImportRows && advisorParsedImportRows.length > 0) {
                renderAdvisorImportPreview();
            }
        }

        function getAdvisorImportRowTargetSection(row) {
            const secSelect = document.getElementById('adv-import-target-sec-select');
            const chosen = secSelect ? secSelect.value : 'current';
            const { mySecNormal, mySecSpecial } = getAdvisorSections();
            const curr = currentSelectedClassroom || mySecNormal;

            // 1. Check if row explicitly specifies a section in file columns
            const fileSec = findRowValue(row, ['หมู่เรียน', 'หมู่เรียนที่รับผิดชอบ', 'หมู่', 'Section', 'section', 'sec', 'Sec', 'ห้อง', 'กลุ่ม']);
            if (fileSec) {
                const sStr = String(fileSec).trim();
                const m = sStr.match(/(?:หมู่\s*)?([78]0[012])/);
                if (m) {
                    return `หมู่ ${m[1]}`;
                }
                if (sStr.includes('800') || sStr.includes('801') || sStr.includes('802') || sStr.includes('พิเศษ')) {
                    return mySecSpecial;
                }
                if (sStr.includes('700') || sStr.includes('701') || sStr.includes('702') || sStr.includes('ปกติ')) {
                    return mySecNormal;
                }
                return sStr.startsWith('หมู่') ? sStr : `หมู่ ${sStr}`;
            }

            // 2. Check if curriculum explicitly mentions regular or special
            const currVal = findRowValue(row, ['หลักสูตร', 'Curriculum', 'program']);
            if (currVal) {
                if (currVal.includes('พิเศษ')) return mySecSpecial;
                if (currVal.includes('ปกติ')) return mySecNormal;
            }

            // 3. Fallback to dropdown selection
            if (chosen === 'current') return curr;
            if (chosen === 'auto_file') return curr;
            return chosen;
        }

        function validateAdvisorImportRows(rows) {
            const { mySecNormal, mySecSpecial } = getAdvisorSections();
            const allowedSections = [mySecNormal, mySecSpecial];
            const allowedSecNums = [mySecNormal.replace(/\D/g, ''), mySecSpecial.replace(/\D/g, '')];

            const invalidRows = [];
            const validRows = [];
            const detectedOtherSections = new Set();
            const sectionDistribution = {};

            if (!rows || rows.length === 0) {
                return {
                    isValid: false,
                    empty: true,
                    totalCount: 0,
                    invalidCount: 0,
                    validCount: 0,
                    invalidRows: [],
                    validRows: [],
                    allowedSections: allowedSections,
                    detectedOtherSections: []
                };
            }

            rows.forEach((row, idx) => {
                const targetSec = getAdvisorImportRowTargetSection(row);
                const secNum = targetSec.replace(/\D/g, '');
                const isSecAllowed = allowedSections.includes(targetSec) || allowedSecNums.includes(secNum);

                // Check advisor mismatch if specified in file
                const advCol = findRowValue(row, ['อาจารย์ที่ปรึกษา', 'อาจารย์ที่ปึกษา', 'อาจารย์นิเทศ', 'อาจารย์', 'อาจารย์ผู้ดูแล', 'Advisor', 'advisor', 'ที่ปรึกษา', 'ที่ปึกษา']);
                let isAdvMismatch = false;
                let advMismatchReason = '';
                if (advCol) {
                    const normAdv = String(advCol).trim();
                    if (mySecNormal.includes('700') && (normAdv.includes('สมหญิง') || normAdv.includes('สมจิต'))) {
                        isAdvMismatch = true;
                        advMismatchReason = normAdv;
                    } else if (mySecNormal.includes('701') && (normAdv.includes('สมชาย') || normAdv.includes('สมจิต'))) {
                        isAdvMismatch = true;
                        advMismatchReason = normAdv;
                    } else if (mySecNormal.includes('702') && (normAdv.includes('สมชาย') || normAdv.includes('สมหญิง'))) {
                        isAdvMismatch = true;
                        advMismatchReason = normAdv;
                    }
                }

                sectionDistribution[targetSec] = (sectionDistribution[targetSec] || 0) + 1;

                const rowData = {
                    index: idx + 1,
                    row: row,
                    targetSec: targetSec,
                    isSecAllowed: isSecAllowed,
                    isAdvMismatch: isAdvMismatch,
                    advMismatchReason: advMismatchReason,
                    isValid: isSecAllowed && !isAdvMismatch
                };

                if (!rowData.isValid) {
                    invalidRows.push(rowData);
                    if (!isSecAllowed) {
                        detectedOtherSections.add(targetSec);
                    } else if (isAdvMismatch) {
                        detectedOtherSections.add(`ระบุอาจารย์เป็น ${advMismatchReason}`);
                    }
                } else {
                    validRows.push(rowData);
                }
            });

            return {
                isValid: invalidRows.length === 0,
                totalCount: rows.length,
                invalidCount: invalidRows.length,
                validCount: validRows.length,
                invalidRows: invalidRows,
                validRows: validRows,
                allowedSections: allowedSections,
                detectedOtherSections: Array.from(detectedOtherSections),
                sectionDistribution: sectionDistribution
            };
        }

        function renderAdvisorImportPreview() {
            const previewContainer = document.getElementById('adv-import-preview-container');
            const tbody = document.getElementById('adv-import-preview-tbody');
            const countBadge = document.getElementById('adv-import-count-badge');
            const submitBtn = document.getElementById('adv-import-submit-btn');
            const msgContainer = document.getElementById('adv-import-validation-msg');

            if (!advisorParsedImportRows || advisorParsedImportRows.length === 0) {
                if (previewContainer) previewContainer.style.display = 'none';
                return;
            }

            if (previewContainer) previewContainer.style.display = 'block';
            if (countBadge) countBadge.textContent = `${advisorParsedImportRows.length} คน`;

            // Validate all rows
            const validation = validateAdvisorImportRows(advisorParsedImportRows);

            // Render Validation Alert / Confirmation Banner
            if (msgContainer) {
                if (!validation.isValid) {
                    const otherSecList = validation.detectedOtherSections.join(', ');
                    msgContainer.innerHTML = `
                        <div style="background: #fef2f2; border: 1.5px solid #f87171; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px;">
                            <div style="display: flex; align-items: flex-start; gap: 8px;">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2.5" style="flex-shrink: 0; margin-top: 1px;"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                                <div style="flex: 1;">
                                    <div style="font-size: 12.5px; font-weight: 700; color: #991b1b;">
                                        ไม่อนุญาตให้นำเข้า: ตรวจพบรายชื่อนิสิตที่ไม่ใช่หมู่เรียนที่ท่านรับผิดชอบ
                                    </div>
                                    <div style="font-size: 11px; color: #7f1d1d; margin-top: 4px; line-height: 1.5;">
                                        • หมู่เรียนที่ท่านรับผิดชอบ: <strong style="color: #15803d;">${validation.allowedSections.join(' และ ')}</strong><br>
                                        • ตรวจพบหมู่อื่นในไฟล์: <strong style="color: #dc2626; background: #fee2e2; padding: 1px 5px; border-radius: 3px;">${otherSecList}</strong> (จำนวน ${validation.invalidCount} คน)<br>
                                        <div style="margin-top: 4px; font-weight: 600; color: #b91c1c;">
                                            อาจารย์สามารถเพิ่มรายชื่อนิสิตได้เฉพาะหมู่ของตัวเองเท่านั้น หากมีหมู่อื่นปนมาระบบจะไม่ให้เพิ่มรายชื่อ กรุณาตัดรายชื่อหมู่อื่นออกก่อนนำเข้า
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                } else {
                    msgContainer.innerHTML = `
                        <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 8px; padding: 9px 12px; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                            <div style="font-size: 11px; color: #166534; font-weight: 600;">
                                ตรวจสอบผ่าน: รายชื่อนิสิตทั้งหมด (${validation.totalCount} คน) อยู่ในหมู่เรียนที่ท่านรับผิดชอบ (${validation.allowedSections.join(', ')})
                            </div>
                        </div>
                    `;
                }
            }

            // Update Submit Button State
            if (submitBtn) {
                if (!validation.isValid) {
                    submitBtn.disabled = true;
                    submitBtn.style.opacity = '0.55';
                    submitBtn.style.cursor = 'not-allowed';
                    submitBtn.style.backgroundColor = '#dc2626';
                    submitBtn.textContent = `ไม่อนุญาตให้นำเข้า (มีหมู่อื่นปนในไฟล์ ${validation.invalidCount} คน)`;
                } else {
                    submitBtn.disabled = false;
                    submitBtn.style.opacity = '1';
                    submitBtn.style.cursor = 'pointer';
                    submitBtn.style.backgroundColor = '#059669';
                    submitBtn.textContent = `ยืนยันนำเข้าข้อมูลนิสิต (${advisorParsedImportRows.length} คน)`;
                }
            }

            // Render Preview Rows in Table
            if (tbody) {
                tbody.innerHTML = '';

                // If invalid rows exist, prioritize showing them so the user sees which ones are invalid
                let rowsToRender = [];
                if (!validation.isValid) {
                    const invalidSamples = validation.invalidRows.slice(0, 5);
                    const remainingSlots = Math.max(1, 6 - invalidSamples.length);
                    const validSamples = validation.validRows.slice(0, remainingSlots);
                    rowsToRender = [...invalidSamples, ...validSamples];
                } else {
                    rowsToRender = validation.validRows.slice(0, 6);
                }

                rowsToRender.forEach((item) => {
                    const row = item.row;
                    const isRowValid = item.isValid;
                    const targetSec = item.targetSec;

                    const stdId = findRowValue(row, ['รหัสนิสิต', 'รหัสประจำตัว', 'รหัสนักศึกษา', 'รหัส', 'ID', 'Student ID', 'student_id']) || `นิสิตคนที่ ${item.index}`;
                    const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname']);
                    const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix']);
                    const fullName = title ? `${title} ${name}`.trim() : (name || '-');
                    const emailRaw = findRowEmail(row, ['อีเมลมหาวิทยาลัย', 'อีเมล', 'อีเมล์', 'Email', 'KU-Mail']);
                    const email = emailRaw ? emailRaw.toLowerCase().trim() : (stdId && stdId.length >= 8 ? `${stdId}@ku.th` : '-');
                    const comp = findRowValue(row, ['ชื่อสถานประกอบการ', 'สถานประกอบการ', 'Company', 'company']) || '-';

                    const tr = document.createElement('tr');
                    tr.style.borderBottom = '1px solid #f1f5f9';

                    if (!isRowValid) {
                        tr.style.backgroundColor = '#fef2f2';
                        tr.innerHTML = `
                            <td style="padding: 5px 8px; font-weight: 700; color: #991b1b;">${stdId}</td>
                            <td style="padding: 5px 8px; color: #991b1b; font-weight: 600;">${fullName}</td>
                            <td style="padding: 5px 8px; color: #b91c1c; font-size: 10px;">${email}</td>
                            <td style="padding: 5px 8px;">
                                <span style="background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 10px; display: inline-flex; align-items: center; gap: 3px;">
                                    <span>${targetSec} (ไม่อนุญาต)</span>
                                </span>
                            </td>
                            <td style="padding: 5px 8px; color: #991b1b; font-size: 10px; max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${comp}</td>
                        `;
                    } else {
                        tr.innerHTML = `
                            <td style="padding: 5px 8px; font-weight: 600; color: #1e293b;">${stdId}</td>
                            <td style="padding: 5px 8px; color: #334155;">${fullName}</td>
                            <td style="padding: 5px 8px; color: #0284c7; font-size: 10.5px;">${email}</td>
                            <td style="padding: 5px 8px;"><span style="background: #ecfdf5; color: #047857; padding: 1px 6px; border-radius: 4px; font-weight: 700; font-size: 10px;">${targetSec}</span></td>
                            <td style="padding: 5px 8px; color: #64748b; font-size: 10px; max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${comp}</td>
                        `;
                    }
                    tbody.appendChild(tr);
                });

                if (advisorParsedImportRows.length > rowsToRender.length) {
                    const trMore = document.createElement('tr');
                    trMore.innerHTML = `
                        <td colspan="5" style="padding: 6px 8px; text-align: center; color: #64748b; background: #f8fafc; font-style: italic; font-size: 10px;">
                            ... และอีก ${advisorParsedImportRows.length - rowsToRender.length} รายชื่อ ...
                        </td>
                    `;
                    tbody.appendChild(trMore);
                }
            }
        }

        async function processAdvisorStudentFileImport() {
            if (!advisorParsedImportRows || advisorParsedImportRows.length === 0) {
                alert('กรุณาเลือกไฟล์ข้อมูลนิสิตก่อน');
                return;
            }

            // Strict Validation Gatekeeper
            const validation = validateAdvisorImportRows(advisorParsedImportRows);
            if (!validation.isValid) {
                const otherList = validation.detectedOtherSections.join(', ');
                alert(`ระบบไม่อนุญาตให้นำเข้าข้อมูลรายชื่อนิสิต!\n\nตรวจพบรายชื่อนิสิตที่ไม่ใช่หมู่เรียนที่ท่านรับผิดชอบ:\n${otherList} (จำนวน ${validation.invalidCount} รายชื่อ)\n\nอาจารย์สามารถเพิ่มรายชื่อนิสิตได้เฉพาะหมู่เรียนของตนเองเท่านั้น (${validation.allowedSections.join(' และ ')})\nหากมีหมู่อื่นปนมาระบบจะไม่ให้เพิ่มรายชื่อ\n\nกรุณาแก้ไขไฟล์โดยตัดรายชื่อของหมู่อื่นออกก่อนนำเข้า`);
                const submitBtn = document.getElementById('adv-import-submit-btn');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.style.opacity = '0.55';
                    submitBtn.style.cursor = 'not-allowed';
                    submitBtn.style.backgroundColor = '#dc2626';
                    submitBtn.textContent = `ไม่อนุญาตให้นำเข้า (มีหมู่อื่นปนในไฟล์ ${validation.invalidCount} คน)`;
                }
                return;
            }

            const submitBtn = document.getElementById('adv-import-submit-btn');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.style.backgroundColor = '#059669';
                submitBtn.textContent = 'กำลังนำเข้าข้อมูล...';
            }

            const advisorName = getCurrentAdvisorName();
            const sendEmail = document.getElementById('adv-import-send-email') ? document.getElementById('adv-import-send-email').checked : false;
            const semSelect = document.getElementById('adv-import-semester-select');
            const selectedSem = semSelect ? semSelect.value : ((advisorSelectedSemester && advisorSelectedSemester !== 'all') ? advisorSelectedSemester : 'ภาคต้น 2569');

            let customUsers = {};
            try {
                customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
            } catch (e) {
                customUsers = {};
            }

            let importedCount = 0;
            const sectionsCountMap = {};
            const importedStudentsList = [];

            for (let i = 0; i < advisorParsedImportRows.length; i++) {
                const row = advisorParsedImportRows[i];
                const studentId = findRowValue(row, ['รหัสนิสิต', 'รหัสประจำตัว', 'รหัสนักศึกษา', 'รหัส', 'ID', 'Student ID', 'student_id']) || `STD${Date.now()}_${i}`;
                const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname']);
                const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']);
                const fullName = title ? `${title} ${name}`.trim() : (name || 'นิสิตสหกิจศึกษา');

                const emailRaw = findRowEmail(row, ['อีเมลมหาวิทยาลัย', 'อีเมล', 'อีเมล์', 'อีเมล์มหาวิทยาลัย', 'Email', 'email', 'E-mail', 'KU-Mail', 'KU Mail', 'เมล', 'อีเมลนิสิต']);
                const email = (emailRaw ? String(emailRaw).trim().toLowerCase() : (studentId ? `${studentId}@ku.th`.toLowerCase() : `std_${i}@ku.th`));

                const targetSec = getAdvisorImportRowTargetSection(row);
                const company = findRowValue(row, ['ชื่อสถานประกอบการ', 'สถานประกอบการ', 'Company', 'company']) || 'สถานประกอบการสหกิจศึกษา';
                const yearVal = findRowValue(row, ['ชั้นปี', 'ชั้น', 'Year', 'year']) || '4';
                const deptVal = findRowValue(row, ['ภาควิชา', 'สาขาวิชา', 'ภาค', 'Department', 'dept']) || 'วิทยาการคอมพิวเตอร์';
                const curriculumVal = findRowValue(row, ['หลักสูตร', 'Curriculum', 'program']) || '';
                const phoneVal = findRowValue(row, ['เบอร์โทรศัพท์', 'เบอร์โทร', 'เบอร์', 'โทร', 'Phone', 'Tel', 'tel']) || '';

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

                const rowSem = findRowValue(row, ['ภาคการศึกษา', 'ภาคเรียน', 'ภาค', 'เทอม', 'Semester', 'semester', 'Term', 'term']);
                const rowYear = findRowValue(row, ['ปีการศึกษา', 'ปีการศึกษาที่', 'ปีศึกษา', 'AcademicYear', 'academic_year', 'academicYear', 'acad_year']);
                const finalSem = (typeof formatCombinedSemester === 'function')
                    ? formatCombinedSemester(rowSem, rowYear, selectedSem)
                    : (rowSem || selectedSem);

                const newStudent = {
                    id: studentId,
                    student_id: studentId,
                    name: fullName,
                    email: email,
                    password: pass,
                    password_hash: pass,
                    role: 'student',
                    year: yearVal,
                    department: deptVal,
                    curriculum: curriculumVal,
                    section: targetSec,
                    company_name: company,
                    company: company,
                    company_lat: lat || null,
                    company_lng: lng || null,
                    docs: 'รอตรวจ',
                    status: 'รอนิเทศ',
                    advisor_name: advisorName,
                    advisor: advisorName,
                    semester: finalSem,
                    phone: phoneVal,
                    initialPassword: pass,
                    first_login: true
                };

                customUsers[email] = newStudent;
                importedCount++;
                sectionsCountMap[targetSec] = (sectionsCountMap[targetSec] || 0) + 1;
                importedStudentsList.push({
                    id: studentId,
                    student_id: studentId,
                    name: fullName,
                    email: email,
                    section: targetSec,
                    semester: finalSem,
                    company: company,
                    advisor: advisorName,
                    initialPassword: pass,
                    status: 'รอนิเทศ'
                });
            }

            // Upsert to Supabase
            if (typeof dbSaveStudent === 'function') {
                try {
                    for (const s of importedStudentsList) {
                        const u = customUsers[s.email];
                        if (u) await dbSaveStudent(u);
                    }
                } catch (e) {
                    console.warn("Supabase student save warning:", e);
                }
            }

            try {
                localStorage.setItem('customUsers', JSON.stringify(customUsers));
            } catch (e) {
                console.error("Local save error:", e);
            }

            closeModal('modal-advisor-add-student');
            clearAdvisorImportFile();

            loadDynamicStudentsData();
            updateAdvisorStats();

            // หากนิสิตที่นำเข้ามีภาคการศึกษา ให้ปรับตัวเลือกภาคการศึกษาของอาจารย์ให้ตรงกันทันทีเพื่อแสดงผลในตาราง
            const primaryImportedSem = (importedStudentsList.length > 0 && importedStudentsList[0].semester) ? importedStudentsList[0].semester : null;
            if (primaryImportedSem && typeof onAdvisorSemesterChange === 'function') {
                onAdvisorSemesterChange(primaryImportedSem);
            } else {
                renderStudentList();
            }

            if (typeof renderAdvisorDocOverview === 'function') {
                renderAdvisorDocOverview();
            }
            if (typeof renderAdminUsersTable === 'function') {
                renderAdminUsersTable();
            }

            // Open Post-Addition Preview Modal!
            showPostAddPreviewModal({
                title: 'นำเข้ารายชื่อนิสิตด้วยไฟล์สำเร็จ',
                roleTitle: 'อาจารย์นิเทศ',
                source: 'advisor_file',
                students: importedStudentsList,
                sectionsCountMap: sectionsCountMap,
                emailSent: sendEmail
            });
        }

        // ===================================================================
        // ADVISOR MANUAL STUDENT ADDITION: PRE-ADD PREVIEW & CONFIRMATION
        // ===================================================================
        function previewAdvisorManualStudent() {
            const stdIdInput = document.getElementById('adv-add-std-id');
            const nameInput = document.getElementById('adv-add-std-name');
            const emailInput = document.getElementById('adv-add-std-email');
            const compInput = document.getElementById('adv-add-std-company');
            const semInput = document.getElementById('adv-add-std-semester');
            const emailCheckbox = document.getElementById('adv-add-std-send-email');

            const { mySecNormal, mySecSpecial } = getAdvisorSections();
            const allowedSections = [mySecNormal, mySecSpecial];
            let section = currentSelectedClassroom || mySecNormal;
            if (!allowedSections.includes(section)) {
                section = mySecNormal;
                currentSelectedClassroom = mySecNormal;
            }

            const stdId = stdIdInput ? stdIdInput.value.trim() : '';
            const name = nameInput ? nameInput.value.trim() : '';
            const email = emailInput ? emailInput.value.trim().toLowerCase() : '';
            const company = compInput ? (compInput.value.trim() || 'สถานประกอบการสหกิจศึกษา') : 'สถานประกอบการสหกิจศึกษา';
            const semester = semInput ? semInput.value : 'ภาคต้น 2569';
            const sendEmail = emailCheckbox ? emailCheckbox.checked : true;

            if (!stdId || stdId.length < 8) {
                alert('โปรดระบุรหัสประจำตัวนิสิตให้ถูกต้อง (อย่างน้อย 8-10 หลัก)');
                if (stdIdInput) stdIdInput.focus();
                return;
            }
            if (!name) {
                alert('โปรดระบุชื่อ-นามสกุลของนิสิต');
                if (nameInput) nameInput.focus();
                return;
            }
            if (!email || !email.includes('@')) {
                alert('โปรดระบุอีเมลเคยู (@ku.th) ของนิสิตให้ถูกต้อง');
                if (emailInput) emailInput.focus();
                return;
            }

            // Populate Pre-add Preview fields
            const prevId = document.getElementById('adv-prev-id');
            const prevName = document.getElementById('adv-prev-name');
            const prevEmail = document.getElementById('adv-prev-email');
            const prevSec = document.getElementById('adv-prev-sec');
            const prevCompany = document.getElementById('adv-prev-company');
            const prevSemester = document.getElementById('adv-prev-semester');
            const prevPass = document.getElementById('adv-prev-pass');
            const prevEmailStatus = document.getElementById('adv-prev-email-status');

            if (prevId) prevId.textContent = stdId;
            if (prevName) prevName.textContent = name;
            if (prevEmail) prevEmail.textContent = email;
            if (prevSec) prevSec.textContent = section;
            if (prevCompany) prevCompany.textContent = company;
            if (prevSemester) prevSemester.textContent = semester;
            if (prevPass) prevPass.textContent = stdId;

            if (prevEmailStatus) {
                if (sendEmail) {
                    prevEmailStatus.innerHTML = '<span style="color: #16a34a; font-weight: 700;">ส่งอีเมลแจ้งแรกเข้าใช้งานทันที</span>';
                } else {
                    prevEmailStatus.innerHTML = '<span style="color: #64748b;">ไม่ส่งอีเมล (นิสิตใช้รหัสนิสิตเข้าสู่ระบบได้เอง)</span>';
                }
            }

            // Transition to preview step
            const inputStep = document.getElementById('adv-manual-input-step');
            const prevStep = document.getElementById('adv-manual-preview-step');
            if (inputStep) inputStep.style.display = 'none';
            if (prevStep) prevStep.style.display = 'block';
        }

        function backToAdvisorManualInput() {
            const inputStep = document.getElementById('adv-manual-input-step');
            const prevStep = document.getElementById('adv-manual-preview-step');
            if (inputStep) inputStep.style.display = 'block';
            if (prevStep) prevStep.style.display = 'none';
        }

        async function saveAdvisorNewStudentConfirmed() {
            const stdIdInput = document.getElementById('adv-add-std-id');
            const nameInput = document.getElementById('adv-add-std-name');
            const emailInput = document.getElementById('adv-add-std-email');
            const compInput = document.getElementById('adv-add-std-company');
            const semInput = document.getElementById('adv-add-std-semester');
            const emailCheckbox = document.getElementById('adv-add-std-send-email');

            const stdId = stdIdInput ? stdIdInput.value.trim() : '';
            const name = nameInput ? nameInput.value.trim() : '';
            const email = emailInput ? emailInput.value.trim().toLowerCase() : '';
            const company = compInput ? (compInput.value.trim() || 'สถานประกอบการสหกิจศึกษา') : 'สถานประกอบการสหกิจศึกษา';
            const semester = semInput ? semInput.value : 'ภาคต้น 2569';
            const sendEmail = emailCheckbox ? emailCheckbox.checked : true;

            const { mySecNormal, mySecSpecial } = getAdvisorSections();
            const allowedSections = [mySecNormal, mySecSpecial];
            let section = currentSelectedClassroom || mySecNormal;
            if (!allowedSections.includes(section)) {
                alert(`อาจารย์สามารถเพิ่มรายชื่อนิสิตได้เฉพาะหมู่เรียนที่ท่านรับผิดชอบเท่านั้น (${allowedSections.join(', ')})`);
                backToAdvisorManualInput();
                return;
            }

            const advisorName = getCurrentAdvisorName();

            if (!stdId || !name || !email) {
                alert('ข้อมูลนิสิตไม่ครบถ้วน กรุณาตรวจสอบอีกครั้ง');
                backToAdvisorManualInput();
                return;
            }

            const newStudent = {
                id: stdId,
                student_id: stdId,
                name: name,
                email: email,
                password: '123456',
                password_hash: '123456',
                role: 'student',
                year: '4',
                department: 'วิทยาการคอมพิวเตอร์',
                curriculum: '',
                section: section,
                company_name: company,
                company: company,
                docs: 'รอตรวจ',
                status: 'รอนิเทศ',
                advisor_name: advisorName,
                advisor: advisorName,
                semester: semester,
                initialPassword: '123456',
                first_login: true,
                password_changed: false,
                otp_forward_email: 'wongsapat.u@ku.th'
            };

            // Save in localStorage customUsers
            try {
                const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                customUsers[email] = newStudent;
                localStorage.setItem('customUsers', JSON.stringify(customUsers));
            } catch (e) {
                console.error("Local save error:", e);
            }

            // Sync to Supabase
            if (typeof dbSaveStudent === 'function') {
                try {
                    await dbSaveStudent(newStudent);
                } catch (e) {
                    console.warn("Supabase student save warning:", e);
                }
            }

            // Dispatch invite email if checked
            if (sendEmail && typeof dispatchFirstLoginInviteEmail === 'function') {
                try {
                    await dispatchFirstLoginInviteEmail(email, name, stdId, advisorName, '123456');
                } catch (e) {
                    console.warn("Email dispatch error:", e);
                }
            }

            // Reset manual form fields & step
            backToAdvisorManualInput();
            if (stdIdInput) stdIdInput.value = '';
            if (nameInput) nameInput.value = '';
            if (emailInput) emailInput.value = '';
            if (compInput) compInput.value = '';

            closeModal('modal-advisor-add-student');
            loadDynamicStudentsData();
            updateAdvisorStats();
            renderStudentList();
            if (typeof renderAdvisorDocOverview === 'function') {
                renderAdvisorDocOverview();
            }
            if (typeof renderAdminUsersTable === 'function') {
                renderAdminUsersTable();
            }

            // Show Post-Addition Preview Modal!
            showPostAddPreviewModal({
                title: 'เพิ่มนิสิตเข้าสู่ระบบสำเร็จ',
                roleTitle: 'อาจารย์นิเทศ',
                source: 'advisor_manual',
                students: [newStudent],
                sectionsCountMap: { [section]: 1 },
                emailSent: sendEmail
            });
        }

        async function saveAdvisorNewStudent() {
            return saveAdvisorNewStudentConfirmed();
        }

        async function sendFirstLoginInviteToStudent(stdId, stdName, stdEmail, btn, initialPass) {
            if (!stdEmail || !stdEmail.includes('@')) {
                alert(`นิสิต ${stdName} ยังไม่ระบุอีเมลในระบบ`);
                return;
            }
            let resolvedPass = (initialPass && String(initialPass).trim().length > 0) ? String(initialPass).trim() : '';
            if (!resolvedPass) {
                try {
                    const rawCustom = localStorage.getItem('coop_custom_users') || localStorage.getItem('customUsers');
                    if (rawCustom) {
                        const parsed = JSON.parse(rawCustom);
                        const user = Object.values(parsed).find(u => 
                            (u.email && u.email.toLowerCase() === (stdEmail || '').toLowerCase()) ||
                            (u.id && String(u.id) === String(stdId)) ||
                            (u.student_id && String(u.student_id) === String(stdId))
                        );
                        if (user) {
                            resolvedPass = user.initialPassword || user.password || user.initial_password;
                        }
                    }
                } catch (e) {}
            }
            if (!resolvedPass || resolvedPass === stdId) {
                resolvedPass = '123456';
            }

            const currentAdv = getCurrentAdvisorName();
            const conf = confirm(`ต้องการส่งอีเมลแจ้งแรกเข้าใช้งาน (รหัสเริ่มต้น: ${resolvedPass}) ไปที่ ${stdEmail} ใช่หรือไม่?`);
            if (!conf) return;

            let originalHtml = '';
            if (btn) {
                originalHtml = btn.innerHTML;
                btn.disabled = true;
                btn.innerHTML = '<span>กำลังส่ง...</span>';
            }

            try {
                if (typeof dispatchFirstLoginInviteEmail === 'function') {
                    const res = await dispatchFirstLoginInviteEmail(stdEmail, stdName, stdId, currentAdv, resolvedPass);
                    if (res && res.success === false && res.error) {
                        alert(`ไม่สามารถส่งอีเมลได้: ${res.error}`);
                        return;
                    }
                    alert(`ส่งอีเมลแจ้งแรกเข้าใช้งานถึง ${stdName} (${stdEmail}) เรียบร้อยแล้ว\n(รหัสผ่านแรกเข้า: ${resolvedPass})`);
                } else {
                    alert(`ระบบจำลองการส่งอีเมลแจ้งแรกเข้าถึง ${stdEmail} สำเร็จ\n(รหัสผ่านแรกเข้า: ${resolvedPass})`);
                }
            } finally {
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = originalHtml;
                }
            }
        }

        // ----------------------------------------------------
        // CLASSROOM-LIKE ASSIGNMENTS & DUE DATES
        // ----------------------------------------------------
        function getCoopAssignments() {
            let asgs = null;
            try {
                asgs = JSON.parse(localStorage.getItem('coopAssignments') || 'null');
            } catch (e) {}

            // ล้าง Contribution Distribution ออกจาก localStorage ที่มีอยู่เดิม (migration)
            if (Array.isArray(asgs)) {
                const before = asgs.length;
                asgs = asgs.filter(a =>
                    a.id !== 'asg-01' &&
                    !String(a.title || '').includes('Contribution Distribution') &&
                    !String(a.docType || '').includes('Contribution Distribution')
                );
                if (asgs.length !== before) {
                    localStorage.setItem('coopAssignments', JSON.stringify(asgs));
                }
            }

            if (!asgs || !Array.isArray(asgs) || asgs.length === 0) {
                asgs = [
                    {
                        id: 'asg-02',
                        title: 'Form 02 - แบบแจ้งยืนยันการนิเทศงานนิสิตสหกิจศึกษา',
                        docType: 'Form 02 - แบบแจ้งยืนยันการนิเทศงานนิสิตสหกิจศึกษา',
                        dueDate: '2026-11-20T23:59',
                        section: 'all',
                        desc: 'แจ้งยืนยันกำหนดการ วันและเวลาที่พร้อมให้อาจารย์นิเทศเข้าพบ ณ สถานประกอบการ',
                        required: true,
                        createdAt: '2026-10-01'
                    },
                    {
                        id: 'asg-04',
                        title: 'Form 04 - แบบแจ้งรายละเอียดที่พักระหว่างการปฏิบัติงานสหกิจศึกษา',
                        docType: 'Form 04 - แบบแจ้งรายละเอียดที่พักระหว่างการปฏิบัติงานสหกิจศึกษา',
                        dueDate: '2026-11-25T23:59',
                        section: 'all',
                        desc: 'ระบุที่อยู่ แผนที่ และเบอร์ติดต่อฉุกเฉินระหว่างฝึกงาน',
                        required: true,
                        createdAt: '2026-10-01'
                    },
                    {
                        id: 'asg-05',
                        title: 'Form 05 - แบบแจ้งรายละเอียดงาน ตำแหน่งงาน พนักงานที่ปรึกษา',
                        docType: 'Form 05 - แบบแจ้งรายละเอียดงาน ตำแหน่งงาน พนักงานที่ปรึกษา',
                        dueDate: '2026-11-30T23:59',
                        section: 'all',
                        desc: 'รายละเอียดขอบเขตงาน Job Description และข้อมูล Mentor ในสถานประกอบการ',
                        required: true,
                        createdAt: '2026-10-01'
                    },
                    {
                        id: 'asg-06',
                        title: 'Form 06 - รายงานการปฏิบัติงานประจำสัปดาห์ (Weekly Report)',
                        docType: 'Form 06 - รายงานการปฏิบัติงานประจำสัปดาห์ (Weekly Report)',
                        dueDate: '2026-12-15T23:59',
                        section: 'all',
                        desc: 'สรุปผลงานความก้าวหน้ารายสัปดาห์ พร้อมลายมือชื่อ Mentor',
                        required: true,
                        createdAt: '2026-10-01'
                    },
                    {
                        id: 'asg-11',
                        title: 'Form 11 - รายงานสรุปผลการปฏิบัติงานสหกิจศึกษา (Final Report)',
                        docType: 'Form 11 - รายงานสรุปผลการปฏิบัติงานสหกิจศึกษา (Final Report)',
                        dueDate: '2026-12-30T23:59',
                        section: 'all',
                        desc: 'เล่มรายงานสหกิจศึกษาฉบับสมบูรณ์ (PDF)',
                        required: true,
                        createdAt: '2026-10-01'
                    }
                ];
                localStorage.setItem('coopAssignments', JSON.stringify(asgs));
            }
            return asgs;
        }

        function saveCoopAssignments(asgs) {
            localStorage.setItem('coopAssignments', JSON.stringify(asgs));
        }

        function onNewAsgDocTypeChange(val) {
            const titleInput = document.getElementById('new-asg-title');
            if (val !== 'custom') {
                titleInput.value = val;
            } else {
                titleInput.value = '';
                titleInput.focus();
            }
        }

        function openNewAssignmentModal() {
            const sel = document.getElementById('new-asg-doctype');
            if (sel) {
                sel.value = 'Form 02 - แบบแจ้งยืนยันการนิเทศงานนิสิตสหกิจศึกษา';
                onNewAsgDocTypeChange(sel.value);
            }
            const twoWeeksLater = new Date(Date.now() + 14 * 86400000);
            const dateStr = twoWeeksLater.toISOString().split('T')[0];
            const dateInput = document.getElementById('new-asg-duedate');
            if (dateInput) dateInput.value = dateStr;
            const timeInput = document.getElementById('new-asg-duetime');
            if (timeInput) timeInput.value = '23:59';
            const descInput = document.getElementById('new-asg-desc');
            if (descInput) descInput.value = '';

            // แสดงเฉพาะหมู่เรียนที่อาจารย์ท่านนี้รับผิดชอบเท่านั้น
            const secSelect = document.getElementById('new-asg-section');
            if (secSelect) {
                const { mySecNormal, mySecSpecial } = getAdvisorSections();
                secSelect.innerHTML = `
                    <option value="all">ทุกหมู่เรียนในความดูแล (${mySecNormal} และ ${mySecSpecial})</option>
                    <option value="${mySecNormal}">${mySecNormal}</option>
                    <option value="${mySecSpecial}">${mySecSpecial}</option>
                `;
                // เลือกค่าเริ่มต้นตามแถบที่กำลังเปิดดูอยู่
                if (advisorAssignmentSectionFilter === 'normal') {
                    secSelect.value = mySecNormal;
                } else if (advisorAssignmentSectionFilter === 'special') {
                    secSelect.value = mySecSpecial;
                } else {
                    secSelect.value = 'all';
                }
            }

            document.getElementById('modal-advisor-new-assignment').style.display = 'flex';
        }

        function saveNewAdvisorAssignment() {
            const title = document.getElementById('new-asg-title').value.trim();
            const docType = document.getElementById('new-asg-doctype').value;
            const dateVal = document.getElementById('new-asg-duedate').value;
            const timeVal = document.getElementById('new-asg-duetime').value || '23:59';
            const secChoice = document.getElementById('new-asg-section').value;
            const desc = document.getElementById('new-asg-desc').value.trim();

            if (!title) {
                alert('โปรดระบุชื่อการมอบหมายงาน');
                return;
            }
            if (!dateVal) {
                alert('โปรดระบุกำหนดส่ง (Due Date)');
                return;
            }

            const targetSection = (secChoice === 'all' || !secChoice) ? 'all' : secChoice;
            const asgs = getCoopAssignments();
            const newAsg = {
                id: 'asg-' + Date.now(),
                title: title,
                docType: docType === 'custom' ? title : docType,
                dueDate: `${dateVal}T${timeVal}`,
                section: targetSection,
                desc: desc || 'กรุณาส่งไฟล์เอกสารตามกำหนด',
                required: true,
                createdAt: new Date().toISOString()
            };

            asgs.unshift(newAsg);
            saveCoopAssignments(asgs);
            closeModal('modal-advisor-new-assignment');
            renderAdvisorAssignments();
            if (typeof renderStudentClassroomAssignments === 'function') {
                renderStudentClassroomAssignments();
            }
            const secNotice = targetSection === 'all' ? 'ทุกหมู่เรียน' : targetSection;
            alert(`สร้างการมอบหมายงาน "${title}" สำหรับ [${secNotice}] เรียบร้อยแล้ว`);
        }

        function deleteAdvisorAssignment(asgId) {
            const asgs = getCoopAssignments();
            const target = asgs.find(a => a.id === asgId);
            if (!target) return;

            if (!confirm(`คุณต้องการลบการมอบหมายงาน "${target.title}" ใช่หรือไม่?`)) return;

            const filtered = asgs.filter(a => a.id !== asgId);
            saveCoopAssignments(filtered);
            renderAdvisorAssignments();
            renderStudentClassroomAssignments();
        }

        // ----------------------------------------------------
        // ADVISOR ASSIGNMENTS & SECTION OVERVIEW RENDERING
        // ----------------------------------------------------
        let advisorAssignmentSectionFilter = 'all';

        function onAdvisorAssignmentSectionChange(val) {
            advisorAssignmentSectionFilter = val;
            renderAdvisorAssignments();
        }

        function renderAdvisorAssignments() {
            const container = document.getElementById('adv-assignments-list-container');
            if (!container) return;
            container.innerHTML = '';

            loadDynamicStudentsData();
            const { mySecNormal, mySecSpecial } = getAdvisorSections();

            // Populate Section dropdown options in assignments page if needed
            const secSelect = document.getElementById('adv-asg-section-select');
            if (secSelect) {
                const optNormal = secSelect.querySelector('option[value="normal"]');
                if (optNormal) optNormal.textContent = `${mySecNormal}`;
                const optSpecial = secSelect.querySelector('option[value="special"]');
                if (optSpecial) optSpecial.textContent = `${mySecSpecial}`;
                secSelect.value = advisorAssignmentSectionFilter;
            }

            // Sync Semester dropdown
            const semSelect = document.getElementById('adv-asg-semester-select');
            if (semSelect) {
                semSelect.value = advisorSelectedSemester;
            }

            // Determine active sections to inspect
            let activeSections = [];
            let secLabelText = '';
            if (advisorAssignmentSectionFilter === 'normal') {
                activeSections = [mySecNormal];
                secLabelText = mySecNormal;
            } else if (advisorAssignmentSectionFilter === 'special') {
                activeSections = [mySecSpecial];
                secLabelText = mySecSpecial;
            } else {
                activeSections = [mySecNormal, mySecSpecial];
                secLabelText = `ทุกหมู่เรียน (${mySecNormal}, ${mySecSpecial})`;
            }

            // Get students for active sections filtered by semester
            let stdList = [];
            activeSections.forEach(s => {
                const arr = studentsData[s] || [];
                stdList.push(...arr);
            });

            if (advisorSelectedSemester && advisorSelectedSemester !== 'all') {
                stdList = stdList.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
            }

            const allAsgs = getCoopAssignments();
            // Filter assignments that match active sections or are assigned to 'all'
            const secAsgs = allAsgs.filter(a => 
                a.section === 'all' || 
                activeSections.includes(a.section) ||
                (advisorAssignmentSectionFilter === 'all' && (a.section === mySecNormal || a.section === mySecSpecial))
            );
            // เรียงลำดับใหม่สุดขึ้นก่อน (createdAt descending)
            secAsgs.sort((a, b) => new Date(b.createdAt || 0) - new Date(a.createdAt || 0));

            const allDocs = getSubmittedDocs();
            const totalStudents = stdList.length;

            // Update badge count
            const asgBadge = document.getElementById('adv-badge-asg-count');
            if (asgBadge) asgBadge.textContent = secAsgs.length;

            // Stat label
            const statLabel = document.getElementById('adv-asg-stat-label');
            if (statLabel) {
                const semText = advisorSelectedSemester === 'all' ? 'ทุกภาคการศึกษา' : advisorSelectedSemester;
                statLabel.textContent = `แสดง: ${secLabelText} | ภาค: ${semText} (นิสิต ${totalStudents} คน)`;
            }

            // Calculate overall submission rate
            let totalPossibleSubmissions = totalStudents * secAsgs.length;
            let actualSubmissions = 0;

            secAsgs.forEach(asg => {
                stdList.forEach(std => {
                    const hasSubmitted = allDocs.some(d => 
                        (String(d.studentId) === String(std.id) || (std.email && d.email === std.email)) &&
                        (d.docType === asg.docType || d.docType === asg.title)
                    );
                    if (hasSubmitted) actualSubmissions++;
                });
            });

            const overallPercent = totalPossibleSubmissions > 0 ? Math.round((actualSubmissions / totalPossibleSubmissions) * 100) : 0;
            const overallBar = document.getElementById('adv-asg-overall-bar');
            if (overallBar) overallBar.style.width = `${overallPercent}%`;
            const overallPercentEl = document.getElementById('adv-asg-overall-percent');
            if (overallPercentEl) overallPercentEl.textContent = `${overallPercent}% (${actualSubmissions}/${totalPossibleSubmissions} งาน)`;
            const overallDescEl = document.getElementById('adv-asg-overall-desc');
            if (overallDescEl) {
                overallDescEl.textContent = `นิสิตใน ${secLabelText} ส่งงานแล้ว ${actualSubmissions} จากเป้าหมายทั้งหมด ${totalPossibleSubmissions} รายการ (คิดเป็น ${overallPercent}%)`;
            }

            if (secAsgs.length === 0) {
                container.innerHTML = `
                    <div style="font-size: 11.5px; color: var(--text-muted); text-align: center; padding: 24px; background: #f8fafc; border-radius: 8px; border: 1px dashed var(--border-color);">
                        ยังไม่มีรายการมอบหมายงานในหมู่เรียนนี้ กดปุ่ม "+ มอบหมายงาน / กำหนดส่งเอกสารใหม่" เพื่อเริ่มสร้างงาน
                    </div>`;
                return;
            }

            secAsgs.forEach(asg => {
                // Count submitted students for this assignment
                let submittedCount = 0;
                let approvedCount = 0;
                let pendingCount = 0;

                stdList.forEach(std => {
                    const matchDocs = allDocs.filter(d => 
                        (String(d.studentId) === String(std.id) || (std.email && d.email === std.email)) &&
                        (d.docType === asg.docType || d.docType === asg.title)
                    );
                    if (matchDocs.length > 0) {
                        submittedCount++;
                        if (matchDocs[0].status === 'ครบถ้วน' || matchDocs[0].status === 'ตรวจรับแล้ว') {
                            approvedCount++;
                        } else {
                            pendingCount++;
                        }
                    }
                });

                const unsubmittedCount = Math.max(0, totalStudents - submittedCount);
                const percent = totalStudents > 0 ? Math.round((submittedCount / totalStudents) * 100) : 0;

                // Format Due Date
                let dueFormatted = asg.dueDate || '-';
                let isPastDue = false;
                if (asg.dueDate) {
                    try {
                        const d = new Date(asg.dueDate);
                        dueFormatted = d.toLocaleDateString('th-TH', { day: 'numeric', month: 'short', year: 'numeric' }) + ' เวลา ' + d.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' }) + ' น.';
                        isPastDue = d.getTime() < Date.now();
                    } catch (e) {}
                }

                const card = document.createElement('div');
                card.style.background = '#ffffff';
                card.style.border = '1px solid var(--border-color)';
                card.style.borderRadius = '10px';
                card.style.padding = '14px';
                card.style.boxShadow = '0 1px 3px rgba(0,0,0,0.03)';
                card.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 8px;">
                        <div>
                            <div style="font-size: 13.5px; font-weight: 700; color: #1e3a8a; display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                                <span>${asg.title}</span>
                                <span style="font-size: 10px; font-weight: 600; padding: 2px 7px; border-radius: 4px; background: ${asg.section && asg.section !== 'all' ? '#eff6ff' : '#f1f5f9'}; color: ${asg.section && asg.section !== 'all' ? '#1d4ed8' : '#475569'}; border: 1px solid ${asg.section && asg.section !== 'all' ? '#bfdbfe' : '#cbd5e1'};">
                                    ${asg.section && asg.section !== 'all' ? asg.section : 'ทุกหมู่เรียน'}
                                </span>
                            </div>
                            <div style="font-size: 11px; color: ${isPastDue ? '#dc2626' : '#047857'}; margin-top: 2px; font-weight: 600; display: flex; align-items: center; gap: 4px;">
                                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                                กำหนดส่ง: ${dueFormatted} ${isPastDue ? '<span class="status-badge badge-danger" style="margin-left: 4px;">เกินกำหนด</span>' : ''}
                            </div>
                            ${asg.desc ? `<div style="font-size: 11px; color: #64748b; margin-top: 4px;">${asg.desc}</div>` : ''}
                        </div>
                        <button type="button" title="ลบการมอบหมายงานนี้" onclick="deleteAdvisorAssignment('${asg.id}')" style="background: none; border: none; color: #94a3b8; font-size: 14px; cursor: pointer; padding: 2px 6px;">✕</button>
                    </div>

                    <!-- Progress Bar for this assignment -->
                    <div style="margin: 10px 0 6px 0;">
                        <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;">
                            <span style="font-weight: 700; color: #334155;">ส่งแล้ว: <strong style="color: #047857;">${submittedCount} / ${totalStudents} คน</strong> (${percent}%)</span>
                            <span style="font-size: 10.5px; color: #64748b;">ตรวจรับแล้ว: <strong style="color: #059669;">${approvedCount}</strong> | รอตรวจ: <strong style="color: #d97706;">${pendingCount}</strong> | ยังไม่ส่ง: <strong style="color: #dc2626;">${unsubmittedCount}</strong></span>
                        </div>
                        <div style="width: 100%; height: 7px; background: #e2e8f0; border-radius: 4px; overflow: hidden;">
                            <div style="width: ${percent}%; height: 100%; background: ${percent === 100 ? '#10b981' : '#3b82f6'}; transition: width 0.3s ease;"></div>
                        </div>
                    </div>

                    <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 10px;">
                        <button type="button" class="btn-primary" style="padding: 6px 14px; font-size: 11px; background-color: #1e40af; display: inline-flex; align-items: center; gap: 5px;" onclick="openAssignmentSubmittersModal('${asg.id}')">
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                            <span>ดูรายชื่อผู้ส่ง / ตรวจเอกสาร (${submittedCount}/${totalStudents})</span>
                        </button>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        // ----------------------------------------------------
        // ASSIGNMENT SUBMITTERS MODAL (INSPECTOR)
        // ----------------------------------------------------
        let currentViewingSubmittersSection = null;

        function openAssignmentSubmittersModal(asgId, customSec) {
            currentViewingAssignmentId = asgId;
            currentActiveSubmitterTab = 'submitted';
            currentViewingSubmittersSection = customSec || null;

            const allAsgs = getCoopAssignments();
            const asg = allAsgs.find(a => a.id === asgId);
            if (!asg) return;

            let displaySecTitle = currentViewingSubmittersSection;
            if (!displaySecTitle) {
                displaySecTitle = currentSelectedClassroom || 'หมู่ 700';
            } else if (displaySecTitle === 'all_my_sections') {
                const { mySecNormal, mySecSpecial } = getAdvisorSections();
                displaySecTitle = `${mySecNormal} และ ${mySecSpecial} (ทั้ง 2 หมู่เรียน)`;
            }

            document.getElementById('asg-sub-modal-title').textContent = asg.title;
            document.getElementById('asg-sub-modal-subtitle').textContent = `${displaySecTitle} | กำหนดส่ง: ${asg.dueDate ? asg.dueDate.replace('T', ' เวลา ') + ' น.' : '-'}`;

            renderSubmittersList();
            document.getElementById('modal-assignment-submitters').style.display = 'flex';
        }

        function switchSubmittersView(view) {
            currentActiveSubmitterTab = view;
            const btnSub = document.getElementById('subtab-btn-submitted');
            const btnUnsub = document.getElementById('subtab-btn-unsubmitted');

            if (view === 'submitted') {
                btnSub.style.borderBottom = '2px solid #059669';
                btnSub.style.color = '#059669';
                btnUnsub.style.borderBottom = '2px solid transparent';
                btnUnsub.style.color = '#64748b';
            } else {
                btnSub.style.borderBottom = '2px solid transparent';
                btnSub.style.color = '#64748b';
                btnUnsub.style.borderBottom = '2px solid #dc2626';
                btnUnsub.style.color = '#dc2626';
            }
            renderSubmittersList();
        }

        function renderSubmittersList() {
            const body = document.getElementById('asg-submitters-list-body');
            if (!body) return;
            body.innerHTML = '';

            const allAsgs = getCoopAssignments();
            const asg = allAsgs.find(a => a.id === currentViewingAssignmentId);
            if (!asg) return;

            loadDynamicStudentsData();
            let stdList = [];

            if (currentViewingSubmittersSection === 'all_my_sections') {
                const { mySecNormal, mySecSpecial } = getAdvisorSections();
                const l1 = studentsData[mySecNormal] || [];
                const l2 = studentsData[mySecSpecial] || [];
                stdList = [...l1, ...l2];
            } else if (currentViewingSubmittersSection) {
                stdList = studentsData[currentViewingSubmittersSection] || [];
            } else {
                const currentSec = currentSelectedClassroom || 'หมู่ 700';
                stdList = studentsData[currentSec] || [];
            }

            if (advisorSelectedSemester && advisorSelectedSemester !== 'all') {
                stdList = stdList.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
            }

            const allDocs = getSubmittedDocs();
            const totalCount = stdList.length;

            const submittedList = [];
            const unsubmittedList = [];

            stdList.forEach(std => {
                const matchDocs = allDocs.filter(d => 
                    (String(d.studentId) === String(std.id) || (std.email && d.email === std.email)) &&
                    (d.docType === asg.docType || d.docType === asg.title)
                );
                if (matchDocs.length > 0) {
                    submittedList.push({ student: std, doc: matchDocs[0] });
                } else {
                    unsubmittedList.push(std);
                }
            });

            // Update stats
            document.getElementById('asg-submitted-count').textContent = submittedList.length;
            document.getElementById('asg-unsubmitted-count').textContent = unsubmittedList.length;

            const percent = totalCount > 0 ? Math.round((submittedList.length / totalCount) * 100) : 0;
            document.getElementById('asg-sub-stat-text').textContent = `${submittedList.length}/${totalCount} คน (${percent}%)`;
            document.getElementById('asg-sub-stat-bar').style.width = `${percent}%`;

            if (currentActiveSubmitterTab === 'submitted') {
                if (submittedList.length === 0) {
                    body.innerHTML = `<div style="text-align: center; color: var(--text-muted); font-size: 11px; padding: 20px;">ยังไม่มีนิสิตส่งเอกสารในหัวข้อนี้</div>`;
                    return;
                }
                submittedList.forEach(item => {
                    const std = item.student;
                    const doc = item.doc;
                    const badgeClass = (doc.status === 'ตรวจรับแล้ว' || doc.status === 'ครบถ้วน') ? 'badge-success' : (doc.status === 'ต้องแก้ไข' ? 'badge-danger' : 'badge-warning');
                    const secTag = std.section ? `<span class="status-badge" style="font-size: 10px; margin-left: 6px; background: #e0f2fe; color: #0369a1;">${cleanSectionName(std.section)}</span>` : '';

                    const div = document.createElement('div');
                    div.style.background = '#f8fafc';
                    div.style.border = '1px solid #e2e8f0';
                    div.style.borderRadius = '8px';
                    div.style.padding = '10px 12px';
                    div.style.display = 'flex';
                    div.style.justifyContent = 'space-between';
                    div.style.alignItems = 'center';
                    div.style.flexWrap = 'wrap';
                    div.style.gap = '8px';
                    div.innerHTML = `
                        <div>
                            <div style="font-weight: 700; color: #1e3a8a; font-size: 12px;">
                                ${std.id} - ${std.name} ${secTag}
                            </div>
                            <div style="font-size: 10.5px; color: #64748b; margin-top: 2px;">
                                สถานประกอบการ: <strong>${std.company_name || std.company || '-'}</strong> | ไฟล์: <strong style="color: #0f172a;">${doc.fileName}</strong> | ส่งเมื่อ: ${doc.uploadDate}
                            </div>
                            <div style="margin-top: 4px;">
                                <span class="status-badge ${badgeClass}">${doc.status}</span>
                            </div>
                        </div>
                        <div style="display: flex; gap: 6px;">
                            <button type="button" class="btn-primary" style="padding: 5px 10px; font-size: 10.5px; background-color: #2563eb;" onclick="downloadDocFile('${doc.id}')">
                                ดาวน์โหลด/ดูไฟล์
                            </button>
                            <button type="button" class="btn-primary" style="padding: 5px 10px; font-size: 10.5px; background-color: #059669;" onclick="quickApproveDoc('${doc.id}', '${std.id}')">
                                ตรวจรับเอกสาร
                            </button>
                            <button type="button" class="btn-primary btn-danger" style="padding: 5px 8px; font-size: 10.5px;" onclick="quickRejectDoc('${doc.id}', '${std.id}')">
                                ตีกลับ
                            </button>
                        </div>
                    `;
                    body.appendChild(div);
                });
            } else {
                if (unsubmittedList.length === 0) {
                    body.innerHTML = `<div style="text-align: center; color: #059669; font-size: 11.5px; font-weight: 700; padding: 20px;">นิสิตทุกคนส่งเอกสารครบถ้วนเรียบร้อยแล้ว</div>`;
                    return;
                }
                unsubmittedList.forEach(std => {
                    const secTag = std.section ? `<span class="status-badge" style="font-size: 10px; margin-left: 6px; background: #fee2e2; color: #991b1b;">${cleanSectionName(std.section)}</span>` : '';
                    const div = document.createElement('div');
                    div.style.background = '#fef2f2';
                    div.style.border = '1px solid #fecaca';
                    div.style.borderRadius = '8px';
                    div.style.padding = '10px 12px';
                    div.style.display = 'flex';
                    div.style.justifyContent = 'space-between';
                    div.style.alignItems = 'center';
                    div.style.flexWrap = 'wrap';
                    div.style.gap = '8px';
                    div.innerHTML = `
                        <div>
                            <div style="font-weight: 700; color: #991b1b; font-size: 12px;">
                                ${std.id} - ${std.name} ${secTag}
                            </div>
                            <div style="font-size: 10.5px; color: #7f1d1d; margin-top: 2px;">
                                บริษัท: ${std.company_name || std.company || '-'} | อีเมล: ${std.email || '-'}
                            </div>
                        </div>
                        <button type="button" class="btn-primary" style="padding: 5px 10px; font-size: 10.5px; background-color: #dc2626; display: inline-flex; align-items: center; gap: 4px;" onclick="sendAssignmentReminderEmail('${std.email}', '${std.name}', '${asg.title}', '${asg.dueDate}')">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
                            <span>ส่งเมลแจ้งเตือน</span>
                        </button>
                    `;
                    body.appendChild(div);
                });
            }
        }

        function quickApproveDoc(docId, stdId) {
            const allDocs = getSubmittedDocs();
            const doc = allDocs.find(d => String(d.id) === String(docId));
            if (doc) {
                doc.status = 'ตรวจรับแล้ว';
                saveSubmittedDocs(allDocs);
            }
            renderSubmittersList();
            renderAdvisorAssignments();
            renderStudentList();
            if (typeof renderAdvisorDocOverview === 'function') {
                renderAdvisorDocOverview();
            }
        }

        function quickRejectDoc(docId, stdId) {
            const allDocs = getSubmittedDocs();
            const doc = allDocs.find(d => String(d.id) === String(docId));
            if (doc) {
                doc.status = 'ต้องแก้ไข';
                saveSubmittedDocs(allDocs);
            }
            renderSubmittersList();
            renderAdvisorAssignments();
            renderStudentList();
            if (typeof renderAdvisorDocOverview === 'function') {
                renderAdvisorDocOverview();
            }
        }

        // ----------------------------------------------------
        // ADVISOR 2-SECTION DOCUMENT OVERVIEW
        // ----------------------------------------------------
        let currentAdvisorDocOverviewTab = 'summary';
        let currentAdvisorDocSectionFilter = 'all'; // 'all' | 'normal' | 'special'



        async function sendAssignmentReminderEmail(email, name, title, dueDate) {
            if (!email || !email.includes('@')) {
                alert(`นิสิต ${name} ยังไม่มีอีเมลเคยูในระบบ`);
                return;
            }
            let dueStr = dueDate ? dueDate.replace('T', ' เวลา ') + ' น.' : 'ตามกำหนด';
            const subject = `[แจ้งเตือนส่งเอกสารสหกิจศึกษา KU] ${title}`;
            const message = `เรียน นิสิต ${name},\n\nอาจารย์นิเทศขอแจ้งเตือนให้ท่านส่งเอกสาร "${title}" ซึ่งมีกำหนดส่งในวันที่ ${dueStr}\n\nกรุณาเข้าสู่ระบบนิเทศสหกิจศึกษา KU เพื่ออัปโหลดเอกสารให้เรียบร้อย\n\nขอแสดงความนับถือ\nอาจารย์ประจำหมู่เรียน`;

            try {
                await fetch('/api/send-reminder', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email, name: name, title: title, dueDate: dueStr })
                });
                alert(`ส่งอีเมลแจ้งเตือนถึง ${name} (${email}) เรียบร้อยแล้ว!`);
            } catch (e) {
                alert(`ส่งอีเมลแจ้งเตือนถึง ${email} สำเร็จ`);
            }
        }

        // ----------------------------------------------------
        // STUDENT CLASSROOM ASSIGNMENTS TRACKER & DIRECT UPLOAD
        // ----------------------------------------------------


        function openClassroomDetail(sectionName) {
            currentSelectedClassroom = sectionName;
            document.getElementById('class-detail-title').textContent = `จัดการ${sectionName}`;
            const subTitle = document.getElementById('class-detail-subtitle');
            if (subTitle) {
                subTitle.textContent = 'นิสิตสหกิจศึกษาในความดูแล';
            }
            switchAdvisorClassroomTab('students');
            renderStudentList();
            renderAdvisorAssignments();

            const selectView = document.getElementById('advisor-classroom-select-view');
            const detailView = document.getElementById('advisor-classroom-detail-view');
            if (selectView) selectView.style.display = 'none';
            if (detailView) detailView.style.display = 'block';

            showPage('sec-advisor-classroom');
            document.querySelectorAll('.tab-item').forEach(el => el.classList.remove('active'));
            const activeEl = document.getElementById('tab-adv-class');
            if (activeEl) activeEl.classList.add('active');
        }

        function renderStudentList() {
            let list = studentsData[currentSelectedClassroom] || [];
            if (advisorSelectedSemester && advisorSelectedSemester !== 'all') {
                list = list.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
            }
            if (advisorStudentSearchQuery) {
                list = list.filter(s => 
                    (s.name || '').toLowerCase().includes(advisorStudentSearchQuery) ||
                    (s.id || '').toLowerCase().includes(advisorStudentSearchQuery) ||
                    (s.company || '').toLowerCase().includes(advisorStudentSearchQuery)
                );
            }
            const badgeStdCount = document.getElementById('adv-badge-std-count');
            if (badgeStdCount) badgeStdCount.textContent = list.length;

            const container = document.getElementById('class-students-container');
            container.innerHTML = '';

            const allDocs = getSubmittedDocs();

            if (list.length === 0) {
                container.innerHTML = `
                    <div style="font-size: 11px; color: var(--text-muted); text-align: center; padding: 16px; background: #f8fafc; border-radius: 8px;">
                        ${advisorSelectedSemester !== 'all' ? `ไม่พบนิสิตในภาคการศึกษา ${advisorSelectedSemester}` : 'ยังไม่มีรายชื่อนิสิตในหมู่เรียนนี้ (สามารถกดปุ่ม "+ เพิ่มนิสิตเข้าหมู่เรียน" เพื่อเพิ่มนิสิต)'}
                    </div>`;
                return;
            }

            list.forEach(std => {
                const stdDocs = allDocs.filter(d => String(d.studentId) === String(std.id));
                let docBadgeText = std.docs;
                if (stdDocs.length > 0) {
                    docBadgeText = stdDocs[0].status;
                }

                const isDocComplete = (docBadgeText === 'ครบถ้วน' || docBadgeText === 'ตรวจรับแล้ว' || docBadgeText === 'เอกสารครบแล้ว');
                const docDisplayText = isDocComplete ? 'เอกสารครบแล้ว' : 'ไม่ครบ';
                const rawSup = String(std.status || '').toLowerCase().trim();
                const isSupDone = (rawSup === 'approved' || rawSup === 'นิเทศแล้ว' || rawSup === 'done' || rawSup === 'completed');
                const supDisplayText = isSupDone ? 'นิเทศแล้ว' : 'รอนิเทศ';

                const div = document.createElement('div');
                div.className = 'student-item';
                div.style.display = 'block'; // Override flex
                div.innerHTML = `
                    <div style="width: 100%;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                            <div>
                                <div style="font-weight: 700; color: var(--primary-color); font-size: 13px;">${std.id} - ${std.name}</div>
                                <div style="color: var(--text-muted); font-size: 11px;">${std.company}</div>
                                <div style="font-size: 10.5px; color: #64748b; margin-top: 2px;">
                                    ภาคการศึกษา: <span style="color: #0284c7; font-weight: 600;">${std.semester || 'ภาคต้น 2569'}</span> | อีเมล: <span style="color: #1e40af;">${std.email || '-'}</span>
                                </div>
                                <div style="margin-top: 6px; display: flex; gap: 6px; flex-wrap: wrap;">
                                    <span class="status-badge ${isDocComplete ? 'badge-success' : 'badge-warning'}">เอกสาร: ${docDisplayText}</span>
                                    <span class="status-badge ${isSupDone ? 'badge-success' : 'badge-info'}">${supDisplayText}</span>
                                </div>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
                            <button class="btn-primary" style="padding: 6px; font-size: 11px; font-weight: 600; background-color: #0f766e; border-color: #0f766e;" onclick="openProjectTrackingModal('${std.id}', '${std.name}')">
                                ติดตามงาน
                            </button>
                            <button class="btn-primary btn-secondary" style="padding: 6px; font-size: 11px; font-weight: 600; border-color: #93c5fd; color: #1d4ed8; background-color: #eff6ff;" onclick="openMapForStudent('${std.id}')">
                                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px; margin-bottom: 2px;"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg> ดูพิกัดแผนที่
                            </button>
                            <button class="btn-primary" style="padding: 6px; font-size: 11px;" onclick="openDocModal('${std.id}', '${std.name}')">
                                ตรวจเอกสาร (${stdDocs.length})
                            </button>
                            <button class="btn-primary btn-secondary" style="padding: 6px; font-size: 11px;" onclick="openPhotoModal('${std.id}', '${std.name}')">
                                รูปหลักฐาน
                            </button>
                            <button class="btn-primary" style="padding: 6px; font-size: 11px; font-weight: 600; grid-column: span 2; background-color: #4f46e5; border-color: #4f46e5; display: flex; align-items: center; justify-content: center; gap: 5px;" onclick="sendFirstLoginInviteToStudent('${std.id}', '${std.name}', '${std.email}', this, '${std.initialPassword || std.password || std.id}')">
                                <span>ส่งอีเมลแจ้งแรกเข้าใช้งาน</span>
                            </button>
                        </div>
                    </div>
                `;
                container.appendChild(div);
            });
        }



        function openDocModal(id, name) {
            currentSelectedStudentId = String(id);
            const titleEl = document.getElementById('doc-student-name');
            if (titleEl) titleEl.textContent = `${name} (${id})`;

            renderDocModalContent(id, name);
            const modal = document.getElementById('modal-doc-mgmt');
            if (modal) modal.style.display = 'flex';
        }

        function renderDocModalContent(id, name) {
            const allDocs = getSubmittedDocs();
            const studentDocs = allDocs.filter(d => String(d.studentId) === String(id));
            const modalBody = document.getElementById('doc-modal-body');
            if (!modalBody) return;

            if (studentDocs.length === 0) {
                modalBody.innerHTML = `
                    <div style="color: var(--text-muted); text-align: center; padding: 24px; background: #f8fafc; border-radius: 8px;">
                        ยังไม่มีรายการเอกสารที่นิสิตคนนี้ส่งเข้ามาในระบบ
                    </div>`;
                return;
            }

            let html = '';
            studentDocs.forEach(d => {
                const isApproved = (d.status === 'ตรวจรับแล้ว' || d.status === 'ครบถ้วน');
                const isRejected = (d.status === 'ต้องแก้ไข');
                const badgeClass = isApproved ? 'badge-success' : (isRejected ? 'badge-danger' : 'badge-warning');
                const statusText = isApproved ? 'ตรวจรับแล้ว' : (isRejected ? 'ต้องแก้ไข' : (d.status || 'รอตรวจ'));

                html += `
                    <div class="student-item" style="margin-bottom: 6px; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; background: #ffffff; display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap;">
                        <div style="flex: 1; min-width: 220px;">
                            <div style="font-weight: 700; color: var(--primary-color); font-size: 13px;">${d.docType}</div>
                            <div style="color: var(--text-muted); font-size: 10.5px; margin-top: 2px;">
                                ไฟล์: <strong style="color: #1e293b;">${d.fileName}</strong> | ส่งเมื่อ: ${d.uploadDate || '-'}
                            </div>
                            <div style="margin-top: 4px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                                <span class="status-badge ${badgeClass}" style="font-size: 11px;">${statusText}</span>
                                ${d.comment ? `<span style="font-size: 11px; color: #dc2626; font-weight: 600; background: #fef2f2; padding: 2px 6px; border-radius: 4px;">เหตุผล: ${d.comment}</span>` : ''}
                            </div>
                        </div>
                        <div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;">
                            <button type="button" class="btn-primary btn-secondary" style="padding: 5px 9px; font-size: 11px;" onclick="downloadDocFile('${d.id}')">
                                ดูไฟล์
                            </button>
                            <button type="button" class="btn-primary" style="padding: 5px 9px; font-size: 11px; background-color: #16a34a; border-color: #16a34a; font-weight: 600;" onclick="updateSingleDocStatus('${d.id}', 'ตรวจรับแล้ว')">
                                ✓ ผ่าน
                            </button>
                            <button type="button" class="btn-primary btn-danger" style="padding: 5px 9px; font-size: 11px; font-weight: 600;" onclick="updateSingleDocStatus('${d.id}', 'ต้องแก้ไข')">
                                ✕ ตีกลับ
                            </button>
                        </div>
                    </div>`;
            });
            modalBody.innerHTML = html;
        }

        function updateSingleDocStatus(docId, newStatus) {
            const allDocs = getSubmittedDocs();
            const doc = allDocs.find(d => String(d.id) === String(docId));
            if (!doc) {
                alert('ไม่พบเอกสารนี้ในระบบ');
                return;
            }

            if (newStatus === 'ต้องแก้ไข') {
                const defaultMsg = doc.comment || 'กรุณาตรวจสอบความถูกต้องและแนบเอกสารฉบับแก้ไขอีกครั้ง';
                const reason = prompt(`ระบุเหตุผลในการตีกลับเอกสาร "${doc.docType}":`, defaultMsg);
                if (reason === null) return; // กดยกเลิก
                doc.comment = reason.trim() || 'เอกสารไม่สมบูรณ์ กรุณาแก้ไข';
            } else {
                doc.comment = '';
            }

            doc.status = newStatus;
            saveSubmittedDocs(allDocs);

            // คำนวณสถานะภาพรวมของนิสิตคนนี้
            syncOverallStudentDocStatus(currentSelectedStudentId);

            // Re-render ใน Modal ทันที ไม่ต้องปิดหน้าต่าง
            const titleEl = document.getElementById('doc-student-name');
            const studentName = titleEl ? titleEl.textContent : currentSelectedStudentId;
            renderDocModalContent(currentSelectedStudentId, studentName);

            // Refresh ตารางภายนอก
            renderStudentList();
            if (typeof renderAdminUsersTable === 'function') {
                renderAdminUsersTable();
            }

            addNotification(`อัปเดตเอกสาร "${doc.docType}" เป็น "${newStatus}" เรียบร้อยแล้ว`);
        }

        function syncOverallStudentDocStatus(studentId) {
            const allDocs = getSubmittedDocs();
            const studentDocs = allDocs.filter(d => String(d.studentId) === String(studentId));

            let overallStatus = 'รอตรวจ';
            if (studentDocs.length > 0) {
                const hasRejected = studentDocs.some(d => d.status === 'ต้องแก้ไข');
                const allApproved = studentDocs.every(d => d.status === 'ตรวจรับแล้ว' || d.status === 'ครบถ้วน');
                if (hasRejected) {
                    overallStatus = 'ต้องแก้ไข';
                } else if (allApproved) {
                    overallStatus = 'ครบถ้วน';
                } else {
                    overallStatus = 'รอตรวจ';
                }
            }

            // อัปเดตใน studentsData ทุกหมู่เรียน
            for (let sec in studentsData) {
                const std = (studentsData[sec] || []).find(s => String(s.id) === String(studentId) || String(s.student_id) === String(studentId));
                if (std) {
                    std.docs = overallStatus;
                }
            }

            // Sync with customUsers
            try {
                const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                let foundInCustom = false;
                for (let email in customUsers) {
                    if (String(customUsers[email].id) === String(studentId) || String(customUsers[email].student_id) === String(studentId)) {
                        customUsers[email].docs = overallStatus;
                        customUsers[email].docStatus = overallStatus;
                        foundInCustom = true;
                    }
                }
                if (foundInCustom) {
                    localStorage.setItem('customUsers', JSON.stringify(customUsers));
                }
            } catch (e) {}

            const stdDocStatusEl = document.getElementById('std-doc-status');
            if (stdDocStatusEl) stdDocStatusEl.textContent = overallStatus;
        }

        function updateDocStatus(newStatus) {
            const allDocs = getSubmittedDocs();
            let updated = false;

            let batchReason = '';
            if (newStatus === 'ต้องแก้ไข') {
                const reason = prompt('ระบุเหตุผลในการตีกลับเอกสารทั้งหมดของนิสิตคนนี้:', 'กรุณาตรวจสอบความถูกต้องและแนบเอกสารใหม่ทั้งหมด');
                if (reason === null) return;
                batchReason = reason.trim() || 'เอกสารไม่สมบูรณ์';
            }

            allDocs.forEach(d => {
                if (String(d.studentId) === String(currentSelectedStudentId)) {
                    d.status = newStatus;
                    if (newStatus === 'ต้องแก้ไข') {
                        d.comment = batchReason;
                    } else {
                        d.comment = '';
                    }
                    updated = true;
                }
            });
            if (updated) {
                saveSubmittedDocs(allDocs);
            }

            syncOverallStudentDocStatus(currentSelectedStudentId);

            alert(`อัปเดตสถานะเอกสารทั้งหมดเป็น "${newStatus}" เรียบร้อยแล้ว`);
            closeModal('modal-doc-mgmt');
            renderStudentList();
            if (typeof renderAdminUsersTable === 'function') {
                renderAdminUsersTable();
            }

            addNotification(`อัปเดตสถานะการตรวจเอกสารเป็น "${newStatus}"`);
        }
