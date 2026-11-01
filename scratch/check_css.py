with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.mobile-device {')
if idx != -1:
    with open('scratch/css_layout.txt', 'w', encoding='utf-8') as out:
        out.write(text[idx-50:idx+2000])
    print("Found .mobile-device CSS")
else:
    print(".mobile-device { not found")

