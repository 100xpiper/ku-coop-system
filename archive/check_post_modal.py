with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function showPostAddPreviewModal')
with open('scratch/post_add_modal.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx:idx+3500])

