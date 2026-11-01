with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function processCheckinAndEval')
idx_end = text.find('function openEvalModalFromResult()', idx)

with open('scratch/checkin_func_full.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx:idx_end])

print("Saved to scratch/checkin_func_full.txt")

