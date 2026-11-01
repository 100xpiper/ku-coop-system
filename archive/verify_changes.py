# -*- coding: utf-8 -*-
import urllib.request
import re

def verify():
    # 1. Check local file contents
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()

    checks = {
        "Has sidebar toggle button": 'id="sidebar-toggle-btn"' in html,
        "Has sidebar backdrop": 'id="sidebar-backdrop"' in html,
        "Has collapsed CSS": '.desktop-sidebar.collapsed' in html,
        "Has mobile responsive query": '@media (max-width: 768px)' in html,
        "Has camera video tag": 'id="qr-camera-video"' in html,
        "Has startRealCameraScanner": 'function startRealCameraScanner()' in html,
        "Has stopRealCameraScanner": 'function stopRealCameraScanner()' in html,
        "Has toggleSidebar": 'function toggleSidebar(' in html,
        "Has scanner viewport box": 'class="scanner-viewport-box"' in html,
        "Has scanner laser anim": 'scanLaserAnim' in html,
        "No emoji in dashboard.html": not re.search(r'[\U0001F300-\U0001F9FF]', html),
    }

    print("=== FILE CHECKS ===")
    all_ok = True
    for name, result in checks.items():
        status = "PASS" if result else "FAIL"
        print(f"[{status}] {name}")
        if not result:
            all_ok = False

    # 2. Check HTTP Server response
    print("\n=== SERVER RESPONSE CHECK ===")
    try:
        req = urllib.request.urlopen("http://localhost:8080/dashboard.html", timeout=5)
        print(f"[PASS] HTTP Status: {req.status}")
        body = req.read().decode('utf-8', errors='ignore')
        print(f"[PASS] HTTP Body received, length: {len(body)}")
        if 'id="sidebar-toggle-btn"' in body and 'id="qr-camera-video"' in body:
            print("[PASS] Served content contains new features!")
        else:
            print("[FAIL] Served content missing features!")
            all_ok = False
    except Exception as e:
        print(f"[FAIL] HTTP error: {e}")
        all_ok = False

    return all_ok

if __name__ == '__main__':
    ok = verify()
    exit(0 if ok else 1)

