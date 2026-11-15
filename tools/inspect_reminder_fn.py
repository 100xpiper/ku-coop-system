with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async function sendAssignmentReminderEmail')
print(text[pos:pos+1000])
