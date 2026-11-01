# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add <script src="jsqr.min.js"></script> to head
if '<script src="jsqr.min.js"></script>' not in content:
    target = '<script src="supabase-client.js?v=2.5"></script>'
    if target in content:
        content = content.replace(target, '<script src="jsqr.min.js"></script>\n    ' + target)
        print("Added <script src=\"jsqr.min.js\"></script> before supabase-client.js")
    else:
        # insert before </head>
        idx_head = content.find('</head>')
        if idx_head != -1:
            content = content[:idx_head] + '    <script src="jsqr.min.js"></script>\n' + content[idx_head:]
            print("Added <script src=\"jsqr.min.js\"></script> before </head>")

# 2. Replace the scanner JS logic
start_marker = 'let activeCameraStream = null;'
end_marker = 'function processCheckinAndEval()'

idx_start = content.find(start_marker)
idx_end = content.find(end_marker)

if idx_start != -1 and idx_end != -1:
    new_scanner_js = '''let activeCameraStream = null;
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
                alert('ไม่สามารถเปิดกล้องได้: ' + (err.name === 'NotAllowedError' ? 'โปรดอนุญาตให้เบราว์เซอร์เข้าถึงกล้อง' : err.message) + '\\n\\nท่านสามารถใช้ปุ่ม "แนบรูปภาพ QR Code" หรือ "สแกนและเช็คอินพิกัด GPS ทันที" ได้ตามปกติ');
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
                    const idMatch = payloadStr.match(/\\b\\d{10}\\b/);
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
        
        '''
    content = content[:idx_start] + new_scanner_js + content[idx_end:]
    print("Scanner logic replaced successfully with jsQR continuous scanner.")

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated dashboard.html saved.")

