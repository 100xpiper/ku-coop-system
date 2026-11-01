import urllib.request
import os

url = "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=6521650101"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as res:
        with open("scratch/test_qr_std.png", "wb") as f:
            f.write(res.read())
    print("Test QR Code for 6521650101 saved to scratch/test_qr_std.png")
except Exception as e:
    print("Could not download sample QR:", e)

