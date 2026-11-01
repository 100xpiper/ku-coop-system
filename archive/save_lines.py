with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx2 = text.find('id="modal-photo-mgmt"')
lines = text[idx2:idx2+6000].splitlines()
with open('scratch/modal3_lines.txt', 'w', encoding='utf-8') as out:
    for i, l in enumerate(lines[:80]):
        out.write(f"{i+1}: {l}\n")

