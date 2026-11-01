# -*- coding: utf-8 -*-
with open('docs/Project_TOR_Final.md', 'r', encoding='utf-8') as f:
    tor = f.read()

tor = tor.replace('Form 01 ถึง Form 11', 'แบบฟอร์มเอกสารสหกิจศึกษา (แบบฟอร์ม 00 และ Form 02 ถึง Form 11)')
tor = tor.replace('Form 01 - 11', 'แบบฟอร์มเอกสารสหกิจศึกษา (แบบฟอร์ม 00, Form 02 - 11)')

with open('docs/Project_TOR_Final.md', 'w', encoding='utf-8') as f:
    f.write(tor)

with open('docs/Project_Proposal_Updated.md', 'r', encoding='utf-8') as f:
    prop = f.read()

prop = prop.replace('Form 01 ถึง Form 11', 'แบบฟอร์มเอกสารสหกิจศึกษา (แบบฟอร์ม 00 และ Form 02 ถึง Form 11)')
prop = prop.replace('Form 01 - 11', 'แบบฟอร์มเอกสารสหกิจศึกษา (แบบฟอร์ม 00, Form 02 - 11)')

with open('docs/Project_Proposal_Updated.md', 'w', encoding='utf-8') as f:
    f.write(prop)

print("Updated TOR and Proposal with real forms!")
