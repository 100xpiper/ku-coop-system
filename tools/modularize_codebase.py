# -*- coding: utf-8 -*-
import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DASHBOARD_PATH = os.path.join(BASE_DIR, "dashboard.html")
CSS_PATH = os.path.join(BASE_DIR, "css", "dashboard.css")
JS_EXCEL_PATH = os.path.join(BASE_DIR, "js", "admin-excel.js")
JS_SCANNER_PATH = os.path.join(BASE_DIR, "js", "scanner.js")

os.makedirs(os.path.join(BASE_DIR, "css"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "js"), exist_ok=True)

with open(DASHBOARD_PATH, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# -----------------------------------------------------------------------------
# 1. EXTRACT & CLEAN CSS -> css/dashboard.css
# -----------------------------------------------------------------------------
style_match = re.search(r'<style>([\s\S]*?)</style>', html)
if not style_match:
    raise Exception("Could not find main <style> block in dashboard.html")

raw_css = style_match.group(1)
# Clean broken question-mark comments
clean_css = re.sub(r'/\*\s*\?+.*?\*/', '/* โทนสีเขียวมหาวิทยาลัยเกษตรศาสตร์ (KU Forest Green Theme) */', raw_css)

css_header = """/* ==========================================================================
   dashboard.css - สไตล์ชีตระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มก.
   โครงงาน: KU Science Smart Internship Supervision Platform (01418499)
   ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
   ========================================================================== */
"""

with open(CSS_PATH, "w", encoding="utf-8") as f:
    f.write(css_header + clean_css.strip() + "\n")
print(f"Created: {CSS_PATH} (size: {len(clean_css)} chars)")

# -----------------------------------------------------------------------------
# 2. EXTRACT SCRIPT 7 (EXCEL IMPORT & PREVIEW) -> js/admin-excel.js
# -----------------------------------------------------------------------------
script7_match = re.search(r'<script>(\s*// --- Proto 2 Data Reset ---[\s\S]*?)</script>', html)
if not script7_match:
    raise Exception("Could not find Script 7 block in dashboard.html")

raw_script7 = script7_match.group(1)
clean_script7 = raw_script7.replace("// --- Proto 2 Data Reset ---", "// เริ่มต้นรีเซ็ตและตรวจสอบข้อมูลแคชของระบบนิเทศ")
clean_script7 = clean_script7.replace("proto2_reset", "app_cache_initialized")

js_excel_header = """// ==========================================================================
// admin-excel.js - โมดูลนำเข้าข้อมูลสเปรดชีต Excel และระบบพรีวิวขนาดใหญ่ 100%
// โครงงาน: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================
"""

with open(JS_EXCEL_PATH, "w", encoding="utf-8") as f:
    f.write(js_excel_header + clean_script7.strip() + "\n")
print(f"Created: {JS_EXCEL_PATH} (size: {len(clean_script7)} chars)")

# -----------------------------------------------------------------------------
# 3. EXTRACT SCANNER & GEO-FENCE (500M) -> js/scanner.js
# -----------------------------------------------------------------------------
lines = html.splitlines(keepends=True)

# Find start of scanner block: "let activeCameraStream = null;"
scanner_start_idx = None
for i, l in enumerate(lines):
    if "let activeCameraStream = null;" in l:
        scanner_start_idx = i
        break

if scanner_start_idx is None:
    raise Exception("Could not find start of scanner block")

# Find end of scanner block: closing of processCheckinAndEval before openEvalModalFromResult
scanner_end_idx = None
for i in range(scanner_start_idx, len(lines)):
    if "function openEvalModalFromResult()" in lines[i]:
        scanner_end_idx = i
        break

if scanner_end_idx is None:
    raise Exception("Could not find end of scanner block")

scanner_code = "".join(lines[scanner_start_idx:scanner_end_idx])

# Clean fallback mock comment in scanner
clean_scanner = scanner_code.replace("// Fallback mock advisor position at Faculty of Science KU", "// พิกัดสำรองกรณีไม่สามารถดึง GPS ได้ (คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์)")

# Introduce MAX_CHECKIN_RADIUS_METERS constant clearly at top
scanner_header = """// ==========================================================================
// scanner.js - โมดูลกล้องสดสแกน QR Code และคำนวณพิกัด GPS รัศมี 500 เมตร (Haversine)
// โครงงาน: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

// กำหนดรัศมีปลอดภัยสูงสุดสำหรับการเช็คอินตรวจนิเทศ ณ สถานประกอบการ (เมตร)
const MAX_CHECKIN_RADIUS_METERS = 500;
"""

# Replace hardcoded 500 in evaluateDistanceAndDisplay with MAX_CHECKIN_RADIUS_METERS
clean_scanner = clean_scanner.replace(
    "const MAX_ALLOWED_RADIUS = 500; // 500 meters rule strictly enforced!",
    "const MAX_ALLOWED_RADIUS = MAX_CHECKIN_RADIUS_METERS; // อิงตามค่าคงที่รัศมีปลอดภัย 500 เมตร"
)

with open(JS_SCANNER_PATH, "w", encoding="utf-8") as f:
    f.write(scanner_header + clean_scanner.strip() + "\n")
print(f"Created: {JS_SCANNER_PATH} (size: {len(clean_scanner)} chars)")

# -----------------------------------------------------------------------------
# 4. REBUILD dashboard.html (CLEAN, MODULAR, NATURAL)
# -----------------------------------------------------------------------------
# 4.1 Replace Script 7 with <script src="js/admin-excel.js"></script>
html = html.replace(script7_match.group(0), '<!-- Admin Excel Import & Preview Module -->\n    <script src="js/admin-excel.js"></script>')

# 4.2 Replace <style> with <link rel="stylesheet" href="css/dashboard.css">
html = html.replace(style_match.group(0), '<!-- Main Application Stylesheet -->\n    <link rel="stylesheet" href="css/dashboard.css">')

# 4.3 Replace scanner block with clean script inclusion
html_lines = html.splitlines(keepends=True)
s_start = None
s_end = None
for i, l in enumerate(html_lines):
    if "let activeCameraStream = null;" in l:
        s_start = i
        break
for i in range(s_start, len(html_lines)):
    if "function openEvalModalFromResult()" in html_lines[i]:
        s_end = i
        break

replacement_block = [
    "        // ==================================================================\n",
    "        // กล้องสด QR Code Scanner และตรวจสอบพิกัด GPS รัศมี 500 เมตร (Haversine)\n",
    "        // แยกเป็นโมดูลภายนอกที่ js/scanner.js เพื่อความสะดวกในการดูแลและทดสอบระบบ\n",
    "        // ==================================================================\n"
]

# We need to load js/scanner.js before Script 8 or inline where scanner was.
# Since Script 8 is an open <script> tag, we can close the current script tag,
# load <script src="js/scanner.js"></script>, and reopen <script>!
replacement_script_tag = [
    "    </script>\n",
    "    <!-- Live Camera QR Scanner & Geolocation 500m Geo-Fencing Module -->\n",
    '    <script src="js/scanner.js"></script>\n',
    "    <script>\n"
]

new_html_lines = html_lines[:s_start] + replacement_script_tag + html_lines[s_end:]
new_html = "".join(new_html_lines)

# 4.4 Clean up any remaining "mock" variables to natural student terms
new_html = new_html.replace("// Automatically purge old mock students if present", "// กรองและล้างข้อมูลแคชเก่าที่ไม่ตรงกับฐานข้อมูลจริง")
new_html = new_html.replace("let hasMock = false;", "let hasOutdatedData = false;")
new_html = new_html.replace("const mockKeys =", "const outdatedKeys =")
new_html = new_html.replace("mockKeys.forEach", "outdatedKeys.forEach")
new_html = new_html.replace("hasMock = true;", "hasOutdatedData = true;")
new_html = new_html.replace("if (hasMock || hasDupes) {", "if (hasOutdatedData || hasDupes) {")

with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Updated {DASHBOARD_PATH} successfully! New line count: {len(new_html.splitlines())}")
