with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function handlePhotoSelected')
with open('scratch/photo_functions.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx:idx+2500])

