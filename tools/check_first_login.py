for fname in ['index.html', 'dashboard.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        t = f.read()
    print(fname, 'send-first-login count:', t.count('send-first-login'))
