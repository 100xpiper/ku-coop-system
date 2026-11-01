with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find sec-advisor-photos
idx = text.find('id="sec-advisor-photos"')
if idx != -1:
    print("Found sec-advisor-photos at", idx)
    print("--- CONTENT SNIPPET ---")
    print(text[idx:idx+2500])

# Find photo modal
idx2 = text.find('Modal 3')
if idx2 != -1:
    print("--- MODAL 3 SNIPPET ---")
    print(text[idx2:idx2+2500])

