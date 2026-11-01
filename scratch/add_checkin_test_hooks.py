# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = "const targetModal = urlParams.get('modal');"
assert target in content, "targetModal not found"

hook_snippet = """const targetModal = urlParams.get('modal');

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
            }"""

if target in content and "test_checkin" not in content:
    content = content.replace(target, hook_snippet, 1)
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added checkin test hooks to dashboard.html successfully.")
else:
    print("Hook already present or target missing.")

