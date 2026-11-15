// ==========================================================================
// notifications.js - ระบบแจ้งเตือนและรายการแจ้งเตือนด่วน (Notifications)
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

function openNotifyModal() {
            renderNotifications();
            document.getElementById('modal-notify').style.display = 'flex';
            notifications.forEach(n => n.unread = false);
            updateNotifyBadge();
        }

        function addNotification(text) {
            notifications.unshift({
                id: Date.now(),
                text: text,
                time: 'เมื่อครู่นี้',
                unread: true
            });
            updateNotifyBadge();
        }

        function updateNotifyBadge() {
            const hasUnread = notifications.some(n => n.unread);
            const badge = document.getElementById('notify-badge');
            if (badge) {
                badge.style.display = hasUnread ? 'block' : 'none';
            }
        }

        function renderNotifications() {
            const container = document.getElementById('notify-list-container');
            container.innerHTML = '';

            if (notifications.length === 0) {
                container.innerHTML = '<div style="color: var(--text-muted); text-align: center; padding: 12px;">ไม่มีการแจ้งเตือนใหม่</div>';
                return;
            }

            notifications.forEach(n => {
                const div = document.createElement('div');
                div.className = 'student-item';
                div.style.backgroundColor = n.unread ? '#f0fdf4' : '#ffffff';
                div.innerHTML = `
                    <div>
                        <div style="font-weight: 600; color: var(--text-main);">${n.text}</div>
                        <div style="color: var(--text-muted); font-size: 9px; margin-top: 2px;">${n.time}</div>
                    </div>
                `;
                container.appendChild(div);
            });
        }



        function sendNotification(targetRole, targetId, message) {
            const notifs = JSON.parse(localStorage.getItem('sysNotifications') || '[]');
            notifs.unshift({ id: Date.now(), role: targetRole, targetId: String(targetId), text: message, read: false });
            localStorage.setItem('sysNotifications', JSON.stringify(notifs));
            updateNotificationBell();
        }

        function updateNotificationBell() {
            const savedSession = (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'));
            if (!savedSession) return;
            const user = JSON.parse(savedSession);
            
            const btn = document.getElementById('header-notification-btn');
            if (!btn) return;
            
            if (user.role === 'admin') {
                btn.style.display = 'none';
                return;
            } else {
                btn.style.display = 'flex';
            }

            const notifs = JSON.parse(localStorage.getItem('sysNotifications') || '[]');
            const myId = String(user.id || user.student_id || '');
            let unreadCount = 0;
            const myNotifs = [];

            for (let n of notifs) {
                if (n.role === user.role && (n.targetId === 'all' || String(n.targetId) === myId || (n.role === 'advisor' && user.role === 'advisor'))) {
                    myNotifs.push(n);
                    if (!n.read) unreadCount++;
                }
            }

            const badge = document.getElementById('notification-badge');
            const listEl = document.getElementById('notification-list');
            if (badge && listEl) {
                if (unreadCount > 0) {
                    badge.style.display = 'flex';
                    badge.alignItems = 'center';
                    badge.justifyContent = 'center';
                    badge.textContent = unreadCount;
                } else {
                    badge.style.display = 'none';
                }

                if (myNotifs.length === 0) {
                    listEl.innerHTML = '<div style="font-size: 11px; color: #94a3b8; text-align: center; padding: 12px 0;">ไม่มีการแจ้งเตือนใหม่</div>';
                } else {
                    listEl.innerHTML = myNotifs.map(n => `
                        <div style="padding: 8px 10px; background: ${n.read ? '#f8fafc' : '#f0fdf4'}; border-left: 3px solid ${n.read ? '#cbd5e1' : '#22c55e'}; border-radius: 4px; font-size: 11px; color: #334155; margin-bottom: 4px;">
                            ${n.text}
                        </div>
                    `).join('');
                }
            }
        }

        function toggleNotificationPopup() {
            const popup = document.getElementById('notification-popup');
            if (popup) {
                const isShowing = popup.style.display === 'flex';
                if (!isShowing) {
                    popup.style.display = 'flex';
                    // Mark as read
                    const savedSession = (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'));
                    if (savedSession) {
                        const user = JSON.parse(savedSession);
                        const notifs = JSON.parse(localStorage.getItem('sysNotifications') || '[]');
                        const myId = String(user.id || user.student_id || '');
                        let changed = false;
                        notifs.forEach(n => {
                            if (!n.read && n.role === user.role && (n.targetId === 'all' || String(n.targetId) === myId || (n.role === 'advisor' && user.role === 'advisor'))) {
                                n.read = true;
                                changed = true;
                            }
                        });
                        if (changed) {
                            localStorage.setItem('sysNotifications', JSON.stringify(notifs));
                            setTimeout(updateNotificationBell, 1500);
                        }
                    }
                } else {
                    popup.style.display = 'none';
                }
            }
        }

        document.addEventListener('click', function(e) {
            const btn = document.getElementById('header-notification-btn');
            const popup = document.getElementById('notification-popup');
            if (btn && popup && !btn.contains(e.target)) {
                popup.style.display = 'none';
            }
        });

        setTimeout(updateNotificationBell, 1000);

    
        /* ==========================================================================
           STUDENT WORKPLACE GPS SETTING FUNCTIONS
           ========================================================================== */

        let currentStudentProfile = null;
