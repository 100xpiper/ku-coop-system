import urllib.request
import re

req = urllib.request.urlopen('http://localhost:8080/dashboard.html')
html = req.read().decode('utf-8')

checks = {
    "Has calculateHaversineDistance": 'function calculateHaversineDistance(' in html,
    "Has MAX_ALLOWED_RADIUS = 500": 'MAX_ALLOWED_RADIUS = 500' in html,
    "Has qr-result-warning-box": 'id="qr-result-warning-box"' in html,
    "Has btn-eval-disabled-notice": 'id="btn-eval-disabled-notice"' in html,
    "Has qr-result-target-gps": 'id="qr-result-target-gps"' in html,
    "Has qr-result-distance": 'id="qr-result-distance"' in html,
    "No emojis": not re.search(r'[\U0001F300-\U0001F9FF]', html)
}

print("=== 500M GEO-FENCE VERIFICATION ===")
all_pass = True
for name, ok in checks.items():
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if not ok:
        all_pass = False

assert all_pass, "Some checks failed!"
print("500-meter geo-fence verification passed 100%!")

