import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Look for user accounts or login credentials
matches = re.finditer(r'\{[^{}]*?username:\s*[\'"](?P<user>[^\'"]+)[\'"][^{}]*?\}', text)
print("=== LOGIN ACCOUNTS IN DASHBOARD.HTML ===")
for m in matches:
    print(m.group(0))

# Also search for advisor options or names
adv_matches = re.findall(r'<option[^>]*value=[\'"]([^\'"]+)[\'"][^>]*>([^<]+)</option>', text)
print("\n=== SELECT OPTIONS (ADVISORS/SEMESTERS) ===")
for val, label in adv_matches:
    if any(k in label for k in ['อาจารย์', 'ภาค', 'หมู่']):
        print(f"  {val} -> {label}")
