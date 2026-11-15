with open('supabase-client.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'Local Storage / customUsers Fallback' in line:
        for j in range(idx-2, min(len(lines), idx+50)):
            print(f"{j+1}: {lines[j]}", end='')
        break
