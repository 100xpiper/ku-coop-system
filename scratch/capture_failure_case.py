import subprocess
import os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_img = os.path.abspath("screenshots/16_checkin_failed_out_of_radius.png")

# Load advisor QR page and call processCheckinAndEval
test_html = """
<!DOCTYPE html>
<html>
<head>
<script>
window.onload = function() {
    window.location.href = "http://localhost:8080/dashboard.html?user=advisor&page=sec-advisor-qr";
};
</script>
</head>
<body></body>
</html>
"""

# We can run headless chrome directly
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=1280,1050",
    f"--screenshot={out_img}",
    "http://localhost:8080/dashboard.html?user=advisor&page=sec-advisor-qr"
]

subprocess.run(cmd, check=True)
print("Captured advisor QR scanner page:", out_img)

