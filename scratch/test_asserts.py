# -*- coding: utf-8 -*-
import urllib.request

req = urllib.request.urlopen("http://localhost:8080/dashboard.html")
html = req.read().decode('utf-8')

assert 'id="sidebar-toggle-btn"' in html
assert 'function toggleSidebar(' in html
assert '.desktop-sidebar.collapsed' in html
assert 'startRealCameraScanner' in html
print("All assertions passed 100%!")

