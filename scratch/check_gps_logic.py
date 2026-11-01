with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function processCheckinAndEval')
with open('scratch/checkin_gps_logic.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx:idx+3500])
print("Saved processCheckinAndEval to scratch/checkin_gps_logic.txt")

