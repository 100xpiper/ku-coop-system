import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('somying.ch@ku.th')
if pos == -1:
    pos = text.find('somying')
if pos != -1:
    print(text[pos-200:pos+400])

print("\n--- ALL ADVISOR OBJECTS ---")
matches = re.finditer(r'\{\s*(?:id|username):\s*[\'"](Q\d+|somying|somchai|somjit)[^\}]*\}', text, re.IGNORECASE)
for m in matches:
    print(m.group(0))
