# -*- coding: utf-8 -*-
with open('tools/update_advisor_and_rebuild.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = """doc.save(DOCX_PATH)
print(f"Generated: {DOCX_PATH}")"""

replacement = """try:
    doc.save(DOCX_PATH)
    print(f"Generated: {DOCX_PATH}")
except PermissionError:
    alt_docx = os.path.join(DOCS_DIR, "Project_Progress_Report_Final_Latest.docx")
    doc.save(alt_docx)
    print(f"Notice: {DOCX_PATH} is locked by Microsoft Word.")
    print(f"Saved latest version to: {alt_docx}")"""

if target in text:
    text = text.replace(target, replacement, 1)
    with open('tools/update_advisor_and_rebuild.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Handled PermissionError in builder!")
