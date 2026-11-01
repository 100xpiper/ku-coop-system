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

# Replace images with base64 embedded tags (clean, no decoration)
def replace_img(match):
    alt = match.group(1)
    url = match.group(2)
    b64 = img_to_base64(url)
    if b64:
        return f'<div style="text-align: center; margin: 24px 0;"><img src="{b64}" alt="{alt}" style="max-width: 95%; height: auto; border: 1px solid #333;" /><br/><div style="font-size: 14px; color: #000; font-weight: normal; margin-top: 6px;">{alt}</div></div>'
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
            html_lines.append(f'<pre style="background: #fdfdfd; border: 1px solid #000; padding: 10px; font-family: monospace; font-size: 13px; overflow-x: auto; margin: 12px 0;"><code>{code_content}</code></pre>')
            continue
            
    if in_code:
        code_lines.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
        continue

    # Image line
    if img_pattern.match(line):
        if in_table:
            html_lines.append("</table></div>\n")
            in_table = False
        html_lines.append(img_pattern.sub(replace_img, line))
        continue

    # Table line
    if line.startswith('|') and line.endswith('|'):
        if not in_table:
            in_table = True
            html_lines.append('<div style="overflow-x: auto; margin: 16px 0;"><table style="width: 100%; border-collapse: collapse; font-size: 14px; border: 1px solid #000;">')
        
        # Check if delimiter line |---|---|
        if re.match(r'^\|[\s\-:|]+\|$', line):
            continue
            
        cells = [c.strip() for c in line.strip('|').split('|')]
        # If first row in table
        if html_lines[-1].startswith('<div style="overflow-x: auto;'):
            row = '<tr style="background-color: #f5f5f5; font-weight: bold; color: #000;">'
            for c in cells:
                row += f'<th style="border: 1px solid #000; padding: 8px 10px; text-align: left;">{c}</th>'
            row += '</tr>'
        else:
            row = '<tr>'
            for c in cells:
                c_fmt = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', c)
                row += f'<td style="border: 1px solid #000; padding: 6px 10px; color: #000;">{c_fmt}</td>'
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

    # Headings - plain black, standard academic
    if line.startswith('# '):
        html_lines.append(f'<h1 style="color: #000000; text-align: center; margin-top: 30px; margin-bottom: 12px; font-size: 24px; font-weight: bold;">{line[2:]}</h1>')
    elif line.startswith('## '):
        html_lines.append(f'<h2 style="color: #000000; margin-top: 24px; margin-bottom: 8px; font-size: 19px; font-weight: bold;">{line[3:]}</h2>')
    elif line.startswith('### '):
        html_lines.append(f'<h3 style="color: #000000; margin-top: 18px; margin-bottom: 6px; font-size: 16px; font-weight: bold;">{line[4:]}</h3>')
    elif line.startswith('#### '):
        html_lines.append(f'<h4 style="color: #000000; margin-top: 14px; margin-bottom: 4px; font-size: 15px; font-weight: bold;">{line[5:]}</h4>')
    elif line.startswith('---'):
        html_lines.append('<hr style="border: none; border-top: 1px solid #000000; margin: 20px 0;" />')
    elif line.startswith('- ') or line.startswith('* '):
        formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line[2:])
        html_lines.append(f'<li style="margin-left: 24px; margin-bottom: 4px; font-size: 15px; color: #000000; line-height: 1.6;">{formatted}</li>')
    elif re.match(r'^\d+\.\s', line):
        num = line.split('.')[0]
        text_content = line[len(num)+2:]
        formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text_content)
        html_lines.append(f'<div style="margin-left: 20px; margin-bottom: 4px; font-size: 15px; color: #000000; line-height: 1.6;"><strong>{num}.</strong> {formatted}</div>')
    else:
        formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
        formatted = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', formatted)
        html_lines.append(f'<p style="font-size: 15px; line-height: 1.65; color: #000000; margin: 6px 0; text-align: justify;">{formatted}</p>')

if in_table:
    html_lines.append('</table></div>\n')

# Plain, unstyled, standard academic paper layout (no decorations)
clean_html = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>รายงานความก้าวหน้าโครงการฉบับสมบูรณ์ (เล่มจบโปรเจกต์)</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap');
    body {{
        font-family: 'Sarabun', 'TH Sarabun New', Tahoma, sans-serif;
        line-height: 1.6;
        color: #000000;
        background-color: #ffffff;
        max-width: 900px;
        margin: 0 auto;
        padding: 40px 20px;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
    }}
    th, td {{
        border: 1px solid #000000;
        padding: 6px 10px;
        color: #000000;
    }}
    th {{
        background-color: #f5f5f5;
    }}
    img {{
        max-width: 100%;
        height: auto;
    }}
    @media print {{
        body {{
            padding: 0;
            max-width: 100%;
        }}
    }}
</style>
</head>
<body>

{"".join(html_lines)}

</body>
</html>
"""

# Write to report.html (simple URL)
with open("report.html", "w", encoding="utf-8") as out:
    out.write(clean_html)
print("Saved report.html successfully!")

# Also overwrite Project_Progress_Report_Final.html with this clean undecorated version
with open("Project_Progress_Report_Final.html", "w", encoding="utf-8") as out:
    out.write(clean_html)
print("Saved Project_Progress_Report_Final.html (undecorated) successfully!")

