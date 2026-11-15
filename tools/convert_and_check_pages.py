import os
import win32com.client

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
try:
    docx_path = os.path.abspath(r"docs\AUCC2026_Paper_OralThai_6521655442.docx")
    pdf_path = os.path.abspath(r"docs\AUCC2026_Paper_OralThai_6521655442.pdf")
    doc = word.Documents.Open(docx_path)
    page_count = doc.ComputeStatistics(2) # 2 = wdStatisticPages
    print(f"PAGE_COUNT: {page_count}")
    doc.SaveAs2(pdf_path, FileFormat=17) # 17 = wdFormatPDF
    doc.Close(False)
    print(f"SUCCESS: Saved PDF to {pdf_path}")
finally:
    word.Quit()
