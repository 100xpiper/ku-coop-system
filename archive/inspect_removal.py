# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_js = text.find('function renderAdminStudentPreImportPreview')
pos_js_end = text.find('function handleAdvisorExcelSelected')
print("--- JS FUNCTION ---")
print(text[pos_js:pos_js_end])

pos_html = text.find('id="admin-student-preview-container"')
print("--- HTML CONTAINER ---")
print(text[pos_html:pos_html+1200])

