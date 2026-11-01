with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Inspect header and sidebar
idx = text.find('class="desktop-sidebar"')
if idx != -1:
    with open('scratch/sidebar_structure.txt', 'w', encoding='utf-8') as out:
        out.write(text[idx-200:idx+2500])
    print("Saved sidebar structure to scratch/sidebar_structure.txt")

# Inspect main content wrapper
idx2 = text.find('class="mobile-device"')
if idx2 != -1:
    print("Found mobile-device at", idx2)

