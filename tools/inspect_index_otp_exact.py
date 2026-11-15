with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async function showOtpModal')
start = pos - 300
end = pos + 900
print(text[start:end])
