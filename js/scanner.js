// ==========================================================================
// scanner.js - โมดูลกล้องสดสแกน QR Code และคำนวณพิกัด GPS รัศมี 500 เมตร (Haversine)
// โครงงาน: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

// กำหนดรัศมีปลอดภัยสูงสุดสำหรับการเช็คอินตรวจนิเทศ ณ สถานประกอบการ (เมตร)
const MAX_CHECKIN_RADIUS_METERS = 500;
let activeCameraStream = null;
        let cameraScanAnimId = null;
        let cameraScanInterval = null;
        const qrScanCanvas = document.createElement('canvas');
        const qrScanCtx = qrScanCanvas.getContext('2d', { willReadFrequently: true });

        async function startRealCameraScanner() {
            const video = document.getElementById('qr-camera-video');
            const placeholder = document.getElementById('qr-camera-placeholder');
            const laser = document.getElementById('scanner-laser-line');
            const statusBadge = document.getElementById('qr-camera-status-badge');
            const btnStart = document.getElementById('btn-start-camera');
            const btnStop = document.getElementById('btn-stop-camera');

            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                alert('เบราว์เซอร์ของท่านไม่รองรับการเปิดกล้องโดยตรง หรือไม่ได้เปิดผ่านการเชื่อมต่อที่ปลอดภัย (HTTPS / localhost)');
                return;
            }

            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: {
                        facingMode: { ideal: "environment" },
                        width: { ideal: 1280 },
                        height: { ideal: 720 }
                    },
                    audio: false
                });

                activeCameraStream = stream;
                if (video) {
                    video.srcObject = stream;
                    video.setAttribute('playsinline', 'true');
                    await video.play();
                    video.style.display = 'block';
                }

                if (placeholder) placeholder.style.display = 'none';
                if (laser) laser.style.display = 'block';
                if (btnStart) btnStart.style.display = 'none';
                if (btnStop) btnStop.style.display = 'inline-flex';
                if (statusBadge) {
                    statusBadge.textContent = 'กล้องกำลังสแกน QR Code (Active)';
                    statusBadge.style.backgroundColor = '#dcfce7';
                    statusBadge.style.color = '#15803d';
                }

                // Start continuous QR scanning loop
                startQrScanningLoop();

            } catch (err) {
                console.warn('Camera access issue:', err);
                alert('ไม่สามารถเปิดกล้องได้: ' + (err.name === 'NotAllowedError' ? 'โปรดอนุญาตให้เบราว์เซอร์เข้าถึงกล้อง' : err.message) + '\n\nท่านสามารถใช้ปุ่ม "แนบรูปภาพ QR Code" หรือ "สแกนและเช็คอินพิกัด GPS ทันที" ได้ตามปกติ');
            }
        }

        function startQrScanningLoop() {
            const video = document.getElementById('qr-camera-video');
            if (!video) return;

            let lastScanTime = 0;

            function scanStep(timestamp) {
                if (!activeCameraStream) return;

                if (timestamp - lastScanTime > 120) {
                    lastScanTime = timestamp;

                    if (video.readyState >= 2 && video.videoWidth > 0 && video.videoHeight > 0) {
                        try {
                            // High precision decoding via jsQR
                            if (typeof jsQR !== 'undefined') {
                                qrScanCanvas.width = video.videoWidth;
                                qrScanCanvas.height = video.videoHeight;
                                qrScanCtx.drawImage(video, 0, 0, qrScanCanvas.width, qrScanCanvas.height);
                                const imageData = qrScanCtx.getImageData(0, 0, qrScanCanvas.width, qrScanCanvas.height);
                                const code = jsQR(imageData.data, imageData.width, imageData.height, {
                                    inversionAttempts: "dontInvert"
                                });
                                if (code && code.data) {
                                    console.log("jsQR detected payload:", code.data);
                                    handleScannedQrPayload(code.data);
                                    return;
                                }
                            }

                            // Native BarcodeDetector fallback
                            if ('BarcodeDetector' in window) {
                                const bd = new BarcodeDetector({ formats: ['qr_code'] });
                                bd.detect(video).then(barcodes => {
                                    if (barcodes && barcodes.length > 0 && barcodes[0].rawValue) {
                                        console.log("BarcodeDetector detected payload:", barcodes[0].rawValue);
                                        handleScannedQrPayload(barcodes[0].rawValue);
                                        return;
                                    }
                                }).catch(() => {});
                            }
                        } catch (e) {}
                    }
                }

                cameraScanAnimId = requestAnimationFrame(scanStep);
            }

            cameraScanAnimId = requestAnimationFrame(scanStep);
        }

        function stopRealCameraScanner() {
            if (cameraScanAnimId) {
                cancelAnimationFrame(cameraScanAnimId);
                cameraScanAnimId = null;
            }
            if (cameraScanInterval) {
                clearInterval(cameraScanInterval);
                cameraScanInterval = null;
            }
            if (activeCameraStream) {
                activeCameraStream.getTracks().forEach(track => track.stop());
                activeCameraStream = null;
            }
            const video = document.getElementById('qr-camera-video');
            const placeholder = document.getElementById('qr-camera-placeholder');
            const laser = document.getElementById('scanner-laser-line');
            const statusBadge = document.getElementById('qr-camera-status-badge');
            const btnStart = document.getElementById('btn-start-camera');
            const btnStop = document.getElementById('btn-stop-camera');

            if (video) {
                video.pause();
                video.srcObject = null;
                video.style.display = 'none';
            }
            if (placeholder) placeholder.style.display = 'flex';
            if (laser) laser.style.display = 'none';
            if (btnStart) btnStart.style.display = 'inline-flex';
            if (btnStop) btnStop.style.display = 'none';
            if (statusBadge) {
                statusBadge.textContent = 'กล้องปิดอยู่ (Standby)';
                statusBadge.style.backgroundColor = '#f1f5f9';
                statusBadge.style.color = '#64748b';
            }
        }

        function handleQrImageUpload(event) {
            const file = event.target.files && event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                const img = new Image();
                img.onload = function() {
                    try {
                        if (typeof jsQR !== 'undefined') {
                            qrScanCanvas.width = img.width;
                            qrScanCanvas.height = img.height;
                            qrScanCtx.drawImage(img, 0, 0);
                            const imageData = qrScanCtx.getImageData(0, 0, qrScanCanvas.width, qrScanCanvas.height);
                            const code = jsQR(imageData.data, imageData.width, imageData.height);
                            if (code && code.data) {
                                handleScannedQrPayload(code.data);
                                return;
                            }
                        }
                    } catch (err) {}

                    if ('BarcodeDetector' in window) {
                        createImageBitmap(img).then(bmp => {
                            const bd = new BarcodeDetector({ formats: ['qr_code'] });
                            bd.detect(bmp).then(barcodes => {
                                if (barcodes && barcodes.length > 0 && barcodes[0].rawValue) {
                                    handleScannedQrPayload(barcodes[0].rawValue);
                                } else {
                                    processCheckinAndEval();
                                }
                            }).catch(() => processCheckinAndEval());
                        }).catch(() => processCheckinAndEval());
                    } else {
                        processCheckinAndEval();
                    }
                };
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
            event.target.value = '';
        }

        function handleScannedQrPayload(payload) {
            stopRealCameraScanner();
            if (!payload) {
                processCheckinAndEval();
                return;
            }

            const payloadStr = String(payload).trim();
            const studentSelect = document.getElementById('qr-scan-student-select');
            let matchedId = null;

            if (studentSelect) {
                // 1. Direct contains check
                for (let opt of studentSelect.options) {
                    if (opt.value && payloadStr.includes(opt.value)) {
                        matchedId = opt.value;
                        studentSelect.value = opt.value;
                        break;
                    }
                }

                // 2. 10-digit ID pattern
                if (!matchedId) {
                    const idMatch = payloadStr.match(/\b\d{10}\b/);
                    if (idMatch) {
                        for (let opt of studentSelect.options) {
                            if (opt.value === idMatch[0]) {
                                matchedId = opt.value;
                                studentSelect.value = opt.value;
                                break;
                            }
                        }
                    }
                }

                // 3. Name pattern
                if (!matchedId) {
                    for (let opt of studentSelect.options) {
                        const namePart = opt.text.split(' - ')[1] || '';
                        if (namePart && payloadStr.includes(namePart.trim())) {
                            matchedId = opt.value;
                            studentSelect.value = opt.value;
                            break;
                        }
                    }
                }
            }

            // Beep sound confirmation
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.frequency.value = 880;
                gain.gain.value = 0.15;
                osc.start();
                setTimeout(() => {
                    osc.stop();
                    audioCtx.close();
                }, 150);
            } catch (e) {}

            processCheckinAndEval(matchedId);
        }
        
        // Haversine Distance Calculation Formula (Returns distance in meters)
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
                const MAX_ALLOWED_RADIUS = MAX_CHECKIN_RADIUS_METERS; // อิงตามค่าคงที่รัศมีปลอดภัย 500 เมตร
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
                                // พิกัดสำรองกรณีไม่สามารถดึง GPS ได้ (คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์)
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
