import os
import sys
import subprocess
import win32com.client

# Stop any dangling word process
subprocess.run(["powershell", "-Command", "Stop-Process -Name WINWORD -Force -ErrorAction SilentlyContinue"], capture_output=True)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")

files_to_convert = [
    "เล่มรายงานการพัฒนาระบบ_ตามเล่มตัวอย่าง.docx",
    "เล่มรายงาน_ต้นฉบับ_GoogleDocs_แก้ไขแล้ว.docx"
]

print("Launching Word...")
word = win32com.client.DispatchEx("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

try:
    for fname in files_to_convert:
        docx_path = os.path.join(DOCS_DIR, fname)
        if not os.path.exists(docx_path):
            continue
        pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
        print(f"Converting: {fname} -> {os.path.basename(pdf_path)}")
        doc = word.Documents.Open(docx_path, ReadOnly=True, Visible=False)
        doc.SaveAs2(pdf_path, FileFormat=17) # 17 = wdFormatPDF
        doc.Close(SaveChanges=0)
        size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        print(f"  Done: {fname} -> {size_mb:.2f} MB")
finally:
    word.Quit()
    print("Word COM closed.")

