with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('modal-advisor-add-student')
print("=== MODAL HTML ===")
print(text[pos:pos+2500])

pos2 = text.find('openAdvisorAddStudentModal')
print("\n=== JS FUNCTION ===")
print(text[pos2:pos2+2500])
