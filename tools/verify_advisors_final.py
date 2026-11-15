with open('supabase-client.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect defaultAccounts in supabase-client.js
pos = text.find('defaultAccounts = {')
print(text[pos:pos+2500])
