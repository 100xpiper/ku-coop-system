with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx2 = text.find('id="modal-photo-mgmt"')
with open('scratch/modal3_full.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx2:idx2+2500])

