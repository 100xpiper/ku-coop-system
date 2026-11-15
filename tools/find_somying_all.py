import glob

for fname in glob.glob('*.html') + glob.glob('*.js') + glob.glob('js/*.js'):
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    if 'สมหญิง แจ่มใส' in text:
        print(f"Found 'สมหญิง แจ่มใส' in {fname}")
    if 'somying.j@ku.th' in text:
        print(f"Found 'somying.j@ku.th' in {fname}")
