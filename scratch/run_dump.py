import subprocess

cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--disable-gpu",
    "--virtual-time-budget=2000",
    "--dump-dom",
    "http://localhost:8080/test_jsqr_runner.html"
]

res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
print("DOM output:")
for line in res.stdout.splitlines():
    if 'DECODED' in line or 'FAILED' in line or 'WAITING' in line:
        print(line)

