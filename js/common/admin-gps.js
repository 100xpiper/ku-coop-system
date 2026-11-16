// ==========================================================================
// admin-gps.js - ระบบตั้งค่าและจัดการพิกัด GPS สถานประกอบการล่วงหน้า
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

function renderAdminGpsSection() {
            const select = document.getElementById('admin-gps-company-select');
            if (!select) return;
            select.innerHTML = '<option value="">-- เลือกสถานประกอบการของนิสิต --</option>';
            const allSecs = ['หมู่ 700', 'หมู่ 701', 'หมู่ 702', 'หมู่ 800', 'หมู่ 801', 'หมู่ 802'];
            let total = 0;
            allSecs.forEach(sec => {
                const sList = studentsData[sec] || [];
                if (sList.length > 0) {
                    total += sList.length;
                    const g = document.createElement('optgroup');
                    g.label = `── ${sec} [${sList.length} คน] ──`;
                    sList.forEach(s => {
                        const opt = document.createElement('option');
                        opt.value = s.id;
                        opt.textContent = `[${sec}] ${s.company} (นิสิต: ${s.name} ${s.id})`;
                        g.appendChild(opt);
                    });
                    select.appendChild(g);
                }
            });
            if (total === 0) {
                select.innerHTML = '<option value="">ยังไม่มีข้อมูลสถานประกอบการ (รอแอดมินนำเข้าข้อมูลนิสิต)</option>';
            }
            renderSavedGpsList();
        }

        function fillCurrentGpsLocationAdmin() {
            if (!navigator.geolocation) {
                alert('เบราว์เซอร์นี้ไม่รองรับ Geolocation API');
                return;
            }
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    document.getElementById('admin-gps-lat-input').value = pos.coords.latitude.toFixed(6);
                    document.getElementById('admin-gps-lng-input').value = pos.coords.longitude.toFixed(6);
                    alert('ดึงพิกัด GPS ปัจจุบันจากอุปกรณ์สำเร็จ!');
                },
                (err) => {
                    alert('ไม่สามารถดึงพิกัด GPS ได้: ' + err.message);
                },
                { enableHighAccuracy: true }
            );
        }

        function saveAdminGpsSetup() {
            const select = document.getElementById('admin-gps-company-select');
            const lat = document.getElementById('admin-gps-lat-input').value;
            const lng = document.getElementById('admin-gps-lng-input').value;
            const compText = select && select.options[select.selectedIndex] ? select.options[select.selectedIndex].text : 'สถานประกอบการ';

            if (!lat || !lng) {
                alert('กรุณาระบุพิกัดละติจูดและลองจิจูด');
                return;
            }

            const gpsData = JSON.parse(localStorage.getItem('companyGpsData') || '{}');
            gpsData[select.value || 'default'] = { company: compText, lat: parseFloat(lat), lng: parseFloat(lng), updatedAt: new Date().toLocaleString('th-TH') };
            localStorage.setItem('companyGpsData', JSON.stringify(gpsData));

            if (select && select.value) {
                const sId = String(select.value);
                const allStds = (typeof getAllSystemStudents === 'function') ? getAllSystemStudents() : [];
                const sObj = allStds.find(s => String(s.id) === sId);
                if (sObj) {
                    sObj.company_lat = lat;
                    sObj.company_lng = lng;
                }
                try {
                    const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                    if (!customUsers[sId]) customUsers[sId] = {};
                    customUsers[sId].company_lat = lat;
                    customUsers[sId].company_lng = lng;
                    if (sObj && sObj.email) {
                        const em = sObj.email.toLowerCase().trim();
                        if (!customUsers[em]) customUsers[em] = {};
                        customUsers[em].company_lat = lat;
                        customUsers[em].company_lng = lng;
                    }
                    localStorage.setItem('customUsers', JSON.stringify(customUsers));
                } catch (e) {}
            }

            alert(`บันทึกตั้งค่าพิกัด GPS สำหรับ ${compText} สำเร็จ!\n\nพิกัดอ้างอิง: Lat ${lat}, Lng ${lng}`);
            renderSavedGpsList();
        }

        function renderSavedGpsList() {
            const container = document.getElementById('admin-saved-gps-list');
            if (!container) return;
            const gpsData = JSON.parse(localStorage.getItem('companyGpsData') || '{}');
            const keys = Object.keys(gpsData);
            if (keys.length === 0) {
                container.innerHTML = `
                    <div style="padding: 24px; text-align: center; color: var(--text-muted); font-size: 11.5px; background: #f8fafc; border-radius: 8px; border: 1px dashed var(--border-color);">
                         ยังไม่มีข้อมูลพิกัด GPS สำหรับสถานประกอบการ<br>
                        <span style="font-size: 10.5px; color: #94a3b8;">สามารถใช้กล่อง "ตั้งค่าพิกัดสถานประกอบการ" ด้านบนเพื่อระบุพิกัดละติจูด/ลองจิจูด</span>
                    </div>
                `;
                return;
            }
            container.innerHTML = keys.map(k => {
                const item = gpsData[k];
                return `
                    <div style="padding: 8px 10px; background: #ffffff; border: 1px solid #bbf7d0; border-radius: 6px; margin-bottom: 6px; font-size: 11px;">
                        <div style="font-weight: 700; color: #166534;"> ${item.company}</div>
                        <div style="color: #374151; margin-top: 2px;">พิกัดอ้างอิง: <strong>Lat ${item.lat}, Lng ${item.lng}</strong></div>
                        <div style="color: var(--text-muted); font-size: 10px; margin-top: 1px;">อัปเดตล่าสุด: ${item.updatedAt}</div>
                    </div>
                `;
            }).join('');
        }

        function openGpsSetupModal() {
            const modal = document.getElementById('modal-gps-setup');
            const select = document.getElementById('gps-student-company-select');
            if (select) {
                select.innerHTML = '';
                const { mySecNormal, mySecSpecial, loggedInUser } = getAdvisorSections();
                const isAdv = (loggedInUser && loggedInUser.role === 'advisor');

                if (isAdv) {
                    let normStds = studentsData[mySecNormal] || [];
                    let specStds = studentsData[mySecSpecial] || [];
                    if (advisorSelectedSemester && advisorSelectedSemester !== 'all') {
                        normStds = normStds.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
                        specStds = specStds.filter(s => (s.semester || 'ภาคต้น 2569') === advisorSelectedSemester);
                    }

                    if (normStds.length === 0 && specStds.length === 0) {
                        select.innerHTML = '<option value="">ยังไม่มีข้อมูลสถานประกอบการ</option>';
                    } else {
                        select.innerHTML = '<option value="">-- เลือกสถานประกอบการของนิสิต --</option>';
                        if (normStds.length > 0) {
                            const gNorm = document.createElement('optgroup');
                            gNorm.label = `── ${mySecNormal} [${normStds.length} คน] ──`;
                            normStds.forEach(s => {
                                const opt = document.createElement('option');
                                opt.value = s.id;
                                opt.textContent = `[${mySecNormal}] ${s.company} (นิสิต: ${s.name} ${s.id})`;
                                gNorm.appendChild(opt);
                            });
                            select.appendChild(gNorm);
                        }
                        if (specStds.length > 0) {
                            const gSpec = document.createElement('optgroup');
                            gSpec.label = `── ${mySecSpecial} [${specStds.length} คน] ──`;
                            specStds.forEach(s => {
                                const opt = document.createElement('option');
                                opt.value = s.id;
                                opt.textContent = `[${mySecSpecial}] ${s.company} (นิสิต: ${s.name} ${s.id})`;
                                gSpec.appendChild(opt);
                            });
                            select.appendChild(gSpec);
                        }
                    }
                } else {
                    const allSecs = ['หมู่ 700', 'หมู่ 701', 'หมู่ 702', 'หมู่ 800', 'หมู่ 801', 'หมู่ 802'];
                    select.innerHTML = '<option value="">-- เลือกสถานประกอบการของนิสิต --</option>';
                    allSecs.forEach(sec => {
                        const sList = studentsData[sec] || [];
                        if (sList.length > 0) {
                            const g = document.createElement('optgroup');
                            g.label = `── ${sec} [${sList.length} คน] ──`;
                            sList.forEach(s => {
                                const opt = document.createElement('option');
                                opt.value = s.id;
                                opt.textContent = `[${sec}] ${s.company} (นิสิต: ${s.name} ${s.id})`;
                                g.appendChild(opt);
                            });
                            select.appendChild(g);
                        }
                    });
                }
            }
            if (modal) modal.style.display = 'flex';
        }

        function fillCurrentGpsLocation() {
            if (!navigator.geolocation) {
                alert('เบราว์เซอร์นี้ไม่รองรับ Geolocation API');
                return;
            }
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    document.getElementById('gps-lat-input').value = pos.coords.latitude.toFixed(6);
                    document.getElementById('gps-lng-input').value = pos.coords.longitude.toFixed(6);
                    alert('ดึงพิกัด GPS ปัจจุบันสำเร็จ!');
                },
                (err) => {
                    alert('ไม่สามารถดึงพิกัด GPS ได้: ' + err.message);
                },
                { enableHighAccuracy: true }
            );
        }

        function saveGpsSetup() {
            const select = document.getElementById('gps-student-company-select');
            const lat = document.getElementById('gps-lat-input').value;
            const lng = document.getElementById('gps-lng-input').value;
            const compText = select && select.options[select.selectedIndex] ? select.options[select.selectedIndex].text : 'สถานประกอบการ';

            if (!lat || !lng) {
                alert('กรุณาระบุพิกัดละติจูดและลองจิจูด');
                return;
            }

            const gpsData = JSON.parse(localStorage.getItem('companyGpsData') || '{}');
            gpsData[select.value || 'default'] = { company: compText, lat: parseFloat(lat), lng: parseFloat(lng), updatedAt: new Date().toISOString() };
            localStorage.setItem('companyGpsData', JSON.stringify(gpsData));

            if (select && select.value) {
                const sId = String(select.value);
                const allStds = (typeof getAllSystemStudents === 'function') ? getAllSystemStudents() : [];
                const sObj = allStds.find(s => String(s.id) === sId);
                if (sObj) {
                    sObj.company_lat = lat;
                    sObj.company_lng = lng;
                }
                try {
                    const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                    if (!customUsers[sId]) customUsers[sId] = {};
                    customUsers[sId].company_lat = lat;
                    customUsers[sId].company_lng = lng;
                    if (sObj && sObj.email) {
                        const em = sObj.email.toLowerCase().trim();
                        if (!customUsers[em]) customUsers[em] = {};
                        customUsers[em].company_lat = lat;
                        customUsers[em].company_lng = lng;
                    }
                    localStorage.setItem('customUsers', JSON.stringify(customUsers));
                } catch (e) {}
            }

            alert(`บันทึกตั้งค่าพิกัด GPS สำหรับ ${compText} เรียบร้อยแล้ว!\n\nพิกัดอ้างอิง: Lat ${lat}, Lng ${lng}`);
            closeModal('modal-gps-setup');
        }
