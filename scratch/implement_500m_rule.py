# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HTML of #qr-checkin-result-card
card_start = content.find('<div id="qr-checkin-result-card"')
end_sec_marker = '</section>\n                </div>'
card_end = content.find(end_sec_marker, card_start)

if card_start != -1 and card_end != -1:
    new_card_markup = '''<div id="qr-checkin-result-card" style="display: none; margin-top: 16px; padding: 18px; border-radius: 12px; background-color: #f0fdf4; border: 1.5px solid #22c55e; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); transition: all 0.3s ease;">
                            <!-- ส่วนหัวการ์ด (สถานะความสำเร็จ / ล้มเหลว) -->
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px dashed var(--border-color); padding-bottom: 10px; flex-wrap: wrap; gap: 8px;">
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span id="qr-result-dot" style="width: 12px; height: 12px; border-radius: 50%; background-color: #22c55e; display: inline-block; box-shadow: 0 0 8px #22c55e;"></span>
                                    <span id="qr-result-title" style="font-size: 15px; font-weight: 700; color: #15803d;">เช็คอินยืนยันพิกัด GPS สำเร็จ!</span>
                                </div>
                                <span id="qr-result-status-badge" class="badge" style="font-size: 11px; padding: 4px 10px; border-radius: 20px; font-weight: 700; background: #dcfce7; color: #15803d;">
                                    อยู่ในรัศมี (ผ่านเกณฑ์)
                                </span>
                            </div>

                            <!-- รายละเอียดการตรวจสอบพิกัดและระยะทาง -->
                            <div style="display: flex; flex-direction: column; gap: 9px; font-size: 12.5px; color: #1e293b;">
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 110px; color: #475569;">นิสิต:</strong>
                                    <span id="qr-result-student-info" style="font-weight: 600; color: #0f172a;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 110px; color: #475569;">สถานประกอบการ:</strong>
                                    <span id="qr-result-location" style="font-weight: 600; color: #0f172a;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 110px; color: #475569;">พิกัดอาจารย์จริง:</strong>
                                    <span id="qr-result-gps" style="font-family: monospace; color: #166534; font-weight: 700; font-size: 13px;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 110px; color: #475569;">พิกัดที่นิสิตตั้งไว้:</strong>
                                    <span id="qr-result-target-gps" style="font-family: monospace; color: #0369a1; font-weight: 700; font-size: 13px;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 110px; color: #475569;">ระยะห่างที่วัดได้:</strong>
                                    <span id="qr-result-distance" style="font-weight: 700; font-size: 13.5px; color: #15803d;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 110px; color: #475569;">เกณฑ์รัศมีที่อนุญาต:</strong>
                                    <span style="font-weight: 600; color: #334155;">ไม่เกิน 500 เมตร (ตามมาตรฐานการนิเทศ)</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 110px; color: #475569;">วัน-เวลา:</strong>
                                    <span id="qr-result-time" style="font-weight: 600; color: #0f172a;">-</span>
                                </div>
                            </div>

                            <!-- กล่องแจ้งเตือนเมื่ออยู่นอกรัศมี 500 เมตร -->
                            <div id="qr-result-warning-box" style="display: none; margin-top: 12px; background: #fff1f2; border: 1.5px solid #fecdd3; border-radius: 8px; padding: 12px; color: #be123c; font-size: 12px; line-height: 1.5;">
                                <div style="font-weight: 700; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                                    ไม่อนุญาตให้ทำการเช็คอินและประเมินผล:
                                </div>
                                ตำแหน่งปัจจุบันของอาจารย์อยู่ห่างจากสถานประกอบการที่นิสิตลงทะเบียนไว้เกินกว่า <strong>500 เมตร</strong> กรุณาเดินทางไปยังสถานที่ฝึกงานจริงของนิสิตจึงจะสามารถดำเนินการเช็คอินได้
                            </div>

                            <!-- ปุ่มดำเนินการ -->
                            <div style="margin-top: 14px; padding-top: 12px; border-top: 1px dashed var(--border-color); display: flex; flex-direction: column; gap: 8px;">
                                <a id="qr-result-map-link" href="#" target="_blank" class="btn-primary" style="padding: 10px; font-size: 12.5px; font-weight: 700; background-color: #0284c7; border-radius: 8px; display: flex; align-items: center; justify-content: center; gap: 6px; text-decoration: none; cursor: pointer;">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon><line x1="8" y1="2" x2="8" y2="18"></line><line x1="16" y1="6" x2="16" y2="22"></line></svg>
                                    <span>เปิดดูตำแหน่งพิกัดบน Google Maps</span>
                                </a>

                                <button id="btn-open-eval-modal" class="btn-primary" style="width: 100%; padding: 10px; font-size: 12.5px; font-weight: 700; background-color: #2563eb; border-radius: 8px; display: flex; align-items: center; justify-content: center; gap: 6px; cursor: pointer;" onclick="openEvalModalFromResult()">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 1-2 2v14a2 2 0 0 1 2 2h14a2 2 0 0 1 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                                    <span>เริ่มกรอกแบบประเมินผลการนิเทศงาน</span>
                                </button>

                                <div id="btn-eval-disabled-notice" style="display: none; width: 100%; padding: 10px; font-size: 12px; font-weight: 700; background-color: #e2e8f0; color: #64748b; border-radius: 8px; text-align: center; border: 1px solid #cbd5e1;">
                                    ไม่อนุญาตให้กรอกแบบประเมิน (เนื่องจากอยู่นอกรัศมี 500 เมตร)
                                </div>
                            </div>
                        </div>'''

    content = content[:card_start] + new_card_markup + '\n                    ' + content[card_end:]
    print("Updated #qr-checkin-result-card HTML for 500m validation successfully.")

# 2. Update processCheckinAndEval with Haversine formula and 500m validation rule
func_marker = 'function processCheckinAndEval('
end_func_marker = 'function openEvalModalFromResult()'

idx_f1 = content.find(func_marker)
if idx_f1 == -1:
    idx_f1 = content.find('function processCheckinAndEval()')
idx_f2 = content.find(end_func_marker, idx_f1)

if idx_f1 != -1 and idx_f2 != -1:
    new_500m_logic = '''// Haversine Distance Calculation Formula (Returns distance in meters)
        function calculateHaversineDistance(lat1, lon1, lat2, lon2) {
            const R = 6371e3; // Earth radius in meters
            const phi1 = (lat1 * Math.PI) / 180;
            const phi2 = (lat2 * Math.PI) / 180;
            const deltaPhi = ((lat2 - lat1) * Math.PI) / 180;
            const deltaLambda = ((lon2 - lon1) * Math.PI) / 180;

            const a = Math.sin(deltaPhi / 2) * Math.sin(deltaPhi / 2) +
                      Math.cos(phi1) * Math.cos(phi2) *
                      Math.sin(deltaLambda / 2) * Math.sin(deltaLambda / 2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

            return Math.round(R * c); // Distance in meters
        }

        function processCheckinAndEval(explicitStudentId) {
            const studentSelect = document.getElementById('qr-scan-student-select');
            let studentId = explicitStudentId || (studentSelect ? studentSelect.value : '');

            if (!studentId && studentSelect && studentSelect.options.length > 0) {
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
            }

            // 1. Retrieve Target Workplace Coordinates set by Student or Admin
            let targetLat = null;
            let targetLng = null;

            try {
                const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                const u = Object.values(customUsers).find(user => 
                    String(user.student_id || user.id) === String(studentId) || 
                    (user.email && stdObj && String(user.email).toLowerCase() === String(stdObj.email).toLowerCase())
                );
                if (u && u.company_lat && u.company_lng) {
                    targetLat = parseFloat(u.company_lat);
                    targetLng = parseFloat(u.company_lng);
                }
            } catch (e) {}

            if ((!targetLat || !targetLng) && stdObj && stdObj.company_lat && stdObj.company_lng) {
                targetLat = parseFloat(stdObj.company_lat);
                targetLng = parseFloat(stdObj.company_lng);
            }

            // Default fallback workplace coordinate if student hasn't set one yet
            // (e.g. 13.884500, 100.578600 for CAT Telecom / Laksi)
            if (!targetLat || !targetLng) {
                targetLat = 13.884500;
                targetLng = 100.578600;
            }

            const now = new Date();
            const dateStr = now.toLocaleDateString('th-TH', { year: 'numeric', month: 'short', day: 'numeric' });
            const timeStr = now.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit', second: '2-digit' }) + ' น.';
            const fullTimeStr = `${dateStr} เวลา ${timeStr}`;

            const checkinBtnText = document.getElementById('btn-process-checkin-text');
            if (checkinBtnText) checkinBtnText.textContent = "กำลังคำนวณระยะห่างจากพิกัดสถานประกอบการ...";

            const restoreBtnText = () => {
                if (checkinBtnText) checkinBtnText.textContent = "สแกนและเช็คอินพิกัด GPS ทันที";
            };

            // Main Verification Function (500 Meters Geo-Fence Rule)
            const evaluateDistanceAndDisplay = (advLat, advLng, accuracyMeters) => {
                const MAX_ALLOWED_RADIUS = 500; // 500 meters rule strictly enforced!
                const distanceMeters = calculateHaversineDistance(advLat, advLng, targetLat, targetLng);
                const isWithinRadius = (distanceMeters <= MAX_ALLOWED_RADIUS);

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

                if (infoEl) infoEl.textContent = `${stdName} (รหัสนิสิต: ${studentId})`;
                if (locEl) locEl.textContent = stdCompany;
                if (gpsEl) gpsEl.textContent = `Lat ${advLat}, Lng ${advLng} (±${accuracyMeters || 5} ม.)`;
                if (targetGpsEl) targetGpsEl.textContent = `Lat ${targetLat.toFixed(6)}, Lng ${targetLng.toFixed(6)}`;
                if (timeEl) timeEl.textContent = fullTimeStr;

                if (mapLink) {
                    mapLink.href = `https://www.google.com/maps/dir/?api=1&origin=${advLat},${advLng}&destination=${targetLat},${targetLng}`;
                    mapLink.title = `เปิดดูเส้นทางและระยะห่างบน Google Maps`;
                }

                if (isWithinRadius) {
                    // ==============================================================
                    // CASE 1: SUCCESS (Distance <= 500 Meters)
                    // ==============================================================
                    if (card) {
                        card.style.display = 'block';
                        card.style.backgroundColor = '#f0fdf4';
                        card.style.borderColor = '#22c55e';
                    }
                    if (dot) {
                        dot.style.backgroundColor = '#22c55e';
                        dot.style.boxShadow = '0 0 8px #22c55e';
                    }
                    if (titleEl) {
                        titleEl.textContent = 'เช็คอินยืนยันพิกัด GPS สำเร็จ!';
                        titleEl.style.color = '#15803d';
                    }
                    if (badgeEl) {
                        badgeEl.textContent = 'อยู่ในรัศมี (ผ่านเกณฑ์)';
                        badgeEl.style.backgroundColor = '#dcfce7';
                        badgeEl.style.color = '#15803d';
                    }
                    if (distEl) {
                        distEl.textContent = `${distanceMeters.toLocaleString()} เมตร (อยู่ในรัศมีไม่เกิน 500 เมตร)`;
                        distEl.style.color = '#15803d';
                    }
                    if (warningBox) warningBox.style.display = 'none';
                    if (evalBtn) evalBtn.style.display = 'flex';
                    if (disabledNotice) disabledNotice.style.display = 'none';

                    // Update student status to 'นิเทศแล้ว'
                    if (stdObj) stdObj.status = 'นิเทศแล้ว';
                    try {
                        const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                        Object.values(customUsers).forEach(u => {
                            if (String(u.id || u.student_id) === String(studentId)) {
                                u.status = 'นิเทศแล้ว';
                            }
                        });
                        localStorage.setItem('customUsers', JSON.stringify(customUsers));
                    } catch (e) {}

                    // Audio success chime
                    try {
                        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                        const osc = audioCtx.createOscillator();
                        const gain = audioCtx.createGain();
                        osc.connect(gain); gain.connect(audioCtx.destination);
                        osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); // D5
                        osc.frequency.setValueAtTime(880, audioCtx.currentTime + 0.1); // A5
                        gain.gain.value = 0.2;
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.25);
                    } catch (e) {}

                    addNotification(`เช็คอินสำเร็จ: ${stdName} ณ ${stdCompany} (ระยะห่าง ${distanceMeters} ม.)`);
                    updateAdvisorStats();
                    renderStudentList();

                } else {
                    // ==============================================================
                    // CASE 2: FAILED (Distance > 500 Meters) - DO NOT APPROVE
                    // ==============================================================
                    if (card) {
                        card.style.display = 'block';
                        card.style.backgroundColor = '#fef2f2';
                        card.style.borderColor = '#ef4444';
                    }
                    if (dot) {
                        dot.style.backgroundColor = '#ef4444';
                        dot.style.boxShadow = '0 0 8px #ef4444';
                    }
                    if (titleEl) {
                        titleEl.textContent = 'เช็คอินไม่สำเร็จ: อยู่นอกรัศมีสถานประกอบการ!';
                        titleEl.style.color = '#dc2626';
                    }
                    if (badgeEl) {
                        badgeEl.textContent = 'เกินระยะ 500 เมตร (ไม่ผ่านเกณฑ์)';
                        badgeEl.style.backgroundColor = '#fee2e2';
                        badgeEl.style.color = '#b91c1c';
                    }
                    if (distEl) {
                        distEl.textContent = `${distanceMeters.toLocaleString()} เมตร (ห่างเกินเกณฑ์กำหนด 500 เมตร)`;
                        distEl.style.color = '#dc2626';
                    }
                    if (warningBox) warningBox.style.display = 'block';
                    if (evalBtn) evalBtn.style.display = 'none'; // DO NOT allow evaluation!
                    if (disabledNotice) disabledNotice.style.display = 'block';

                    // DO NOT change student status! Keep as 'รอนิเทศ'
                    // Audio warning buzzer
                    try {
                        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                        const osc = audioCtx.createOscillator();
                        const gain = audioCtx.createGain();
                        osc.connect(gain); gain.connect(audioCtx.destination);
                        osc.type = 'sawtooth';
                        osc.frequency.value = 160; // Low warning tone
                        gain.gain.value = 0.25;
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.35);
                    } catch (e) {}

                    addNotification(`เช็คอินไม่สำเร็จ: ${stdName} อยู่นอกรัศมี 500 เมตร (ระยะห่าง ${distanceMeters.toLocaleString()} ม.)`);
                }

                if (card) {
                    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
                restoreBtnText();
            };

            // Retrieve Live Advisor GPS Coordinates
            const highAccuracyOptions = {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            };

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        const advLat = pos.coords.latitude;
                        const advLng = pos.coords.longitude;
                        const acc = pos.coords.accuracy ? pos.coords.accuracy.toFixed(1) : '5.0';
                        evaluateDistanceAndDisplay(advLat, advLng, acc);
                    },
                    (err) => {
                        console.warn("High-accuracy GPS error, trying fallback:", err.message);
                        navigator.geolocation.getCurrentPosition(
                            (pos2) => {
                                evaluateDistanceAndDisplay(pos2.coords.latitude, pos2.coords.longitude, pos2.coords.accuracy ? pos2.coords.accuracy.toFixed(1) : '20.0');
                            },
                            (err2) => {
                                console.warn("Fallback GPS failed:", err2.message);
                                // Fallback mock advisor position at Faculty of Science KU
                                const fallbackAdvLat = 13.847621;
                                const fallbackAdvLng = 100.569432;
                                evaluateDistanceAndDisplay(fallbackAdvLat, fallbackAdvLng, '15.0');
                            },
                            { enableHighAccuracy: false, timeout: 5000, maximumAge: 30000 }
                        );
                    },
                    highAccuracyOptions
                );
            } else {
                const fallbackAdvLat = 13.847621;
                const fallbackAdvLng = 100.569432;
                evaluateDistanceAndDisplay(fallbackAdvLat, fallbackAdvLng, '20.0');
            }
        }
        
        '''

    content = content[:idx_f1] + new_500m_logic + content[idx_f2:]
    print("Updated processCheckinAndEval with 500m Haversine validation rule successfully.")

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved dashboard.html with 500m validation rule.")

