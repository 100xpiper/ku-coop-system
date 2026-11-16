// ==========================================================================
// advisor-dashboard.js - ระบบแดชบอร์ดภาพรวมและสถิตินิเทศงานของอาจารย์
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

function updateAdvisorStats() {
            loadDynamicStudentsData();
            const raw700 = ['หมู่ 700', 'หมู่ 701', 'หมู่ 702'].flatMap(sec => studentsData[sec] || []);
            const raw800 = ['หมู่ 800', 'หมู่ 801', 'หมู่ 802'].flatMap(sec => studentsData[sec] || []);

            // Admin filtered by semester
            let adminList700 = raw700;
            let adminList800 = raw800;
            if (adminSelectedSemester && adminSelectedSemester !== 'all') {
                if (adminSelectedSemester === 'all_2569') {
                    adminList700 = adminList700.filter(s => (s.semester || 'ภาคต้น 2569').includes('2569'));
                    adminList800 = adminList800.filter(s => (s.semester || 'ภาคต้น 2569').includes('2569'));
                } else {
                    adminList700 = adminList700.filter(s => (s.semester || 'ภาคต้น 2569') === adminSelectedSemester);
                    adminList800 = adminList800.filter(s => (s.semester || 'ภาคต้น 2569') === adminSelectedSemester);
                }
            }
            const adminTotal = adminList700.length + adminList800.length;

            const adminTotalEl = document.getElementById('admin-total-std');
            if (adminTotalEl) adminTotalEl.textContent = `${adminTotal} คน`;

            if (document.getElementById('admin-total-700')) document.getElementById('admin-total-700').textContent = `${adminList700.length} คน`;
            if (document.getElementById('admin-total-800')) document.getElementById('admin-total-800').textContent = `${adminList800.length} คน`;

            const overviewSel = document.getElementById('admin-overview-semester-select');
            if (overviewSel && adminSelectedSemester) {
                overviewSel.value = adminSelectedSemester;
            }

            // Identify logged in user & Advisor's specific sections
            const { mySecNormal, mySecSpecial, loggedInUser } = getAdvisorSections();

            // Advisor's classroom lists
            const rawMyNorm = studentsData[mySecNormal] || [];
            const rawMySpec = studentsData[mySecSpecial] || [];

            let listNorm = rawMyNorm;
            let listSpec = rawMySpec;
            if (advisorSelectedSemester && advisorSelectedSemester !== 'all') {
                listNorm = listNorm.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
                listSpec = listSpec.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
            }

            const total = listNorm.length + listSpec.length;
            const evalNorm = listNorm.filter(s => s.status === 'นิเทศแล้ว').length;
            const evalSpec = listSpec.filter(s => s.status === 'นิเทศแล้ว').length;
            const evalCount = evalNorm + evalSpec;
            const pendingCount = total - evalCount;

            const statTotal = document.getElementById('stat-total-count');
            if (statTotal) statTotal.textContent = `${total} คน`;
            const statEval = document.getElementById('stat-evaluated-count');
            if (statEval) statEval.textContent = `${evalCount} คน`;
            const statPending = document.getElementById('stat-pending-count');
            if (statPending) statPending.textContent = `${pendingCount} คน`;

            const normNum = mySecNormal.replace(/[^0-9]/g, '');
            const specNum = mySecSpecial.replace(/[^0-9]/g, '');
            const secNormText = `จำนวนนิสิต: ${listNorm.length} คน | นิเทศแล้ว: ${evalNorm} คน`;
            const secSpecText = `จำนวนนิสิต: ${listSpec.length} คน | นิเทศแล้ว: ${evalSpec} คน`;

            // Dynamically render or update classroom cards
            const dashClassList = document.getElementById('adv-dash-classroom-list');
            if (dashClassList) {
                dashClassList.innerHTML = `
                    <div class="classroom-item" onclick="openClassroomDetail('${mySecNormal}')" style="cursor: pointer;">
                        <div>
                            <div style="font-size: 13px; font-weight: 700; color: var(--primary-color);">หมู่เรียน ${normNum}</div>
                            <div style="font-size: 11px; color: var(--text-muted);">${secNormText}</div>
                        </div>
                        <span class="status-badge badge-success">จัดการ ></span>
                    </div>
                    <div class="classroom-item" onclick="openClassroomDetail('${mySecSpecial}')" style="cursor: pointer;">
                        <div>
                            <div style="font-size: 13px; font-weight: 700; color: var(--primary-color);">หมู่เรียน ${specNum}</div>
                            <div style="font-size: 11px; color: var(--text-muted);">${secSpecText}</div>
                        </div>
                        <span class="status-badge badge-success">จัดการ ></span>
                    </div>
                `;
            }

            const tabClassList = document.getElementById('adv-tab-classroom-list');
            if (tabClassList) {
                tabClassList.innerHTML = `
                    <div class="classroom-item" onclick="openClassroomDetail('${mySecNormal}')" style="cursor: pointer;">
                        <div>
                            <div style="font-size: 13px; font-weight: 700; color: var(--primary-color);">หมู่เรียน ${normNum}</div>
                            <div style="font-size: 11px; color: var(--text-muted);">${secNormText}</div>
                        </div>
                        <span class="status-badge badge-success">เข้าจัดการ ></span>
                    </div>
                    <div class="classroom-item" onclick="openClassroomDetail('${mySecSpecial}')" style="cursor: pointer;">
                        <div>
                            <div style="font-size: 13px; font-weight: 700; color: var(--primary-color);">หมู่เรียน ${specNum}</div>
                            <div style="font-size: 11px; color: var(--text-muted);">${secSpecText}</div>
                        </div>
                        <span class="status-badge badge-success">เข้าจัดการ ></span>
                    </div>
                `;
            }

            // Sync semester selects
            const dashSel = document.getElementById('adv-semester-dash-select');
            if (dashSel) dashSel.value = advisorSelectedSemester;
            const tabSel = document.getElementById('adv-semester-select-tab');
            if (tabSel) tabSel.value = advisorSelectedSemester;
            const classSel = document.getElementById('adv-classroom-semester-select');
            if (classSel) classSel.value = advisorSelectedSemester;

            // Populate student dropdown in appointment form & QR checkin (Separated & Grouped by Section)
            populateAdvisorStudentSelects(listNorm, listSpec, mySecNormal, mySecSpecial);

            // Render the advisor's 2-section document overview
            if (typeof renderAdvisorDocOverview === 'function') {
                renderAdvisorDocOverview();
            }
        }

        let currentCalSectionFilter = 'all';
        let currentQrSectionFilter = 'all';



        function switchAdvisorDocOverviewTab(tab) {
            currentAdvisorDocOverviewTab = tab;
            const btnSummary = document.getElementById('adv-doc-tab-summary-btn');
            const btnMatrix = document.getElementById('adv-doc-tab-matrix-btn');
            const viewSummary = document.getElementById('adv-doc-summary-view');
            const viewMatrix = document.getElementById('adv-doc-matrix-view');

            if (tab === 'summary') {
                if (btnSummary) {
                    btnSummary.style.background = '#ffffff';
                    btnSummary.style.color = 'var(--primary-color)';
                    btnSummary.style.fontWeight = '700';
                    btnSummary.style.boxShadow = '0 1px 2px rgba(0,0,0,0.05)';
                }
                if (btnMatrix) {
                    btnMatrix.style.background = 'transparent';
                    btnMatrix.style.color = '#64748b';
                    btnMatrix.style.fontWeight = '600';
                    btnMatrix.style.boxShadow = 'none';
                }
                if (viewSummary) viewSummary.style.display = 'block';
                if (viewMatrix) viewMatrix.style.display = 'none';
                renderAdvisorDocOverview();
            } else {
                if (btnSummary) {
                    btnSummary.style.background = 'transparent';
                    btnSummary.style.color = '#64748b';
                    btnSummary.style.fontWeight = '600';
                    btnSummary.style.boxShadow = 'none';
                }
                if (btnMatrix) {
                    btnMatrix.style.background = '#ffffff';
                    btnMatrix.style.color = 'var(--primary-color)';
                    btnMatrix.style.fontWeight = '700';
                    btnMatrix.style.boxShadow = '0 1px 2px rgba(0,0,0,0.05)';
                }
                if (viewSummary) viewSummary.style.display = 'none';
                if (viewMatrix) viewMatrix.style.display = 'block';
                renderAdvisorDocMatrixTable();
            }
        }

        function setAdvisorDocSectionFilter(filter) {
            currentAdvisorDocSectionFilter = filter;
            const btnAll = document.getElementById('adv-doc-sec-filter-all');
            const btnNorm = document.getElementById('adv-doc-sec-filter-norm');
            const btnSpec = document.getElementById('adv-doc-sec-filter-spec');

            [btnAll, btnNorm, btnSpec].forEach(btn => {
                if (btn) {
                    btn.style.background = '#ffffff';
                    btn.style.color = '#475569';
                    btn.style.borderColor = 'var(--border-color)';
                }
            });

            const activeBtn = filter === 'normal' ? btnNorm : (filter === 'special' ? btnSpec : btnAll);
            if (activeBtn) {
                activeBtn.style.background = 'var(--primary-color)';
                activeBtn.style.color = '#ffffff';
                activeBtn.style.borderColor = 'var(--primary-color)';
            }

            renderAdvisorDocOverview();
        }

        function renderAdvisorDocOverview() {
            const container = document.getElementById('adv-doc-summary-cards-container');
            if (!container) return;

            loadDynamicStudentsData();
            const { mySecNormal, mySecSpecial, loggedInUser } = getAdvisorSections();
            const allAsgs = getCoopAssignments();
            const allDocs = getSubmittedDocs();

            let normStds = studentsData[mySecNormal] || [];
            let specStds = studentsData[mySecSpecial] || [];

            if (advisorSelectedSemester && advisorSelectedSemester !== 'all') {
                normStds = normStds.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
                specStds = specStds.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
            }

            // Update Section Filter Buttons label with section names & counts
            const btnNorm = document.getElementById('adv-doc-sec-filter-norm');
            if (btnNorm) btnNorm.textContent = `${mySecNormal} (${normStds.length})`;
            const btnSpec = document.getElementById('adv-doc-sec-filter-spec');
            if (btnSpec) btnSpec.textContent = `${mySecSpecial} (${specStds.length})`;
            const btnAll = document.getElementById('adv-doc-sec-filter-all');
            if (btnAll) btnAll.textContent = `ทั้ง 2 หมู่เรียน (${normStds.length + specStds.length})`;

            // Active list based on filter
            let activeStds = [];
            if (currentAdvisorDocSectionFilter === 'normal') {
                activeStds = normStds;
            } else if (currentAdvisorDocSectionFilter === 'special') {
                activeStds = specStds;
            } else {
                activeStds = [...normStds, ...specStds];
            }

            const totalStudents = activeStds.length;
            const subtitleEl = document.getElementById('adv-doc-overview-subtitle');
            if (subtitleEl) {
                const semText = advisorSelectedSemester === 'all' ? 'ทุกภาคการศึกษา' : (advisorSelectedSemester || 'ภาคต้น 2569');
                const filterDesc = currentAdvisorDocSectionFilter === 'normal' ? ` (${mySecNormal})` : (currentAdvisorDocSectionFilter === 'special' ? ` (${mySecSpecial})` : '');
                subtitleEl.textContent = `อาจารย์: ${loggedInUser ? loggedInUser.name : 'อาจารย์'} | ดูแล ${mySecNormal} และ ${mySecSpecial} | ภาคการศึกษา: ${semText} (นิสิต ${totalStudents} คน${filterDesc})`;
            }

            // Calculate total submissions across all assignments
            const totalRequiredSubmissions = totalStudents * allAsgs.length;
            let actualSubmissions = 0;

            allAsgs.forEach(asg => {
                activeStds.forEach(std => {
                    const hasSubmitted = allDocs.some(d => 
                        (String(d.studentId) === String(std.id) || (std.email && d.email === std.email)) &&
                        (d.docType === asg.docType || d.docType === asg.title)
                    );
                    if (hasSubmitted) actualSubmissions++;
                });
            });

            const overallPercent = totalRequiredSubmissions > 0 ? Math.round((actualSubmissions / totalRequiredSubmissions) * 100) : 0;
            const overallStatPill = document.getElementById('adv-doc-overall-stat-pill');
            if (overallStatPill) {
                overallStatPill.innerHTML = `ภาพรวมการส่งเอกสาร: <strong style="color: #047857;">${actualSubmissions}/${totalRequiredSubmissions} รายการ</strong> (${overallPercent}%)`;
            }

            container.innerHTML = '';
            if (totalStudents === 0) {
                container.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; color: var(--text-muted); font-size: 12px; padding: 32px; background: #f8fafc; border-radius: 8px; border: 1px dashed var(--border-color);">
                        ไม่มีข้อมูลนิสิตใน ${currentAdvisorDocSectionFilter === 'normal' ? mySecNormal : (currentAdvisorDocSectionFilter === 'special' ? mySecSpecial : '2 หมู่เรียนนี้')} สำหรับภาคการศึกษาที่เลือก
                    </div>`;
                renderAdvisorDocMatrixTable();
                return;
            }

            allAsgs.forEach((asg, index) => {
                // Count submitted, approved, pending for active students
                let submittedCount = 0;
                let approvedCount = 0;
                let pendingCount = 0;

                // Also count by normal and special for breakdown
                let normSubCount = 0;
                let specSubCount = 0;

                normStds.forEach(std => {
                    const hasSubmitted = allDocs.some(d => 
                        (String(d.studentId) === String(std.id) || (std.email && d.email === std.email)) &&
                        (d.docType === asg.docType || d.docType === asg.title)
                    );
                    if (hasSubmitted) normSubCount++;
                });

                specStds.forEach(std => {
                    const hasSubmitted = allDocs.some(d => 
                        (String(d.studentId) === String(std.id) || (std.email && d.email === std.email)) &&
                        (d.docType === asg.docType || d.docType === asg.title)
                    );
                    if (hasSubmitted) specSubCount++;
                });

                activeStds.forEach(std => {
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

                const badgeBg = percent === 100 ? '#dcfce7' : (percent >= 50 ? '#dbeafe' : '#fef3c7');
                const badgeColor = percent === 100 ? '#15803d' : (percent >= 50 ? '#1e40af' : '#b45309');
                const progressBarColor = percent === 100 ? 'linear-gradient(90deg, #10b981, #059669)' : (percent >= 50 ? 'linear-gradient(90deg, #3b82f6, #2563eb)' : 'linear-gradient(90deg, #f59e0b, #d97706)');

                let dueFormatted = asg.dueDate || '-';
                if (asg.dueDate) {
                    try {
                        const d = new Date(asg.dueDate);
                        dueFormatted = d.toLocaleDateString('th-TH', { day: 'numeric', month: 'short', year: '2-digit' });
                    } catch (e) {}
                }

                let docCode = `Doc ${index + 1}`;
                if (asg.title.includes('สัดส่วนการทำงานร่วมกัน')) docCode = 'คู-01 (สัดส่วนงาน)';
                else if (asg.title.includes('Form 02')) docCode = 'Form 02 (นิเทศ)';
                else if (asg.title.includes('Form 04')) docCode = 'Form 04 (ที่พัก)';
                else if (asg.title.includes('Form 05')) docCode = 'Form 05 (ตำแหน่ง/Mentor)';
                else if (asg.title.includes('Form 06')) docCode = 'Form 06 (Weekly)';
                else if (asg.title.includes('Form 11')) docCode = 'Form 11 (Final)';

                const card = document.createElement('div');
                card.style.background = '#ffffff';
                card.style.border = '1px solid var(--border-color)';
                card.style.borderRadius = '10px';
                card.style.padding = '14px 16px';
                card.style.boxShadow = '0 1px 3px rgba(0,0,0,0.03)';
                card.style.display = 'flex';
                card.style.flexDirection = 'column';
                card.style.justifyContent = 'space-between';
                card.style.transition = 'transform 0.15s ease, box-shadow 0.15s ease';
                card.onmouseenter = () => { card.style.transform = 'translateY(-2px)'; card.style.boxShadow = '0 4px 12px rgba(0,0,0,0.06)'; };
                card.onmouseleave = () => { card.style.transform = 'translateY(0)'; card.style.boxShadow = '0 1px 3px rgba(0,0,0,0.03)'; };

                card.innerHTML = `
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 8px;">
                            <span style="font-size: 10.5px; font-weight: 700; padding: 2px 8px; border-radius: 4px; background: ${badgeBg}; color: ${badgeColor};">
                                ${docCode}
                            </span>
                            <span style="font-size: 10.5px; color: #64748b; display: flex; align-items: center; gap: 3px;">
                                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                                ส่งภายใน: ${dueFormatted}
                            </span>
                        </div>

                        <div style="font-size: 12.5px; font-weight: 700; color: #1e293b; line-height: 1.35; margin-bottom: 10px; min-height: 34px;">
                            ${asg.title}
                        </div>

                        <!-- Progress Bar & Count -->
                        <div style="margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
                                <span style="font-size: 12px; font-weight: 700; color: #0f172a;">
                                    ส่งแล้ว <strong style="color: #047857; font-size: 14px;">${submittedCount}</strong> / ${totalStudents} คน
                                </span>
                                <span style="font-size: 12px; font-weight: 700; color: ${percent === 100 ? '#10b981' : '#2563eb'};">
                                    ${percent}%
                                </span>
                            </div>
                            <div style="width: 100%; height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden;">
                                <div style="width: ${percent}%; height: 100%; background: ${progressBarColor}; transition: width 0.4s ease; border-radius: 4px;"></div>
                            </div>
                        </div>

                        <!-- Pill Details -->
                        <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; font-size: 10.5px;">
                            <span style="background: #f0fdf4; color: #166534; padding: 2px 7px; border-radius: 4px; border: 1px solid #bbf7d0;">
                                ตรวจรับแล้ว: <strong>${approvedCount}</strong>
                            </span>
                            <span style="background: #fffbeb; color: #92400e; padding: 2px 7px; border-radius: 4px; border: 1px solid #fde68a;">
                                รอตรวจ: <strong>${pendingCount}</strong>
                            </span>
                            <span style="background: #fef2f2; color: #991b1b; padding: 2px 7px; border-radius: 4px; border: 1px solid #fecaca;">
                                ยังไม่ส่ง: <strong>${unsubmittedCount}</strong>
                            </span>
                        </div>

                        <!-- Breakdown by Selected Section or Both -->
                        ${currentAdvisorDocSectionFilter === 'normal' ? `
                            <div style="padding: 6px 10px; background: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 10.5px; color: #64748b; margin-bottom: 12px; display: flex; justify-content: flex-start; align-items: center;">
                                <span>${mySecNormal}: <strong style="color: #1e40af;">${normSubCount}/${normStds.length}</strong></span>
                            </div>
                        ` : (currentAdvisorDocSectionFilter === 'special' ? `
                            <div style="padding: 6px 10px; background: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 10.5px; color: #64748b; margin-bottom: 12px; display: flex; justify-content: flex-start; align-items: center;">
                                <span>${mySecSpecial}: <strong style="color: #0d9488;">${specSubCount}/${specStds.length}</strong></span>
                            </div>
                        ` : `
                            <div style="padding: 6px 10px; background: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 10.5px; color: #64748b; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                                <span>${mySecNormal}: <strong style="color: #1e40af;">${normSubCount}/${normStds.length}</strong></span>
                                <span style="color: #cbd5e1;">|</span>
                                <span>${mySecSpecial}: <strong style="color: #0d9488;">${specSubCount}/${specStds.length}</strong></span>
                            </div>
                        `)}
                    </div>

                    <!-- Action Button -->
                    <button type="button" class="btn-primary" onclick="openAssignmentSubmittersModal('${asg.id}', '${currentAdvisorDocSectionFilter === 'normal' ? mySecNormal : (currentAdvisorDocSectionFilter === 'special' ? mySecSpecial : 'all_my_sections')}')" style="width: 100%; padding: 7px 12px; font-size: 11px; background: #1e40af; display: flex; align-items: center; justify-content: center; gap: 6px; border-radius: 6px; cursor: pointer;">
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                        <span>ดูรายชื่อนิสิต / ตรวจเอกสาร (${submittedCount}/${totalStudents})</span>
                    </button>
                `;
                container.appendChild(card);
            });

            // Also refresh matrix table
            renderAdvisorDocMatrixTable();
        }

        function renderAdvisorDocMatrixTable() {
            const tbody = document.getElementById('adv-doc-matrix-tbody');
            if (!tbody) return;
            tbody.innerHTML = '';

            loadDynamicStudentsData();
            const { mySecNormal, mySecSpecial } = getAdvisorSections();
            const allAsgs = getCoopAssignments();
            const allDocs = getSubmittedDocs();

            let normStds = studentsData[mySecNormal] || [];
            let specStds = studentsData[mySecSpecial] || [];

            if (advisorSelectedSemester && advisorSelectedSemester !== 'all') {
                normStds = normStds.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
                specStds = specStds.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
            }

            let stdList = [];
            if (currentAdvisorDocSectionFilter === 'normal') {
                stdList = normStds;
            } else if (currentAdvisorDocSectionFilter === 'special') {
                stdList = specStds;
            } else {
                stdList = [...normStds, ...specStds];
            }

            // Search filter
            const searchInput = document.getElementById('adv-doc-matrix-search');
            const searchVal = searchInput ? searchInput.value.trim().toLowerCase() : '';
            if (searchVal) {
                stdList = stdList.filter(s => 
                    (s.id && s.id.toLowerCase().includes(searchVal)) ||
                    (s.name && s.name.toLowerCase().includes(searchVal)) ||
                    (s.company && s.company.toLowerCase().includes(searchVal)) ||
                    (s.company_name && s.company_name.toLowerCase().includes(searchVal)) ||
                    (s.section && s.section.toLowerCase().includes(searchVal))
                );
            }

            const footer = document.getElementById('adv-doc-matrix-footer');
            if (footer) {
                const secDesc = currentAdvisorDocSectionFilter === 'normal' ? mySecNormal : (currentAdvisorDocSectionFilter === 'special' ? mySecSpecial : 'ทั้ง 2 หมู่เรียน');
                footer.innerHTML = `<span>แสดงนิสิต: <strong>${stdList.length} คน</strong> จาก${secDesc}</span>`;
            }

            if (stdList.length === 0) {
                tbody.innerHTML = `<tr><td colspan="11" style="text-align: center; color: var(--text-muted); padding: 24px; font-size: 11.5px;">ไม่พบนิสิตตรงตามเงื่อนไขการค้นหา</td></tr>`;
                return;
            }

            stdList.forEach(std => {
                let submittedCount = 0;
                const docStatusCells = allAsgs.map(asg => {
                    const matchDocs = allDocs.filter(d => 
                        (String(d.studentId) === String(std.id) || (std.email && d.email === std.email)) &&
                        (d.docType === asg.docType || d.docType === asg.title)
                    );
                    if (matchDocs.length > 0) {
                        submittedCount++;
                        const doc = matchDocs[0];
                        const isApproved = doc.status === 'ครบถ้วน' || doc.status === 'ตรวจรับแล้ว';
                        if (isApproved) {
                            return `<td style="padding: 8px; text-align: center;">
                                <span title="ตรวจรับแล้ว (${doc.docType})" onclick="openAssignmentSubmittersModal('${asg.id}', 'all_my_sections')" style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; background: #dcfce7; color: #15803d; font-size: 12px; font-weight: bold; cursor: pointer;"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
                            </td>`;
                        } else {
                            return `<td style="padding: 8px; text-align: center;">
                                <span title="ส่งแล้ว - รอตรวจ (${doc.docType})" onclick="openAssignmentSubmittersModal('${asg.id}', 'all_my_sections')" style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; background: #fef3c7; color: #b45309; font-size: 11px; font-weight: bold; cursor: pointer;"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg></span>
                            </td>`;
                        }
                    } else {
                        return `<td style="padding: 8px; text-align: center;">
                            <span title="ยังไม่ส่ง (${asg.title})" style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; background: #f1f5f9; color: #94a3b8; font-size: 12px; font-weight: bold;">—</span>
                        </td>`;
                    }
                }).join('');

                const isAll = submittedCount === allAsgs.length;
                const compName = std.company_name || std.company || '-';
                const secBadgeColor = (std.section || '').includes('80') ? 'background: #ccfbf1; color: #0f766e;' : 'background: #dbeafe; color: #1e40af;';

                const tr = document.createElement('tr');
                tr.style.borderBottom = '1px solid var(--border-color)';
                tr.innerHTML = `
                    <td style="padding: 10px 12px; font-weight: 700; color: #1e3a8a; white-space: nowrap;">${std.id}</td>
                    <td style="padding: 10px 12px; font-weight: 600; color: var(--text-main); white-space: nowrap;">${std.name}</td>
                    <td style="padding: 10px 12px; white-space: nowrap;">
                        <span class="status-badge" style="${secBadgeColor} font-size: 10.5px;">${cleanSectionName(std.section) || '-'}</span>
                    </td>
                    <td style="padding: 10px 12px; color: #475569; font-size: 11px; max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${compName}">
                        ${compName}
                    </td>
                    ${docStatusCells}
                    <td style="padding: 10px 12px; text-align: center; white-space: nowrap;">
                        <span class="status-badge ${isAll ? 'badge-success' : (submittedCount > 0 ? 'badge-warning' : 'badge-danger')}" style="font-weight: 700;">
                            ${submittedCount}/${allAsgs.length} ฉบับ
                        </span>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }



        function openMapForStudent(stdId) {
            // ค้นหาจาก studentsData ก่อน
            const allStds = getAllSystemStudents();
            let std = allStds.find(s => String(s.id) === String(stdId) || String(s.student_id) === String(stdId));

            // Fallback: ค้นหาจาก customUsers (localStorage) ซึ่งนำเข้าจาก Excel
            if (!std || (!std.company_lat && !std.company_lng)) {
                const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                const userEntry = Object.values(customUsers).find(u =>
                    String(u.student_id || u.id) === String(stdId)
                );
                if (userEntry) std = userEntry;
            }

            if (std && std.company_lat && std.company_lng) {
                const lat = std.company_lat;
                const lng = std.company_lng;
                const name = encodeURIComponent(std.company_name || std.company || 'สถานประกอบการ');
                const url = `https://www.google.com/maps/search/?api=1&query=${lat},${lng}&query_place_id=${name}`;
                window.open(url, '_blank');
            } else if (std && std.company_name) {
                // ถ้าไม่มีพิกัดแต่มีชื่อสถานประกอบการ ให้ค้นหาด้วยชื่อแทน
                const name = encodeURIComponent(std.company_name || std.company);
                const url = `https://www.google.com/maps/search/?api=1&query=${name}`;
                window.open(url, '_blank');
            } else {
                alert('ไม่พบพิกัดสถานประกอบการ กรุณาตรวจสอบว่าไฟล์ Excel มีคอลัมน์ "พิกัด" รูปแบบ "14.076, 100.601" หรือไม่');
            }
        }

        // --- Notification & Student Project Tracking Logic ---
