# -*- coding: utf-8 -*-
import sys

def apply_updates():
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)
    print(f"Original length: {original_len}")

    # 1. Add CSS rules before </style>
    css_to_add = '''
        /* ==========================================================================
           DESKTOP COLLAPSED SIDEBAR & MOBILE RESPONSIVE STYLES
           ========================================================================== */
        
        /* Smooth transitions for sidebar */
        .desktop-sidebar {
            transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1), min-width 0.25s cubic-bezier(0.4, 0, 0.2, 1), transform 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        /* Desktop Collapsed Sidebar (width: 68px) */
        .desktop-sidebar.collapsed {
            width: 68px !important;
            min-width: 68px !important;
        }
        .desktop-sidebar.collapsed .sidebar-brand {
            justify-content: center !important;
            padding: 16px 8px !important;
        }
        .desktop-sidebar.collapsed .sidebar-brand > div:last-child {
            display: none !important;
        }
        .desktop-sidebar.collapsed .sidebar-user-box {
            display: none !important;
        }
        .desktop-sidebar.collapsed .sidebar-nav-label {
            display: none !important;
        }
        .desktop-sidebar.collapsed .sidebar-nav-item {
            justify-content: center !important;
            padding: 12px 0 !important;
            gap: 0 !important;
        }
        .desktop-sidebar.collapsed .sidebar-nav-item span {
            display: none !important;
        }
        .desktop-sidebar.collapsed .sidebar-footer {
            padding: 12px 6px !important;
        }
        .desktop-sidebar.collapsed .sidebar-logout-btn {
            justify-content: center !important;
            padding: 10px 0 !important;
            gap: 0 !important;
            font-size: 0 !important;
        }
        .desktop-sidebar.collapsed .sidebar-logout-btn svg {
            margin: 0 !important;
        }

        /* Sidebar backdrop for mobile drawer */
        #sidebar-backdrop {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.55);
            z-index: 998;
            backdrop-filter: blur(2px);
            transition: opacity 0.25s ease;
        }
        #sidebar-backdrop.active {
            display: block !important;
        }

        /* QR Camera Scanner Viewport & Laser Animation */
        .scanner-viewport-box {
            position: relative;
            width: 100%;
            max-width: 520px;
            height: 320px;
            background-color: #0f172a;
            border-radius: 12px;
            overflow: hidden;
            margin: 0 auto 14px auto;
            border: 2px solid #334155;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .scanner-viewport-box video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: none;
        }
        .scanner-overlay-frame {
            position: absolute;
            width: 220px;
            height: 220px;
            border: 2px dashed rgba(255, 255, 255, 0.4);
            border-radius: 16px;
            box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.45);
            pointer-events: none;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .scanner-overlay-frame::before {
            content: '';
            position: absolute;
            top: -2px; left: -2px; width: 24px; height: 24px;
            border-top: 4px solid #22c55e;
            border-left: 4px solid #22c55e;
            border-top-left-radius: 12px;
        }
        .scanner-overlay-frame::after {
            content: '';
            position: absolute;
            bottom: -2px; right: -2px; width: 24px; height: 24px;
            border-bottom: 4px solid #22c55e;
            border-right: 4px solid #22c55e;
            border-bottom-right-radius: 12px;
        }
        .scanner-frame-corner-tr {
            position: absolute;
            top: -2px; right: -2px; width: 24px; height: 24px;
            border-top: 4px solid #22c55e;
            border-right: 4px solid #22c55e;
            border-top-right-radius: 12px;
        }
        .scanner-frame-corner-bl {
            position: absolute;
            bottom: -2px; left: -2px; width: 24px; height: 24px;
            border-bottom: 4px solid #22c55e;
            border-left: 4px solid #22c55e;
            border-bottom-left-radius: 12px;
        }
        .scanner-laser-line {
            position: absolute;
            left: 4px;
            right: 4px;
            height: 3px;
            background: linear-gradient(90deg, transparent, #22c55e, #86efac, #22c55e, transparent);
            box-shadow: 0 0 12px #22c55e;
            display: none;
            animation: scanLaserAnim 2s ease-in-out infinite alternate;
        }
        @keyframes scanLaserAnim {
            0% { top: 8px; }
            100% { top: 208px; }
        }

        /* Mobile Responsiveness Rules (max-width: 768px) */
        @media (max-width: 768px) {
            .mobile-device {
                flex-direction: column !important;
                width: 100vw !important;
                height: 100vh !important;
                overflow: hidden !important;
                position: relative !important;
            }
            .desktop-sidebar {
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                bottom: 0 !important;
                width: 270px !important;
                min-width: 270px !important;
                height: 100vh !important;
                z-index: 1000 !important;
                transform: translateX(-100%);
                box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3) !important;
            }
            .desktop-sidebar.mobile-open {
                transform: translateX(0) !important;
            }
            .desktop-main {
                width: 100vw !important;
                max-width: 100vw !important;
                height: 100vh !important;
                flex: 1 1 auto !important;
                overflow-y: auto !important;
                -webkit-overflow-scrolling: touch !important;
            }
            header {
                padding: 0 12px !important;
                height: 54px !important;
            }
            main {
                padding: 10px !important;
                overflow-x: hidden !important;
            }
            .page-content {
                max-width: 100% !important;
                padding-bottom: 30px !important;
            }
            .section-card {
                padding: 12px 10px !important;
                margin-bottom: 12px !important;
                border-radius: 8px !important;
            }
            table {
                min-width: 580px;
            }
            div[style*="overflow-x: auto"] {
                max-width: 100% !important;
                -webkit-overflow-scrolling: touch;
            }
            .modal-card {
                width: 94vw !important;
                max-width: 95vw !important;
                padding: 14px !important;
                max-height: 90vh !important;
                overflow-y: auto !important;
            }
            .scanner-viewport-box {
                height: 250px !important;
            }
            .scanner-overlay-frame {
                width: 180px !important;
                height: 180px !important;
            }
            @keyframes scanLaserAnim {
                0% { top: 8px; }
                100% { top: 168px; }
            }
        }
'''
    if '/* DESKTOP COLLAPSED SIDEBAR & MOBILE RESPONSIVE STYLES */' not in content:
        style_close_idx = content.find('</style>')
        if style_close_idx != -1:
            content = content[:style_close_idx] + css_to_add + '\n' + content[style_close_idx:]
            print("CSS rules inserted successfully.")

    # 2. Add sidebar toggle button to header
    toggle_btn_html = '''<button type="button" id="sidebar-toggle-btn" class="header-back-btn" onclick="toggleSidebar()" title="ย่อ / ขยายเมนูด้านซ้าย" style="display:inline-flex;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
                </button>'''
    
    if 'id="sidebar-toggle-btn"' not in content:
        target_header = '<div class="system-title">'
        idx_ht = content.find(target_header)
        if idx_ht != -1:
            insert_pos = idx_ht + len(target_header)
            content = content[:insert_pos] + '\n                ' + toggle_btn_html + content[insert_pos:]
            print("Header toggle button inserted.")

    # 3. Add sidebar backdrop
    backdrop_html = '<div id="sidebar-backdrop" onclick="toggleSidebar(false)"></div>'
    if 'id="sidebar-backdrop"' not in content:
        aside_close = '</aside>'
        idx_ac = content.find(aside_close)
        if idx_ac != -1:
            insert_pos = idx_ac + len(aside_close)
            content = content[:insert_pos] + '\n\n        ' + backdrop_html + content[insert_pos:]
            print("Sidebar backdrop inserted.")

    # 4. Replace sec-advisor-qr with full camera scanner layout
    sec_qr_start = content.find('id="sec-advisor-qr"')
    if sec_qr_start != -1:
        # Find closing </div> of this section
        div_start = content.rfind('<div', 0, sec_qr_start)
        # Find matching closing </div>
        # Let's locate next section id="sec-student-dash"
        next_sec = content.find('id="sec-student-dash"')
        if next_sec != -1:
            div_end = content.rfind('</div>', 0, next_sec)
            div_end = content.rfind('</div>', 0, div_end) + 6 # closing of sec-advisor-qr
            
            new_qr_html = '''<div id="sec-advisor-qr" class="page-content">
                    <section class="section-card">
                        <div class="section-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; flex-wrap: wrap; gap: 8px;">
                            <div class="section-title" style="display: flex; align-items: center; gap: 8px; margin: 0; font-size: 15px;">
                                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--primary-color)" stroke-width="2"><path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2"/><rect x="7" y="7" width="10" height="10" rx="1"/></svg>
                                <span>สแกน QR Code เช็คอินสถานประกอบการ</span>
                            </div>
                            <span id="qr-camera-status-badge" class="badge" style="background-color: #f1f5f9; color: #64748b; font-weight: 600; font-size: 11px; padding: 4px 10px; border-radius: 20px;">
                                กล้องปิดอยู่ (Standby)
                            </span>
                        </div>

                        <div style="font-size: 11.5px; color: var(--text-muted); margin-bottom: 14px; line-height: 1.5;">
                            เปิดกล้องเพื่อสแกน QR Code ประจำตัวนิสิต ณ สถานประกอบการจริง ระบบจะตรวจจับและบันทึกพิกัด GPS เพื่อยืนยันการลงตรวจนิเทศโดยอัตโนมัติ
                        </div>

                        <!-- ช่องแสดงภาพจากกล้องสแกน QR Code จริง -->
                        <div class="scanner-viewport-box" id="scanner-viewport-box">
                            <video id="qr-camera-video" playsinline autoplay muted></video>

                            <div class="scanner-overlay-frame" id="scanner-overlay-frame">
                                <div class="scanner-frame-corner-tr"></div>
                                <div class="scanner-frame-corner-bl"></div>
                                <div class="scanner-laser-line" id="scanner-laser-line"></div>
                            </div>

                            <!-- กล่องสแตนด์บายเมื่อยังไม่เปิดกล้อง -->
                            <div id="qr-camera-placeholder" style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; color: #94a3b8; padding: 20px; z-index: 2;">
                                <div style="width: 56px; height: 56px; border-radius: 50%; background: rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: center; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.15);">
                                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#e2e8f0" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
                                </div>
                                <div style="font-size: 13px; font-weight: 700; color: #f8fafc; margin-bottom: 4px;">กล้องอยู่ในสถานะพร้อมใช้งาน</div>
                                <div style="font-size: 11px; color: #94a3b8; max-width: 320px; line-height: 1.4;">
                                    กดปุ่ม <strong style="color: #4ade80;">"เปิดกล้องสแกนทันที"</strong> ด้านล่างเพื่อเริ่มการตรวจจับ QR Code สดผ่านกล้อง
                                </div>
                            </div>
                        </div>

                        <!-- ซ่อน input ไฟล์สำหรับเลือกภาพ QR Code -->
                        <input type="file" id="qr-file-input" accept="image/*" style="display: none;" onchange="handleQrImageUpload(event)">

                        <!-- ปุ่มควบคุมกล้องและเลือกนิสิต -->
                        <div style="display: flex; flex-direction: column; gap: 10px; background: #f8fafc; padding: 14px; border-radius: 10px; border: 1px solid var(--border-color);">
                            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                                <button type="button" id="btn-start-camera" class="btn-primary" style="flex: 1; min-width: 140px; padding: 10px; font-size: 12px; font-weight: 700; background-color: var(--primary-color); display: flex; align-items: center; justify-content: center; gap: 6px; border-radius: 8px; cursor: pointer;" onclick="startRealCameraScanner()">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
                                    <span>เปิดกล้องสแกนทันที</span>
                                </button>

                                <button type="button" id="btn-stop-camera" class="btn-primary" style="flex: 1; min-width: 140px; padding: 10px; font-size: 12px; font-weight: 700; background-color: #dc2626; display: none; align-items: center; justify-content: center; gap: 6px; border-radius: 8px; cursor: pointer;" onclick="stopRealCameraScanner()">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/></svg>
                                    <span>ปิดกล้อง</span>
                                </button>

                                <button type="button" id="btn-upload-qr" class="btn-primary" style="flex: 1; min-width: 140px; padding: 10px; font-size: 12px; font-weight: 700; background-color: #0284c7; display: flex; align-items: center; justify-content: center; gap: 6px; border-radius: 8px; cursor: pointer;" onclick="document.getElementById('qr-file-input').click()">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                                    <span>แนบรูปภาพ QR Code</span>
                                </button>
                            </div>

                            <div style="border-top: 1px dashed var(--border-color); padding-top: 10px; margin-top: 4px;">
                                <label style="font-size: 11.5px; font-weight: 700; color: #334155; display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                                    เลือกนิสิตเป้าหมาย หรือยืนยันรหัสนิสิตที่ตรวจพบ:
                                </label>
                                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                                    <select id="qr-scan-student-select" style="flex: 1; min-width: 200px; padding: 9px 12px; font-size: 12px; border-radius: 8px; border: 1px solid var(--border-color); background-color: #fff; font-weight: 500;">
                                        <option value="">ยังไม่มีข้อมูลนิสิต (รอแอดมินนำเข้าข้อมูล)</option>
                                    </select>

                                    <button id="btn-process-checkin" class="btn-primary" style="padding: 9px 16px; font-size: 12px; font-weight: 700; background-color: #16a34a; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; gap: 6px; cursor: pointer; white-space: nowrap;" onclick="processCheckinAndEval()">
                                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                        <span id="btn-process-checkin-text">สแกนและเช็คอินพิกัด GPS ทันที</span>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- การ์ดแสดงผลลัพธ์การเช็คอิน (เมื่อสแกนแล้วจะแสดงรายละเอียด) -->
                        <div id="qr-checkin-result-card" style="display: none; margin-top: 16px; padding: 16px; border-radius: 12px; background-color: #f0fdf4; border: 1.5px solid #22c55e;">
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px dashed #bbf7d0; padding-bottom: 10px;">
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="width: 10px; height: 10px; border-radius: 50%; background-color: #22c55e; display: inline-block;"></span>
                                    <span style="font-size: 14px; font-weight: 700; color: #15803d;">เช็คอินเรียบร้อยแล้ว!</span>
                                </div>
                                <span class="status-badge badge-success" style="font-size: 11px;">นิเทศแล้ว</span>
                            </div>

                            <div style="display: flex; flex-direction: column; gap: 8px; font-size: 12px; color: #1e293b;">
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 80px; color: #334155;">นิสิต:</strong>
                                    <span id="qr-result-student-info" style="font-weight: 600; color: #0f172a;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 80px; color: #334155;">สถานที่:</strong>
                                    <span id="qr-result-location" style="font-weight: 600; color: #0f172a;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 80px; color: #334155;">พิกัด GPS:</strong>
                                    <span id="qr-result-gps" style="font-family: monospace; color: #166534; font-weight: 600;">-</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 8px;">
                                    <strong style="min-width: 80px; color: #334155;">วัน-เวลา:</strong>
                                    <span id="qr-result-time" style="font-weight: 600; color: #0f172a;">-</span>
                                </div>
                            </div>

                            <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid #bbf7d0;">
                                <button class="btn-primary" style="width: 100%; padding: 10px; font-size: 13px; font-weight: 700; background-color: #2563eb; border-radius: 8px; display: flex; align-items: center; justify-content: center; gap: 6px; cursor: pointer;" onclick="openEvalModalFromResult()">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 1-2 2v14a2 2 0 0 1 2 2h14a2 2 0 0 1 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                                    เริ่มกรอกแบบประเมินผลการนิเทศงาน
                                </button>
                            </div>
                        </div>
                    </section>
                </div>'''
            content = content[:div_start] + new_qr_html + '\n\n                ' + content[next_sec:]
            print("Section sec-advisor-qr updated with live camera scanner.")

    # 5. Add JavaScript functions
    js_camera_and_sidebar = '''
        /* ==========================================================================
           SIDEBAR TOGGLE & REAL CAMERA QR SCANNER LOGIC
           ========================================================================== */

        function toggleSidebar(forceState) {
            const sidebar = document.getElementById('desktop-sidebar');
            const backdrop = document.getElementById('sidebar-backdrop');
            if (!sidebar) return;

            const isMobile = window.innerWidth <= 768;

            if (isMobile) {
                if (typeof forceState === 'boolean') {
                    if (forceState) {
                        sidebar.classList.add('mobile-open');
                        if (backdrop) backdrop.classList.add('active');
                    } else {
                        sidebar.classList.remove('mobile-open');
                        if (backdrop) backdrop.classList.remove('active');
                    }
                } else {
                    const isOpen = sidebar.classList.toggle('mobile-open');
                    if (backdrop) backdrop.classList.toggle('active', isOpen);
                }
            } else {
                if (typeof forceState === 'boolean') {
                    sidebar.classList.toggle('collapsed', !forceState);
                } else {
                    sidebar.classList.toggle('collapsed');
                }
            }
        }

        let activeCameraStream = null;
        let cameraScanInterval = null;

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
                    await video.play();
                    video.style.display = 'block';
                }

                if (placeholder) placeholder.style.display = 'none';
                if (laser) laser.style.display = 'block';
                if (btnStart) btnStart.style.display = 'none';
                if (btnStop) btnStop.style.display = 'inline-flex';
                if (statusBadge) {
                    statusBadge.textContent = 'กล้องสดกำลังทำงาน (Live Stream)';
                    statusBadge.style.backgroundColor = '#dcfce7';
                    statusBadge.style.color = '#15803d';
                }

                // Check BarcodeDetector API support
                if ('BarcodeDetector' in window) {
                    try {
                        const barcodeDetector = new BarcodeDetector({ formats: ['qr_code'] });
                        cameraScanInterval = setInterval(async () => {
                            if (!activeCameraStream || !video || video.readyState < 2) return;
                            try {
                                const barcodes = await barcodeDetector.detect(video);
                                if (barcodes && barcodes.length > 0) {
                                    handleScannedQrPayload(barcodes[0].rawValue);
                                }
                            } catch (e) {}
                        }, 500);
                    } catch (e) {}
                }
            } catch (err) {
                console.warn('Camera error:', err);
                alert('ไม่สามารถเปิดกล้องได้: ' + (err.name === 'NotAllowedError' ? 'โปรดอนุญาตให้เบราว์เซอร์เข้าถึงกล้อง' : err.message) + '\\n\\nท่านสามารถใช้ปุ่ม "แนบรูปภาพ QR Code" หรือ "สแกนและเช็คอินพิกัด GPS ทันที" ได้ตามปกติ');
            }
        }

        function stopRealCameraScanner() {
            if (activeCameraStream) {
                activeCameraStream.getTracks().forEach(track => track.stop());
                activeCameraStream = null;
            }
            if (cameraScanInterval) {
                clearInterval(cameraScanInterval);
                cameraScanInterval = null;
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

            if ('BarcodeDetector' in window) {
                createImageBitmap(file).then(async bmp => {
                    try {
                        const barcodeDetector = new BarcodeDetector({ formats: ['qr_code'] });
                        const barcodes = await barcodeDetector.detect(bmp);
                        if (barcodes && barcodes.length > 0) {
                            handleScannedQrPayload(barcodes[0].rawValue);
                            return;
                        }
                    } catch (e) {}
                    processCheckinAndEval();
                }).catch(() => {
                    processCheckinAndEval();
                });
            } else {
                processCheckinAndEval();
            }
            event.target.value = '';
        }

        function handleScannedQrPayload(payload) {
            stopRealCameraScanner();
            const studentSelect = document.getElementById('qr-scan-student-select');
            if (studentSelect) {
                for (let opt of studentSelect.options) {
                    if (opt.value && (payload.includes(opt.value) || (opt.text && opt.text.includes(payload)))) {
                        studentSelect.value = opt.value;
                        break;
                    }
                }
            }
            processCheckinAndEval();
        }
'''
    # Replace existing html5QrCodeInstance & startRealCameraScanner block
    old_start_scanner = content.find('let html5QrCodeInstance = null;')
    if old_start_scanner != -1:
        # find where processCheckinAndEval begins
        next_func = content.find('function processCheckinAndEval()', old_start_scanner)
        if next_func != -1:
            content = content[:old_start_scanner] + js_camera_and_sidebar + '\n\n        ' + content[next_func:]
            print("Camera and sidebar JS replaced old stub successfully.")
    elif 'function toggleSidebar(' not in content:
        # Insert before script close
        script_close = content.rfind('</script>')
        if script_close != -1:
            content = content[:script_close] + js_camera_and_sidebar + '\n' + content[script_close:]
            print("Camera and sidebar JS appended.")

    # 6. Update sidebarNavigate to close mobile sidebar and stop camera
    sn_idx = content.find('function sidebarNavigate(targetId, pageId, btn) {')
    if sn_idx != -1:
        nav_hook = '''function sidebarNavigate(targetId, pageId, btn) {
            if (window.innerWidth <= 768) {
                toggleSidebar(false);
            }
            if (targetId !== 'sec-advisor-qr' && pageId !== 'sec-advisor-qr') {
                stopRealCameraScanner();
            }'''
        content = content[:sn_idx] + nav_hook + content[sn_idx + len('function sidebarNavigate(targetId, pageId, btn) {'):]
        print("sidebarNavigate updated with mobile close and camera stop hooks.")

    # 7. Update buildSidebarNav to include tooltip title="${item.text}"
    old_btn_str = 'html += `<button class="sidebar-nav-item" onclick="sidebarNavigate(\'${item.id}\', \'${item.page}\', this)">${item.icon}<span>${item.text}</span></button>`;'
    new_btn_str = 'html += `<button class="sidebar-nav-item" title="${item.text}" onclick="sidebarNavigate(\'${item.id}\', \'${item.page}\', this)">${item.icon}<span>${item.text}</span></button>`;'
    if old_btn_str in content:
        content = content.replace(old_btn_str, new_btn_str)
        print("buildSidebarNav button updated with tooltip title.")

    # Write back to dashboard.html
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Update complete! New length: {len(content)}")

if __name__ == '__main__':
    apply_updates()

