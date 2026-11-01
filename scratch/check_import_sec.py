with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="admin-card-import"')
start = text.rfind('<section', 0, idx)
end = text.find('</section>', idx)
end2 = text.find('</section>', end+10)

with open('scratch/import_section_full.txt', 'w', encoding='utf-8') as out:
    out.write(text[start:end2+20])
print("Saved to scratch/import_section_full.txt")

