// ==========================================================================
// student-calendar.js - ระบบดูตารางนัดหมายฝั่งนิสิต (Student Schedule)
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

function renderStudentScheduleList() {
            const container = document.getElementById('std-schedule-container');
            if (!container) return;
            const apps = getSystemAppointments();
            if (apps.length === 0) {
                container.innerHTML = `<div style="text-align: center; color: var(--text-muted); font-size: 12px; padding: 16px; background: #f8fafc; border-radius: 8px;">ยังไม่มีรายการนัดหมายตรวจนิเทศงาน</div>`;
                return;
            }
            container.innerHTML = apps.map(a => `
                <div style="padding: 12px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-weight: 700; font-size: 13px; color: #166534;">กำหนดการนัดหมายนิเทศงาน</div>
                        <span style="font-size: 10px; background: #dcfce7; color: #15803d; padding: 2px 6px; border-radius: 4px; font-weight: 600;">นัดหมายแล้ว</span>
                    </div>
                    <div style="font-size: 12px; color: #374151; margin-top: 4px;">วันที่: <strong>${a.dateStr}</strong> | เวลา: <strong>${a.timeStr}</strong></div>
                    <div style="font-size: 11px; color: #6b7280; margin-top: 2px;">ผู้นัดหมาย: ${a.studentName}</div>
                </div>
            `).join('');
        }
