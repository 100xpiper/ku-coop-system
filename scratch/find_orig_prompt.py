# -*- coding: utf-8 -*-
import json

with open(r'C:\Users\PER\.gemini\antigravity\brain\ddb60d44-47b2-4e84-bca5-28d119fdaf51\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('type') == 'USER_INPUT':
            content = obj.get('content', '')
            if '13:36:35' in content:
                with open('scratch/orig_prompt.txt', 'w', encoding='utf-8') as out:
                    out.write(content)
                print("Found original prompt!")
                break

