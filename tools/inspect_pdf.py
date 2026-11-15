from pypdf import PdfReader
reader = PdfReader(r"docs\AUCC2026_Paper_OralThai_6521655442.pdf")
print(f"Total pages: {len(reader.pages)}")
for i, page in enumerate(reader.pages):
    print(f"=== PAGE {i+1} ===")
    txt = page.extract_text()
    lines = [l.strip() for l in txt.split("\n") if l.strip()]
    if lines:
        print("  Top:   ", lines[0][:80])
        if len(lines) > 1:
            print("  Bottom:", lines[-1][:80])
    print(f"  Total lines: {len(lines)}")
