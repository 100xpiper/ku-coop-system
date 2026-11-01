# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make the hook execute synchronously and scroll the import card into view
old_hook_pre = "setTimeout(() => {\n                    renderAdminStudentPreImportPreview(false);\n                    const previewCard = document.getElementById('admin-student-preview-container');\n                    if (previewCard) previewCard.scrollIntoView();\n                }, 100);"
new_hook_pre = """renderAdminStudentPreImportPreview(false);
                const elImport = document.getElementById('admin-card-import');
                if (elImport) {
                    elImport.scrollIntoView({ behavior: 'instant', block: 'start' });
                    window.scrollTo(0, elImport.offsetTop - 40);
                }"""

old_hook_post = "setTimeout(() => {\n                    renderAdminStudentPreImportPreview(true, samplePostList);\n                    const previewCard = document.getElementById('admin-student-preview-container');\n                    if (previewCard) previewCard.scrollIntoView();\n                }, 100);"
new_hook_post = """renderAdminStudentPreImportPreview(true, samplePostList);
                const elImport = document.getElementById('admin-card-import');
                if (elImport) {
                    elImport.scrollIntoView({ behavior: 'instant', block: 'start' });
                    window.scrollTo(0, elImport.offsetTop - 40);
                }"""

if old_hook_pre in content:
    content = content.replace(old_hook_pre, new_hook_pre)
if old_hook_post in content:
    content = content.replace(old_hook_post, new_hook_post)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated hook to instant scroll.")

