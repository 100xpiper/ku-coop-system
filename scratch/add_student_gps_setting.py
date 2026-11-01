# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update sec-student-qrcode HTML
sec_qr_start = content.find('id="sec-student-qrcode"')
next_view_marker = '<!-- ==============================================\n                VIEW 3:'
if next_view_marker not in content:
    next_view_marker = '<!-- =============================================='

idx_end_sec = content.find(next_view_marker, sec_qr_start)

if sec_qr_start != -1 and idx_end_sec != -1:
    # Find closing </div> of sec-student-qrcode
    div_close = content.rfind('</div>', sec_qr_start, idx_end_sec) + 6
    
    new_student_qrcode_html = '''id="sec-student-qrcode" class="page-content">
                    <section class="section-card" style="text-align: center;">
                        <div class="section-header" style="justify-content: center;">
                            <div class="section-title">QR Code ประจำตัวและพิกัดสถานประกอบการ</div>
                        </div>
                        <div style="font-size: 11.5px; color: var(--text-muted); margin-bottom: 16px;">
                            ยื่นหน้าจอนี้ให้อาจารย์สแกนเพื่อเช็คอินยืนยันพิกัด ณ สถานประกอบการ หรือกำหนดพิกัดตำแหน่งจริงด้วยตนเอง
                        </div>

                        <!-- 1. การ์ดแสดง QR Code ประจำตัวนิสิต -->
                        <div style="background-color: #ffffff; border: 2px solid var(--primary-color); padding: 18px; border-radius: 16px; display: inline-block; box-shadow: 0 4px 14px rgba(0,0,0,0.06); max-width: 360px; width: 100%; margin: 0 auto 18px auto;">
                            <!-- Real QR Code Image -->
                            <div id="std-qr-placeholder" style="width: 160px; height: 160px; background: #f1f5f9; display: flex; align-items: center; justify-content: center; border-radius: 8px; margin: 0 auto;">
                                <span style="font-size: 12px; color: #94a3b8;">กำลังสร้าง...</span>
                            </div>
                            <img id="std-qr-image" src="" alt="QR Code" style="width: 160px; height: 160px; display: none; margin: 0 auto;" />
                            <div style="font-size: 14px; font-weight: 700; color: var(--primary-color); margin-top: 10px;" id="std-qr-id">รหัสนิสิต: -</div>
                            <div style="font-size: 12px; font-weight: 600; color: #1e293b;" id="std-qr-name">นิสิต</div>
                            <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;" id="std-qr-company">-</div>
                        </div>

                        <!-- 2. การ์ดตั้งค่าและบันทึกพิกัดสถานประกอบการของนิสิต -->
                        <div class="section-card" style="text-align: left; max-width: 540px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1.5px solid #cbd5e1; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                            <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                                <div style="display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 700; color: var(--primary-color);">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
                                    <span>กำหนดพิกัดสถานประกอบการของฉัน</span>
                                </div>
                                <span id="std-gps-status-badge" class="badge" style="font-size: 11px; padding: 4px 10px; border-radius: 20px; font-weight: 600; background: #fef3c7; color: #b45309;">
                                    ยังไม่ได้ตั้งพิกัด
                                </span>
                            </div>

                            <div style="font-size: 11.5px; color: var(--text-muted); margin-bottom: 14px; line-height: 1.5;">
                                นิสิตสามารถกดปุ่มเพื่อดึงพิกัดตำแหน่งจริงผ่านชิปดาวเทียม GPS ณ สถานที่ฝึกงาน หรือป้อนตัวเลขละติจูด-ลองจิจูดด้วยตนเอง เพื่อให้อาจารย์ใช้ตรวจสอบและนำทางในวันออกตรวจนิเทศ
                            </div>

                            <!-- กล่องแสดงสถานะพิกัดปัจจุบัน -->
                            <div id="std-current-coords-box" style="background: #f8fafc; border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; margin-bottom: 14px;">
                                <div style="font-size: 10.5px; color: #64748b; font-weight: 700; margin-bottom: 4px; text-transform: uppercase;">
                                    พิกัดที่บันทึกไว้ในระบบ:
                                </div>
                                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 6px;">
                                    <div id="std-saved-coords-text" style="font-family: monospace; font-size: 13px; font-weight: 700; color: #0f172a;">
                                        ยังไม่ได้กำหนดพิกัด
                                    </div>
                                    <a id="btn-view-saved-map" href="#" target="_blank" class="btn-primary" style="display: none; font-size: 11px; font-weight: 700; background: #0284c7; padding: 4px 8px; border-radius: 6px; text-decoration: none; align-items: center; gap: 4px;">
                                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>
                                        ดูบน Google Maps
                                    </a>
                                </div>
                            </div>

                            <!-- ปุ่มดึงพิกัดอัตโนมัติ -->
                            <button type="button" id="btn-std-auto-gps" class="btn-primary" style="width: 100%; padding: 11px; font-size: 12.5px; font-weight: 700; background-color: #059669; border-radius: 8px; display: flex; align-items: center; justify-content: center; gap: 6px; cursor: pointer; margin-bottom: 14px; box-shadow: 0 2px 4px rgba(5,150,105,0.2);" onclick="autoDetectStudentGps()">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>
                                <span id="btn-std-auto-gps-text">ดึงพิกัดตำแหน่งปัจจุบันของฉัน (GPS จริง)</span>
                            </button>

                            <!-- ช่องกรอกหรือแก้ไขพิกัด -->
                            <div style="border-top: 1px dashed var(--border-color); padding-top: 12px;">
                                <div style="font-size: 11px; font-weight: 700; color: #475569; margin-bottom: 8px;">
                                    หรือป้อนตัวเลขพิกัดด้วยตนเอง (Latitude, Longitude):
                                </div>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px;">
                                    <div>
                                        <label style="font-size: 10.5px; color: var(--text-muted); font-weight: 600; display: block; margin-bottom: 3px;">ละติจูด (Latitude):</label>
                                        <input type="text" id="std-input-lat" placeholder="เช่น 13.847621" style="width: 100%; padding: 8px 10px; font-size: 12px; font-family: monospace; border: 1px solid var(--border-color); border-radius: 6px; background: #ffffff;">
                                    </div>
                                    <div>
                                        <label style="font-size: 10.5px; color: var(--text-muted); font-weight: 600; display: block; margin-bottom: 3px;">ลองจิจูด (Longitude):</label>
                                        <input type="text" id="std-input-lng" placeholder="เช่น 100.569432" style="width: 100%; padding: 8px 10px; font-size: 12px; font-family: monospace; border: 1px solid var(--border-color); border-radius: 6px; background: #ffffff;">
                                    </div>
                                </div>

                                <button type="button" class="btn-primary" style="width: 100%; padding: 10px; font-size: 12.5px; font-weight: 700; background-color: var(--primary-color); border-radius: 8px; display: flex; align-items: center; justify-content: center; gap: 6px; cursor: pointer;" onclick="saveStudentWorkplaceGps()">
                                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                    <span>บันทึกพิกัดสถานประกอบการ</span>
                                </button>
                            </div>
                        </div>
                    </section>
                </div>'''

    content = content[:sec_qr_start] + new_student_qrcode_html + content[div_close:]
    print("Updated sec-student-qrcode HTML successfully.")

# 2. Add JavaScript functions for Student GPS Settings
js_funcs = '''
        /* ==========================================================================
           STUDENT WORKPLACE GPS SETTING FUNCTIONS
           ========================================================================== */

        let currentStudentProfile = null;

        function renderStudentGpsSettings(user) {
            currentStudentProfile = user;
            if (!user) return;

            const companyEl = document.getElementById('std-qr-company');
            if (companyEl) {
                companyEl.textContent = user.company_name || user.company || 'สถานประกอบการ: -';
            }

            // Check if coordinates already exist in user object, customUsers, or studentsData
            let lat = user.company_lat || user.lat;
            let lng = user.company_lng || user.lng;

            if (!lat || !lng) {
                try {
                    const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                    const u = customUsers[user.email] || customUsers[user.id] || customUsers[user.student_id];
                    if (u && u.company_lat && u.company_lng) {
                        lat = u.company_lat;
                        lng = u.company_lng;
                    }
                } catch (e) {}
            }

            if (!lat || !lng) {
                const allStds = getAllSystemStudents();
                const std = allStds.find(s => String(s.id) === String(user.id || user.student_id));
                if (std && std.company_lat && std.company_lng) {
                    lat = std.company_lat;
                    lng = std.company_lng;
                }
            }

            const inputLat = document.getElementById('std-input-lat');
            const inputLng = document.getElementById('std-input-lng');
            const savedText = document.getElementById('std-saved-coords-text');
            const badge = document.getElementById('std-gps-status-badge');
            const mapLink = document.getElementById('btn-view-saved-map');

            if (lat && lng) {
                if (inputLat) inputLat.value = lat;
                if (inputLng) inputLng.value = lng;
                if (savedText) savedText.textContent = `Lat: ${lat}, Lng: ${lng}`;
                if (badge) {
                    badge.textContent = 'บันทึกพิกัดแล้ว';
                    badge.style.backgroundColor = '#dcfce7';
                    badge.style.color = '#15803d';
                }
                if (mapLink) {
                    mapLink.href = `https://www.google.com/maps?q=${lat},${lng}&z=18`;
                    mapLink.style.display = 'inline-flex';
                }
            } else {
                if (savedText) savedText.textContent = 'ยังไม่ได้กำหนดพิกัดสถานประกอบการ';
                if (badge) {
                    badge.textContent = 'ยังไม่ได้ตั้งพิกัด';
                    badge.style.backgroundColor = '#fef3c7';
                    badge.style.color = '#b45309';
                }
                if (mapLink) mapLink.style.display = 'none';
            }
        }

        function autoDetectStudentGps() {
            const btnText = document.getElementById('btn-std-auto-gps-text');
            if (btnText) btnText.textContent = 'กำลังค้นหาสัญญาณดาวเทียม GPS...';

            if (!navigator.geolocation) {
                alert('เบราว์เซอร์ของท่านไม่รองรับการดึงพิกัด Geolocation');
                if (btnText) btnText.textContent = 'ดึงพิกัดตำแหน่งปัจจุบันของฉัน (GPS จริง)';
                return;
            }

            const options = {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            };

            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    const lat = pos.coords.latitude.toFixed(6);
                    const lng = pos.coords.longitude.toFixed(6);
                    const acc = pos.coords.accuracy ? pos.coords.accuracy.toFixed(1) : '5.0';

                    const inputLat = document.getElementById('std-input-lat');
                    const inputLng = document.getElementById('std-input-lng');
                    if (inputLat) inputLat.value = lat;
                    if (inputLng) inputLng.value = lng;

                    if (btnText) btnText.textContent = 'ดึงพิกัดตำแหน่งปัจจุบันของฉัน (GPS จริง)';

                    // Automatically save
                    saveStudentWorkplaceGps(true, acc);
                },
                (err) => {
                    console.warn("Auto GPS error:", err);
                    if (btnText) btnText.textContent = 'ดึงพิกัดตำแหน่งปัจจุบันของฉัน (GPS จริง)';
                    alert('ไม่สามารถดึงพิกัด GPS ได้: ' + (err.name === 'NotAllowedError' ? 'โปรดอนุญาตให้เบราว์เซอร์เข้าถึงตำแหน่ง (Location)' : err.message) + '\\n\\nท่านสามารถป้อนตัวเลขพิกัดจาก Google Maps ด้วยตนเองในช่องด้านล่างได้ครับ');
                },
                options
            );
        }

        async function saveStudentWorkplaceGps(isAuto, accuracyMeters) {
            const inputLat = document.getElementById('std-input-lat');
            const inputLng = document.getElementById('std-input-lng');

            if (!inputLat || !inputLng || !inputLat.value.trim() || !inputLng.value.trim()) {
                alert('กรุณากรอกตัวเลขพิกัดละติจูดและลองจิจูดให้ครบถ้วน');
                return;
            }

            const latVal = parseFloat(inputLat.value.trim());
            const lngVal = parseFloat(inputLng.value.trim());

            if (isNaN(latVal) || isNaN(lngVal)) {
                alert('ตัวเลขพิกัดไม่ถูกต้อง โปรดตรวจสอบว่าเป็นตัวเลข เช่น 13.847621, 100.569432');
                return;
            }

            const latStr = latVal.toFixed(6);
            const lngStr = lngVal.toFixed(6);

            // Get logged in student
            let std = currentStudentProfile;
            if (!std) {
                try {
                    std = JSON.parse(localStorage.getItem('currentUser') || '{}');
                } catch (e) {}
            }

            if (!std || !std.id) {
                std = { id: '6521650101', student_id: '6521650101', name: 'นิสิต' };
            }

            std.company_lat = latStr;
            std.company_lng = lngStr;

            // Save to currentUser session in localStorage
            localStorage.setItem('currentUser', JSON.stringify(std));

            // Save to customUsers
            try {
                let customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                const emailKey = String(std.email || '').toLowerCase().trim();
                if (emailKey) {
                    if (!customUsers[emailKey]) customUsers[emailKey] = { ...std };
                    customUsers[emailKey].company_lat = latStr;
                    customUsers[emailKey].company_lng = lngStr;
                }
                const idKey = String(std.id || std.student_id);
                if (idKey) {
                    if (!customUsers[idKey]) customUsers[idKey] = { ...std };
                    customUsers[idKey].company_lat = latStr;
                    customUsers[idKey].company_lng = lngStr;
                }
                localStorage.setItem('customUsers', JSON.stringify(customUsers));
            } catch (e) {}

            // Update in-memory studentsData
            const allStds = getAllSystemStudents();
            const foundStd = allStds.find(s => String(s.id) === String(std.id || std.student_id));
            if (foundStd) {
                foundStd.company_lat = latStr;
                foundStd.company_lng = lngStr;
            }

            // Sync with Supabase if active
            if (typeof supabaseClient !== 'undefined' && supabaseClient) {
                try {
                    await supabaseClient.from('users').update({
                        company_lat: latVal,
                        company_lng: lngVal
                    }).eq('id', std.id);
                } catch (e) {
                    console.warn("Supabase update error:", e);
                }
            }

            // Update UI elements
            const savedText = document.getElementById('std-saved-coords-text');
            const badge = document.getElementById('std-gps-status-badge');
            const mapLink = document.getElementById('btn-view-saved-map');

            if (savedText) savedText.textContent = `Lat: ${latStr}, Lng: ${lngStr}`;
            if (badge) {
                badge.textContent = 'บันทึกพิกัดแล้ว';
                badge.style.backgroundColor = '#dcfce7';
                badge.style.color = '#15803d';
            }
            if (mapLink) {
                mapLink.href = `https://www.google.com/maps?q=${latStr},${lngStr}&z=18`;
                mapLink.style.display = 'inline-flex';
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

            const successMsg = isAuto && accuracyMeters
                ? `ดึงพิกัดจาก GPS เรียบร้อยแล้ว (Lat: ${latStr}, Lng: ${lngStr}) ความแม่นยำ ±${accuracyMeters} เมตร และบันทึกลงระบบสำเร็จ!`
                : `บันทึกพิกัดสถานประกอบการ (Lat: ${latStr}, Lng: ${lngStr}) เรียบร้อยแล้ว!`;

            alert(successMsg);
        }
'''

# 3. Hook renderStudentGpsSettings into initUserDashboard
hook_target = 'loadStudentProjectTracking(stdIdVal);'
if hook_target in content and 'renderStudentGpsSettings(user);' not in content:
    content = content.replace(hook_target, hook_target + '\n                renderStudentGpsSettings(user);')
    print("Hooked renderStudentGpsSettings into initUserDashboard.")

# Insert js_funcs before script closing
idx_sc = content.rfind('</script>')
if idx_sc != -1:
    content = content[:idx_sc] + js_funcs + '\n    ' + content[idx_sc:]
    print("Appended Student GPS setting functions to JavaScript.")

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated dashboard.html successfully.")

