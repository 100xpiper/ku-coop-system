// ==========================================================================
// advisor-calendar.js - ระบบปฏิทินนัดหมายตรวจนิเทศของอาจารย์
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

function getSystemAppointments() {
            try {
                const stored = localStorage.getItem('systemAppointments');
                return stored ? JSON.parse(stored) : [];
            } catch (e) {
                return [];
            }
        }

        function saveSystemAppointments(apps) {
            localStorage.setItem('systemAppointments', JSON.stringify(apps));
        }

        const THAI_MONTHS = [
            'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน',
            'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม',
            'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
        ];

        let currentCalYear = new Date().getFullYear(); // e.g. 2026
        let currentCalMonth = new Date().getMonth();   // 0-11
        let selectedCalDateStr = '';

        function initCalendarControls() {
            const yearSelect = document.getElementById('cal-year-select');
            if (yearSelect && yearSelect.options.length === 0) {
                const startYear = 2024;
                const endYear = 2032;
                for (let y = startYear; y <= endYear; y++) {
                    const opt = document.createElement('option');
                    opt.value = y;
                    opt.textContent = `${y + 543} (${y})`;
                    if (y === currentCalYear) opt.selected = true;
                    yearSelect.appendChild(opt);
                }
            }
        }

        function changeCalendarMonth(delta) {
            currentCalMonth += delta;
            if (currentCalMonth < 0) {
                currentCalMonth = 11;
                currentCalYear--;
            } else if (currentCalMonth > 11) {
                currentCalMonth = 0;
                currentCalYear++;
            }
            syncCalendarDropdowns();
            renderCalendarEvents();
        }

        function onCalendarSelectChange() {
            const monthEl = document.getElementById('cal-month-select');
            const yearEl = document.getElementById('cal-year-select');
            if (monthEl && yearEl) {
                currentCalMonth = parseInt(monthEl.value);
                currentCalYear = parseInt(yearEl.value);
                renderCalendarEvents();
            }
        }

        function jumpToCurrentDate() {
            const now = new Date();
            currentCalYear = now.getFullYear();
            currentCalMonth = now.getMonth();
            syncCalendarDropdowns();
            
            const todayDateStr = `${now.getDate()} ${THAI_MONTHS[currentCalMonth]} ${currentCalYear + 543}`;
            selectCalDate(now.getDate(), todayDateStr);
            renderCalendarEvents();
        }

        function syncCalendarDropdowns() {
            const monthEl = document.getElementById('cal-month-select');
            const yearEl = document.getElementById('cal-year-select');
            if (monthEl) monthEl.value = currentCalMonth;
            if (yearEl) yearEl.value = currentCalYear;
        }

        function selectCalDate(day, dateStr) {
            if (!dateStr || typeof dateStr !== 'string') {
                const beYear = currentCalYear + 543;
                dateStr = `${day} ${THAI_MONTHS[currentCalMonth]} ${beYear}`;
            }
            selectedCalDateStr = dateStr;

            const inputEl = document.getElementById('cal-date-input');
            if (inputEl) inputEl.value = dateStr;

            document.querySelectorAll('.calendar-cell').forEach(cell => cell.classList.remove('selected-day'));
            const targetCell = document.getElementById(`cal-cell-${day}`);
            if (targetCell && !targetCell.classList.contains('other-month')) {
                targetCell.classList.add('selected-day');
            }
        }

        function renderCalendarEvents() {
            const container = document.getElementById('dynamic-calendar-grid');
            if (!container) return;

            initCalendarControls();
            syncCalendarDropdowns();

            const beYear = currentCalYear + 543;
            const monthName = THAI_MONTHS[currentCalMonth];
            const headerTitle = document.getElementById('cal-header-title');
            if (headerTitle) {
                headerTitle.textContent = `ปฏิทินนัดหมายนิเทศ (${monthName} ${beYear})`;
            }

            const apps = getSystemAppointments();
            const now = new Date();
            const isCurrentRealMonth = (now.getFullYear() === currentCalYear && now.getMonth() === currentCalMonth);
            const realTodayDate = now.getDate();

            // First day of month (0 = Sun, 1 = Mon, ..., 6 = Sat)
            const firstDayIndex = new Date(currentCalYear, currentCalMonth, 1).getDay();
            // Days in current month
            const daysInMonth = new Date(currentCalYear, currentCalMonth + 1, 0).getDate();
            // Days in previous month
            const prevMonthDays = new Date(currentCalYear, currentCalMonth, 0).getDate();

            let html = `
                <div class="calendar-day-header">อา</div>
                <div class="calendar-day-header">จ</div>
                <div class="calendar-day-header">อ</div>
                <div class="calendar-day-header">พ</div>
                <div class="calendar-day-header">พฤ</div>
                <div class="calendar-day-header">ศ</div>
                <div class="calendar-day-header">ส</div>
            `;

            // 1. Padding cells from previous month
            for (let i = firstDayIndex; i > 0; i--) {
                const prevDay = prevMonthDays - i + 1;
                html += `<div class="calendar-cell other-month" style="opacity: 0.35; cursor: default; background-color: #f1f5f9;">${prevDay}</div>`;
            }

            // 2. Actual month days
            for (let day = 1; day <= daysInMonth; day++) {
                const fullDateStr = `${day} ${monthName} ${beYear}`;
                
                const hasEvent = apps.some(a => {
                    if (!a.dateStr) return false;
                    const cleanAppDate = String(a.dateStr).trim();
                    if (cleanAppDate === fullDateStr) return true;
                    const m = cleanAppDate.match(/^(\d+)\s+([^\s]+)(?:\s+(\d+))?/);
                    if (m) {
                        const appDay = parseInt(m[1], 10);
                        const appMonth = m[2];
                        const appYear = m[3] ? parseInt(m[3], 10) : null;
                        if (appDay === day && appMonth === monthName) {
                            if (!appYear || appYear === beYear || appYear === currentCalYear) {
                                return true;
                            }
                        }
                    }
                    return false;
                });

                const isToday = isCurrentRealMonth && (day === realTodayDate);
                const isSelected = (selectedCalDateStr === fullDateStr);

                let cellClasses = ['calendar-cell'];
                if (isToday) cellClasses.push('is-today');
                if (isSelected) cellClasses.push('selected-day');
                if (hasEvent) cellClasses.push('has-event');

                const dotHtml = hasEvent ? '<div class="event-dot"></div>' : '';
                const todayBadge = isToday ? '<div style="font-size: 8px; color: #15803d; margin-top: -2px; font-weight: 700;">วันนี้</div>' : '';

                html += `
                    <div class="${cellClasses.join(' ')}" id="cal-cell-${day}" onclick="selectCalDate(${day}, '${fullDateStr}')">
                        <div>${day}</div>
                        ${todayBadge}
                        ${dotHtml}
                    </div>`;
            }

            // 3. Padding cells for next month
            const totalCells = firstDayIndex + daysInMonth;
            const remainingCells = (totalCells % 7 === 0) ? 0 : (7 - (totalCells % 7));
            for (let i = 1; i <= remainingCells; i++) {
                html += `<div class="calendar-cell other-month" style="opacity: 0.35; cursor: default; background-color: #f1f5f9;">${i}</div>`;
            }

            container.innerHTML = html;

            renderAdvisorAppointmentsList();
            renderStudentScheduleList();
        }

        async function addAppointment() {
            const studentSelect = document.getElementById('cal-student-select');
            const studentId = studentSelect ? studentSelect.value : '';
            if (!studentId) {
                alert('กรุณาเลือกนิสิตที่ต้องการนัดหมายก่อน');
                return;
            }
            const studentText = studentSelect && studentSelect.options[studentSelect.selectedIndex] ? studentSelect.options[studentSelect.selectedIndex].text : 'นิสิตทั่วไป';
            const dateStr = document.getElementById('cal-date-input').value;
            const timeStr = document.getElementById('cal-time-select').value;

            if (!dateStr) {
                alert('กรุณาเลือกวันที่จากปฏิทินก่อน');
                return;
            }

            const apps = getSystemAppointments();
            const newApp = {
                id: 'app_' + Date.now(),
                studentId: studentId,
                studentName: studentText,
                dateStr: dateStr,
                timeStr: timeStr,
                createdAt: new Date().toISOString()
            };
            apps.push(newApp);
            saveSystemAppointments(apps);
            sendNotification('student', studentId, `มีการนัดหมายนิเทศงานใหม่ วันที่ ${dateStr} เวลา ${timeStr}`);

            if (typeof dbAddAppointment === 'function') {
                await dbAddAppointment('1234', studentId, dateStr, timeStr);
            }

            renderCalendarEvents();
            addNotification(`เพิ่มนัดหมายนิเทศ (${dateStr} เวลา ${timeStr}) เรียบร้อยแล้ว`);
            alert(`บันทึกการนัดหมายวันที่ ${dateStr} เวลา ${timeStr} สำเร็จ! ปฏิทินแสดงไฮไลท์เรียบร้อยแล้ว`);
        }

        function clearCalForm() {
            document.getElementById('cal-date-input').value = '';
            document.querySelectorAll('.calendar-cell').forEach(cell => cell.classList.remove('selected-day'));
        }

        function deleteAppointment(id) {
            if (!confirm('คุณต้องการยกเลิกนัดหมายนี้ใช่หรือไม่?')) return;
            let apps = getSystemAppointments();
            apps = apps.filter(a => a.id !== id);
            saveSystemAppointments(apps);
            renderCalendarEvents();
            addNotification('ยกเลิกนัดหมายนิเทศเรียบร้อยแล้ว');
        }

        function renderAdvisorAppointmentsList() {
            const container = document.getElementById('adv-appointments-list');
            if (!container) return;
            const apps = getSystemAppointments();
            if (apps.length === 0) {
                container.innerHTML = `<div style="text-align: center; color: var(--text-muted); font-size: 12px; padding: 12px; background: #f8fafc; border-radius: 8px;">ยังไม่มีนัดหมายนิเทศในระบบ</div>`;
                return;
            }
            container.innerHTML = apps.map(a => `
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; background: #f8fafc; border: 1px solid var(--border-color); border-radius: 8px; margin-bottom: 8px;">
                    <div>
                        <div style="font-weight: 700; font-size: 13px; color: var(--text-color);">${a.studentName}</div>
                        <div style="font-size: 11px; color: var(--text-muted);">วันที่ ${a.dateStr} | เวลา ${a.timeStr}</div>
                    </div>
                    <button class="btn-primary" style="background-color: #ef4444; padding: 4px 10px; font-size: 11px;" onclick="deleteAppointment('${a.id}')">ยกเลิก</button>
                </div>
            `).join('');
        }
