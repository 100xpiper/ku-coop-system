import subprocess
import time

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Run chrome headless with --dump-dom
res = subprocess.run([
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--dump-dom",
    "http://localhost:8080/dashboard.html"
], capture_output=True, text=True, encoding="utf-8", errors="ignore")

print("Output length:", len(res.stdout))
print("Contains 'index.html' redirect logic or title:")
if "เข้าสู่ระบบ" in res.stdout or "ระบบสหกิจศึกษา" in res.stdout:
    print("Found login page text in DOM!")
for line in res.stdout.split('\n')[:25]:
    print(line)
