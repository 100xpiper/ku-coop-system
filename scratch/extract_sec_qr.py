with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="sec-advisor-qr"')
end = text.find('</section>', start)
end2 = text.find('</div>', end)

with open('scratch/full_sec_advisor_qr.txt', 'w', encoding='utf-8') as out:
    out.write(text[start:end2+10])
print(f"Length of sec-advisor-qr: {end2 - start}")

