with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length of index.html:", len(text))
print("Has viewport meta:", 'name="viewport"' in text)
print("Has mobile query:", '@media' in text)

