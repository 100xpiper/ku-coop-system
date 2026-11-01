# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. In renderAdminStudentPreImportPreview, check both
old_rows_display = """            const rowsToDisplay = isPostImport && Array.isArray(postImportList) 
                ? postImportList 
                : adminParsedStudentRows;"""

new_rows_display = """            const rawRows = (typeof adminParsedStudentRows !== 'undefined' && adminParsedStudentRows && adminParsedStudentRows.length > 0)
                ? adminParsedStudentRows
                : (window.adminParsedStudentRows || []);
            const rowsToDisplay = isPostImport && Array.isArray(postImportList) 
                ? postImportList 
                : rawRows;"""

if old_rows_display in content:
    content = content.replace(old_rows_display, new_rows_display)
    print("Updated rowsToDisplay in renderAdminStudentPreImportPreview.")

# 2. In the hook, assign both adminParsedStudentRows and window.adminParsedStudentRows
content = content.replace("window.adminParsedStudentRows = [", "adminParsedStudentRows = window.adminParsedStudentRows = [")

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved dashboard.html successfully.")

