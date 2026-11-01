import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

# Add saveAuthSession function after let supabaseOtpSent = false;
idx_auth_func = """
        function saveAuthSession(user) {
            try {
                sessionStorage.setItem('currentUser', JSON.stringify(user));
            } catch (e) {}
            try {
                localStorage.removeItem('currentUser');
            } catch (e) {}
        }
"""

if 'function saveAuthSession' not in idx_content:
    target = 'let supabaseOtpSent = false;'
    idx_content = idx_content.replace(target, target + '\n' + idx_auth_func, 1)

# Clean legacy fallback adminku
legacy_clean = """
        // Clean legacy fallback admin session
        try {
            const legacy = localStorage.getItem('currentUser');
            if (legacy) {
                const u = JSON.parse(legacy);
                if (u && (u.id === 'adminku' || u.email === 'admin@ku.th')) {
                    localStorage.removeItem('currentUser');
                }
            }
        } catch (e) {}
"""
if 'Clean legacy fallback admin session' not in idx_content:
    idx_content = idx_content.replace('function saveAuthSession(user) {', legacy_clean + '\n        function saveAuthSession(user) {', 1)

# Replace all 8 occurrences of localStorage.setItem('currentUser', ...) with saveAuthSession(...)
idx_content = idx_content.replace(
    "localStorage.setItem('currentUser', JSON.stringify(user));",
    "saveAuthSession(user);"
)
idx_content = idx_content.replace(
    "localStorage.setItem('currentUser', JSON.stringify(pendingFirstLoginUser));",
    "saveAuthSession(pendingFirstLoginUser);"
)
idx_content = idx_content.replace(
    "localStorage.setItem('currentUser', JSON.stringify(result.user));",
    "saveAuthSession(result.user);"
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx_content)
print("index.html updated successfully!")

# 2. Update dashboard.html
with open('dashboard.html', 'r', encoding='utf-8') as f:
    dash_content = f.read()

# Replace getInitialUser body
# Find from "const savedSession = localStorage.getItem('currentUser');" inside getInitialUser to "return defaultUser;"
pos_initial = dash_content.find("function getInitialUser()")
pos_saved = dash_content.find("const savedSession = localStorage.getItem('currentUser');", pos_initial)
pos_default = dash_content.find("return defaultUser;\n        }", pos_saved)

old_block = dash_content[pos_saved:pos_default + len("return defaultUser;\n        }")]

new_block = """const savedSession = sessionStorage.getItem('currentUser');
            if (savedSession) {
                try {
                    const parsed = JSON.parse(savedSession);
                    if (parsed && parsed.role) {
                        if (parsed.role === 'advisor') {
                            const advId = String(parsed.id || parsed.advisor_id || '');
                            const advEmail = String(parsed.email || '').toLowerCase();
                            const advName = String(parsed.name || '');
                            if (advId.includes('Q2222') || advEmail.includes('somying') || advName.includes('สมหญิง')) {
                                parsed.section = 'หมู่ 701, หมู่ 801';
                            } else if (advId.includes('Q3333') || advEmail.includes('somjit') || advName.includes('สมจิต')) {
                                parsed.section = 'หมู่ 702, หมู่ 802';
                            } else {
                                parsed.section = 'หมู่ 700, หมู่ 800';
                            }
                            try { sessionStorage.setItem('currentUser', JSON.stringify(parsed)); } catch (e) {}
                        }
                        return parsed;
                    }
                } catch (e) {
                    console.error("Session parse error:", e);
                }
            }

            // Authentication Guard: หากไม่มี Session ผู้ใช้ ให้ดีดกลับไปหน้า Login (index.html) ทันที
            window.location.replace('index.html');
            return null;
        }"""

dash_content = dash_content[:pos_saved] + new_block + dash_content[pos_default + len("return defaultUser;\n        }"):]

# Update DOMContentLoaded to abort if user is null
old_dom = """window.addEventListener('DOMContentLoaded', () => {
            const user = getInitialUser();
            if (user) {"""

new_dom = """window.addEventListener('DOMContentLoaded', () => {
            const user = getInitialUser();
            if (!user) {
                // Not authenticated, redirecting to login page
                return;
            }
            if (user) {"""

dash_content = dash_content.replace(old_dom, new_dom, 1)

# Update logout()
old_logout = """function logout() {
            localStorage.removeItem('currentUser');
            window.location.href = 'index.html';
        }"""

new_logout = """function logout() {
            try { sessionStorage.removeItem('currentUser'); } catch (e) {}
            try { localStorage.removeItem('currentUser'); } catch (e) {}
            window.location.replace('index.html');
        }"""

dash_content = dash_content.replace(old_logout, new_logout, 1)

# Replace remaining localStorage.getItem('currentUser') with (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'))
dash_content = dash_content.replace(
    "localStorage.getItem('currentUser')",
    "(sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'))"
)

# And in line where std saves:
old_std_save = """            // Save to currentUser session in localStorage
            localStorage.setItem('currentUser', JSON.stringify(std));"""

new_std_save = """            // Save to currentUser session in sessionStorage & localStorage
            try { sessionStorage.setItem('currentUser', JSON.stringify(std)); } catch (e) {}
            try { localStorage.setItem('currentUser', JSON.stringify(std)); } catch (e) {}"""

dash_content = dash_content.replace(old_std_save, new_std_save, 1)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash_content)
print("dashboard.html updated successfully!")
