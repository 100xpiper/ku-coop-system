# -*- coding: utf-8 -*-
import subprocess
import os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_collapsed = os.path.abspath("screenshots/14_desktop_collapsed_sidebar.png")

# Use a test file or html query that adds collapsed class
test_html = """
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="0; url=http://localhost:8080/dashboard.html?user=advisor">
<script>
window.onload = function() {
    setTimeout(function() {
        document.getElementById('desktop-sidebar').classList.add('collapsed');
    }, 100);
};
</script>
</head>
<body></body>
</html>
"""

# Let's directly capture with chrome devtools or load dashboard and execute JS:
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=1280,850",
    f"--screenshot={out_collapsed}",
    "http://localhost:8080/dashboard.html?user=advisor"
]
subprocess.run(cmd, check=True)
print("Standard desktop captured:", out_collapsed)

