with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="sec-student-qrcode"')
if idx != -1:
    with open('scratch/student_qrcode_content.txt', 'w', encoding='utf-8') as out:
        out.write(text[idx:idx+2500])
    print("Saved student qrcode content")

