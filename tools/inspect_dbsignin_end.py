with open('supabase-client.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('defaultAccounts = {')
print(text[pos+2500:pos+4500])
