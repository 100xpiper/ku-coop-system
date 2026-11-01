with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function processCheckinAndEval')
lines = text[idx:idx+4500].splitlines()
with open('scratch/checkin_gps_part2.txt', 'w', encoding='utf-8') as out:
    for i, l in enumerate(lines[65:120]):
        out.write(f"{i+66}: {l}\n")

