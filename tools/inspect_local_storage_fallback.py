with open('supabase-client.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('// Local Storage / customUsers Fallback')
print(text[pos:pos+1800])
