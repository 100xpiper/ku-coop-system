"""
convert_docx_to_pdf.py
แปลงไฟล์ DOCX เป็น PDF โดยใช้ Word COM API ผ่าน Python (pywin32)
แปลงทั้ง 2 ฉบับ:
  - เล่มรายงานการพัฒนาระบบ_ฉบับสมบูรณ์.docx -> .pdf
  - เล่มรายงานการพัฒนาระบบ_ตามเล่มตัวอย่าง.docx -> .pdf
"""

import os
import sys
import time

try:
    import win32com.client
except ImportError:
    print("Error: pywin32 is required.")
    sys.exit(1)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")

target_files = [
    "เล่มรายงานการพัฒนาระบบ_ฉบับสมบูรณ์.docx",
    "เล่มรายงานการพัฒนาระบบ_ตามเล่มตัวอย่าง.docx"
]

def convert():
    print(f"Connecting to Microsoft Word COM...")
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0  # wdAlertsNone

    try:
        for fname in target_files:
            docx_path = os.path.join(DOCS_DIR, fname)
            if not os.path.exists(docx_path):
                print(f"File not found: {docx_path}")
                continue
            
            pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
            print(f"Converting: {fname} -> {os.path.basename(pdf_path)}...")
            
            # เปิดเอกสาร (ReadOnly = True)
            doc = word.Documents.Open(docx_path, ReadOnly=True, Visible=False)
            # 17 = wdFormatPDF
            doc.SaveAs2(pdf_path, FileFormat=17)
            doc.Close(SaveChanges=0) # 0 = wdDoNotSaveChanges
            
            size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
            print(f"  Success: {pdf_path} ({size_mb:.2f} MB)")
            
    finally:
        word.Quit()
        print("Microsoft Word closed successfully.")

if __name__ == "__main__":
    convert()

