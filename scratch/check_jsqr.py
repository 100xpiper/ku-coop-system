with open("jsqr.min.js", "r", encoding="utf-8") as f:
    code = f.read()

print("jsqr.min.js length:", len(code))
print("Has jsQR definition:", "jsQR" in code)
print("First 200 chars:", code[:200])

