// ==========================================================================
// navigation.js - ระบบการสลับหน้าและแถบเมนูนำทาง (Navigation & Tabs)
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

function renderTabBar() {
            const container = document.getElementById('tab-bar-container');
            if (!container) return;
            if (currentRole === 'advisor') {
                container.style.gridTemplateColumns = 'repeat(4, 1fr)';
                container.innerHTML = `
                    <div class="tab-item active" id="tab-adv-dash" onclick="navTab('sec-advisor-dash', 'tab-adv-dash')">
                        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
                        <span>ภาพรวม</span>
                    </div>
                    <div class="tab-item" id="tab-adv-class" onclick="navTab('sec-advisor-classroom', 'tab-adv-class')">
                        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                        <span>หมู่เรียน</span>
                    </div>
                    <div class="tab-item" id="tab-adv-cal" onclick="navTab('sec-advisor-calendar', 'tab-adv-cal')">
                        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                        <span>นัดหมาย</span>
                    </div>
                    <div class="tab-item" id="tab-adv-qr" onclick="navTab('sec-advisor-qr', 'tab-adv-qr')">
                        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/></svg>
                        <span>สแกน QR</span>
                    </div>
                `;
            } else if (currentRole === 'student') {
                container.style.gridTemplateColumns = 'repeat(5, 1fr)';
                container.innerHTML = `
                    <div class="tab-item active" id="tab-std-docs" onclick="navTab('sec-student-docs', 'tab-std-docs')">
                        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                        <span>ส่งงาน/เอกสาร</span>
                    </div>
                    <div class="tab-item" id="tab-std-dash" onclick="navTab('sec-student-dash', 'tab-std-dash')">
                        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
                        <span>ภาพรวม</span>
                    </div>
                    <div class="tab-item" id="tab-std-tracking" onclick="navTab('sec-student-tracking', 'tab-std-tracking')">
                        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
                        <span>ติดตามงาน</span>
                    </div>
                    <div class="tab-item" id="tab-std-sch" onclick="navTab('sec-student-schedule', 'tab-std-sch')">
                        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                        <span>ตารางนัดหมาย</span>
                    </div>
                    <div class="tab-item" id="tab-std-qr" onclick="navTab('sec-student-qrcode', 'tab-std-qr')">
                        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><rect x="7" y="7" width="3" height="3"/><rect x="14" y="7" width="3" height="3"/><rect x="7" y="14" width="3" height="3"/></svg>
                        <span>คิวอาร์ประจำตัว</span>
                    </div>
                `;
            } else {
                container.style.gridTemplateColumns = '1fr';
                container.innerHTML = `
                    <div class="tab-item active" style="grid-column: span 4;">
                        <span>โหมดผู้ดูแลระบบ Web Dashboard (ภาพรวมทั้งคณะ)</span>
                    </div>
                `;
            }
        }



        function navTab(pageId, tabId) {
            showPage(pageId);
            document.querySelectorAll('.tab-item').forEach(el => el.classList.remove('active'));
            const activeEl = document.getElementById(tabId);
            if (activeEl) activeEl.classList.add('active');

            if (pageId === 'sec-advisor-classroom') {
                updateAdvisorStats();
                backToClassroomList();
                renderAdvisorAssignments();
            } else if (pageId === 'sec-advisor-calendar' || pageId === 'sec-student-schedule') {
                renderCalendarEvents();
            } else if (pageId === 'sec-student-docs' || pageId === 'sec-student-dash') {
                renderStudentDocsList();
                renderBlankFormsGrid();
                renderStudentClassroomAssignments();
            } else if (pageId === 'sec-student-tracking') {
                const savedSession = (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'));
                if (savedSession) {
                    const u = JSON.parse(savedSession);
                    if (typeof loadStudentProjectTracking === 'function') {
                        loadStudentProjectTracking(String(u.id || u.student_id));
                    }
                }
            }
        }

        function syncSidebarActive(pageId) {
            document.querySelectorAll('.sidebar-nav-item').forEach(el => {
                const onclickStr = el.getAttribute('onclick') || '';
                if (onclickStr.includes(`'${pageId}'`)) {
                    el.classList.add('active');
                    const span = el.querySelector('span');
                    if (span) {
                        const titleEl = document.getElementById('header-role-title');
                        if (titleEl) titleEl.textContent = span.textContent;
                    }
                } else {
                    el.classList.remove('active');
                }
            });
        }

        function showPage(pageId, keepExistingActive = false) {
            document.querySelectorAll('.page-content').forEach(el => el.classList.remove('active'));
            const target = document.getElementById(pageId);
            if (target) target.classList.add('active');
            if (!keepExistingActive) {
                syncSidebarActive(pageId);
            }
            if (pageId === 'sec-student-tracking') {
                const savedSession = (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'));
                if (savedSession) {
                    const u = JSON.parse(savedSession);
                    if (typeof loadStudentProjectTracking === 'function') {
                        loadStudentProjectTracking(String(u.id || u.student_id));
                    }
                }
            }
            if (pageId === 'sec-advisor-photos') {
                if (typeof renderAdvisorPhotosPage === 'function') {
                    renderAdvisorPhotosPage();
                }
            }
            if (pageId === 'sec-advisor-assignments') {
                if (typeof renderAdvisorAssignments === 'function') {
                    renderAdvisorAssignments();
                }
            }
        }



        function handleHeaderBack() {
            const detailView = document.getElementById('advisor-classroom-detail-view');
            if (detailView && detailView.style.display !== 'none') {
                backToClassroomList();
                return;
            }

            if (currentRole === 'advisor') {
                navTab('sec-advisor-dash', 'tab-adv-dash');
            } else if (currentRole === 'student') {
                navTab('sec-student-docs', 'tab-std-docs');
            } else if (currentRole === 'admin') {
                showPage('sec-admin-dash');
            }
        }

        // ----------------------------------------------------
        // ADVISOR SEMESTER & CLASSROOM TAB STATE
        // ----------------------------------------------------
        let advisorSelectedSemester = 'ภาคต้น 2569';
        let currentAdvisorClassroomTab = 'students';
        let currentActiveSubmitterTab = 'submitted';
        let currentViewingAssignmentId = null;
        let advisorStudentSearchQuery = '';



        function toggleSidebar(forceState) {
            const sidebar = document.getElementById('desktop-sidebar');
            const backdrop = document.getElementById('sidebar-backdrop');
            if (!sidebar) return;

            const isMobile = window.innerWidth <= 768;

            if (isMobile) {
                if (typeof forceState === 'boolean') {
                    if (forceState) {
                        sidebar.classList.add('mobile-open');
                        if (backdrop) backdrop.classList.add('active');
                    } else {
                        sidebar.classList.remove('mobile-open');
                        if (backdrop) backdrop.classList.remove('active');
                    }
                } else {
                    const isOpen = sidebar.classList.toggle('mobile-open');
                    if (backdrop) backdrop.classList.toggle('active', isOpen);
                }
            } else {
                if (typeof forceState === 'boolean') {
                    sidebar.classList.toggle('collapsed', !forceState);
                } else {
                    sidebar.classList.toggle('collapsed');
                }
            }
        }



        function buildSidebarNav(role) {
            const container = document.getElementById('sidebar-nav-container');
            if (!container) return;

            const navsByRole = {
                advisor: [
                    { label: 'ภาพรวม', items: [
                        { id: 'sec-advisor-dash', page: 'sec-advisor-dash', text: 'แดชบอร์ดภาพรวม', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>' },
                    ]},
                    { label: 'จัดการนิสิต', items: [
                        { id: 'sec-advisor-classroom', page: 'sec-advisor-classroom', text: 'หมู่เรียน / เอกสาร', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>' },
                        { id: 'sec-advisor-calendar', page: 'sec-advisor-calendar', text: 'ปฏิทินนัดหมาย', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>' },
                        { id: 'sec-advisor-qr', page: 'sec-advisor-qr', text: 'GPS Check-in / QR', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>' },
                    ]},
                    { label: 'กำหนดส่งเอกสาร', items: [
                        { id: 'sec-advisor-assignments', page: 'sec-advisor-assignments', text: 'กำหนดส่งเอกสาร', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>' },
                    ]},
                    { label: 'หลักฐานการนิเทศ', items: [
                        { id: 'sec-advisor-photos', page: 'sec-advisor-photos', text: 'หลักฐานการนิเทศ', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>' },
                    ]},
                ],
                student: [
                    { label: 'สหกิจศึกษา', items: [
                        { id: 'sec-student-docs', page: 'sec-student-docs', text: 'ส่งงาน / เอกสารที่สั่ง', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>' },
                        { id: 'sec-student-dash', page: 'sec-student-dash', text: 'ภาพรวมนิสิต', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>' },
                        { id: 'sec-student-tracking', page: 'sec-student-tracking', text: 'ติดตามงาน', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>' },
                        { id: 'sec-student-schedule', page: 'sec-student-schedule', text: 'ตารางนัดหมาย', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>' },
                        { id: 'sec-student-qrcode', page: 'sec-student-qrcode', text: 'QR Code ประจำตัว', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"></rect><rect x="7" y="7" width="3" height="3"></rect><rect x="14" y="7" width="3" height="3"></rect><rect x="7" y="14" width="3" height="3"></rect></svg>' },
                    ]},
                ],
                admin: [
                    { label: 'ภาพรวมระบบ', items: [
                        { id: 'admin-card-overview', page: 'sec-admin-dash', text: 'แดชบอร์ดสถิติภาพรวม', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>' },
                        { id: 'admin-card-users', page: 'sec-admin-dash', text: 'จัดการนิสิต & อาจารย์', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>' },
                    ]},
                    { label: 'เครื่องมือแอดมิน', items: [
                        { id: 'admin-card-import', page: 'sec-admin-dash', text: 'นำเข้าข้อมูล Excel', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="12" y1="18" x2="12" y2="12"></line><line x1="9" y1="15" x2="15" y2="15"></line></svg>' },
                    ]},
                ]
            };

            const groups = navsByRole[role] || navsByRole['advisor'];
            let html = '';
            groups.forEach(group => {
                group.items.forEach(item => {
                    html += `<button class="sidebar-nav-item" title="${item.text}" onclick="sidebarNavigate('${item.id}', '${item.page}', this)">${item.icon}<span>${item.text}</span></button>`;
                });
            });
            container.innerHTML = html;

            // Set first item as active
            const firstBtn = container.querySelector('.sidebar-nav-item');
            if (firstBtn) firstBtn.classList.add('active');
        }

        function sidebarNavigate(targetId, pageId, btn) {
            if (window.innerWidth <= 768) {
                toggleSidebar(false);
            }
            if (targetId !== 'sec-advisor-qr' && pageId !== 'sec-advisor-qr') {
                stopRealCameraScanner();
            }
            // Update active state in sidebar
            document.querySelectorAll('.sidebar-nav-item').forEach(el => el.classList.remove('active'));
            if (btn) btn.classList.add('active');

            // Update header title
            const titleEl = btn ? btn.querySelector('span') : null;
            if (titleEl) {
                document.getElementById('header-role-title').textContent = titleEl.textContent;
            }

            // Determine page to show
            const actualPageId = pageId || targetId;
            showPage(actualPageId, true);

            // Trigger renders for dynamic pages
            if (actualPageId === 'sec-advisor-assignments') {
                setTimeout(() => { renderAdvisorAssignments(); }, 50);
            }
            if (actualPageId === 'sec-advisor-photos') {
                setTimeout(() => { renderAdvisorPhotosPage(); }, 50);
            }

            // If navigating within a page (e.g. admin cards), smoothly scroll to that element
            if (targetId && targetId !== actualPageId) {
                const targetEl = document.getElementById(targetId);
                if (targetEl) {
                    targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }

            // Also trigger role-specific views if needed
            if (actualPageId === 'sec-advisor-classroom') {
                updateAdvisorStats();
                backToClassroomList();
                renderAdvisorAssignments();
            } else if (actualPageId === 'sec-advisor-calendar') {
                renderCalendarEvents();
            } else if (actualPageId === 'sec-student-docs') {
                renderStudentDocsList();
                renderBlankFormsGrid();
                renderStudentClassroomAssignments();
            } else if (actualPageId === 'sec-student-schedule') {
                renderCalendarEvents();
            } else if (actualPageId === 'sec-admin-dash') {
                updateAdvisorStats();
                renderAdminUsersTable();
                renderAdminGpsSection();
            }
        }

        // ------------------ Project Tracking & Map ------------------
        let currentTrackingStudentId = null;
