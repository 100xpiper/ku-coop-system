// ==========================================================================
// advisor-evidence.js - ระบบบันทึกภาพถ่ายและหลักฐานการลงตรวจนิเทศ
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

/**
 * เปิดหน้าต่าง Modal แสดงและจัดการรูปภาพหลักฐานการนิเทศของนิสิต
 */
function openPhotoModal(id, name, sec) {
    currentSelectedStudentId = id;
    if (sec) currentSelectedClassroom = sec;

    loadDynamicStudentsData();
    let std = null;
    if (currentSelectedClassroom && studentsData[currentSelectedClassroom]) {
        std = studentsData[currentSelectedClassroom].find(s => String(s.id) === String(id));
    }
    if (!std) {
        for (let sSec in studentsData) {
            std = (studentsData[sSec] || []).find(s => String(s.id) === String(id));
            if (std) {
                currentSelectedClassroom = sSec;
                break;
            }
        }
    }
    if (!std) {
        try {
            let customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
            std = customUsers[id] || customUsers[String(id).toLowerCase().trim()];
        } catch (e) {}
    }

    const displayName = (std && std.name) ? std.name : (name || '-');
    const nameEl = document.getElementById('photo-student-name');
    if (nameEl) nameEl.textContent = `${displayName} (${id})`;

    pendingPhotoDataUrl = null;
    const confirmBtn = document.getElementById('btn-confirm-upload-photo');
    if (confirmBtn) confirmBtn.style.display = 'none';
    const noticeEl = document.getElementById('photo-pending-notice');
    if (noticeEl) noticeEl.style.display = 'none';

    const img = document.getElementById('photo-preview-img');
    const emptyText = document.getElementById('photo-empty-text');
    const delBtn = document.getElementById('btn-delete-photo');

    if (std && std.photo) {
        if (img) {
            img.src = std.photo;
            img.style.display = 'block';
        }
        if (emptyText) emptyText.style.display = 'none';
        if (delBtn) delBtn.style.display = 'inline-flex';
    } else {
        if (img) {
            img.src = '';
            img.style.display = 'none';
        }
        if (emptyText) emptyText.style.display = 'block';
        if (delBtn) delBtn.style.display = 'none';
    }

    // เปิดหน้าต่าง Modal (รองรับทั้ง modal-photo-mgmt และ modal-photo-evidence)
    if (typeof openModal === 'function') {
        openModal('modal-photo-mgmt');
        openModal('modal-photo-evidence');
    } else {
        const el = document.getElementById('modal-photo-mgmt') || document.getElementById('modal-photo-evidence');
        if (el) el.style.display = 'flex';
    }
}

/**
 * รับและอ่านไฟล์รูปภาพที่เลือกจากเครื่อง หรือถ่ายจากกล้อง
 */
function handlePhotoSelected(event) {
    const file = event.target.files && event.target.files[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
        alert('กรุณาเลือกไฟล์รูปภาพเท่านั้น (เช่น JPG, PNG, WEBP)');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        pendingPhotoDataUrl = e.target.result;

        const img = document.getElementById('photo-preview-img');
        const emptyText = document.getElementById('photo-empty-text');
        const confirmBtn = document.getElementById('btn-confirm-upload-photo');
        const noticeEl = document.getElementById('photo-pending-notice');

        if (img) {
            img.src = pendingPhotoDataUrl;
            img.style.display = 'block';
        }
        if (emptyText) emptyText.style.display = 'none';
        if (confirmBtn) confirmBtn.style.display = 'inline-flex';
        if (noticeEl) noticeEl.style.display = 'block';
    };
    reader.readAsDataURL(file);
    event.target.value = '';
}

/**
 * บันทึกรูปถ่ายหลักฐานลงในระบบ LocalStorage และ Database
 */
async function confirmPhotoUpload() {
    if (!pendingPhotoDataUrl) {
        alert('โปรดเลือกรูปภาพหรือถ่ายรูปก่อนกดยืนยันการอัปโหลด');
        return;
    }

    loadDynamicStudentsData();
    let std = null;
    if (currentSelectedClassroom && studentsData[currentSelectedClassroom]) {
        std = studentsData[currentSelectedClassroom].find(s => String(s.id) === String(currentSelectedStudentId));
    }
    if (!std) {
        for (let sSec in studentsData) {
            std = (studentsData[sSec] || []).find(s => String(s.id) === String(currentSelectedStudentId));
            if (std) break;
        }
    }
    if (!std) {
        try {
            let customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
            std = customUsers[currentSelectedStudentId];
        } catch (e) {}
    }

    if (std) {
        std.photo = pendingPhotoDataUrl;
        // บันทึกลง customUsers ใน localStorage
        try {
            let customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
            const emailKey = String(std.email || '').toLowerCase().trim();
            if (emailKey && customUsers[emailKey]) {
                customUsers[emailKey].photo = pendingPhotoDataUrl;
            }
            if (customUsers[std.id]) {
                customUsers[std.id].photo = pendingPhotoDataUrl;
            }
            if (std.student_id && customUsers[std.student_id]) {
                customUsers[std.student_id].photo = pendingPhotoDataUrl;
            }
            localStorage.setItem('customUsers', JSON.stringify(customUsers));
        } catch (err) {}

        // บันทึกลง Supabase DB (หากเชื่อมต่ออยู่)
        try {
            if (typeof dbUploadPhoto === 'function') {
                await dbUploadPhoto(std.id || std.student_id, pendingPhotoDataUrl);
            }
        } catch (err) {}

        alert(`อัปโหลดและบันทึกรูปถ่ายหลักฐานของ ${std.name} เรียบร้อยแล้ว`);
        pendingPhotoDataUrl = null;
        openPhotoModal(std.id, std.name, currentSelectedClassroom);
        if (typeof renderAdvisorPhotosPage === 'function') renderAdvisorPhotosPage();
        if (typeof renderStudentList === 'function') renderStudentList();
    }
}

/**
 * ลบรูปภาพหลักฐานการออกตรวจนิเทศ
 */
function deletePhotoEvidence() {
    if (!confirm('คุณต้องการลบรูปภาพหลักฐานการออกตรวจนี้หรือไม่?')) return;
    loadDynamicStudentsData();
    let std = null;
    if (currentSelectedClassroom && studentsData[currentSelectedClassroom]) {
        std = studentsData[currentSelectedClassroom].find(s => String(s.id) === String(currentSelectedStudentId));
    }
    if (!std) {
        for (let sSec in studentsData) {
            std = (studentsData[sSec] || []).find(s => String(s.id) === String(currentSelectedStudentId));
            if (std) break;
        }
    }
    if (!std) {
        try {
            let customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
            std = customUsers[currentSelectedStudentId];
        } catch (e) {}
    }

    if (std) {
        std.photo = '';
        pendingPhotoDataUrl = null;
        try {
            let customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
            const emailKey = String(std.email || '').toLowerCase().trim();
            if (emailKey && customUsers[emailKey]) {
                customUsers[emailKey].photo = '';
            }
            if (customUsers[std.id]) {
                customUsers[std.id].photo = '';
            }
            if (std.student_id && customUsers[std.student_id]) {
                customUsers[std.student_id].photo = '';
            }
            localStorage.setItem('customUsers', JSON.stringify(customUsers));
        } catch (err) {}

        alert('ลบรูปภาพหลักฐานเรียบร้อยแล้ว');
        openPhotoModal(std.id, std.name, currentSelectedClassroom);
        if (typeof renderAdvisorPhotosPage === 'function') renderAdvisorPhotosPage();
        if (typeof renderStudentList === 'function') renderStudentList();
    }
}

/**
 * แสดงตารางรายชื่อนิสิตในความดูแลและสถานะรูปหลักฐานการตรวจนิเทศ
 */
function renderAdvisorPhotosPage() {
    const tbody = document.getElementById('adv-photos-table-body');
    if (!tbody) return;
    tbody.innerHTML = '';

    loadDynamicStudentsData();
    const { mySecNormal, mySecSpecial } = getAdvisorSections();

    // เติมตัวเลือกหมู่เรียน
    const secSelect = document.getElementById('adv-photo-sec-select');
    if (secSelect) {
        const optNormal = secSelect.querySelector('option[value="normal"]');
        if (optNormal) optNormal.textContent = `${mySecNormal} (ภาคปกติ)`;
        const optSpecial = secSelect.querySelector('option[value="special"]');
        if (optSpecial) optSpecial.textContent = `${mySecSpecial} (ภาคพิเศษ)`;
    }

    const secChoice = secSelect ? secSelect.value : 'all';
    const searchVal = document.getElementById('adv-photo-search-input') ? document.getElementById('adv-photo-search-input').value.trim().toLowerCase() : '';

    let targetSections = [];
    if (secChoice === 'normal') {
        targetSections = [mySecNormal];
    } else if (secChoice === 'special') {
        targetSections = [mySecSpecial];
    } else {
        targetSections = [mySecNormal, mySecSpecial];
    }

    let allList = [];
    targetSections.forEach(sec => {
        const list = studentsData[sec] || [];
        list.forEach(std => {
            allList.push({ ...std, _assignedSection: sec });
        });
    });

    // กรองตามคำค้นหา
    if (searchVal) {
        allList = allList.filter(s => 
            (s.id && String(s.id).toLowerCase().includes(searchVal)) ||
            (s.name && s.name.toLowerCase().includes(searchVal)) ||
            (s.company && s.company.toLowerCase().includes(searchVal))
        );
    }

    const countBadge = document.getElementById('adv-photos-count-badge');
    if (countBadge) countBadge.textContent = `${allList.length} คน`;

    if (allList.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 24px; color: var(--text-muted); font-size: 12px;">ไม่พบรายชื่อนิสิตในตัวกรองนี้</td></tr>`;
        return;
    }

    allList.forEach(std => {
        const hasPhoto = !!(std.photo && std.photo.length > 0);
        const tr = document.createElement('tr');
        tr.style.borderBottom = '1px solid var(--border-color)';

        const safeId = String(std.id || '').replace(/'/g, "\\'");
        const safeName = String(std.name || '').replace(/'/g, "\\'");
        const safeSec = String(std.section || std._assignedSection || '').replace(/'/g, "\\'");

        tr.innerHTML = `
            <td style="padding: 10px 12px; font-weight: 700; color: var(--primary-color); white-space: nowrap;">${std.id}</td>
            <td style="padding: 10px 12px; font-weight: 600; color: var(--text-main);">${std.name}</td>
            <td style="padding: 10px 12px; white-space: nowrap; color: #475569; font-weight: 600;">${std.section || std._assignedSection}</td>
            <td style="padding: 10px 12px; color: #334155;">${std.company || '-'}</td>
            <td style="padding: 10px 12px; white-space: nowrap;">
                ${hasPhoto ? 
                    `<span class="status-badge badge-success" style="display: inline-flex; align-items: center; gap: 4px;">มีรูปหลักฐานแล้ว</span>` : 
                    `<span class="status-badge badge-neutral" style="color: #64748b;">ยังไม่มีรูป</span>`
                }
            </td>
            <td style="padding: 10px 12px; text-align: center; white-space: nowrap;">
                <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                    ${hasPhoto ? `
                        <img src="${std.photo}" alt="รูปหลักฐาน" style="width: 32px; height: 32px; object-fit: cover; border-radius: 4px; border: 1px solid var(--border-color); cursor: pointer;" onclick="openPhotoModal('${safeId}', '${safeName}', '${safeSec}')" title="คลิกเพื่อดูรูปใหญ่">
                        <button type="button" class="btn-primary" style="padding: 5px 10px; font-size: 11px; background-color: #0284c7;" onclick="openPhotoModal('${safeId}', '${safeName}', '${safeSec}')">
                            ดู / จัดการรูป
                        </button>
                    ` : `
                        <button type="button" class="btn-primary" style="padding: 5px 10px; font-size: 11px; background-color: #059669; display: inline-flex; align-items: center; gap: 4px;" onclick="openPhotoModal('${safeId}', '${safeName}', '${safeSec}')">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                            <span>+ แนบรูป / ถ่ายรูป</span>
                        </button>
                    `}
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}
