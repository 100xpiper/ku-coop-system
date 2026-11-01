import sys

with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx2 = text.find('Modal 3')
if idx2 != -1:
    modal_content = text[idx2:idx2+3000]
    with open('scratch/modal3_snippet.txt', 'w', encoding='utf-8') as out:
        out.write(modal_content)
    print("Modal 3 saved to scratch/modal3_snippet.txt")

# Also check qr scanner and sidebar collapse status
print("Has startRealCameraScanner:", "startRealCameraScanner" in text)
print("Has toggleSidebar:", "toggleSidebar" in text)
print("Has mobile-device:", "mobile-device" in text)
print("Has desktop-sidebar.collapsed:", "desktop-sidebar.collapsed" in text)

