// ==========================================================================
// auth.js - ระบบตรวจสอบสิทธิ์และจัดการ Session ผู้ใช้ (Authentication)
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

var currentRole = 'admin'; // default: admin, advisor, student
var currentSelectedClassroom = 'หมู่ 700';
var currentSelectedStudentId = null;

let studentsData = {
    'หมู่ 700': [],
    'หมู่ 800': [],
    'หมู่ 701': [],
    'หมู่ 801': [],
    'หมู่ 702': [],
    'หมู่ 802': []
};

let notifications = [];

        async function syncDatabaseUsers() {
            ensureSeedUsers();
            if (typeof supabaseClient !== 'undefined' && supabaseClient) {
                try {
                    const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                    // Sync real students from Supabase
                    const { data: stds, error: sErr } = await supabaseClient.from('students').select('*');
                    if (!sErr && stds && stds.length > 0) {
                        stds.forEach(s => {
                            if (!customUsers[s.email]) {
                                customUsers[s.email] = {
                                    id: s.student_id,
                                    student_id: s.student_id,
                                    name: s.full_name,
                                    email: s.email,
                                    role: 'student',
                                    section: s.section,
                                    company_name: s.company_name,
                                    docs: s.doc_status || 'รอตรวจ',
                                    status: s.supervision_status || 'รอนิเทศ',
                                    photo: s.photo_url || ''
                                };
                            }
                        });
                    }
                    // Sync real advisors from Supabase
                    const { data: advs, error: aErr } = await supabaseClient.from('advisors').select('*');
                    if (!aErr && advs && advs.length > 0) {
                        advs.forEach(a => {
                            if (!customUsers[a.email]) {
                                customUsers[a.email] = {
                                    id: a.advisor_id,
                                    advisor_id: a.advisor_id,
                                    name: a.full_name,
                                    email: a.email,
                                    role: 'advisor',
                                    section: a.section
                                };
                            }
                        });
                    }
                    localStorage.setItem('customUsers', JSON.stringify(customUsers));
                } catch (e) {
                    console.warn("Database sync notice:", e);
                }
            }
        }

        function loadDynamicStudentsData() {
            ensureSeedUsers();
            let customUsersObj = {};
            try {
                customUsersObj = JSON.parse(localStorage.getItem('customUsers') || '{}');
                // กรองและล้างข้อมูลแคชเก่าที่ไม่ตรงกับฐานข้อมูลจริง
                let hasOutdatedData = false;
                const outdatedKeys = [
                    'somsak.r@ku.th', '64010101', 
                    'taweesak.c@ku.th', '64010103',
                    'poravee.w@ku.th', '1235'
                ];
                outdatedKeys.forEach(k => {
                    if (customUsersObj[k]) {
                        delete customUsersObj[k];
                        hasOutdatedData = true;
                    }
                });

                if (hasOutdatedData) {
                    localStorage.setItem('customUsers', JSON.stringify(customUsersObj));
                }
            } catch (e) {}

            const customUsers = customUsersObj;
            studentsData = { 
                'หมู่ 700': [], 
                'หมู่ 800': [],
                'หมู่ 701': [],
                'หมู่ 801': [],
                'หมู่ 702': [],
                'หมู่ 802': []
            };
            
            const uniqueStudents = new Map();
            Object.values(customUsers).forEach(u => {
                if (u && u.role === 'student') {
                    const key = (u.email || u.student_id || u.id || '').toLowerCase().trim();
                    if (key && !uniqueStudents.has(key)) {
                        uniqueStudents.set(key, u);
                    }
                }
            });

            uniqueStudents.forEach(u => {
                const rawSec = String(u.section || '');
                const m = rawSec.match(/(?:หมู่\s*)?([78]0[012])/);
                let targetSec = '';
                if (m) {
                    targetSec = `หมู่ ${m[1]}`;
                } else {
                    const isSpecial = (rawSec.includes('800') || rawSec.includes('801') || rawSec.includes('802') || rawSec.includes('พิเศษ'));
                    targetSec = isSpecial ? 'หมู่ 800' : 'หมู่ 700';
                }

                const stdObj = {
                    id: u.id || u.student_id || '-',
                    name: u.name || 'นิสิต',
                    email: u.email || '',
                    section: rawSec || targetSec,
                    company: u.company_name || u.company || '-',
                    company_lat: u.company_lat || u.lat || null,
                    company_lng: u.company_lng || u.lng || null,
                    docs: u.docs || 'รอตรวจ',
                    status: u.status || 'รอนิเทศ',
                    photo: u.photo || '',
                    advisor_name: u.advisor_name || u.advisor || '-',
                    semester: u.semester || 'ภาคต้น 2569',
                    initialPassword: u.initialPassword || u.password || u.initial_password || u.id
                };

                if (!studentsData[targetSec]) studentsData[targetSec] = [];
                studentsData[targetSec].push(stdObj);
            });
        }

        function getAllSystemStudents() {
            const sections = ['หมู่ 700', 'หมู่ 701', 'หมู่ 702', 'หมู่ 800', 'หมู่ 801', 'หมู่ 802'];
            const seen = new Set();
            const result = [];
            sections.forEach(sec => {
                (studentsData[sec] || []).forEach(s => {
                    const key = String(s.id || s.student_id || s.email || '').trim().toLowerCase();
                    if (key && !seen.has(key)) {
                        seen.add(key);
                        result.push(s);
                    }
                });
            });
            return result;
        }



        function getInitialUser() {
            const urlParams = new URLSearchParams(window.location.search);
            const userParam = urlParams.get('user');
            if (userParam === 'advisor') {
                return {
                    id: 'Q2222',
                    advisor_id: 'Q2222',
                    name: 'อาจารย์ สมหญิง จงจิต',
                    email: 'somying.ch@ku.th',
                    role: 'advisor',
                    section: 'หมู่ 701, หมู่ 801'
                };
            }
            if (userParam === 'admin') {
                return {
                    id: 'adminku',
                    name: 'ผู้ดูแลระบบ (Admin)',
                    email: 'admin@ku.th',
                    role: 'admin'
                };
            }
            if (userParam === 'student') {
                return {
                    id: '6521650101',
                    student_id: '6521650101',
                    name: 'นาย กิตติศักดิ์ พลอยประเสริฐ',
                    email: 'kittisak.plo@ku.th',
                    role: 'student',
                    section: 'หมู่ 700 (ภาคปกติ)',
                    company_name: 'บริษัท กสท โทรคมนาคม จำกัด (มหาชน)',
                    advisor_name: '-',
                    docs: 'ครบถ้วน',
                    status: 'นิเทศแล้ว',
                    score: 95
                };
            }

            const savedSession = sessionStorage.getItem('currentUser');
            if (savedSession) {
                try {
                    const parsed = JSON.parse(savedSession);
                    if (parsed && parsed.role) {
                        if (parsed.role === 'advisor') {
                            const advId = String(parsed.id || parsed.advisor_id || '');
                            const advEmail = String(parsed.email || '').toLowerCase();
                            const advName = String(parsed.name || '');
                            if (advId.includes('Q2222') || advEmail.includes('somying') || advName.includes('สมหญิง')) {
                                parsed.section = 'หมู่ 701, หมู่ 801';
                            } else if (advId.includes('Q3333') || advEmail.includes('somjit') || advName.includes('สมจิต')) {
                                parsed.section = 'หมู่ 702, หมู่ 802';
                            } else {
                                parsed.section = 'หมู่ 700, หมู่ 800';
                            }
                            try { sessionStorage.setItem('currentUser', JSON.stringify(parsed)); } catch (e) {}
                        }
                        return parsed;
                    }
                } catch (e) {
                    console.error("Session parse error:", e);
                }
            }

            // Authentication Guard: หากไม่มี Session ผู้ใช้ ให้ดีดกลับไปหน้า Login (index.html) ทันที
            window.location.replace('index.html');
            return null;
        }

        window.addEventListener('DOMContentLoaded', () => {
            const user = getInitialUser();
            if (!user) {
                // Not authenticated, redirecting to login page
                return;
            }
            if (user) {
                // 1. Immediately render UI to prevent any blank screen
                initUserDashboard(user);

                // 2. Non-blocking background sync from Supabase
                setTimeout(() => {
                    syncDatabaseUsers()
                        .then(() => {
                            if (currentRole === 'admin') {
                                renderAdminUsersTable();
                            } else if (currentRole === 'advisor') {
                                updateAdvisorStats();
                                renderStudentList();
                            }
                        })
                        .catch(err => console.warn("Background sync warning:", err));
                }, 50);
            }
        });

        function initUserDashboard(user) {
            // ปรับแก้ข้อมูลอาจารย์ 3 ท่านให้ถูกต้อง 100% ป้องกันข้อผิดพลาดจากการจำลองข้อมูล
            const uName = String(user.name || '');
            const uEmail = String(user.email || '').toLowerCase();
            const uId = String(user.id || user.advisor_id || '').toUpperCase();

            if (uName.includes('สมหญิง') || uEmail.includes('somying') || uId === 'Q2222') {
                user.role = 'advisor';
                user.name = 'อาจารย์ สมหญิง จงจิต';
                user.id = 'Q2222';
                user.advisor_id = 'Q2222';
                user.email = user.email || 'somying.ch@ku.th';
                user.section = 'หมู่ 701, หมู่ 801';
            } else if (uName.includes('สมจิต') || uEmail.includes('somjit') || uId === 'Q3333') {
                user.role = 'advisor';
                user.name = 'อาจารย์ สมจิต มั่งมี';
                user.id = 'Q3333';
                user.advisor_id = 'Q3333';
                user.email = user.email || 'somjit.m@ku.th';
                user.section = 'หมู่ 702, หมู่ 802';
            }

            try {
                localStorage.setItem('currentUser', JSON.stringify(user));
                sessionStorage.setItem('currentUser', JSON.stringify(user));
            } catch (e) {}

            currentRole = user.role;

            // 1. Update Sidebar User Card & Header User Pill
            const displayName = user.name || (currentRole === 'admin' ? 'ผู้ดูแลระบบ (Admin)' : currentRole === 'advisor' ? 'อาจารย์นิเทศ' : 'นิสิตสหกิจศึกษา');
            const roleBadgeText = currentRole === 'admin' ? 'ผู้ดูแลระบบ (Admin)' : (currentRole === 'advisor' ? 'อาจารย์นิเทศ' : 'นิสิตสหกิจศึกษา');
            
            const sidebarName = document.getElementById('sidebar-username');
            const sidebarRole = document.getElementById('sidebar-userrole');
            if (sidebarName) sidebarName.textContent = displayName;
            if (sidebarRole) sidebarRole.textContent = roleBadgeText;

            const headerName = document.getElementById('header-display-name');
            const headerAvatar = document.getElementById('header-avatar-initial');
            if (headerName) headerName.textContent = displayName.replace(/นาย|นางสาว|ดร\.|อาจารย์?/g, '').trim().split(' ')[0] || displayName;
            if (headerAvatar) headerAvatar.textContent = displayName.trim().charAt(0) || 'U';

            // 2. Build Sidebar Navigation for this role
            buildSidebarNav(currentRole);

            // 3. Set Theme & Role Views
            const root = document.documentElement;
            if (currentRole === 'advisor') {
                root.style.setProperty('--primary-color', '#15803d');
                root.style.setProperty('--bg-body', '#f8fafc');
                document.getElementById('header-role-title').textContent = 'ระบบนิเทศสหกิจศึกษา (อาจารย์นิเทศ)';
                
                const advNameEl = document.getElementById('adv-welcome-name');
                if (advNameEl) advNameEl.textContent = `สวัสดีครับ, ${displayName}`;
                const advIdEl = document.getElementById('adv-welcome-id');
                if (advIdEl) advIdEl.textContent = user.id || user.advisor_id || '-';

                const advSecStr = String(user.section || '');
                const advIdVal = String(user.id || user.advisor_id || '');
                const advEmailVal = String(user.email || '').toLowerCase();
                const advNameVal = String(user.name || '');

                if (advIdVal.includes('Q2222') || advEmailVal.includes('somying') || advNameVal.includes('สมหญิง')) {
                    currentSelectedClassroom = 'หมู่ 701';
                } else if (advIdVal.includes('Q3333') || advEmailVal.includes('somjit') || advNameVal.includes('สมจิต')) {
                    currentSelectedClassroom = 'หมู่ 702';
                } else {
                    const mNorm = advSecStr.match(/70[0123]/);
                    if (mNorm) {
                        currentSelectedClassroom = `หมู่ ${mNorm[0]}`;
                    } else {
                        currentSelectedClassroom = 'หมู่ 700';
                    }
                }

                showPage('sec-advisor-dash');
                updateAdvisorStats();
                renderStudentList();
                renderAdvisorAssignments();
            } else if (currentRole === 'student') {
                root.style.setProperty('--primary-color', '#0f766e');
                root.style.setProperty('--bg-body', '#f8fafc');
                document.getElementById('header-role-title').textContent = 'ระบบส่งงานและเอกสารสหกิจศึกษา (นิสิต)';

                const stdName = document.getElementById('std-welcome-name');
                if (stdName) stdName.textContent = `สวัสดีครับ, ${displayName}`;
                const stdDocsName = document.getElementById('std-docs-welcome-name');
                if (stdDocsName) stdDocsName.textContent = `สวัสดีครับ, ${displayName}`;

                const stdSub = document.getElementById('std-welcome-sub');
                const stdIdVal = user.id || user.student_id || '-';
                const stdSecVal = user.section || 'ไม่ระบุ';
                const formattedSection = stdSecVal.includes('หมู่') ? stdSecVal : `หมู่ ${stdSecVal}`;
                const stdSemester = user.semester || 'ภาคต้น 2569';
                if (stdSub) stdSub.textContent = `รหัสนิสิต: ${stdIdVal} | ${formattedSection} | ภาคการศึกษา: ${stdSemester}`;
                const stdDocsSub = document.getElementById('std-docs-welcome-sub');
                if (stdDocsSub) stdDocsSub.textContent = `รหัสนิสิต: ${stdIdVal} | ${formattedSection} | ภาคการศึกษา: ${stdSemester}`;

                const compName = user.company_name || user.company || 'ยังไม่ระบุสถานประกอบการ';
                const advName = user.advisor || user.advisor_name || 'ยังไม่ระบุอาจารย์นิเทศ';

                const stdCompany = document.getElementById('std-company-name');
                if (stdCompany) stdCompany.textContent = compName;

                const stdAdvisor = document.getElementById('std-advisor-name');
                if (stdAdvisor) stdAdvisor.textContent = `อาจารย์นิเทศ: ${advName}`;

                const stdDocsComp = document.getElementById('std-docs-company-info');
                if (stdDocsComp) stdDocsComp.textContent = `สถานประกอบการ: ${compName} | อาจารย์นิเทศ: ${advName}`;

                const stdBadge = document.getElementById('std-supervision-badge');
                if (stdBadge) {
                    const isInspected = (user.status === 'นิเทศแล้ว');
                    stdBadge.className = `status-badge ${isInspected ? 'badge-success' : 'badge-info'}`;
                    stdBadge.textContent = isInspected ? 'นิเทศแล้ว' : 'รอนิเทศงาน';
                }

                const qrId = document.getElementById('std-qr-id');
                if (qrId) qrId.textContent = `${stdIdVal}`;
                const qrName = document.getElementById('std-qr-name');
                if (qrName) qrName.textContent = `${displayName}`;
                
                const qrImg = document.getElementById('std-qr-image');
                const qrPlace = document.getElementById('std-qr-placeholder');
                if (qrImg && qrPlace) {
                    qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=${encodeURIComponent(stdIdVal)}`;
                    qrImg.onload = () => {
                        qrPlace.style.display = 'none';
                        qrImg.style.display = 'block';
                    };
                }

                loadStudentProjectTracking(stdIdVal);
                renderStudentGpsSettings(user);

                const stdScore = document.getElementById('std-score-val');
                if (stdScore) {
                    stdScore.textContent = (user.score !== undefined && user.score !== null) ? `${user.score} / 100` : 'รอการประเมิน';
                }
                const stdDocStatus = document.getElementById('std-doc-status');
                if (stdDocStatus) {
                    stdDocStatus.textContent = user.docs || 'รอนิเทศงาน';
                }
                const stdFeedback = document.getElementById('std-feedback-val');
                if (stdFeedback) {
                    if (user.feedback) {
                        stdFeedback.textContent = user.feedback;
                        stdFeedback.style.color = 'var(--text-main)';
                        stdFeedback.style.fontStyle = 'normal';
                    } else {
                        stdFeedback.textContent = 'ยังไม่มีข้อคิดเห็น (รออาจารย์นิเทศออกตรวจนิเทศงาน)';
                        stdFeedback.style.color = '#94a3b8';
                        stdFeedback.style.fontStyle = 'italic';
                    }
                }

                showPage('sec-student-docs');
                renderStudentDocsList();
                renderBlankFormsGrid();
                renderStudentClassroomAssignments();
            } else if (currentRole === 'admin') {
                root.style.setProperty('--primary-color', '#1e293b');
                root.style.setProperty('--bg-body', '#f8fafc');
                document.getElementById('header-role-title').textContent = 'ระบบบริหารจัดการสำหรับแอดมิน (Admin Web Dashboard)';

                showPage('sec-admin-dash');
                updateAdvisorStats();
                renderAdminUsersTable();
                renderAdminGpsSection();
            }

            renderCalendarEvents();
            renderTabBar();
            updateNotifyBadge();

            // Check URL search parameters for automated preview or screenshot
            const urlParams = new URLSearchParams(window.location.search);
            const targetPage = urlParams.get('page');
            const targetClassroom = urlParams.get('classroom');
            const targetModal = urlParams.get('modal');

            // Hook for checkin success / failure test previews
            if (urlParams.get('test_checkin') === 'success') {
                showPage('sec-advisor-qr');
                setTimeout(() => {
                    const card = document.getElementById('qr-checkin-result-card');
                    const dot = document.getElementById('qr-result-dot');
                    const titleEl = document.getElementById('qr-result-title');
                    const badgeEl = document.getElementById('qr-result-status-badge');
                    const infoEl = document.getElementById('qr-result-student-info');
                    const locEl = document.getElementById('qr-result-location');
                    const gpsEl = document.getElementById('qr-result-gps');
                    const targetGpsEl = document.getElementById('qr-result-target-gps');
                    const distEl = document.getElementById('qr-result-distance');
                    const timeEl = document.getElementById('qr-result-time');
                    const warningBox = document.getElementById('qr-result-warning-box');
                    const evalBtn = document.getElementById('btn-open-eval-modal');
                    const disabledNotice = document.getElementById('btn-eval-disabled-notice');
                    const mapLink = document.getElementById('qr-result-map-link');

                    if (card) { card.style.display = 'block'; card.style.backgroundColor = '#f0fdf4'; card.style.borderColor = '#22c55e'; }
                    if (dot) { dot.style.backgroundColor = '#22c55e'; dot.style.boxShadow = '0 0 8px #22c55e'; }
                    if (titleEl) { titleEl.textContent = 'เช็คอินยืนยันพิกัด GPS สำเร็จ!'; titleEl.style.color = '#15803d'; }
                    if (badgeEl) { badgeEl.textContent = 'อยู่ในรัศมี (ผ่านเกณฑ์)'; badgeEl.style.backgroundColor = '#dcfce7'; badgeEl.style.color = '#15803d'; }
                    if (infoEl) infoEl.textContent = 'นาย กิตติศักดิ์ พลอยประเสริฐ (รหัสนิสิต: 6521650101)';
                    if (locEl) locEl.textContent = 'บริษัท กสท โทรคมนาคม จำกัด (มหาชน)';
                    if (gpsEl) gpsEl.textContent = 'Lat 13.884532, Lng 100.578645 (±8 ม.)';
                    if (targetGpsEl) targetGpsEl.textContent = 'Lat 13.884500, Lng 100.578600';
                    if (distEl) { distEl.textContent = '42.5 เมตร (อยู่ในรัศมีไม่เกิน 500 เมตร)'; distEl.style.color = '#16a34a'; }
                    if (timeEl) timeEl.textContent = '31 ต.ค. 2569 เวลา 14:35:10 น.';
                    if (warningBox) warningBox.style.display = 'none';
                    if (evalBtn) { evalBtn.style.display = 'block'; evalBtn.disabled = false; evalBtn.style.opacity = '1'; evalBtn.style.cursor = 'pointer'; }
                    if (disabledNotice) disabledNotice.style.display = 'none';
                    if (card) { card.scrollIntoView({ behavior: 'instant', block: 'start' }); }
                }, 150);
            } else if (urlParams.get('test_checkin') === 'failed') {
                showPage('sec-advisor-qr');
                setTimeout(() => {
                    const card = document.getElementById('qr-checkin-result-card');
                    const dot = document.getElementById('qr-result-dot');
                    const titleEl = document.getElementById('qr-result-title');
                    const badgeEl = document.getElementById('qr-result-status-badge');
                    const infoEl = document.getElementById('qr-result-student-info');
                    const locEl = document.getElementById('qr-result-location');
                    const gpsEl = document.getElementById('qr-result-gps');
                    const targetGpsEl = document.getElementById('qr-result-target-gps');
                    const distEl = document.getElementById('qr-result-distance');
                    const timeEl = document.getElementById('qr-result-time');
                    const warningBox = document.getElementById('qr-result-warning-box');
                    const evalBtn = document.getElementById('btn-open-eval-modal');
                    const disabledNotice = document.getElementById('btn-eval-disabled-notice');

                    if (card) { card.style.display = 'block'; card.style.backgroundColor = '#fff5f5'; card.style.borderColor = '#ef4444'; }
                    if (dot) { dot.style.backgroundColor = '#ef4444'; dot.style.boxShadow = '0 0 8px #ef4444'; }
                    if (titleEl) { titleEl.textContent = 'เช็คอินไม่สำเร็จ: อยู่นอกรัศมีที่กำหนด!'; titleEl.style.color = '#dc2626'; }
                    if (badgeEl) { badgeEl.textContent = 'อยู่นอกรัศมี 500 เมตร'; badgeEl.style.backgroundColor = '#fee2e2'; badgeEl.style.color = '#dc2626'; }
                    if (infoEl) infoEl.textContent = 'นาย กิตติศักดิ์ พลอยประเสริฐ (รหัสนิสิต: 6521650101)';
                    if (locEl) locEl.textContent = 'บริษัท กสท โทรคมนาคม จำกัด (มหาชน)';
                    if (gpsEl) gpsEl.textContent = 'Lat 13.847621, Lng 100.569432 (±15 ม.)';
                    if (targetGpsEl) targetGpsEl.textContent = 'Lat 13.884500, Lng 100.578600';
                    if (distEl) { distEl.textContent = '4,215.8 เมตร (เกินระยะ 500 เมตรที่กำหนด)'; distEl.style.color = '#dc2626'; }
                    if (timeEl) timeEl.textContent = '31 ต.ค. 2569 เวลา 14:38:22 น.';
                    if (warningBox) warningBox.style.display = 'block';
                    if (evalBtn) evalBtn.style.display = 'none';
                    if (disabledNotice) disabledNotice.style.display = 'block';
                    if (card) { card.scrollIntoView({ behavior: 'instant', block: 'start' }); }
                }, 150);
            }

            // Quick verification hook for Excel import pre/post preview
            if (urlParams.get('test_pre_import') === '1') {
                adminParsedStudentRows = window.adminParsedStudentRows = [
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
                renderAdminStudentPreImportPreview(false);
                const elImport = document.getElementById('admin-card-import');
                if (elImport) {
                    elImport.scrollIntoView({ behavior: 'instant', block: 'start' });
                    window.scrollTo(0, elImport.offsetTop - 40);
                }
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
                renderAdminStudentPreImportPreview(true, samplePostList);
                const elImport = document.getElementById('admin-card-import');
                if (elImport) {
                    elImport.scrollIntoView({ behavior: 'instant', block: 'start' });
                    window.scrollTo(0, elImport.offsetTop - 40);
                }
            }

            if (targetPage) {
                showPage(targetPage);
                if (targetPage === 'sec-advisor-assignments') renderAdvisorAssignments();
                if (targetPage === 'sec-advisor-photos') renderAdvisorPhotosPage();
                if (targetPage === 'sec-advisor-calendar') renderCalendar();
                if (targetPage === 'sec-advisor-classroom') {
                    if (targetClassroom) {
                        openClassroomDetail("หมู่ " + targetClassroom);
                    }
                }
            }
            if (targetModal === 'photo') {
                openPhotoModal('6521650101', 'นาย กิตติศักดิ์ พลอยประเสริฐ', 'หมู่ 700');
            } else if (targetModal === 'photo_confirm') {
                openPhotoModal('6521650101', 'นาย กิตติศักดิ์ พลอยประเสริฐ', 'หมู่ 700');
                const img = document.getElementById('photo-preview-img');
                const emptyText = document.getElementById('photo-empty-text');
                const confirmBtn = document.getElementById('btn-confirm-upload-photo');
                const noticeEl = document.getElementById('photo-pending-notice');
                if (img) {
                    img.src = 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=600&q=80';
                    img.style.display = 'block';
                }
                if (emptyText) emptyText.style.display = 'none';
                if (confirmBtn) confirmBtn.style.display = 'flex';
                if (noticeEl) noticeEl.style.display = 'block';
            }
        }



        function logout() {
            try { sessionStorage.removeItem('currentUser'); } catch (e) {}
            try { localStorage.removeItem('currentUser'); } catch (e) {}
            window.location.replace('index.html');
        }

        // ==================== DESKTOP SIDEBAR NAVIGATION ====================
