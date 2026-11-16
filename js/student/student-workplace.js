// ==========================================================================
// student-workplace.js - ระบบสร้าง QR Code ประจำตัวและระบุพิกัดสถานประกอบการ
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

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
            if (btnText) btnText.textContent = 'กำลังดึงพิกัดตำแหน่งปัจจุบัน...';

            if (!navigator.geolocation) {
                alert('เบราว์เซอร์ของท่านไม่รองรับการดึงพิกัด Geolocation');
                if (btnText) btnText.textContent = 'ดึงพิกัดปัจจุบัน (GPS จริง)';
                return;
            }

            const onPosSuccess = (pos) => {
                const lat = pos.coords.latitude.toFixed(6);
                const lng = pos.coords.longitude.toFixed(6);
                const acc = pos.coords.accuracy ? pos.coords.accuracy.toFixed(1) : '5.0';

                const inputLat = document.getElementById('std-input-lat');
                const inputLng = document.getElementById('std-input-lng');
                if (inputLat) inputLat.value = lat;
                if (inputLng) inputLng.value = lng;

                if (btnText) btnText.textContent = 'ดึงพิกัดปัจจุบัน (GPS จริง)';

                // Automatically save
                saveStudentWorkplaceGps(true, acc);
            };

            const tryLowAccuracy = () => {
                navigator.geolocation.getCurrentPosition(
                    onPosSuccess,
                    (err) => {
                        console.warn("Low accuracy GPS error:", err);
                        if (btnText) btnText.textContent = 'ดึงพิกัดปัจจุบัน (GPS จริง)';
                        alert('ไม่สามารถดึงพิกัดตำแหน่งปัจจุบันได้: ' + (err.name === 'NotAllowedError' ? 'โปรดอนุญาตให้เบราว์เซอร์เข้าถึงตำแหน่ง (Location Permission)' : err.message) + '\n\nท่านสามารถกดปุ่ม "เลือกพิกัดจากแผนที่ (Map)" เพื่อคลิกเลือกสถานที่ทำงานได้โดยตรงครับ');
                    },
                    { enableHighAccuracy: false, timeout: 15000, maximumAge: 0 }
                );
            };

            navigator.geolocation.getCurrentPosition(
                onPosSuccess,
                (err) => {
                    console.warn("High accuracy GPS failed, falling back to network/wifi location...", err);
                    tryLowAccuracy();
                },
                { enableHighAccuracy: true, timeout: 7000, maximumAge: 0 }
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
                    std = JSON.parse((sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser')) || '{}');
                } catch (e) {}
            }

            if (!std || !std.id) {
                std = { id: '6521650101', student_id: '6521650101', name: 'นิสิต' };
            }

            std.company_lat = latStr;
            std.company_lng = lngStr;

            // Save to currentUser session in sessionStorage & localStorage
            try { sessionStorage.setItem('currentUser', JSON.stringify(std)); } catch (e) {}
            try { localStorage.setItem('currentUser', JSON.stringify(std)); } catch (e) {}

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
                    const sid = String(std.id || std.student_id);
                    await supabaseClient.from('students').update({
                        company_lat: String(latStr),
                        company_lng: String(lngStr),
                        company_name: std.company_name || std.company || 'สถานประกอบการ'
                    }).eq('student_id', sid);
                    console.log("Supabase student GPS synced successfully:", sid, latStr, lngStr);
                } catch (e) {
                    console.warn("Supabase students table update error:", e);
                }

                try {
                    if (std.email) {
                        await supabaseClient.from('users').update({
                            company_lat: latVal,
                            company_lng: lngVal
                        }).eq('email', std.email);
                    }
                } catch (e) {}
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

            // อัปเดต QR Code ประจำตัวนิสิตให้บรรจุพิกัดล่าสุดที่ตั้งไว้ทันที
            const qrImg = document.getElementById('std-qr-image');
            if (qrImg) {
                const qrPayload = JSON.stringify({
                    id: String(std.id || std.student_id),
                    lat: parseFloat(latStr),
                    lng: parseFloat(lngStr),
                    company: std.company_name || std.company || '',
                    name: std.name || ''
                });
                qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(qrPayload)}`;
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
