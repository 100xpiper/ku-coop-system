import urllib.request

urls = [
    "https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/html5-qrcode/2.3.8/html5-qrcode.min.js",
    "https://unpkg.com/jsqr@1.4.0/dist/jsQR.js"
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read()
            print(f"Success fetching {url}: length {len(data)}")
            with open("jsqr.min.js", "wb") as f:
                f.write(data)
            print("Saved to jsqr.min.js")
            break
    except Exception as e:
        print(f"Failed {url}: {e}")

