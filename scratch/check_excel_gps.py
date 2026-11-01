with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("findRowValue(row, ['พิกัด'")
with open('scratch/excel_gps_logic.txt', 'w', encoding='utf-8') as out:
    out.write(text[idx-200:idx+2500])
print("Saved to scratch/excel_gps_logic.txt")

