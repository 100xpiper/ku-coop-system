// ==========================================================================
// modal.js - ระบบจัดการเปิด-ปิดหน้าต่างป็อปอัป (Modal Manager)
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

function openModal(modalId) {
    if (modalId === 'modal-photo-evidence' || modalId === 'modal-photo-mgmt') {
        const el1 = document.getElementById('modal-photo-mgmt');
        const el2 = document.getElementById('modal-photo-evidence');
        if (el1) el1.style.display = 'flex';
        if (el2) el2.style.display = 'flex';
        return;
    }
    const el = document.getElementById(modalId);
    if (el) el.style.display = 'flex';
}

function closeModal(modalId) {
    if (modalId === 'modal-photo-evidence' || modalId === 'modal-photo-mgmt') {
        const el1 = document.getElementById('modal-photo-mgmt');
        const el2 = document.getElementById('modal-photo-evidence');
        if (el1) el1.style.display = 'none';
        if (el2) el2.style.display = 'none';
        return;
    }
    const el = document.getElementById(modalId);
    if (el) el.style.display = 'none';
}

// ==================== BLANK FORM TEMPLATES SYSTEM ====================
