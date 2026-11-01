with open('docs/Project_Progress_Report_Final.md', 'r', encoding='utf-8') as f:
    text = f.read()

p = text.find('สมชาย')
print('Chars after สมชาย at', p)
for c in text[p:p+20]:
    print(c, hex(ord(c)))
