"""ปรับแต่งและสร้างภาพหน้าจอ UI ระบบที่เกี่ยวข้อง 3 ระบบ ให้คมชัด ไร้ scrollbar สวยงามระดับมืออาชีพ"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

output_dir = "screenshots/related_systems"
os.makedirs(output_dir, exist_ok=True)

# 1. QR Attendance System UI (ไม่มี scrollbar, จัดวางสมบูรณ์แบบ)
html_qr = """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>QR Code Attendance System</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
  body { background: #f8fafc; padding: 24px; color: #1e293b; width: 1080px; }
  .header { background: #0f172a; color: white; padding: 18px 24px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.06); margin-bottom: 20px; }
  .header h1 { font-size: 20px; font-weight: 700; letter-spacing: -0.3px; }
  .header p { font-size: 13px; color: #94a3b8; margin-top: 3px; }
  .header .badge { background: #10b981; color: white; padding: 6px 14px; border-radius: 20px; font-size: 12.5px; font-weight: 600; }
  .grid { display: grid; grid-template-columns: 1.15fr 1fr; gap: 20px; }
  .card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; display: flex; flex-direction: column; }
  .card-title { font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; }
  .scanner-view { background: #020617; border-radius: 10px; height: 230px; position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; border: 2px solid #334155; }
  .reticle { width: 150px; height: 150px; border: 3px solid #10b981; border-radius: 14px; position: relative; box-shadow: 0 0 20px rgba(16,185,129,0.3); }
  .laser { position: absolute; width: 100%; height: 3px; background: #10b981; top: 48%; box-shadow: 0 0 10px #10b981; }
  .scan-tip { margin-top: 12px; font-size: 12.5px; color: #10b981; font-weight: 600; display: flex; align-items: center; gap: 6px; }
  .pulse { width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block; }
  .controls { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 14px; }
  .btn { padding: 9px; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; text-align: center; }
  .btn-primary { background: #2563eb; color: white; }
  .btn-outline { background: #f8fafc; color: #475569; border: 1px solid #cbd5e1; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { text-align: left; padding: 8px 10px; background: #f8fafc; color: #475569; font-weight: 600; border-bottom: 2px solid #e2e8f0; }
  td { padding: 9px 10px; border-bottom: 1px solid #f1f5f9; color: #334155; }
  .tag { display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 11.5px; font-weight: 600; }
  .tag-green { background: #d1fae5; color: #065f46; }
  .info-bar { margin-top: auto; padding: 10px 12px; background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; font-size: 12px; color: #0369a1; line-height: 1.4; }
  .warning-bar { margin-top: auto; padding: 10px 12px; background: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; font-size: 12px; color: #92400e; line-height: 1.4; }
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1>ระบบลงเวลาและเช็คชื่อด้วย QR Code (QR Code Attendance System)</h1>
      <p>ระบบบันทึกเวลาการเข้าร่วมกิจกรรมและปฏิบัติงานผ่านการสแกนรหัสสองมิติแบบเรียลไทม์</p>
    </div>
    <div class="badge">● เชื่อมต่อกล้องพร้อมใช้งาน</div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-title">
        <span>กล้องสแกนตรวจสอบรหัส QR Code</span>
        <span style="font-size: 12px; font-weight: 400; color: #64748b;">โหมด: ตรวจจับอัตโนมัติ</span>
      </div>
      <div class="scanner-view">
        <div class="reticle">
          <div class="laser"></div>
        </div>
        <div class="scan-tip"><span class="pulse"></span> กล้องกำลังสแกนรหัส QR Code ของผู้เข้าร่วม...</div>
      </div>
      <div class="controls">
        <button class="btn btn-primary">สแกนผ่านกล้องเว็บ</button>
        <button class="btn btn-outline">อัปโหลดรูปภาพ QR Code</button>
      </div>
      <div class="info-bar">
        <strong>หลักการทำงาน:</strong> ระบบอ่านข้อมูลแบบภาพสองมิติและถอดรหัสผ่านกล้องเบราว์เซอร์ เพื่อบันทึกเวลาเข้าสู่ฐานข้อมูลโดยตรง
      </div>
    </div>
    <div class="card">
      <div class="card-title">
        <span>รายการบันทึกเวลาล่าสุด (Attendance Logs)</span>
        <span style="font-size: 12px; font-weight: 600; color: #2563eb;">วันนี้: 4 รายการ</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>รหัสนิสิต</th>
            <th>ชื่อ - นามสกุล</th>
            <th>เวลาที่บันทึก</th>
            <th>ผลการตรวจสอบ</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>6510402280</strong></td>
            <td>นาย วงศพัทธ์ อุเทน</td>
            <td>09:00:15 น.</td>
            <td><span class="tag tag-green">สำเร็จ (ตรงเวลา)</span></td>
          </tr>
          <tr>
            <td><strong>6510401145</strong></td>
            <td>นาย กิตติศักดิ์ พานิช</td>
            <td>09:04:30 น.</td>
            <td><span class="tag tag-green">สำเร็จ (ตรงเวลา)</span></td>
          </tr>
          <tr>
            <td><strong>6510403328</strong></td>
            <td>นางสาว นลินรัตน์ ศรีสุข</td>
            <td>09:08:12 น.</td>
            <td><span class="tag tag-green">สำเร็จ (ตรงเวลา)</span></td>
          </tr>
          <tr>
            <td><strong>6510404491</strong></td>
            <td>นาย ธีรเทพ พรหมพิชัย</td>
            <td>09:12:45 น.</td>
            <td><span class="tag tag-green">สำเร็จ (ตรงเวลา)</span></td>
          </tr>
        </tbody>
      </table>
      <div class="warning-bar">
        <strong>ข้อจำกัดเชิงระบบ:</strong> หากไม่มีระบบตรวจสอบพิกัดตำแหน่งทางกายภาพควบคู่ อาจมีความเสี่ยงในการส่งต่อภาพ QR Code ให้ผู้อื่นสแกนแทนได้
      </div>
    </div>
  </div>
</body>
</html>"""

# 2. GPS Geofencing System UI
html_geofence = """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>GPS Geofencing Verification System</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
  body { background: #f8fafc; padding: 24px; color: #1e293b; width: 1080px; }
  .header { background: #0f172a; color: white; padding: 18px 24px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.06); margin-bottom: 20px; }
  .header h1 { font-size: 20px; font-weight: 700; letter-spacing: -0.3px; }
  .header p { font-size: 13px; color: #94a3b8; margin-top: 3px; }
  .header .badge { background: #0284c7; color: white; padding: 6px 14px; border-radius: 20px; font-size: 12.5px; font-weight: 600; }
  .grid { display: grid; grid-template-columns: 1.25fr 1fr; gap: 20px; }
  .card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; display: flex; flex-direction: column; }
  .card-title { font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 12px; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; display: flex; justify-content: space-between; }
  #map { height: 320px; border-radius: 10px; border: 2px solid #cbd5e1; }
  .info-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f5f9; font-size: 13px; }
  .info-label { color: #64748b; font-weight: 600; }
  .info-val { color: #0f172a; font-weight: 600; }
  .status-box { margin-top: 14px; padding: 12px; background: #ecfdf5; border: 1.5px solid #a7f3d0; border-radius: 10px; display: flex; align-items: center; gap: 10px; }
  .status-icon { width: 32px; height: 32px; background: #10b981; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: bold; flex-shrink: 0; }
  .status-text h4 { font-size: 13.5px; color: #065f46; font-weight: 700; }
  .status-text p { font-size: 11.5px; color: #047857; margin-top: 2px; }
  .legend { display: flex; gap: 14px; margin-top: 10px; font-size: 12px; color: #64748b; }
  .legend-item { display: flex; align-items: center; gap: 5px; }
  .dot { width: 10px; height: 10px; border-radius: 50%; }
  .footer-note { margin-top: auto; padding: 10px 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 12px; color: #64748b; line-height: 1.4; }
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1>ระบบตรวจสอบพิกัดและขอบเขตพื้นที่เสมือน (GPS Geofencing System)</h1>
      <p>การคำนวณและตรวจสอบระยะห่างตำแหน่งทางภูมิศาสตร์ด้วยเทคโนโลยี Geofencing</p>
    </div>
    <div class="badge">● GPS ความแม่นยำสูง (±5 ม.)</div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-title">
        <span>แผนที่แสดงรัศมีขอบเขตพื้นที่เสมือน (Geofence Perimeter)</span>
        <span style="font-size: 12px; font-weight: 600; color: #0284c7;">รัศมี: 500 เมตร</span>
      </div>
      <div id="map"></div>
      <div class="legend">
        <div class="legend-item"><div class="dot" style="background: #ef4444;"></div> หมุดสถานประกอบการ</div>
        <div class="legend-item"><div class="dot" style="background: #3b82f6;"></div> รัศมี Geofence 500 ม.</div>
        <div class="legend-item"><div class="dot" style="background: #10b981;"></div> พิกัดปัจจุบันของผู้ใช้</div>
      </div>
    </div>
    <div class="card">
      <div class="card-title">
        <span>ผลการตรวจสอบพิกัดและระยะห่าง</span>
        <span style="font-size: 12px; font-weight: 400; color: #64748b;">คำนวณด้วย Haversine Formula</span>
      </div>
      <div class="info-row">
        <span class="info-label">พิกัดสถานประกอบการ:</span>
        <span class="info-val">13.8476° N, 100.5696° E</span>
      </div>
      <div class="info-row">
        <span class="info-label">พิกัดปัจจุบันของผู้ใช้:</span>
        <span class="info-val">13.8488° N, 100.5702° E</span>
      </div>
      <div class="info-row">
        <span class="info-label">ระยะห่างจากการคำนวณ:</span>
        <span class="info-val" style="color: #0284c7; font-size: 14.5px;">148.50 เมตร</span>
      </div>
      <div class="info-row">
        <span class="info-label">เกณฑ์รัศมีที่อนุญาต:</span>
        <span class="info-val">ไม่เกิน 500.00 เมตร</span>
      </div>

      <div class="status-box">
        <div class="status-icon">✓</div>
        <div class="status-text">
          <h4>ผ่านเกณฑ์การตรวจสอบขอบเขตพื้นที่</h4>
          <p>ตำแหน่งของผู้ใช้งานอยู่ในรัศมี Geofencing สามารถบันทึกเวลาการนิเทศได้</p>
        </div>
      </div>

      <div class="footer-note">
        <strong>การประยุกต์ใช้:</strong> ป้องกันการเช็คอินนอกสถานที่ และยืนยันว่าอาจารย์นิเทศและนิสิตได้เข้าพบปะ ณ สถานประกอบการจริง
      </div>
    </div>
  </div>

  <script>
    var lat = 13.8476, lng = 100.5696;
    var map = L.map('map', {zoomControl: false}).setView([lat, lng], 15);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
    }).addTo(map);

    var markerCo = L.circleMarker([lat, lng], {
      radius: 8,
      fillColor: "#ef4444",
      color: "#ffffff",
      weight: 2,
      opacity: 1,
      fillOpacity: 1
    }).addTo(map);

    var circle = L.circle([lat, lng], {
      color: '#2563eb',
      fillColor: '#3b82f6',
      fillOpacity: 0.15,
      weight: 2,
      radius: 500
    }).addTo(map);

    var markerUser = L.circleMarker([13.8488, 100.5702], {
      radius: 8,
      fillColor: "#10b981",
      color: "#ffffff",
      weight: 2,
      opacity: 1,
      fillOpacity: 1
    }).addTo(map);
  </script>
</body>
</html>"""

# 3. Online Cooperative Education Document System UI
html_docs = """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>Online Cooperative Education Document System</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
  body { background: #f8fafc; padding: 24px; color: #1e293b; width: 1080px; }
  .header { background: #0f172a; color: white; padding: 18px 24px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.06); margin-bottom: 20px; }
  .header h1 { font-size: 20px; font-weight: 700; letter-spacing: -0.3px; }
  .header p { font-size: 13px; color: #94a3b8; margin-top: 3px; }
  .header .badge { background: #6366f1; color: white; padding: 6px 14px; border-radius: 20px; font-size: 12.5px; font-weight: 600; }
  .grid { display: grid; grid-template-columns: 1.15fr 1fr; gap: 20px; }
  .card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; display: flex; flex-direction: column; }
  .card-title { font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 12px; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; display: flex; justify-content: space-between; }
  .form-group { margin-bottom: 11px; }
  .form-label { display: block; font-size: 12.5px; font-weight: 600; color: #334155; margin-bottom: 4px; }
  .form-input { width: 100%; padding: 8px 10px; border: 1px solid #cbd5e1; border-radius: 7px; font-size: 13px; background: #f8fafc; color: #1e293b; }
  .upload-box { border: 2px dashed #cbd5e1; border-radius: 8px; padding: 14px; text-align: center; background: #f8fafc; }
  .upload-icon { font-size: 22px; color: #6366f1; margin-bottom: 4px; }
  .btn-submit { width: 100%; background: #6366f1; color: white; border: none; padding: 10px; border-radius: 7px; font-size: 13.5px; font-weight: 600; margin-top: 8px; cursor: pointer; }
  .doc-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 9px; background: #ffffff; }
  .doc-name { font-size: 13px; font-weight: 600; color: #1e293b; }
  .doc-meta { font-size: 11.5px; color: #64748b; margin-top: 2px; }
  .tag { padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; }
  .tag-approved { background: #dcfce7; color: #15803d; }
  .tag-pending { background: #fef9c3; color: #a16207; }
  .footer-note { margin-top: auto; padding: 10px 12px; background: #eef2ff; border: 1px solid #c7d2fe; border-radius: 8px; font-size: 12px; color: #3730a3; line-height: 1.4; }
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1>ระบบจัดการและส่งเอกสารแบบฟอร์มสหกิจศึกษาออนไลน์ (Online Document System)</h1>
      <p>การบันทึกรายงานความก้าวหน้าและการตรวจรับเอกสารสหกิจศึกษาแบบดิจิทัล</p>
    </div>
    <div class="badge">● ระบบรับเอกสารเปิดให้บริการ</div>
  </div>
  <div class="grid">
    <div class="card">
      <div class="card-title">
        <span>แบบฟอร์มบันทึกและส่งรายงานการปฏิบัติงาน</span>
        <span style="font-size: 12px; font-weight: 600; color: #6366f1;">FORM-02: รายงานประจำสัปดาห์</span>
      </div>
      <div class="form-group">
        <label class="form-label">สัปดาห์ที่ปฏิบัติงาน</label>
        <input class="form-input" value="สัปดาห์ที่ 4 (ระหว่างวันที่ 15 - 19 ก.ค. 2567)" readonly>
      </div>
      <div class="form-group">
        <label class="form-label">งานที่ได้รับมอบหมายและผลการดำเนินงาน</label>
        <textarea class="form-input" style="height: 60px; resize: none;" readonly>พัฒนาโมดูลสแกน QR Code และทดสอบระบบตรวจสอบพิกัด Geofencing ร่วมกับเซิร์ฟเวอร์จำลอง</textarea>
      </div>
      <div class="form-group">
        <label class="form-label">แนบไฟล์รายงาน / เอกสารประกอบ (PDF ไม่เกิน 10MB)</label>
        <div class="upload-box">
          <div class="upload-icon">📄</div>
          <div style="font-size: 12.5px; font-weight: 600; color: #475569;">FORM-02_Wongsapat_Week4.pdf (1.2 MB)</div>
          <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">อัปโหลดและตรวจสอบความถูกต้องแล้ว</div>
        </div>
      </div>
      <button class="btn-submit">ส่งเอกสารให้อาจารย์นิเทศตรวจรับ</button>
    </div>

    <div class="card">
      <div class="card-title">
        <span>สถานะการตรวจรับเอกสารสหกิจศึกษา (Document Tracking)</span>
        <span style="font-size: 12px; font-weight: 400; color: #64748b;">ตรวจรับแบบรายฉบับ</span>
      </div>
      
      <div class="doc-item">
        <div>
          <div class="doc-name">FORM-00: ใบสมัครและข้อมูลสถานประกอบการ</div>
          <div class="doc-meta">ส่งเมื่อ 10 มิ.ย. 2567 | ตรวจโดย: อ.ปรวี วงศ์สวัสดิ์สุริยะ</div>
        </div>
        <span class="tag tag-approved">อนุมัติแล้ว</span>
      </div>

      <div class="doc-item">
        <div>
          <div class="doc-name">FORM-01: แผนปฏิบัติงานสหกิจศึกษา</div>
          <div class="doc-meta">ส่งเมื่อ 24 มิ.ย. 2567 | ตรวจโดย: อ.ปรวี วงศ์สวัสดิ์สุริยะ</div>
        </div>
        <span class="tag tag-approved">อนุมัติแล้ว</span>
      </div>

      <div class="doc-item">
        <div>
          <div class="doc-name">FORM-02: รายงานประจำสัปดาห์ (Week 1-4)</div>
          <div class="doc-meta">ส่งเมื่อ 19 ก.ค. 2567 | รอการตรวจรับ</div>
        </div>
        <span class="tag tag-pending">รออาจารย์ตรวจรับ</span>
      </div>

      <div class="footer-note">
        <strong>ข้อดีเชิงระบบ:</strong> สามารถติดตามความคืบหน้าของเอกสารได้รายฉบับ ลดการสูญหายของเอกสารกระดาษ และอาจารย์สามารถให้ข้อเสนอแนะสะท้อนกลับได้ทันที
      </div>
    </div>
  </div>
</body>
</html>"""

files = {
    "screenshots/test_capture/ui_qr.html": html_qr,
    "screenshots/test_capture/ui_geofence.html": html_geofence,
    "screenshots/test_capture/ui_docs.html": html_docs,
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1140,750")
driver = webdriver.Chrome(options=options)

targets = [
    ("screenshots/test_capture/ui_qr.html", f"{output_dir}/01_qr_attendance_system.png"),
    ("screenshots/test_capture/ui_geofence.html", f"{output_dir}/02_gps_geofencing_system.png"),
    ("screenshots/test_capture/ui_docs.html", f"{output_dir}/03_online_document_system.png"),
]

for src, dst in targets:
    abs_src = "file:///" + os.path.abspath(src).replace("\\", "/")
    driver.get(abs_src)
    time.sleep(2)
    driver.save_screenshot(dst)
    print(f"Captured: {dst}")

driver.quit()
print("All optimized screenshots generated successfully!")
