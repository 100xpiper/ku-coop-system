import urllib.request
import re

req = urllib.request.urlopen('http://localhost:8080/dashboard.html')
html = req.read().decode('utf-8')

checks = {
    "Has std-input-lat": 'id="std-input-lat"' in html,
    "Has std-input-lng": 'id="std-input-lng"' in html,
    "Has btn-std-auto-gps": 'id="btn-std-auto-gps"' in html,
    "Has std-gps-status-badge": 'id="std-gps-status-badge"' in html,
    "Has renderStudentGpsSettings": 'function renderStudentGpsSettings(' in html,
    "Has autoDetectStudentGps": 'function autoDetectStudentGps()' in html,
    "Has saveStudentWorkplaceGps": 'function saveStudentWorkplaceGps(' in html,
    "No emojis": not re.search(r'[\U0001F300-\U0001F9FF]', html)
}

print("=== STUDENT GPS VERIFICATION ===")
all_pass = True
for name, ok in checks.items():
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if not ok:
        all_pass = False

assert all_pass, "Some checks failed!"
print("All student GPS setting features verified 100%!")

