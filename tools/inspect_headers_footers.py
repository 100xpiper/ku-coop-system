import pymupdf

doc = pymupdf.open('docs/รายงานพัฒนาระบบ_ล่าสุด_user.pdf')
for p in range(len(doc)):
    page = doc[p]
    rect = page.rect
    top_txt = page.get_text('text', clip=pymupdf.Rect(0, 0, rect.width, 60)).strip()
    bot_txt = page.get_text('text', clip=pymupdf.Rect(0, rect.height - 60, rect.width, rect.height)).strip()
    if top_txt or bot_txt:
        print(f"Physical Page {p+1}: Top='{top_txt}' | Bot='{bot_txt}'")

