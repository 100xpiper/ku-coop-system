import os
import pypdf

folder = 'docs/coop_forms'
files = sorted(os.listdir(folder))

with open('tools/forms_extracted_info.txt', 'w', encoding='utf-8') as out:
    for f in files:
        if not f.endswith('.pdf'):
            continue
        path = os.path.join(folder, f)
        out.write(f"==================================================\n")
        out.write(f"FILE: {f}\n")
        out.write(f"==================================================\n")
        try:
            reader = pypdf.PdfReader(path)
            out.write(f"Pages: {len(reader.pages)}\n")
            full_text = ""
            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                full_text += f"\n--- Page {idx+1} ---\n" + text
            
            # Write first 1000 chars of extracted text
            out.write(full_text[:1200] + "\n\n")
        except Exception as e:
            out.write(f"Error reading {f}: {e}\n\n")

print("PDF inspection complete! Output written to tools/forms_extracted_info.txt")
