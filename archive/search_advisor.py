import glob

keywords = ['สมชาย', 'อาจารย์ที่ปรึกษา']
for path in glob.glob('docs/**/*.*', recursive=True) + glob.glob('tools/**/*.*', recursive=True):
    if not path.endswith(('.md', '.py', '.html', '.txt')):
        continue
    try:
        with open(path, 'r', encoding='utf-8') as fp:
            c = fp.read()
            found = [k for k in keywords if k in c]
            if found:
                counts = {k: c.count(k) for k in found}
                print(f'{path}: {counts}')
    except Exception as e:
        pass
