import json

transcript_path = r'C:\Users\PER\.gemini\antigravity\brain\ddb60d44-47b2-4e84-bca5-28d119fdaf51\.system_generated\logs\transcript.jsonl'
with open('scratch/transcript_context.txt', 'w', encoding='utf-8') as out:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            if (615 <= idx <= 628) or (705 <= idx <= 758):
                data = json.loads(line)
                source = data.get('source', '') or data.get('type', '')
                content = data.get('content', '')
                out.write(f'=== Line {idx} [{source}] ===\n')
                # truncate long content
                lines = content.split('\n')
                if len(lines) > 25:
                    lines = lines[:25] + ['... [truncated] ...']
                out.write('\n'.join(lines) + '\n\n')

print("Context written to scratch/transcript_context.txt")

