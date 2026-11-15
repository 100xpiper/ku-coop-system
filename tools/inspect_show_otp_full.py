with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async function showOtpModal')
end = text.find('function closeOtpModal')
print(text[pos:end])
