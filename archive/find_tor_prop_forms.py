with open('docs/Project_TOR_Final.md', 'r', encoding='utf-8') as f:
    tor = f.read()

with open('docs/Project_Proposal_Updated.md', 'r', encoding='utf-8') as f:
    prop = f.read()

with open('tools/tor_prop_forms.txt', 'w', encoding='utf-8') as out:
    out.write("=== TOR FORM MENTIONS ===\n")
    for l in tor.split('\n'):
        if 'Form' in l or 'แบบฟอร์ม' in l:
            out.write(l + '\n\n')
    out.write("\n=== PROPOSAL FORM MENTIONS ===\n")
    for l in prop.split('\n'):
        if 'Form' in l or 'แบบฟอร์ม' in l:
            out.write(l + '\n\n')

print("TOR and Proposal form mentions dumped!")
