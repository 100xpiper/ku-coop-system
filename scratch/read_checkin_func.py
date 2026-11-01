with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function processCheckinAndEval')
idx_end = text.find('function openEvalModalFromResult()', idx)
print(text[idx:idx_end])

