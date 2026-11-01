with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="sec-student-qrcode"')
with open('scratch/sec_student_qr_inspect.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx-50:idx+2500])
print("Saved to scratch/sec_student_qr_inspect.txt")

