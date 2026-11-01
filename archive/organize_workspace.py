import os
import shutil

os.makedirs('docs', exist_ok=True)
os.makedirs('docs/screenshots', exist_ok=True)
os.makedirs('tools', exist_ok=True)
os.makedirs('archive', exist_ok=True)

# 1. Copy all screenshots to docs/screenshots
if os.path.exists('screenshots'):
    for f in os.listdir('screenshots'):
        src = os.path.join('screenshots', f)
        dst = os.path.join('docs/screenshots', f)
        if os.path.isfile(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
print("Screenshots synced to docs/screenshots!")

# 2. Move report and documentation files to docs/
docs_files = [
    'Project_Progress_Report_Final.docx',
    'Project_Progress_Report_Final.html',
    'Project_Progress_Report_Final.md',
    'Project_Proposal_Updated.docx',
    'Project_Proposal_Updated.md',
    'Project_TOR_Final.docx',
    'Project_TOR_Final.html',
    'Project_TOR_Final.md',
    'Test_Results_and_Evaluation.html',
    'Test_Results_and_Evaluation.md',
    'Progress_Timesheet.md',
    'Timesheet_Version2_Task_Based.md',
    'Admin_Scope_Table.md',
    'Advisor_Scope_Table.md',
    'Student_Scope_Table.md',
    'Scope_of_Work.md',
    'Scope_of_Work_Flowchart.md',
    'Development_Tools.md',
    'Expected_Benefits.md',
    'References.md',
    'Timeline.md'
]

for filename in docs_files:
    if os.path.exists(filename):
        dst = os.path.join('docs', filename)
        shutil.move(filename, dst)
        print(f"Moved {filename} -> docs/{filename}")

# 3. Categorize scratch scripts into tools/ and archive/
key_tools = [
    'build_clean_report_final.py',
    'build_clean_report.py',
    'build_full_tor.py',
    'build_proposal_clean.py',
    'build_report_html.py',
    'generate_docx_report.py',
    'generate_test_report.py',
    'tor_data.py',
    'tor_helpers.py',
    'test_auth_guard.py'
]

if os.path.exists('scratch'):
    for item in os.listdir('scratch'):
        src_item = os.path.join('scratch', item)
        if item in key_tools:
            shutil.move(src_item, os.path.join('tools', item))
            print(f"Moved tool {item} -> tools/{item}")
        else:
            dst_archive = os.path.join('archive', item)
            if os.path.isdir(src_item):
                if os.path.exists(dst_archive):
                    shutil.rmtree(dst_archive)
                shutil.move(src_item, dst_archive)
            else:
                shutil.move(src_item, dst_archive)

    # If scratch is empty, remove it
    if len(os.listdir('scratch')) == 0:
        os.rmdir('scratch')
        print("Removed empty scratch directory!")

print("\nWorkspace organized successfully!")
