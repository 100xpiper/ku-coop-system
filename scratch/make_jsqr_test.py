# -*- coding: utf-8 -*-
import subprocess
import base64
import json

with open("scratch/test_qr_std.png", "rb") as f:
    b64_img = base64.b64encode(f.read()).decode('utf-8')

test_html = f"""
<!DOCTYPE html>
<html>
<head>
<script src="jsqr.min.js"></script>
</head>
<body>
<img id="img" src="data:image/png;base64,{b64_img}">
<div id="result">WAITING</div>
<script>
window.onload = function() {{
    const img = document.getElementById('img');
    const canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const code = jsQR(imgData.data, imgData.width, imgData.height);
    if (code) {{
        document.getElementById('result').innerText = 'DECODED: ' + code.data;
    }} else {{
        document.getElementById('result').innerText = 'FAILED';
    }}
}};
</script>
</body>
</html>
"""

with open("test_jsqr_runner.html", "w", encoding="utf-8") as f:
    f.write(test_html)

print("Saved test_jsqr_runner.html")

