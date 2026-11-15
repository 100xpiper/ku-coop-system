import docx

doc = docx.Document('docs/เล่มรายงานการพัฒนาระบบ_ตามเล่มตัวอย่าง.docx')

print("=== VERIFY TOC (first 10 and last 5) ===")
for i in range(58, 68):
    print(f"p{i}: {doc.paragraphs[i].text}")
print("...")
for i in range(88, 94):
    print(f"p{i}: {doc.paragraphs[i].text}")

print("\n=== VERIFY FIGURES (first 5 and last 3) ===")
for i in range(95, 100):
    print(f"p{i}: {doc.paragraphs[i].text}")
print("...")
for i in range(135, 139):
    print(f"p{i}: {doc.paragraphs[i].text}")

print("\n=== VERIFY TABLES (all) ===")
for i in range(140, 149):
    print(f"p{i}: {doc.paragraphs[i].text}")

print("\n=== VERIFY CH2 CITATIONS ===")
for i in range(211, 225):
    t = doc.paragraphs[i].text.strip()
    if t.startswith('2.3'):
        print(f"p{i}: {t}")

print("\n=== VERIFY BIBLIOGRAPHY ===")
for i in range(443, 458):
    t = doc.paragraphs[i].text.strip()
    if t:
        print(f"p{i}: {t}")

