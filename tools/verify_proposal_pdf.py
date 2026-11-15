import pymupdf

doc = pymupdf.open(r'C:\Users\per30\OneDrive\เดสก์ท็อป\Project ปี5\Project\docs\แบบเสนอโครงงาน_Proposal_ฉบับปรับปรุง_Workflow.pdf')
print('Total pages:', len(doc))
for i in range(len(doc)):
    page = doc[i]
    images = page.get_images()
    text = page.get_text()
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    first_line = lines[0] if lines else 'EMPTY'
    last_line = lines[-1] if lines else 'EMPTY'
    print(f'Page {i+1} ({len(images)} img): First="{first_line[:45]}" | Last="{last_line[:45]}"')

