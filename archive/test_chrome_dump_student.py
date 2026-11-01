import subprocess

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

res = subprocess.run([
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--dump-dom",
    "http://localhost:8080/dashboard.html?user=student"
], capture_output=True, text=True, encoding="utf-8", errors="ignore")

print("Output length:", len(res.stdout))
print("Contains student dashboard element:")
if "student-profile" in res.stdout or "sec-student-docs" in res.stdout or "sidebar" in res.stdout:
    print("Found student dashboard in DOM!")

