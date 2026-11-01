with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('company_lat')
while idx != -1:
    print(text[idx-40:idx+60])
    idx = text.find('company_lat', idx+1)

