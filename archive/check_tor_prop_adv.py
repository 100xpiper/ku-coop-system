with open('docs/Project_TOR_Final.md', 'r', encoding='utf-8') as f:
    tor = f.read()

with open('docs/Project_Proposal_Updated.md', 'r', encoding='utf-8') as f:
    prop = f.read()

with open('tools/adv_matches.txt', 'w', encoding='utf-8') as out:
    out.write('TOR matches:\n')
    for l in tor.split('\n'):
        if 'สมชาย' in l or 'อาจารย์ที่ปรึกษา' in l:
            out.write('  ' + l + '\n')
    out.write('\nProposal matches:\n')
    for l in prop.split('\n'):
        if 'สมชาย' in l or 'อาจารย์ที่ปรึกษา' in l:
            out.write('  ' + l + '\n')
