// ==========================================================================
// map-picker.js - ระบบแผนที่ Leaflet และปักหมุดพิกัดสถานประกอบการ (Map Picker)
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

var studentPickerMap = null;
var studentPickerMarker = null;
var currentPickedLat = 13.847621;
var currentPickedLng = 100.569432;
var mapPickerTarget = { latId: 'std-input-lat', lngId: 'std-input-lng', autoSave: true };

// ----------------------------------------------------------------------
// เปิด Modal แผนที่สำหรับนิสิตกำหนดพิกัดสถานประกอบการ
// ----------------------------------------------------------------------
function openStudentMapPicker() {
    mapPickerTarget = { latId: 'std-input-lat', lngId: 'std-input-lng', autoSave: true };
    initAndOpenMapModal('std-input-lat', 'std-input-lng');
}

// ----------------------------------------------------------------------
// เปิด Modal แผนที่สำหรับแอดมิน/อาจารย์ตั้งค่าพิกัด GPS
// ----------------------------------------------------------------------
function openGpsSetupMapPicker() {
    mapPickerTarget = { latId: 'gps-lat-input', lngId: 'gps-lng-input', autoSave: false };
    if (typeof closeModal === 'function') {
        closeModal('modal-gps-setup');
    } else {
        const m = document.getElementById('modal-gps-setup');
        if (m) m.style.display = 'none';
    }
    initAndOpenMapModal('gps-lat-input', 'gps-lng-input');
}

// ----------------------------------------------------------------------
// ฟังก์ชันกลาง: แสดง Modal และตั้งค่าแผนที่ Leaflet
// ----------------------------------------------------------------------
function initAndOpenMapModal(sourceLatId, sourceLngId) {
    const modal = document.getElementById('modal-student-map-picker');
    if (!modal) {
        alert('ไม่พบหน้าต่างแผนที่ในระบบ');
        return;
    }

    // อ่านค่าพิกัดจากช่อง Input ปัจจุบัน (ถ้ามี)
    const inputLat = document.getElementById(sourceLatId);
    const inputLng = document.getElementById(sourceLngId);
    if (inputLat && inputLng && inputLat.value.trim() && inputLng.value.trim()) {
        const pLat = parseFloat(inputLat.value.trim());
        const pLng = parseFloat(inputLng.value.trim());
        if (!isNaN(pLat) && !isNaN(pLng)) {
            currentPickedLat = pLat;
            currentPickedLng = pLng;
        }
    } else {
        currentPickedLat = 13.847621;
        currentPickedLng = 100.569432;
    }

    modal.style.display = 'flex';
    updatePickedCoordinates(currentPickedLat, currentPickedLng);

    // หน่วงเวลาเล็กน้อยเพื่อให้เบราว์เซอร์ Render Modal ขนาดจริงก่อนวาด Leaflet Map
    setTimeout(() => {
        const mapContainer = document.getElementById('student-leaflet-map');
        if (!mapContainer) return;

        if (typeof L === 'undefined') {
            mapContainer.innerHTML = `
                <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;color:#64748b;gap:10px;padding:20px;text-align:center;">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/></svg>
                    <div style="font-weight:700;font-size:13px;color:#334155;">กำลังเชื่อมต่อระบบแผนที่ หรือไม่พบการเชื่อมต่ออินเทอร์เน็ต</div>
                    <div style="font-size:11px;">ท่านสามารถพิมพ์ค้นหาด้านบน หรือกรอกตัวเลขพิกัดด้วยตนเองที่หน้าต่างหลักได้ทันที</div>
                    <div style="font-size:11px;color:#2563eb;font-weight:600;">พิกัดปัจจุบัน: Lat ${currentPickedLat.toFixed(6)}, Lng ${currentPickedLng.toFixed(6)}</div>
                </div>`;
            return;
        }

        // สร้างไอคอนหมุดสีแดง (SVG DivIcon เพื่อให้แสดงผลคมชัด ไม่ต้องรอโหลดไฟล์รูปจากเน็ต)
        const redPinIcon = L.divIcon({
            className: 'custom-map-pin',
            html: `<div style="position:relative; width:30px; height:30px; display:flex; align-items:center; justify-content:center;">
                     <svg width="30" height="30" viewBox="0 0 24 24" fill="#dc2626" stroke="#ffffff" stroke-width="1.5" style="filter: drop-shadow(0 3px 6px rgba(0,0,0,0.4));">
                       <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
                       <circle cx="12" cy="9" r="2.8" fill="#ffffff"/>
                     </svg>
                   </div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 30],
            popupAnchor: [0, -30]
        });

        if (!studentPickerMap) {
            studentPickerMap = L.map('student-leaflet-map', {
                zoomControl: true,
                scrollWheelZoom: true
            }).setView([currentPickedLat, currentPickedLng], 16);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '© OpenStreetMap contributors'
            }).addTo(studentPickerMap);

            studentPickerMarker = L.marker([currentPickedLat, currentPickedLng], {
                draggable: true,
                icon: redPinIcon
            }).addTo(studentPickerMap);

            studentPickerMarker.bindPopup('<b>ตำแหน่งสถานประกอบการ</b><br>คลิกบนแผนที่หรือลากหมุดนี้เพื่อระบุตำแหน่ง').openPopup();

            studentPickerMarker.on('dragend', function(e) {
                const pos = e.target.getLatLng();
                updatePickedCoordinates(pos.lat, pos.lng);
            });

            studentPickerMap.on('click', function(e) {
                studentPickerMarker.setLatLng(e.latlng);
                updatePickedCoordinates(e.latlng.lat, e.latlng.lng);
                studentPickerMarker.openPopup();
            });
        } else {
            studentPickerMap.invalidateSize();
            studentPickerMap.setView([currentPickedLat, currentPickedLng], 16);
            if (studentPickerMarker) {
                studentPickerMarker.setLatLng([currentPickedLat, currentPickedLng]);
            }
        }
    }, 180);
}

// ----------------------------------------------------------------------
// อัปเดตการแสดงผลตัวเลขพิกัดและลิงก์ Google Maps ใน Modal
// ----------------------------------------------------------------------
function updatePickedCoordinates(lat, lng) {
    currentPickedLat = typeof lat === 'number' ? lat : parseFloat(lat);
    currentPickedLng = typeof lng === 'number' ? lng : parseFloat(lng);

    const latStr = currentPickedLat.toFixed(6);
    const lngStr = currentPickedLng.toFixed(6);

    const dispLat = document.getElementById('map-picked-lat-display');
    const dispLng = document.getElementById('map-picked-lng-display');
    if (dispLat) dispLat.textContent = latStr;
    if (dispLng) dispLng.textContent = lngStr;

    const gmapsLink = document.getElementById('map-view-in-gmaps-link');
    if (gmapsLink) {
        gmapsLink.href = `https://www.google.com/maps?q=${latStr},${lngStr}&z=18`;
    }
}

// ----------------------------------------------------------------------
// ค้นหาสถานที่ผ่าน OpenStreetMap Nominatim
// ----------------------------------------------------------------------
async function searchLocationOnMap() {
    const input = document.getElementById('map-picker-search-input');
    const query = input ? input.value.trim() : '';
    if (!query) {
        alert('กรุณากรอกชื่อสถานที่ บริษัท หรือถนนที่ต้องการค้นหา');
        if (input) input.focus();
        return;
    }

    const statusEl = document.getElementById('map-picker-search-status');
    if (statusEl) {
        statusEl.textContent = `กำลังค้นหา "${query}"...`;
        statusEl.style.display = 'block';
    }

    try {
        const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1&countrycodes=th`;
        const res = await fetch(url, {
            headers: { 'Accept-Language': 'th,en' }
        });
        const data = await res.json();

        if (statusEl) statusEl.style.display = 'none';

        if (data && data.length > 0) {
            const first = data[0];
            const lat = parseFloat(first.lat);
            const lon = parseFloat(first.lon);

            if (studentPickerMap && studentPickerMarker) {
                studentPickerMap.setView([lat, lon], 17);
                studentPickerMarker.setLatLng([lat, lon]);
                updatePickedCoordinates(lat, lon);
                const placeShort = first.display_name.split(',')[0];
                studentPickerMarker.bindPopup(`<b>${placeShort}</b><br><span style="font-size:11px;color:#475569;">${first.display_name}</span>`).openPopup();
            }
        } else {
            // ค้นหาแบบทั่วโลก (กรณีชื่อภาษาอังกฤษ)
            const urlGlobal = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`;
            const resG = await fetch(urlGlobal);
            const dataG = await resG.json();
            if (dataG && dataG.length > 0) {
                const first = dataG[0];
                const lat = parseFloat(first.lat);
                const lon = parseFloat(first.lon);
                if (studentPickerMap && studentPickerMarker) {
                    studentPickerMap.setView([lat, lon], 17);
                    studentPickerMarker.setLatLng([lat, lon]);
                    updatePickedCoordinates(lat, lon);
                    const placeShort = first.display_name.split(',')[0];
                    studentPickerMarker.bindPopup(`<b>${placeShort}</b>`).openPopup();
                }
            } else {
                alert(`ไม่พบสถานที่ "${query}" บนแผนที่\n\nท่านสามารถเลื่อนแผนที่หรือคลิกปักหมุดด้วยตนเองได้ครับ`);
            }
        }
    } catch (err) {
        if (statusEl) statusEl.style.display = 'none';
        console.warn("Nominatim search error:", err);
        alert('ไม่สามารถเชื่อมต่อบริการค้นหาสถานที่ได้ในขณะนี้ ท่านสามารถคลิกปักหมุดบนแผนที่ได้โดยตรง');
    }
}

// ----------------------------------------------------------------------
// เลื่อนแผนที่ไปยังพิกัด GPS จริงของเครื่องปัจจุบัน
// ----------------------------------------------------------------------
function centerMapOnDeviceGps() {
    if (!navigator.geolocation) {
        alert('อุปกรณ์หรือเบราว์เซอร์นี้ไม่รองรับระบบ Geolocation');
        return;
    }

    const statusEl = document.getElementById('map-picker-search-status');
    if (statusEl) {
        statusEl.textContent = 'กำลังค้นหาตำแหน่ง GPS ปัจจุบันของคุณ...';
        statusEl.style.display = 'block';
    }

    const onSuccess = (pos) => {
        if (statusEl) statusEl.style.display = 'none';
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        if (studentPickerMap && studentPickerMarker) {
            studentPickerMap.setView([lat, lng], 17);
            studentPickerMarker.setLatLng([lat, lng]);
            updatePickedCoordinates(lat, lng);
            studentPickerMarker.bindPopup('<b>ตำแหน่งปัจจุบันของคุณ (GPS จริง)</b><br>สามารถลากหมุดเพื่อปรับความแม่นยำได้').openPopup();
        }
    };

    const onFail = (err) => {
        navigator.geolocation.getCurrentPosition(
            onSuccess,
            (err2) => {
                if (statusEl) statusEl.style.display = 'none';
                alert('ไม่สามารถดึงตำแหน่งปัจจุบันได้: ' + (err2.name === 'NotAllowedError' ? 'โปรดอนุญาตสิทธิ์ Location ในเบราว์เซอร์' : err2.message));
            },
            { enableHighAccuracy: false, timeout: 15000, maximumAge: 0 }
        );
    };

    navigator.geolocation.getCurrentPosition(onSuccess, onFail, { enableHighAccuracy: true, timeout: 7000, maximumAge: 0 });
}

// ----------------------------------------------------------------------
// ยืนยันการเลือกพิกัด และบันทึกค่ากลับสู่แบบฟอร์ม
// ----------------------------------------------------------------------
function confirmMapPickedLocation() {
    const latId = (mapPickerTarget && mapPickerTarget.latId) ? mapPickerTarget.latId : 'std-input-lat';
    const lngId = (mapPickerTarget && mapPickerTarget.lngId) ? mapPickerTarget.lngId : 'std-input-lng';
    const inputLat = document.getElementById(latId);
    const inputLng = document.getElementById(lngId);

    const latStr = currentPickedLat.toFixed(6);
    const lngStr = currentPickedLng.toFixed(6);

    if (inputLat) inputLat.value = latStr;
    if (inputLng) inputLng.value = lngStr;

    // อัปเดตข้อความแสดงพิกัดที่บันทึกไว้ในหน้าจอของนิสิต
    const coordDisplay = document.getElementById('std-current-loc-display');
    if (coordDisplay && latId === 'std-input-lat') {
        coordDisplay.textContent = `Lat: ${latStr}, Lng: ${lngStr}`;
    }

    if (typeof closeModal === 'function') {
        closeModal('modal-student-map-picker');
    } else {
        const modal = document.getElementById('modal-student-map-picker');
        if (modal) modal.style.display = 'none';
    }

    // หากเป็นการกำหนดพิกัดของนิสิต ให้บันทึกลงระบบทันที
    if (mapPickerTarget && mapPickerTarget.autoSave) {
        if (typeof saveStudentWorkplaceGps === 'function') {
            saveStudentWorkplaceGps(false);
        } else {
            // บันทึกตรงลง localStorage เพื่อความชัวร์
            try {
                const sessionStr = sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser');
                if (sessionStr) {
                    const u = JSON.parse(sessionStr);
                    u.company_lat = latStr;
                    u.company_lng = lngStr;
                    sessionStorage.setItem('currentUser', JSON.stringify(u));
                    localStorage.setItem('currentUser', JSON.stringify(u));
                }
            } catch (e) {}
            alert(`บันทึกพิกัดสถานประกอบการ (Lat: ${latStr}, Lng: ${lngStr}) เรียบร้อยแล้ว!`);
        }
    }
}
