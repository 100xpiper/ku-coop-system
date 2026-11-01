# -*- coding: utf-8 -*-
with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. In HTML: Remove statusTag from the header of admin-student-preview-container
old_header_tag = '<span id="admin-student-preview-status-tag" class="badge" style="background: #fef3c7; color: #b45309; font-size: 11px; padding: 3px 10px; border-radius: 12px; font-weight: 700;">ก่อนนำเข้า (รอการยืนยัน)</span>'
new_header_tag = ''

if old_header_tag in content:
    content = content.replace(old_header_tag, new_header_tag)
    print("Removed statusTag from HTML preview header.")
else:
    print("WARNING: old_header_tag not found directly.")

# 2. In HTML table thead: Remove the <th> for สถานะ
old_th_status = '<th style="padding: 10px 12px; text-align: center; width: 120px;">สถานะ</th>'
new_th_status = ''

if old_th_status in content:
    content = content.replace(old_th_status, new_th_status)
    print("Removed <th>สถานะ</th> from HTML table header.")
else:
    print("WARNING: old_th_status not found directly.")

# 3. In JS: Update renderAdminStudentPreImportPreview
# Replace the post-import row rendering td for status
old_post_row = '''                        tr.innerHTML = `
                            <td style="padding: 10px 12px; text-align: center; color: #64748b; font-weight: 600;">${idx + 1}</td>
                            <td style="padding: 10px 12px; font-weight: 700; color: #0f172a;">${item.student_id || item.id || '-'}</td>
                            <td style="padding: 10px 12px; font-weight: 600; color: #1e293b;">
                                <div>${item.name || '-'}</div>
                                <div style="font-size: 10.5px; color: #64748b;">${item.email || ''}</div>
                            </td>
                            <td style="padding: 10px 12px; text-align: center;">
                                <span style="background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">
                                    ${item.section || 'หมู่ 700'}
                                </span>
                            </td>
                            <td style="padding: 10px 12px; color: #334155; font-size: 11.5px;">${item.advisor || '-'}</td>
                            <td style="padding: 10px 12px; color: #1e293b; font-size: 11.5px; font-weight: 500;">${item.company || item.company_name || '-'}</td>
                            <td style="padding: 10px 12px; text-align: center;">${coordsBadge}</td>
                            <td style="padding: 10px 12px; text-align: center;">
                                <span style="background: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 12px; font-weight: 700; font-size: 11px; display: inline-flex; align-items: center; gap: 4px;">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                                    พร้อมใช้งาน
                                </span>
                            </td>
                        `;'''

new_post_row = '''                        tr.innerHTML = `
                            <td style="padding: 10px 12px; text-align: center; color: #64748b; font-weight: 600;">${idx + 1}</td>
                            <td style="padding: 10px 12px; font-weight: 700; color: #0f172a;">${item.student_id || item.id || '-'}</td>
                            <td style="padding: 10px 12px; font-weight: 600; color: #1e293b;">
                                <div>${item.name || '-'}</div>
                                <div style="font-size: 10.5px; color: #64748b;">${item.email || ''}</div>
                            </td>
                            <td style="padding: 10px 12px; text-align: center;">
                                <span style="background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">
                                    ${item.section || 'หมู่ 700'}
                                </span>
                            </td>
                            <td style="padding: 10px 12px; color: #334155; font-size: 11.5px;">${item.advisor || '-'}</td>
                            <td style="padding: 10px 12px; color: #1e293b; font-size: 11.5px; font-weight: 500;">${item.company || item.company_name || '-'}</td>
                            <td style="padding: 10px 12px; text-align: center;">${coordsBadge}</td>
                        `;'''

if old_post_row in content:
    content = content.replace(old_post_row, new_post_row)
    print("Removed status column from post-import table rows.")
else:
    print("WARNING: old_post_row not found directly.")

# Replace the pre-import row rendering td for status
old_pre_row = '''                        tr.innerHTML = `
                            <td style="padding: 10px 12px; text-align: center; color: #64748b; font-weight: 600;">${idx + 1}</td>
                            <td style="padding: 10px 12px; font-weight: 700; color: #0f172a;">${studentId}</td>
                            <td style="padding: 10px 12px; font-weight: 600; color: #1e293b;">
                                <div>${fullName}</div>
                                <div style="font-size: 10.5px; color: #64748b;">${emailVal}</div>
                            </td>
                            <td style="padding: 10px 12px; text-align: center;">
                                <span style="background: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">
                                    ${sec}
                                </span>
                            </td>
                            <td style="padding: 10px 12px; color: #334155; font-size: 11.5px;">${advisorVal}</td>
                            <td style="padding: 10px 12px; color: #1e293b; font-size: 11.5px; font-weight: 500;">${company}</td>
                            <td style="padding: 10px 12px; text-align: center;">${coordsBadge}</td>
                            <td style="padding: 10px 12px; text-align: center;">
                                <span style="background: #fef3c7; color: #b45309; padding: 3px 8px; border-radius: 12px; font-weight: 700; font-size: 11px;">
                                    รอการยืนยัน
                                </span>
                            </td>
                        `;'''

new_pre_row = '''                        tr.innerHTML = `
                            <td style="padding: 10px 12px; text-align: center; color: #64748b; font-weight: 600;">${idx + 1}</td>
                            <td style="padding: 10px 12px; font-weight: 700; color: #0f172a;">${studentId}</td>
                            <td style="padding: 10px 12px; font-weight: 600; color: #1e293b;">
                                <div>${fullName}</div>
                                <div style="font-size: 10.5px; color: #64748b;">${emailVal}</div>
                            </td>
                            <td style="padding: 10px 12px; text-align: center;">
                                <span style="background: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 11px;">
                                    ${sec}
                                </span>
                            </td>
                            <td style="padding: 10px 12px; color: #334155; font-size: 11.5px;">${advisorVal}</td>
                            <td style="padding: 10px 12px; color: #1e293b; font-size: 11.5px; font-weight: 500;">${company}</td>
                            <td style="padding: 10px 12px; text-align: center;">${coordsBadge}</td>
                        `;'''

if old_pre_row in content:
    content = content.replace(old_pre_row, new_pre_row)
    print("Removed status column from pre-import table rows.")
else:
    print("WARNING: old_pre_row not found directly.")

# Also in JS, if statusTag is null or present, make sure it doesn't try to show "รอการยืนยัน"
old_pre_status_js = """                if (statusTag) {
                    statusTag.textContent = 'ก่อนนำเข้า (รอการยืนยัน)';
                    statusTag.style.background = '#fef3c7';
                    statusTag.style.color = '#b45309';
                }"""
new_pre_status_js = """                if (statusTag) {
                    statusTag.style.display = 'none';
                }"""

if old_pre_status_js in content:
    content = content.replace(old_pre_status_js, new_pre_status_js)
    print("Removed status text update in JS for pre-import.")

# Also in title text before import, simplify to:
# 'พรีวิวข้อมูลในไฟล์ Excel:' (instead of 'พรีวิวข้อมูลในไฟล์ Excel ก่อนยืนยันนำเข้า:')
content = content.replace(
    "พรีวิวข้อมูลในไฟล์ Excel ก่อนยืนยันนำเข้า:",
    "พรีวิวข้อมูลในไฟล์ Excel:"
)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved dashboard.html successfully.")

