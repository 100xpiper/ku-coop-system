with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

stray = 'id="sec-student-dash" class="page-content">'
fixed = '<!-- STUDENT DASHBOARD -->\n                <div id="sec-student-dash" class="page-content">'

if '<div id="sec-student-dash"' not in text:
    text = text.replace(stray, fixed, 1)
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed stray id tag successfully.")
else:
    print("Already has <div id=\"sec-student-dash\"")

