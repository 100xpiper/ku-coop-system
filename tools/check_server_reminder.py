with open('server.ps1', 'r', encoding='utf-8') as f:
    text = f.read()

print('server.ps1 reminder count:', text.count('reminder'))
