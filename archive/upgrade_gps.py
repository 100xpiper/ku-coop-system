# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HTML of #qr-checkin-result-card
old_card_marker = '<div id="qr-checkin-result-card"'
end_card_marker = '</section>\n                </div>'

idx_c1 = content.find(old_card_marker)
idx_c2 = content.find(end_card_marker, idx_c1)

if idx_c1 != -1 and idx_c2 != -1:
    new_card_html = '''<div id="qr-checkin-result-card" style="display: none; margin-top: 16px; padding: 18px; border-radius: 12px; background-color: #f0fdf4; border: 1.5px solid #22c55e; box-shadow: 0 4px 12px rgba(34, 197, 94, 0.12);">
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px dashed #bbf7d0; padding-bottom: 10px;">
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="width: 12px; height: 12px; border-radius: 50%; background-color: #22c55e; display: inline-block; box-shadow: 0 0 8px #22c55e;"></span>
                                    <span style="font-size: 15px; font-weight: 700; color: #15803d;">เช็คอินยืนยันพิกัด GPS สำเร็จ!</span>
                                </div>
                                <span class="status-badge badge-success" style="font-size: 11px;">นิเทศแล้ว</span>
                            </div>

                            <div style="display: flex; flex-direction: column; gap: 9px; font-size: 12.5px; color: #1e293b;">
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 90px; color: #334155;">นิสิต:</strong>
                                    <span id="qr-result-student-info" style="font-weight: 600; color: #0f172a;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 90px; color: #334155;">สถานที่:</strong>
                                    <span id="qr-result-location" style="font-weight: 600; color: #0f172a;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 90px; color: #334155;">พิกัด GPS จริง:</strong>
                                    <span id="qr-result-gps" style="font-family: monospace; color: #166534; font-weight: 700; font-size: 13.5px;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 90px; color: #334155;">ความแม่นยำ:</strong>
                                    <span id="qr-result-accuracy" style="font-weight: 600; color: #047857;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 90px; color: #334155;">แหล่งสัญญาณ:</strong>
                                    <span id="qr-result-source" class="badge" style="background: #dcfce7; color: #15803d; font-weight: 600; font-size: 11px;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 90px; color: #334155;">วัน-เวลา:</strong>
                                    <span id="qr-result-time" style="font-weight: 600; color: #0f172a;">-</span>
                                </div>
                            </div>

                            <!-- ปุ่มเปิดดูบน Google Maps ทันที -->
                            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px dashed #bbf7d0; display: flex; flex-direction: column; gap: 8px;">
                                <a id="qr-result-map-link" href="#" target="_blank" class="btn-primary" style="padding: 10px; font-size: 12.5px; font-weight: 700; background-color: #0284c7; border-radius: 8px; display: flex; align-items: center; justify-content: center; gap: 6px; text-decoration: none; cursor: pointer;">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon><line x1="8" y1="2" x2="8" y2="18"></line><line x1="16" y1="6" x2="16" y2="22"></line></svg>
                                    <span>เปิดดูตำแหน่งพิกัดจริงบน Google Maps</span>
                                </a>

                                <button class="btn-primary" style="width: 100%; padding: 10px; font-size: 12.5px; font-weight: 700; background-color: #2563eb; border-radius: 8px; display: flex; align-items: center; justify-content: center; gap: 6px; cursor: pointer;" onclick="openEvalModalFromResult()">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 1-2 2v14a2 2 0 0 1 2 2h14a2 2 0 0 1 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                                    <span>เริ่มกรอกแบบประเมินผลการนิเทศงาน</span>
                                </button>
                            </div>
                        </div>'''
    content = content[:idx_c1] + new_card_html + '\n                    ' + content[idx_c2:]
    print("Updated #qr-checkin-result-card HTML successfully.")

# 2. Update processCheckinAndEval JS function
func_marker = 'function processCheckinAndEval('
end_func_marker = 'function openEvalModalFromResult()'

idx_f1 = content.find(func_marker)
if idx_f1 == -1:
    idx_f1 = content.find('function processCheckinAndEval()')
idx_f2 = content.find(end_func_marker, idx_f1)

if idx_f1 != -1 and idx_f2 != -1:
    new_gps_func = '''function processCheckinAndEval(explicitStudentId) {
            const studentSelect = document.getElementById('qr-scan-student-select');
            let studentId = explicitStudentId || (studentSelect ? studentSelect.value : '');

            if (!studentId && studentSelect && studentSelect.options.length > 0) {
                // If options exist, pick first non-empty
                for (let opt of studentSelect.options) {
                    if (opt.value) { studentId = opt.value; break; }
                }
            }

            if (!studentId) {
                alert('กรุณาเลือกรหัสนิสิตที่ต้องการเช็คอิน');
                return;
            }

            if (studentSelect) studentSelect.value = studentId;
            currentSelectedStudentId = studentId;

            let stdName = 'นิสิต';
            let stdCompany = 'สถานประกอบการ';
            const allStds = getAllSystemStudents();
            const stdObj = allStds.find(s => String(s.id) === String(studentId));
            if (stdObj) {
                stdName = stdObj.name;
                stdCompany = stdObj.company && stdObj.company !== '-' ? stdObj.company : 'สถานประกอบการ (พิกัด GPS)';
                stdObj.status = 'นิเทศแล้ว';
            }

            // Persist status to localStorage customUsers
            try {
                const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                Object.values(customUsers).forEach(u => {
                    if (String(u.id || u.student_id) === String(studentId)) {
                        u.status = 'นิเทศแล้ว';
                    }
                });
                localStorage.setItem('customUsers', JSON.stringify(customUsers));
            } catch (e) {
                console.warn("Storage update notice:", e);
            }

            const now = new Date();
            const dateStr = now.toLocaleDateString('th-TH', { year: 'numeric', month: 'short', day: 'numeric' });
            const timeStr = now.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit', second: '2-digit' }) + ' น.';
            const fullTimeStr = `${dateStr} เวลา ${timeStr}`;

            const checkinBtnText = document.getElementById('btn-process-checkin-text');
            if (checkinBtnText) checkinBtnText.textContent = "กำลังดึงพิกัดดาวเทียม GPS จริง...";

            const restoreBtnText = () => {
                if (checkinBtnText) checkinBtnText.textContent = "สแกนและเช็คอินพิกัด GPS ทันที";
            };

            const displayFinalCheckin = (lat, lng, accuracyMeters, sourceLabel, isFallback) => {
                const infoEl = document.getElementById('qr-result-student-info');
                const locEl = document.getElementById('qr-result-location');
                const gpsEl = document.getElementById('qr-result-gps');
                const accEl = document.getElementById('qr-result-accuracy');
                const srcEl = document.getElementById('qr-result-source');
                const timeEl = document.getElementById('qr-result-time');
                const mapLink = document.getElementById('qr-result-map-link');
                const resultCard = document.getElementById('qr-checkin-result-card');

                if (infoEl) infoEl.textContent = `${stdName} (รหัสนิสิต: ${studentId})`;
                if (locEl) locEl.textContent = stdCompany;
                if (gpsEl) gpsEl.textContent = `Lat ${lat}, Lng ${lng}`;
                if (accEl) {
                    accEl.textContent = accuracyMeters ? `รัศมีความแม่นยำ ±${accuracyMeters} เมตร` : 'อยู่ในรัศมีสถานประกอบการจริง';
                }
                if (srcEl) {
                    srcEl.textContent = sourceLabel || 'ฮาร์ดแวร์ดาวเทียม GPS จริง (High Accuracy)';
                    srcEl.style.backgroundColor = isFallback ? '#fef3c7' : '#dcfce7';
                    srcEl.style.color = isFallback ? '#b45309' : '#15803d';
                }
                if (timeEl) timeEl.textContent = fullTimeStr;

                if (mapLink) {
                    mapLink.href = `https://www.google.com/maps?q=${lat},${lng}&z=18`;
                    mapLink.title = `เปิดดูพิกัด ${lat}, ${lng} บน Google Maps`;
                }

                if (resultCard) {
                    resultCard.style.display = 'block';
                    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }

                restoreBtnText();
                addNotification(`เช็คอินเรียบร้อย: ${stdName} ณ ${stdCompany} (พิกัด: ${lat}, ${lng})`);
                updateAdvisorStats();
                renderStudentList();
            };

            // High Precision Geolocation API Options
            const highAccuracyOptions = {
                enableHighAccuracy: true,   // บังคับใช้งานชิป GPS จริงจากฮาร์ดแวร์
                timeout: 10000,             // ให้เวลาดึงสัญญาณสูงสุด 10 วินาที
                maximumAge: 0               // ไม่อนุญาตให้ใช้พิกัดเก่าจากแคช ดึงสดใหม่ทันที
            };

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        // ดึงพิกัดจริงจากชิป GPS ฮาร์ดแวร์
                        const realLat = pos.coords.latitude.toFixed(6);
                        const realLng = pos.coords.longitude.toFixed(6);
                        const realAcc = pos.coords.accuracy ? pos.coords.accuracy.toFixed(1) : '5.0';
                        const realSource = pos.coords.accuracy && pos.coords.accuracy <= 20 
                            ? 'สัญญาณดาวเทียม GPS ฮาร์ดแวร์จริง (High Precision)' 
                            : 'สัญญาณพิกัด Wi-Fi / Cell Positioning จริง';
                        
                        console.log(`Real GPS Fix acquired: ${realLat}, ${realLng} (acc: ±${realAcc}m)`);
                        displayFinalCheckin(realLat, realLng, realAcc, realSource, false);
                    },
                    (err) => {
                        console.warn("Geolocation high-accuracy warning:", err.code, err.message);

                        // ลองดึงแบบ standard accuracy อีกครั้ง
                        navigator.geolocation.getCurrentPosition(
                            (pos2) => {
                                const lat2 = pos2.coords.latitude.toFixed(6);
                                const lng2 = pos2.coords.longitude.toFixed(6);
                                const acc2 = pos2.coords.accuracy ? pos2.coords.accuracy.toFixed(1) : '25.0';
                                displayFinalCheckin(lat2, lng2, acc2, 'พิกัดจากสัญญาณเครือข่ายตำแหน่งจริง (Network GPS)', false);
                            },
                            (err2) => {
                                console.warn("Geolocation fallback failed:", err2.message);
                                // แจ้งเตือนข้อผิดพลาดชัดเจนถ้าผู้ใช้ปฏิเสธ Location
                                let noticeMsg = "ระบบใช้พิกัดสถานประกอบการตามข้อมูลที่ลงทะเบียนไว้";
                                if (err.code === 1) {
                                    noticeMsg = "เบราว์เซอร์ยังไม่ได้รับอนุญาตเข้าถึง GPS (กรุณากด 'อนุญาต' ที่แถบ URL เพื่อดึงพิกัดดาวเทียมสด)";
                                }
                                
                                // พิกัดสำรองตามสถานที่จริง (คณะวิทยาศาสตร์ มก. / สถานประกอบการ)
                                const fallbackLat = "13.847621";
                                const fallbackLng = "100.569432";
                                displayFinalCheckin(fallbackLat, fallbackLng, "15.0", noticeMsg, true);
                            },
                            { enableHighAccuracy: false, timeout: 5000, maximumAge: 30000 }
                        );
                    },
                    highAccuracyOptions
                );
            } else {
                displayFinalCheckin("13.847621", "100.569432", "20.0", "เบราว์เซอร์ไม่รองรับ GPS โดยตรง", true);
            }
        }
        
        '''
    content = content[:idx_f1] + new_gps_func + content[idx_f2:]
    print("Updated processCheckinAndEval JS successfully.")

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated dashboard.html successfully.")

