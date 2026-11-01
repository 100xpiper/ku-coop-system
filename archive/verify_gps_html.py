import urllib.request

req = urllib.request.urlopen('http://localhost:8080/dashboard.html')
html = req.read().decode('utf-8')
print('Has enableHighAccuracy:', 'enableHighAccuracy: true' in html)
print('Has qr-result-map-link:', 'id="qr-result-map-link"' in html)
print('Has qr-result-accuracy:', 'id="qr-result-accuracy"' in html)
print('Has qr-result-source:', 'id="qr-result-source"' in html)

