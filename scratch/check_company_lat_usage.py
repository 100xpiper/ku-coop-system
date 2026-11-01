with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('if (!std || (!std.company_lat && !std.company_lng))')
if idx != -1:
    print(text[idx-100:idx+1500])
else:
    print("Not found")

