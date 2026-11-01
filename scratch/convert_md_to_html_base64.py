# -*- coding: utf-8 -*-
import base64
import os
import re

def img_to_base64(path):
    # resolve path
    if path.startswith("file:///"):
        path = path.replace("file:///", "").replace("/", "\\")
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
            return f"data:image/png;base64,{b64}"
    return None

with open("Test_Results_and_Evaluation.md", "r", encoding="utf-8") as f:
    md_text = f.read()

# Replace images with base64 embedded tags
def replace_img(match):
    alt = match.group(1)
    url = match.group(2)
    b64 = img_to_base64(url)
    if b64:
        return f'<div style="text-align: center; margin: 16px 0;"><img src="{b64}" alt="{alt}" style="max-width: 100%; height: auto; border: 1px solid #cbd5e1; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);" /><br/><span style="font-size: 13px; color: #64748b; font-style: italic;">{alt}</span></div>'
    return match.group(0)

# Pattern for markdown image: ![alt](url)
img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

lines = md_text.split('\n')
html_lines = []
in_table = False
table_html = []

for line in lines:
    line = line.strip()
    
    # Image line
    if img_pattern.match(line):
        if in_table:
            html_lines.append("</table>\n")
            in_table = False
        html_lines.append(img_pattern.sub(replace_img, line))
        continue

    # Table line
    if line.startswith('|') and line.endswith('|'):
        if not in_table:
            in_table = True
            html_lines.append('<table style="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; border: 1px solid #cbd5e1;">')
        
        # Check if delimiter line |---|---|
        if re.match(r'^\|[\s\-:|]+\|$', line):
            continue
            
        cells = [c.strip() for c in line.strip('|').split('|')]
        # If first row in table
        if html_lines[-1].startswith('<table'):
            row = '<tr style="background-color: #f1f5f9; font-weight: bold;">'
            for c in cells:
                row += f'<th style="border: 1px solid #cbd5e1; padding: 10px 12px; text-align: left;">{c}</th>'
            row += '</tr>'
        else:
            row = '<tr>'
            for c in cells:
                # bold formatting in cell
                c_fmt = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', c)
                row += f'<td style="border: 1px solid #cbd5e1; padding: 8px 12px;">{c_fmt}</td>'
            row += '</tr>'
        html_lines.append(row)
        continue
    else:
        if in_table:
            html_lines.append('</table>\n')
            in_table = False

    if not line:
        html_lines.append('<br/>')
        continue

    # Headings
    if line.startswith('# '):
        html_lines.append(f'<h1 style="color: #15803d; border-bottom: 2px solid #16a34a; padding-bottom: 8px; margin-top: 24px; font-size: 24px;">{line[2:]}</h1>')
    elif line.startswith('## '):
        html_lines.append(f'<h2 style="color: #166534; border-bottom: 1px solid #86efac; padding-bottom: 6px; margin-top: 20px; font-size: 20px;">{line[3:]}</h2>')
    elif line.startswith('### '):
        html_lines.append(f'<h3 style="color: #1e293b; margin-top: 16px; font-size: 16px;">{line[4:]}</h3>')
    elif line.startswith('#### '):
        html_lines.append(f'<h4 style="color: #334155; margin-top: 12px; font-size: 14px;">{line[5:]}</h4>')
    elif line.startswith('---'):
        html_lines.append('<hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;" />')
    elif line.startswith('- ') or line.startswith('* '):
        formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line[2:])
        html_lines.append(f'<li style="margin-left: 20px; margin-bottom: 6px; font-size: 14px; line-height: 1.6;">{formatted}</li>')
    elif re.match(r'^\d+\.\s', line):
        num = line.split('.')[0]
        text_content = line[len(num)+2:]
        formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text_content)
        html_lines.append(f'<div style="margin-left: 20px; margin-bottom: 6px; font-size: 14px; line-height: 1.6;"><strong>{num}.</strong> {formatted}</div>')
    else:
        formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
        formatted = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', formatted)
        html_lines.append(f'<p style="font-size: 14px; line-height: 1.6; color: #1e293b; margin: 8px 0;">{formatted}</p>')

if in_table:
    html_lines.append('</table>\n')

full_html = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>รายงานผลการทำงานและผลการทดลองระบบ - KU Science Coop</title>
<style>
    body {{
        font-family: 'Sarabun', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #1e293b;
        max-width: 900px;
        margin: 0 auto;
        padding: 30px;
        background-color: #ffffff;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 16px 0;
    }}
    th, td {{
        border: 1px solid #cbd5e1;
        padding: 8px 12px;
    }}
    th {{
        background-color: #f1f5f9;
    }}
    img {{
        max-width: 100%;
        height: auto;
    }}
    .tip-box {{
        background: #ecfdf5;
        border: 1.5px solid #86efac;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 24px;
        font-size: 14px;
        color: #065f46;
    }}
</style>
</head>
<body>
<div class="tip-box">
    <strong>คำแนะนำสำหรับการนำเข้า Google Docs:</strong><br/>
    1. กด <code>Ctrl + A</code> (เลือกทั้งหมด) แล้วกด <code>Ctrl + C</code> (คัดลอก)<br/>
    2. เปิดเอกสารใหม่ใน Google Docs แล้วกด <code>Ctrl + V</code> (วาง) - รูปภาพและตารางทั้งหมดจะติดไปด้วย 100%<br/>
    หรือนำไฟล์ <code>Test_Results_and_Evaluation.html</code> นี้อัปโหลดขึ้น Google Drive แล้วคลิกขวาเลือก <em>"เปิดด้วย Google เอกสาร" (Open with Google Docs)</em>
</div>

{"".join(html_lines)}

</body>
</html>
"""

with open("Test_Results_and_Evaluation.html", "w", encoding="utf-8") as out:
    out.write(full_html)

print("Created Test_Results_and_Evaluation.html successfully!")

