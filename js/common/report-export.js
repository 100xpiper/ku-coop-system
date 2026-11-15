// ==========================================================================
// report-export.js - ระบบส่งออกเอกสาร Excel, PDF และพิมพ์แบบฟอร์มเปล่า
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

function exportToExcel() {
            loadDynamicStudentsData();
            const allStds = getAllSystemStudents();
            const allDocs = getSubmittedDocs();
            const data = [
                ["รหัสนิสิต", "ชื่อ-นามสกุล", "สถานประกอบการ", "สถานะเอกสาร", "สถานะการนิเทศ", "คะแนนประเมิน"]
            ];
            if (allStds.length === 0) {
                data.push(["-", "ไม่มีข้อมูลนิสิตในระบบ (รอแอดมินนำเข้าข้อมูล)", "-", "-", "-", "-"]);
            } else {
                allStds.forEach(s => {
                    const stdDocs = allDocs.filter(d => String(d.studentId) === String(s.id));
                    let rawDoc = s.docs || 'รอตรวจ';
                    if (stdDocs.length > 0) {
                        rawDoc = stdDocs[0].status;
                    }
                    const isDocComplete = (rawDoc === 'ครบถ้วน' || rawDoc === 'ตรวจรับแล้ว' || rawDoc === 'เอกสารครบแล้ว');
                    const docStatusText = isDocComplete ? 'เอกสารครบแล้ว' : 'ไม่ครบ';

                    const rawSup = String(s.status || '').toLowerCase().trim();
                    const isSupDone = (rawSup === 'approved' || rawSup === 'นิเทศแล้ว' || rawSup === 'done' || rawSup === 'completed');
                    const supStatusText = isSupDone ? 'นิเทศแล้ว' : 'รอนิเทศ';

                    data.push([
                        s.id || '-',
                        s.name || '-',
                        s.company || '-',
                        docStatusText,
                        supStatusText,
                        (s.score !== undefined && s.score !== null) ? String(s.score) : '-'
                    ]);
                });
            }
            const ws = XLSX.utils.aoa_to_sheet(data);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "รายงานผลการนิเทศ");
            XLSX.writeFile(wb, "Coop_Supervision_Report.xlsx");
        }

        function exportToPDF() {
            loadDynamicStudentsData();
            const allStds = getAllSystemStudents();
            const allDocs = getSubmittedDocs();
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            doc.text("รายงานสรุปผลการนิเทศสหกิจศึกษา", 14, 15);
            
            const columns = ["รหัสนิสิต", "ชื่อ-นามสกุล", "สถานประกอบการ", "สถานะเอกสาร", "สถานะการนิเทศ", "คะแนนประเมิน"];
            let rows = [];
            if (allStds.length === 0) {
                rows.push(["-", "ไม่มีข้อมูลนิสิตในระบบ", "-", "-", "-", "-"]);
            } else {
                rows = allStds.map(s => {
                    const stdDocs = allDocs.filter(d => String(d.studentId) === String(s.id));
                    let rawDoc = s.docs || 'รอตรวจ';
                    if (stdDocs.length > 0) {
                        rawDoc = stdDocs[0].status;
                    }
                    const isDocComplete = (rawDoc === 'ครบถ้วน' || rawDoc === 'ตรวจรับแล้ว' || rawDoc === 'เอกสารครบแล้ว');
                    const docStatusText = isDocComplete ? 'เอกสารครบแล้ว' : 'ไม่ครบ';

                    const rawSup = String(s.status || '').toLowerCase().trim();
                    const isSupDone = (rawSup === 'approved' || rawSup === 'นิเทศแล้ว' || rawSup === 'done' || rawSup === 'completed');
                    const supStatusText = isSupDone ? 'นิเทศแล้ว' : 'รอนิเทศ';

                    return [
                        String(s.id || '-'),
                        String(s.name || '-'),
                        String(s.company || '-'),
                        docStatusText,
                        supStatusText,
                        String((s.score !== undefined && s.score !== null) ? s.score : '-')
                    ];
                });
            }

            doc.autoTable({
                head: [columns],
                body: rows,
                startY: 25
            });
            doc.save("Coop_Supervision_Report.pdf");
        }



        function renderBlankFormsGrid() {
            const grid = document.getElementById('blank-forms-grid');
            if (!grid) return;
            grid.innerHTML = coopBlankForms.map(f => `
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; gap: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.03); transition: all 0.2s ease;">
                    <div>
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                            <span style="font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px; background: ${f.badgeColor}15; color: ${f.badgeColor}; border: 1px solid ${f.badgeColor}30;">
                                ${f.code || f.badge}
                            </span>
                            <span style="font-size: 10px; color: #64748b; font-weight: 600;">
                                ${f.pages}
                            </span>
                        </div>
                        <div style="font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 4px; line-height: 1.4;">
                            ${f.title}
                        </div>
                        <div style="font-size: 11px; color: #64748b; margin-bottom: 4px; line-height: 1.4;">
                            ${f.subtitle}
                        </div>
                        <div style="font-size: 10.5px; color: #0f766e; font-weight: 600;">
                            ${f.target}
                        </div>
                    </div>

                    <div style="display: flex; gap: 6px; padding-top: 8px; border-top: 1px dashed #e2e8f0;">
                        <button type="button" class="btn-primary" style="flex: 1; padding: 8px 10px; font-size: 11px; font-weight: 700; background-color: #059669; display: flex; align-items: center; justify-content: center; gap: 5px;" onclick="printBlankForm('${f.id}')">
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
                            พิมพ์ / PDF
                        </button>
                        <button type="button" style="padding: 8px 10px; font-size: 11px; font-weight: 600; background: #f8fafc; color: #334155; border: 1px solid #cbd5e1; border-radius: 6px; cursor: pointer; display: flex; align-items: center; gap: 4px;" onclick="previewBlankForm('${f.id}')">
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                            ตัวอย่าง
                        </button>
                    </div>
                </div>
            `).join('');
        }

        function previewBlankForm(formId) {
            const form = coopBlankForms.find(f => f.id === formId);
            if (!form) return;
            currentPreviewBlankFormId = formId;
            const titleEl = document.getElementById('modal-blank-form-title');
            const subEl = document.getElementById('modal-blank-form-subtitle');
            const sheetEl = document.getElementById('modal-blank-form-sheet');
            if (titleEl) titleEl.textContent = (form.code ? form.code + ': ' : '') + form.title;
            if (subEl) subEl.textContent = form.subtitle + ' (' + form.pages + ')';
            if (sheetEl) sheetEl.innerHTML = form.renderHtml();
            openModal('modal-blank-form-preview');
        }

        function printCurrentBlankForm() {
            if (currentPreviewBlankFormId) {
                printBlankForm(currentPreviewBlankFormId);
            }
        }

        function downloadCurrentBlankFormDoc() {
            if (currentPreviewBlankFormId) {
                downloadBlankFormDoc(currentPreviewBlankFormId);
            }
        }

        function printBlankForm(formId) {
            const form = coopBlankForms.find(f => f.id === formId);
            if (!form) return;
            const printWin = window.open('', '_blank', 'width=900,height=900');
            if (!printWin) {
                alert('กรุณาอนุญาตให้เปิดหน้าต่างป๊อปอัปเพื่อสั่งพิมพ์หรือบันทึก PDF');
                return;
            }
            const formContent = form.renderHtml();
            printWin.document.open();
            printWin.document.write(`
                <!DOCTYPE html>
                <html lang="th">
                <head>
                    <meta charset="UTF-8">
                    <title>${form.code ? form.code + ' - ' : ''}${form.title}</title>
                    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap" rel="stylesheet">
                    <style>
                        @page {
                            size: A4 portrait;
                            margin: 15mm 18mm 15mm 18mm;
                        }
                        * {
                            box-sizing: border-box;
                            -webkit-print-color-adjust: exact !important;
                            print-color-adjust: exact !important;
                        }
                        body {
                            font-family: 'Sarabun', 'TH Sarabun New', sans-serif;
                            font-size: 13.5pt;
                            line-height: 1.5;
                            color: #000;
                            margin: 0;
                            padding: 0;
                            background: #fff;
                        }
                        .page {
                            position: relative;
                            width: 100%;
                            min-height: 250mm;
                        }
                        .page-break {
                            page-break-before: always;
                            break-before: page;
                        }
                        table {
                            width: 100%;
                            border-collapse: collapse;
                            margin: 10px 0;
                        }
                        th, td {
                            border: 1px solid #000;
                            padding: 6px 8px;
                            font-size: 13pt;
                        }
                        th {
                            background-color: #f2f2f2 !important;
                            font-weight: bold;
                            text-align: center;
                        }
                        @media screen {
                            body {
                                background: #e2e8f0;
                                padding: 20px;
                            }
                            .page {
                                background: #fff;
                                max-width: 210mm;
                                margin: 0 auto 20px auto;
                                padding: 18mm 20mm;
                                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                            }
                        }
                    </style>
                </head>
                <body>
                    ${formContent}
                    <script>
                        window.onload = function() {
                            setTimeout(function() {
                                window.focus();
                                window.print();
                            }, 350);
                        };
                    <\/script>
                </body>
                </html>
            `);
            printWin.document.close();
        }

        function downloadBlankFormDoc(formId) {
            const form = coopBlankForms.find(f => f.id === formId);
            if (!form) return;
            const content = `
                <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
                <head>
                    <meta charset="utf-8">
                    <title>${form.title}</title>
                    <style>
                        body { font-family: 'TH Sarabun New', 'Cordia New', sans-serif; font-size: 14pt; line-height: 1.5; color: #000; }
                        table { width: 100%; border-collapse: collapse; margin: 12px 0; }
                        th, td { border: 1px solid #000; padding: 6px; font-size: 13pt; }
                        th { background-color: #f2f2f2; text-align: center; }
                    </style>
                </head>
                <body>
                    ${form.renderHtml()}
                </body>
                </html>
            `;
            const blob = new Blob(['\ufeff' + content], { type: 'application/msword' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${form.code ? form.code.replace(/\s+/g, '_') + '_' : ''}${form.title.replace(/\s+/g, '_')}.doc`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
