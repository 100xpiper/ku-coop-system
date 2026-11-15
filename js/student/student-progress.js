// ==========================================================================
// student-progress.js - ระบบติดตามงานรายสัปดาห์ของนิสิต (Weekly Diary)
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

let currentReportImages = []; // อาเรย์เก็บรูปภาพ Base64 ของสัปดาห์ที่กำลังเลือก

// ฟังก์ชันเปิดดูรูปภาพขนาดใหญ่ (Modal Lightbox)
function viewImagePreviewModal(imgSrc, title) {
    let modal = document.getElementById('modal-image-preview');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'modal-image-preview';
        modal.className = 'modal-overlay';
        modal.style.cssText = 'display: none; position: fixed; inset: 0; background: rgba(15, 23, 42, 0.88); z-index: 99999; justify-content: center; align-items: center; padding: 20px;';
        modal.onclick = function(e) {
            if (e.target === modal || e.target.classList.contains('close-btn') || e.target.closest('.close-btn')) {
                modal.style.display = 'none';
            }
        };
        modal.innerHTML = `
            <div style="position: relative; max-width: 90vw; max-height: 90vh; display: flex; flex-direction: column; align-items: center;">
                <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 10px; color: #ffffff;">
                    <span id="modal-image-preview-title" style="font-size: 14px; font-weight: 600;">รูปภาพประกอบ</span>
                    <button class="close-btn" style="background: rgba(255,255,255,0.2); border: none; color: white; border-radius: 50%; width: 30px; height: 30px; font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center; line-height: 1;">✕</button>
                </div>
                <img id="modal-image-preview-img" src="" style="max-width: 90vw; max-height: 80vh; object-fit: contain; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
            </div>
        `;
        document.body.appendChild(modal);
    }

    const imgEl = document.getElementById('modal-image-preview-img');
    const titleEl = document.getElementById('modal-image-preview-title');
    if (imgEl) imgEl.src = imgSrc;
    if (titleEl) titleEl.textContent = title || 'รูปภาพประกอบการปฏิบัติงาน';
    modal.style.display = 'flex';
}

// ฟังก์ชันบีบอัดรูปภาพผ่าน HTML5 Canvas เพื่อประหยัดพื้นที่จัดเก็บและเพิ่มความเร็ว
function compressImage(dataUrl, maxWidth, maxHeight, quality, callback) {
    const img = new Image();
    img.onload = function() {
        let width = img.width;
        let height = img.height;

        if (width > maxWidth || height > maxHeight) {
            if (width > height) {
                height = Math.round((height * maxWidth) / width);
                width = maxWidth;
            } else {
                width = Math.round((width * maxHeight) / height);
                height = maxHeight;
            }
        }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);
        callback(canvas.toDataURL('image/jpeg', quality));
    };
    img.src = dataUrl;
}

// จัดการเมื่อนิสิตเลือกไฟล์รูปภาพ
function handleStudentReportImages(event) {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    const maxFiles = 5;
    if (currentReportImages.length + files.length > maxFiles) {
        alert(`สามารถแนบรูปภาพได้สูงสุด ${maxFiles} รูปต่อสัปดาห์`);
    }

    const availableSlots = maxFiles - currentReportImages.length;
    if (availableSlots <= 0) return;

    const filesToProcess = Array.from(files).slice(0, availableSlots);

    filesToProcess.forEach(file => {
        if (!file.type.startsWith('image/')) {
            alert(`ไฟล์ ${file.name} ไม่ใช่ไฟล์รูปภาพ`);
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            compressImage(e.target.result, 1200, 1200, 0.8, function(compressedDataUrl) {
                currentReportImages.push(compressedDataUrl);
                renderImagePreviews();
            });
        };
        reader.readAsDataURL(file);
    });

    event.target.value = '';
}

// ลบรูปภาพที่เลือกไว้ก่อนกดบันทึก
function removeReportImage(index) {
    currentReportImages.splice(index, 1);
    renderImagePreviews();
}

// แสดงพรีวิวรูปภาพที่เลือกไว้ในฟอร์มบันทึก
function renderImagePreviews() {
    const container = document.getElementById('student-pt-image-previews');
    const countEl = document.getElementById('student-pt-image-count');
    if (!container) return;

    if (!currentReportImages || currentReportImages.length === 0) {
        container.innerHTML = '';
        if (countEl) countEl.textContent = '(ยังไม่ได้เลือกรูปภาพ)';
        return;
    }

    if (countEl) countEl.textContent = `(เลือกแล้ว ${currentReportImages.length} รูป - สูงสุด 5 รูป)`;

    container.innerHTML = currentReportImages.map((src, idx) => `
        <div style="position: relative; width: 72px; height: 72px; border-radius: 6px; overflow: hidden; border: 1px solid #cbd5e1; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
            <img src="${src}" style="width: 100%; height: 100%; object-fit: cover; cursor: pointer;" onclick="viewImagePreviewModal('${src}', 'รูปที่ ${idx+1}')" alt="ตัวอย่างรูปที่ ${idx+1}">
            <button type="button" onclick="removeReportImage(${idx})" title="ลบรูปนี้" style="position: absolute; top: 3px; right: 3px; width: 20px; height: 20px; border-radius: 50%; background: rgba(220, 38, 38, 0.9); color: white; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; line-height: 1;">✕</button>
        </div>
    `).join('');
}

// สลับสัปดาห์ใน Dropdown แล้วดึงข้อมูลเดิม (รวมรูปภาพเดิม) มาแสดง
function onStudentWeekChange() {
    const savedSession = (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'));
    if (!savedSession) return;
    const user = JSON.parse(savedSession);
    const stdId = String(user.id || user.student_id);
    const data = JSON.parse(localStorage.getItem('projectTracking_' + stdId) || '{"projectName": "", "weeklyReports": []}');

    const weekEl = document.getElementById('student-pt-week');
    if (!weekEl) return;
    const weekVal = parseInt(weekEl.value);
    const existing = (data.weeklyReports || []).find(r => r.week === weekVal);

    if (existing) {
        document.getElementById('student-pt-issues').value = existing.issues || '';
        currentReportImages = existing.images ? [...existing.images] : [];
    } else {
        document.getElementById('student-pt-issues').value = '';
        currentReportImages = [];
    }
    renderImagePreviews();
}

// เปิดหน้าต่าง Modal ติดตามงานฝั่งอาจารย์ที่ปรึกษา
function openProjectTrackingModal(stdId, stdName) {
    currentTrackingStudentId = stdId;
    const modal = document.getElementById('modal-project-tracking');
    if (modal) {
        document.getElementById('project-tracking-std-name').textContent = `${stdId} - ${stdName}`;
        
        // Load data from localStorage
        const data = JSON.parse(localStorage.getItem('projectTracking_' + stdId) || '{}');
        document.getElementById('pt-project-name').value = data.projectName || '';
        
        // Render history
        const histContainer = document.getElementById('advisor-pt-history');
        if (histContainer) {
            if (!data.weeklyReports || data.weeklyReports.length === 0) {
                histContainer.innerHTML = '<div style="font-size: 11px; color: var(--text-muted); text-align: center; padding: 16px; background: #f8fafc; border-radius: 8px;">ยังไม่มีการบันทึกงานจากนิสิต</div>';
            } else {
                const sorted = [...data.weeklyReports].sort((a, b) => b.week - a.week);
                histContainer.innerHTML = sorted.map(r => `
                    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                            <span style="font-weight: 700; font-size: 13px; color: #0f766e;">สัปดาห์ที่ ${r.week}</span>
                            <span class="status-badge badge-success" style="font-size: 10px;">บันทึกแล้ว</span>
                        </div>
                        <div style="font-size: 11px; color: #475569; margin-bottom: 4px;">
                            <strong>บันทึกงาน / ปัญหา:</strong> ${r.issues || '-'}
                        </div>
                        ${r.images && r.images.length > 0 ? `
                            <div style="margin: 8px 0;">
                                <div style="font-size: 10.5px; font-weight: 600; color: #64748b; margin-bottom: 4px;">รูปภาพประกอบ (${r.images.length} รูป):</div>
                                <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                                    ${r.images.map((imgSrc, idx) => `
                                        <div style="position: relative; border-radius: 6px; overflow: hidden; border: 1px solid #cbd5e1; width: 64px; height: 64px; cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,0.06);" onclick="viewImagePreviewModal('${imgSrc}', 'รูปภาพสัปดาห์ที่ ${r.week} - นิสิต ${stdName}')" title="คลิกเพื่อดูรูปภาพขนาดใหญ่">
                                            <img src="${imgSrc}" style="width: 100%; height: 100%; object-fit: cover;" alt="รูปสัปดาห์ที่ ${r.week}">
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        ` : ''}
                        <div style="font-size: 10px; color: #94a3b8; text-align: right;">อัปเดตเมื่อ: ${r.dateStr}</div>
                    </div>
                `).join('');
            }
        }
        
        modal.style.display = 'flex';
    }
}

function closeProjectTrackingModal() {
    const modal = document.getElementById('modal-project-tracking');
    if (modal) modal.style.display = 'none';
}

// แสดงรายการประวัติการบันทึกงานของนิสิต
function renderStudentProjectHistory(stdId, data) {
    const container = document.getElementById('std-tracking-history-container');
    if (!container) return;
    
    if (!data.weeklyReports || data.weeklyReports.length === 0) {
        container.innerHTML = '<div style="font-size: 11px; color: var(--text-muted); text-align: center; padding: 16px; background: #f8fafc; border-radius: 8px;">ยังไม่มีประวัติการบันทึกงาน</div>';
        return;
    }

    const sorted = [...data.weeklyReports].sort((a, b) => b.week - a.week);
    container.innerHTML = sorted.map(r => `
        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                <span style="font-weight: 700; font-size: 13px; color: #0f766e;">สัปดาห์ที่ ${r.week}</span>
                <span class="status-badge badge-success" style="font-size: 10px;">บันทึกแล้ว</span>
            </div>
            <div style="font-size: 11px; color: #475569; margin-bottom: 6px;">
                <strong>บันทึกงาน / ปัญหา:</strong> ${r.issues || '-'}
            </div>
            ${r.images && r.images.length > 0 ? `
                <div style="margin: 8px 0;">
                    <div style="font-size: 10.5px; font-weight: 600; color: #64748b; margin-bottom: 4px;">รูปภาพประกอบการปฏิบัติงาน (${r.images.length} รูป):</div>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                        ${r.images.map((imgSrc, idx) => `
                            <div style="position: relative; border-radius: 6px; overflow: hidden; border: 1px solid #cbd5e1; width: 72px; height: 72px; cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,0.06);" onclick="viewImagePreviewModal('${imgSrc}', 'รูปภาพสัปดาห์ที่ ${r.week} (รูปที่ ${idx+1})')" title="คลิกเพื่อดูรูปภาพขนาดใหญ่">
                                <img src="${imgSrc}" style="width: 100%; height: 100%; object-fit: cover;" alt="รูปสัปดาห์ที่ ${r.week}">
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
            <div style="font-size: 10px; color: #94a3b8; text-align: right;">อัปเดตเมื่อ: ${r.dateStr}</div>
        </div>
    `).join('');
}

// โหลดข้อมูลการติดตามงานของนิสิต
function loadStudentProjectTracking(stdId) {
    const data = JSON.parse(localStorage.getItem('projectTracking_' + stdId) || '{}');
    const pName = document.getElementById('student-pt-name');
    if (pName && data.projectName) pName.value = data.projectName;
    
    const pWeek = document.getElementById('student-pt-week');
    if (pWeek && data.weeklyReports && data.weeklyReports.length > 0) {
        const maxWeek = Math.max(...data.weeklyReports.map(r => r.week));
        if (maxWeek < 16) {
            pWeek.value = String(maxWeek + 1);
        } else {
            pWeek.value = '16';
        }
    }
    onStudentWeekChange();
    renderStudentProjectHistory(stdId, data);
}

// บันทึกข้อมูลประจำสัปดาห์ (พร้อมรูปภาพประกอบ)
function saveStudentProjectTracking() {
    const savedSession = (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'));
    if (!savedSession) return;
    const user = JSON.parse(savedSession);
    const stdId = String(user.id || user.student_id);
    
    const data = JSON.parse(localStorage.getItem('projectTracking_' + stdId) || '{"projectName": "", "weeklyReports": []}');
    
    const pName = document.getElementById('student-pt-name').value;
    const weekStr = document.getElementById('student-pt-week').value;
    const issuesText = document.getElementById('student-pt-issues').value;
    const nowStr = new Date().toLocaleString('th-TH');

    if (!pName) { alert('กรุณาระบุหัวข้องาน'); return; }

    data.projectName = pName;
    if (!data.weeklyReports) data.weeklyReports = [];
    
    const wNum = parseInt(weekStr);
    const existingIdx = data.weeklyReports.findIndex(r => r.week === wNum);
    
    const newReport = {
        week: wNum,
        issues: issuesText,
        images: [...currentReportImages],
        dateStr: nowStr
    };

    if (existingIdx >= 0) {
        if (confirm(`สัปดาห์ที่ ${wNum} เคยมีการบันทึกแล้ว ต้องการอัปเดตข้อมูลทับหรือไม่?`)) {
            data.weeklyReports[existingIdx] = newReport;
        } else {
            return;
        }
    } else {
        data.weeklyReports.push(newReport);
    }

    localStorage.setItem('projectTracking_' + stdId, JSON.stringify(data));
    addNotification(`บันทึกงาน สัปดาห์ที่ ${wNum} สำเร็จ`);
    alert('บันทึกข้อมูลประจำสัปดาห์เรียบร้อยแล้ว');
    
    loadStudentProjectTracking(stdId);
}
