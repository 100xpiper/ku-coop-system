# -*- coding: utf-8 -*-
with open('Test_Results_and_Evaluation.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Total lines:", len(lines))
# print sections
for i, line in enumerate(lines):
    if line.startswith('#'):
        print(f"L{i+1}: {line.strip()}")

