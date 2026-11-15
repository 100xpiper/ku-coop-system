// ==========================================================================
// utils.js - ฟังก์ชันช่วยเหลือทั่วไป (Utilities & Helpers)
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

function updateClock() {
            const now = new Date();
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const el = document.getElementById('live-time');
            if (el) el.textContent = `${hours}:${minutes}`;
        }
        updateClock();
        setInterval(updateClock, 1000);



function formatThaiDate(dateObj) {
    if (!dateObj) return '-';
    try {
        const d = new Date(dateObj);
        return d.toLocaleDateString('th-TH', { day: 'numeric', month: 'short', year: 'numeric' });
    } catch(e) {
        return String(dateObj);
    }
}

function playBeepSound(freq = 880, durationMs = 150) {
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.frequency.value = freq;
        gain.gain.value = 0.15;
        osc.start();
        setTimeout(() => {
            osc.stop();
            audioCtx.close();
        }, durationMs);
    } catch (e) {}
}
