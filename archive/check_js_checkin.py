with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function processCheckinAndEval')
if idx != -1:
    with open('scratch/js_checkin.txt', 'w', encoding='utf-8') as out:
        out.write(text[idx-200:idx+3500])
    print("Found processCheckinAndEval")

