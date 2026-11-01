# -*- coding: utf-8 -*-
import base64
import os
import re

def img_to_base64(path):
    if path.startswith("file:///"):
        path = path.replace("file:///", "").replace("/", "\\")
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
            return f"data:image/png;base64,{b64}"
    return None

with open("Project_Progress_Report_Final.md", "r", encoding="utf-8") as f:
    md_text = f.read()

# Replace images with base64 embedded tags
def replace_img(match):
    alt = match.group(1)
    url = match.group(2)
    b64 = img_to_base64(url)
    if b64:
        return f'<div style="text-align: center; margin: 20px 0;"><img src="{b64}" alt="{alt}" style="max-width: 100%; height: auto; border: 1.5px solid #cbd5e1; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.08);" /><br/><span style="font-size: 13px; color: #475569; font-weight: 500; margin-top: 6px; display: inline-block;">{alt}</span></div>'
    return match.group(0)

img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

lines = md_text.split('\n')
html_lines = []
in_table = False
table_html = []
in_code = False
code_lines = []

for line in lines:
    line = line.strip()
    
    # Code block
    if line.startswith('```'):
        if not in_code:
            in_code = True
            code_lines = []
            continue
        else:
            in_code = False
            code_content = "\n".join(code_lines)
            html_lines.append(f'<pre style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 14px; font-family: Consolas, monospace; font-size: 13px; overflow-x: auto; margin: 14px 0;"><code>{code_content}</code></pre>')
            continue
            
    if in_code:
        code_lines.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
        continue

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
            html_lines.append('<div style="overflow-x: auto; margin: 16px 0;"><table style="width: 100%; border-collapse: collapse; font-size: 13.5px; border: 1.5px solid #cbd5e1;">')
        
        # Check if delimiter line |---|---|
        if re.match(r'^\|[\s\-:|]+\|$', line):
            continue
            
        cells = [c.strip() for c in line.strip('|').split('|')]
        # If first row in table
        if html_lines[-1].startswith('<div style="overflow-x: auto;'):
            row = '<tr style="background-color: #f1f5f9; font-weight: bold; color: #1e293b;">'
            for c in cells:
                row += f'<th style="border: 1px solid #cbd5e1; padding: 10px 12px; text-align: left;">{c}</th>'
            row += '</tr>'
        else:
            row = '<tr>'
            for c in cells:
                c_fmt = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', c)
                row += f'<td style="border: 1px solid #cbd5e1; padding: 8px 12px; line-height: 1.5;">{c_fmt}</td>'
            row += '</tr>'
        html_lines.append(row)
        continue
    else:
        if in_table:
            html_lines.append('</table></div>\n')
            in_table = False

    if not line:
        html_lines.append('<br/>')
        continue

    # Headings
    if line.startswith('# '):
        html_lines.append(f'<h1 style="color: #15803d; border-bottom: 3px solid #16a34a; padding-bottom: 10px; margin-top: 32px; font-size: 26px; text-align: center;">{line[2:]}</h1>')
    elif line.startswith('## '):
        html_lines.append(f'<h2 style="color: #166534; border-bottom: 2px solid #86efac; padding-bottom: 8px; margin-top: 26px; font-size: 20px;">{line[3:]}</h2>')
    elif line.startswith('### '):
        html_lines.append(f'<h3 style="color: #1e293b; margin-top: 18px; font-size: 16px; font-weight: 700;">{line[4:]}</h3>')
    elif line.startswith('#### '):
        html_lines.append(f'<h4 style="color: #334155; margin-top: 14px; font-size: 14.5px; font-weight: 600;">{line[5:]}</h4>')
    elif line.startswith('---'):
        html_lines.append('<hr style="border: none; border-top: 1.5px solid #e2e8f0; margin: 24px 0;" />')
    elif line.startswith('- ') or line.startswith('* '):
        formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line[2:])
        html_lines.append(f'<li style="margin-left: 24px; margin-bottom: 6px; font-size: 14px; line-height: 1.6;">{formatted}</li>')
    elif re.match(r'^\d+\.\s', line):
        num = line.split('.')[0]
        text_content = line[len(num)+2:]
        formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text_content)
        html_lines.append(f'<div style="margin-left: 20px; margin-bottom: 6px; font-size: 14px; line-height: 1.6;"><strong>{num}.</strong> {formatted}</div>')
    else:
        formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
        formatted = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', formatted)
        html_lines.append(f'<p style="font-size: 14px; line-height: 1.65; color: #1e293b; margin: 8px 0; text-align: justify;">{formatted}</p>')

if in_table:
    html_lines.append('</table></div>\n')

full_html = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>รายงานความก้าวหน้าโครงการฉบับสมบูรณ์ (เล่มจบโปรเจกต์) - มหาวิทยาลัยเกษตรศาสตร์</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap');
    body {{
        font-family: 'Sarabun', 'TH Sarabun New', 'Segoe UI', Tahoma, sans-serif;
        line-height: 1.65;
        color: #1e293b;
        max-width: 960px;
        margin: 0 auto;
        padding: 40px;
        background-color: #f8fafc;
    }}
    .document-page {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 50px 60px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }}
    .tip-box {{
        background: #ecfdf5;
        border: 1.5px solid #86efac;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 30px;
        font-size: 14.5px;
        color: #065f46;
        line-height: 1.6;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 16px 0;
    }}
    th, td {{
        border: 1px solid #cbd5e1;
        padding: 9px 12px;
    }}
    th {{
        background-color: #f1f5f9;
    }}
    img {{
        max-width: 100%;
        height: auto;
    }}
    @media print {{
        body {{
            background: #ffffff;
            padding: 0;
        }}
        .document-page {{
            border: none;
            box-shadow: none;
            padding: 0;
        }}
        .tip-box {{
            display: none;
        }}
    }}
</style>
</head>
<body>

<div class="tip-box">
    <div style="font-size: 16px; font-weight: 700; margin-bottom: 6px;">คำแนะนำสำหรับการนำเข้าสู่ Google Docs พร้อมรูปภาพครบ 100%:</div>
    1. <strong>วิธีคัดลอก (ง่ายและเร็วที่สุด):</strong> กด <code>Ctrl + A</code> (เลือกทั้งหมด) แล้วกด <code>Ctrl + C</code> (คัดลอก) -> เปิดเอกสารใหม่ใน Google Docs แล้วกด <code>Ctrl + V</code> (วาง) - ข้อความ ตาราง และรูปภาพความละเอียดสูงทั้ง 18 รูปจะติดไปด้วยทันที<br/>
    2. <strong>วิธีอัปโหลดไฟล์:</strong> นำไฟล์ <code>Project_Progress_Report_Final.html</code> อัปโหลดขึ้น Google Drive แล้วคลิกขวาเลือก <em>"เปิดด้วย Google เอกสาร" (Open with Google Docs)</em>
</div>

<div class="document-page">
{"".join(html_lines)}
</div>

</body>
</html>
"""

with open("Project_Progress_Report_Final.html", "w", encoding="utf-8") as out:
    out.write(full_html)

print("Created Project_Progress_Report_Final.html successfully!")

