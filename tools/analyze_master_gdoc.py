# -*- coding: utf-8 -*-
import docx
import re

doc_path = r'docs/เล่มรายงาน_ต้นฉบับ_GoogleDocs.docx'
doc = docx.Document(doc_path)

print(f"Total paragraphs: {len(doc.paragraphs)}")
print(f"Total tables: {len(doc.tables)}")

# 1. Check title and headers
print("\n--- FIRST 30 PARAGRAPHS ---")
for i, p in enumerate(doc.paragraphs[:30]):
    t = p.text.strip()
    if t:
        print(f"[{i}] {t[:100]}")

# 2. Search for target phrases
targets = [
    "ระบบจัดการการตรวจนิเทศงานสหกิจศึกษา คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์",
    "ระบบจัดการการตรวจนิเทศงานสหกิจศึกษา",
    "KU Science Smart Internship Supervision System",
    "KU Science Smart Internship Supervision Platform",
    "ความพึงพอใจ",
    "System Usability Scale",
    "SUS",
    "4.4"
]

print("\n--- TARGET PHRASE OCCURRENCES ---")
for target in targets:
    matches = []
    for i, p in enumerate(doc.paragraphs):
        if target.lower() in p.text.lower():
            matches.append((i, p.text.strip()[:80]))
    print(f"Target '{target}': {len(matches)} occurrences")
    for idx, txt in matches[:5]:
        print(f"   Line {idx}: {txt}")
    if len(matches) > 5:
        print(f"   ... and {len(matches) - 5} more")

# 3. Find Table of Contents
print("\n--- TABLE OF CONTENTS / HEADINGS ---")
toc_paras = []
in_toc = False
for i, p in enumerate(doc.paragraphs[:150]):
    t = p.text.strip()
    if "สารบัญ" in t:
        in_toc = True
    if in_toc:
        if t:
            print(f"[{i}] {t[:90]}")
        if "บทที่ 1" in t and ("ความสำคัญ" in t or "1.1" in t):
            # Probably reached end of TOC
            pass

