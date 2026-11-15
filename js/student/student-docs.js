// ==========================================================================
// student-docs.js - ระบบส่งงานและจัดการเอกสารฝั่งนิสิต (Student Documents)
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

function getSubmittedDocs() {
            return JSON.parse(localStorage.getItem('submittedDocs') || '[]');
        }

        function saveSubmittedDocs(docs) {
            localStorage.setItem('submittedDocs', JSON.stringify(docs));
        }

        function renderStudentDocsList() {
            const savedSession = (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'));
            if (!savedSession) return;
            const user = JSON.parse(savedSession);
            const stdId = String(user.id || user.student_id || '');

            const allDocs = getSubmittedDocs();
            const myDocs = allDocs.filter(d =>
                (String(d.studentId) === stdId || (user.email && d.email === user.email)) &&
                !String(d.docType || '').includes('Contribution Distribution')
            );

            const container = document.getElementById('std-doc-list-container');
            if (!container) return;

            if (myDocs.length === 0) {
                container.innerHTML = `
                    <div style="font-size: 11px; color: var(--text-muted); text-align: center; padding: 16px; background: #f8fafc; border-radius: 8px;">
                        ยังไม่มีประวัติการส่งเอกสารในระบบ
                    </div>`;
                return;
            }

            let html = '';
            myDocs.forEach(d => {
                const badgeClass = d.status === 'ตรวจรับแล้ว' || d.status === 'ครบถ้วน' ? 'badge-success' : (d.status === 'ต้องแก้ไข' ? 'badge-danger' : 'badge-warning');
                html += `
                    <div class="student-item" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <div>
                            <div style="font-weight: 700;">${d.docType}</div>
                            <div style="color: var(--text-muted); font-size: 10px;">ไฟล์: ${d.fileName} | อัปโหลด: ${d.uploadDate || '-'}</div>
                            ${d.comment ? `<div style="font-size: 10.5px; color: #dc2626; font-weight: 600; margin-top: 2px;">หมายเหตุจากอาจารย์: ${d.comment}</div>` : ''}
                        </div>
                        <span class="status-badge ${badgeClass}">${d.status}</span>
                    </div>`;
            });
            container.innerHTML = html;
        }



        function onAsgFileSelected(asgId) {
            const fileInput = document.getElementById(`asg-file-${asgId}`);
            const nameDisplay = document.getElementById(`asg-filename-display-${asgId}`);
            const submitBtn = document.getElementById(`asg-submit-btn-${asgId}`);
            if (fileInput && fileInput.files && fileInput.files.length > 0) {
                const file = fileInput.files[0];
                const sizeMb = (file.size / (1024 * 1024)).toFixed(2);
                if (nameDisplay) {
                    nameDisplay.textContent = `${file.name} (${sizeMb} MB)`;
                    nameDisplay.style.color = '#0f766e';
                    nameDisplay.style.fontWeight = '600';
                    nameDisplay.style.fontStyle = 'normal';
                }
                if (submitBtn) {
                    submitBtn.style.background = '#0f766e';
                    submitBtn.style.pointerEvents = 'auto';
                    submitBtn.style.cursor = 'pointer';
                    submitBtn.style.opacity = '1';
                    submitBtn.style.boxShadow = '0 2px 6px rgba(15, 118, 110, 0.3)';
                }
            }
        }

        function toggleAsgReupload(asgId) {
            const box = document.getElementById(`asg-reupload-box-${asgId}`);
            if (box) {
                const isHidden = (box.style.display === 'none' || !box.style.display);
                box.style.display = isHidden ? 'block' : 'none';
            }
        }

        async function submitAssignmentFileDirect(asgId, encodedDocType) {
            const docType = decodeURIComponent(encodedDocType);
            const fileInput = document.getElementById(`asg-file-${asgId}`);
            if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
                alert('กรุณาเลือกไฟล์เอกสารก่อนกดส่งงาน');
                return;
            }
            const file = fileInput.files[0];
            const submitBtn = document.getElementById(`asg-submit-btn-${asgId}`);
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = `<span>กำลังส่งงาน...</span>`;
            }

            const reader = new FileReader();
            reader.onload = async function(e) {
                try {
                    const fileDataUrl = e.target.result;
                    const savedSession = (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'));
                    const user = savedSession ? JSON.parse(savedSession) : {};
                    const stdId = String(user.id || user.student_id || '6521655442');
                    const stdName = user.name || 'นิสิต';
                    const fileName = file.name;
                    const nowStr = new Date().toLocaleDateString('th-TH') + ' ' + new Date().toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' }) + ' น.';

                    const allDocs = getSubmittedDocs();
                    // Replace existing doc for this assignment if exists
                    const filteredDocs = allDocs.filter(d => !(
                        (String(d.studentId) === stdId || (user.email && d.email === user.email)) &&
                        (d.asgId === asgId || d.docType === docType)
                    ));

                    const newDoc = {
                        id: Date.now(),
                        asgId: asgId,
                        studentId: stdId,
                        studentName: stdName,
                        email: user.email || '',
                        docType: docType,
                        fileName: fileName,
                        fileDataUrl: fileDataUrl,
                        uploadDate: nowStr,
                        status: 'รอตรวจ'
                    };

                    filteredDocs.unshift(newDoc);
                    saveSubmittedDocs(filteredDocs);

                    sendNotification('advisor', 'all', `นิสิต ${stdName} (รหัส ${stdId}) ส่งงาน: ${docType}`);
                    await dbUploadDocument(stdId, docType, fileName, fileDataUrl);

                    renderStudentDocsList();
                    renderStudentClassroomAssignments();

                    const stdDocStatusEl = document.getElementById('std-doc-status');
                    if (stdDocStatusEl) stdDocStatusEl.textContent = 'รอตรวจ';

                    addNotification(`ส่งงาน "${docType}" เรียบร้อยแล้ว (ส่งให้อาจารย์ตรวจ)`);
                    alert(`ส่งงาน "${docType}" เรียบร้อยแล้ว! ข้อมูลและไฟล์ถูกส่งให้อาจารย์ผู้สอนตรวจรับแล้ว`);
                } catch (err) {
                    console.error("Error submitting assignment:", err);
                    alert("เกิดข้อผิดพลาดในการส่งงาน: " + err.message);
                } finally {
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = `<span>ส่งงานให้อาจารย์</span>`;
                    }
                }
            };
            reader.readAsDataURL(file);
        }

        function renderStudentClassroomAssignments() {
            const container = document.getElementById('std-classroom-assignments-grid');
            if (!container) return;
            container.innerHTML = '';

            const savedSession = (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'));
            if (!savedSession) return;
            const user = JSON.parse(savedSession);
            const stdId = String(user.id || user.student_id || '');
            const stdSec = String(user.section || 'หมู่ 700');

            const allAsgs = getCoopAssignments();
            const targetAsgs = allAsgs.filter(a => {
                if (!a.section || a.section === 'all') return true;
                const asgSec = String(a.section).trim();
                const curSec = stdSec.trim();
                return asgSec === curSec || asgSec.includes(curSec) || curSec.includes(asgSec);
            });
            // เรียงลำดับใหม่สุดขึ้นก่อน (createdAt descending)
            targetAsgs.sort((a, b) => new Date(b.createdAt || 0) - new Date(a.createdAt || 0));

            const allDocs = getSubmittedDocs();
            const myDocs = allDocs.filter(d =>
                (String(d.studentId) === stdId || (user.email && d.email === user.email)) &&
                !String(d.docType || '').includes('Contribution Distribution')
            );

            let completedCount = 0;
            const totalCount = targetAsgs.length;

            targetAsgs.forEach(asg => {
                const submitted = myDocs.find(d => (d.asgId && d.asgId === asg.id) || d.docType === asg.docType || d.docType === asg.title);
                if (submitted) completedCount++;
            });

            const percent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;
            const progressBadge = document.getElementById('std-asg-progress-badge');
            if (progressBadge) progressBadge.textContent = `ส่งแล้ว ${completedCount}/${totalCount} รายการ (${percent}%)`;
            const progressBar = document.getElementById('std-asg-progress-bar');
            if (progressBar) progressBar.style.width = `${percent}%`;

            if (targetAsgs.length === 0) {
                container.innerHTML = `
                    <div style="text-align: center; padding: 24px 16px; background: #ffffff; border-radius: 8px; border: 1px dashed #cbd5e1; color: #64748b;">
                        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom: 6px; opacity: 0.6;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                        <div style="font-size: 13px; font-weight: 600; color: #334155;">ยังไม่มีรายการสั่งงานในขณะนี้</div>
                        <div style="font-size: 11px; margin-top: 4px;">เมื่ออาจารย์นิเทศโพสต์สั่งงานหรือมอบหมายแบบฟอร์ม รายการจะปรากฏที่นี่</div>
                    </div>
                `;
                return;
            }

            targetAsgs.forEach(asg => {
                const submitted = myDocs.find(d => (d.asgId && d.asgId === asg.id) || d.docType === asg.docType || d.docType === asg.title);
                let dueFormatted = asg.dueDate || '-';
                let isPastDue = false;
                if (asg.dueDate) {
                    try {
                        const d = new Date(asg.dueDate);
                        dueFormatted = d.toLocaleDateString('th-TH', { day: 'numeric', month: 'short', year: 'numeric' }) + ' เวลา ' + d.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' }) + ' น.';
                        isPastDue = d.getTime() < Date.now();
                    } catch (e) {}
                }

                const card = document.createElement('div');
                card.style.background = '#ffffff';
                card.style.border = submitted ? '1.5px solid #10b981' : (isPastDue ? '1.5px solid #f87171' : '1px solid #cbd5e1');
                card.style.borderRadius = '10px';
                card.style.padding = '14px 16px';
                card.style.boxShadow = '0 2px 6px rgba(0,0,0,0.03)';
                card.style.transition = 'box-shadow 0.2s ease';

                let statusBadge = '';
                if (submitted) {
                    const st = submitted.status || 'รอตรวจ';
                    if (st === 'ตรวจรับแล้ว' || st === 'ครบถ้วน') {
                        statusBadge = `<span class="status-badge badge-success" style="font-size: 11px; padding: 4px 8px;">ตรวจรับแล้ว</span>`;
                    } else if (st === 'ต้องแก้ไข') {
                        statusBadge = `<span class="status-badge badge-danger" style="font-size: 11px; padding: 4px 8px;">ส่งแล้ว (ต้องแก้ไข)</span>`;
                    } else {
                        statusBadge = `<span class="status-badge badge-warning" style="background-color: #fef3c7; color: #b45309; font-size: 11px; padding: 4px 8px;">ส่งแล้ว (รออาจารย์ตรวจ)</span>`;
                    }
                } else if (isPastDue) {
                    statusBadge = `<span class="status-badge badge-danger" style="font-size: 11px; padding: 4px 8px;">ยังไม่ส่ง (เลยกำหนด)</span>`;
                } else {
                    statusBadge = `<span class="status-badge badge-warning" style="font-size: 11px; padding: 4px 8px;">ยังไม่ส่ง</span>`;
                }

                let uploadActionHtml = '';
                const docTypeParam = encodeURIComponent(asg.docType || asg.title);

                if (submitted) {
                    uploadActionHtml = `
                        <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 10px 12px; margin-top: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <div style="width: 32px; height: 32px; border-radius: 6px; background: #dcfce7; display: flex; align-items: center; justify-content: center; color: #16a34a; flex-shrink: 0;">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
                                    </div>
                                    <div>
                                        <div style="font-size: 12px; font-weight: 700; color: #166534; word-break: break-all;">ไฟล์ที่ส่งแล้ว: ${submitted.fileName}</div>
                                        <div style="font-size: 10.5px; color: #15803d; margin-top: 1px;">ส่งเมื่อ: ${submitted.uploadDate}</div>
                                    </div>
                                </div>
                                <div style="display: flex; align-items: center; gap: 6px;">
                                    <button type="button" class="btn-secondary" style="padding: 5px 10px; font-size: 11px; background: #ffffff; border: 1px solid #86efac; color: #166534; border-radius: 6px;" onclick="downloadDocFile('${submitted.id}')">
                                        ดาวน์โหลดดูไฟล์
                                    </button>
                                    <button type="button" class="btn-primary" style="padding: 5px 12px; font-size: 11px; background-color: #0f766e; border-radius: 6px;" onclick="toggleAsgReupload('${asg.id}')">
                                        แนบส่งไฟล์ใหม่/แก้ไข
                                    </button>
                                </div>
                            </div>
                            ${submitted.feedback ? `
                                <div style="margin-top: 8px; padding: 6px 10px; background: #ffffff; border-radius: 6px; border: 1px dashed #16a34a; font-size: 11px; color: #15803d;">
                                    <strong>ข้อคิดเห็นจากอาจารย์:</strong> ${submitted.feedback}
                                </div>
                            ` : ''}
                        </div>

                        <!-- กล่องส่งไฟล์ใหม่กรณีต้องการแก้ไข (Toggle ได้) -->
                        <div id="asg-reupload-box-${asg.id}" style="display: none; margin-top: 10px; background: #f8fafc; border: 1.5px dashed #0f766e; border-radius: 8px; padding: 12px;">
                            <div style="font-size: 11.5px; font-weight: 700; color: #0f766e; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                                แนบไฟล์เอกสารเพื่อส่งใหม่ / แก้ไขงานนี้
                            </div>
                            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                                <div style="display: flex; align-items: center; gap: 8px; flex: 1; min-width: 220px;">
                                    <label for="asg-file-${asg.id}" class="btn-secondary" style="cursor: pointer; padding: 6px 12px; font-size: 11px; font-weight: 600; display: inline-flex; align-items: center; gap: 5px; margin: 0; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; color: #334155;">
                                        เลือกไฟล์ใหม่...
                                    </label>
                                    <input type="file" id="asg-file-${asg.id}" accept=".pdf,.doc,.docx,.png,.jpg,.jpeg" style="display: none;" onchange="onAsgFileSelected('${asg.id}')">
                                    <span id="asg-filename-display-${asg.id}" style="font-size: 11px; color: #64748b; font-style: italic; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 220px;">ยังไม่ได้เลือกไฟล์</span>
                                </div>
                                <button type="button" id="asg-submit-btn-${asg.id}" class="btn-primary" style="padding: 6px 14px; font-size: 11px; background: #94a3b8; pointer-events: none; border-radius: 6px; font-weight: 600; display: flex; align-items: center; gap: 5px;" onclick="submitAssignmentFileDirect('${asg.id}', '${docTypeParam}')">
                                    อัปโหลดส่งงาน
                                </button>
                            </div>
                        </div>
                    `;
                } else {
                    uploadActionHtml = `
                        <div id="asg-upload-box-${asg.id}" style="margin-top: 10px; background: #f8fafc; border: 1.5px dashed #0f766e; border-radius: 8px; padding: 12px;">
                            <div style="font-size: 11.5px; font-weight: 700; color: #0f766e; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                                เพิ่มไฟล์เอกสารเพื่อส่งให้อาจารย์:
                            </div>
                            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                                <div style="display: flex; align-items: center; gap: 8px; flex: 1; min-width: 220px;">
                                    <label for="asg-file-${asg.id}" class="btn-secondary" style="cursor: pointer; padding: 7px 12px; font-size: 11px; font-weight: 600; display: inline-flex; align-items: center; gap: 5px; margin: 0; background: #ffffff; border: 1px solid #0f766e; border-radius: 6px; color: #0f766e;">
                                        เลือกไฟล์เอกสาร...
                                    </label>
                                    <input type="file" id="asg-file-${asg.id}" accept=".pdf,.doc,.docx,.png,.jpg,.jpeg" style="display: none;" onchange="onAsgFileSelected('${asg.id}')">
                                    <span id="asg-filename-display-${asg.id}" style="font-size: 11px; color: #64748b; font-style: italic; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 240px;">ยังไม่ได้เลือกไฟล์ (PDF, Word, รูปถ่าย)</span>
                                </div>
                                <button type="button" id="asg-submit-btn-${asg.id}" class="btn-primary" style="padding: 7px 16px; font-size: 11.5px; background: #94a3b8; pointer-events: none; border-radius: 6px; font-weight: 600; display: flex; align-items: center; gap: 5px; transition: all 0.2s;" onclick="submitAssignmentFileDirect('${asg.id}', '${docTypeParam}')">
                                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                                    ส่งงานให้อาจารย์
                                </button>
                            </div>
                        </div>
                    `;
                }

                card.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 10px;">
                        <div style="flex: 1;">
                            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: ${submitted ? '#10b981' : '#0f766e'};"></span>
                                <span style="font-weight: 700; color: #0f766e; font-size: 13.5px;">${asg.title}</span>
                                <span style="font-size: 10px; font-weight: 600; padding: 1px 6px; border-radius: 4px; background: ${asg.section && asg.section !== 'all' ? '#ecfdf5' : '#f1f5f9'}; color: ${asg.section && asg.section !== 'all' ? '#047857' : '#475569'}; border: 1px solid ${asg.section && asg.section !== 'all' ? '#a7f3d0' : '#cbd5e1'};">
                                    ${asg.section && asg.section !== 'all' ? asg.section : 'ทุกหมู่เรียน'}
                                </span>
                            </div>
                            <div style="font-size: 11px; color: ${isPastDue && !submitted ? '#dc2626' : '#64748b'}; margin-top: 3px; display: flex; align-items: center; gap: 4px;">
                                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                                <strong>กำหนดส่ง:</strong> ${dueFormatted}
                            </div>
                            ${asg.desc ? `
                                <div style="font-size: 11.5px; color: #334155; background: #f8fafc; border-left: 3px solid #0f766e; padding: 6px 10px; border-radius: 4px; margin-top: 6px; line-height: 1.5;">
                                    <strong>รายละเอียดคำสั่งงาน:</strong> ${asg.desc}
                                </div>
                            ` : ''}
                        </div>
                        <div>
                            ${statusBadge}
                        </div>
                    </div>
                    ${uploadActionHtml}
                `;
                container.appendChild(card);
            });
        }

        function quickStudentUploadAssignment(docType) {
            const selectEl = document.getElementById('std-doc-type-select');
            if (selectEl) {
                let found = false;
                for (let i = 0; i < selectEl.options.length; i++) {
                    if (selectEl.options[i].value === docType) {
                        selectEl.selectedIndex = i;
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    const opt = document.createElement('option');
                    opt.value = docType;
                    opt.textContent = docType;
                    selectEl.appendChild(opt);
                    selectEl.value = docType;
                }
            }
            const fileInput = document.getElementById('std-doc-file-input');
            if (fileInput) {
                fileInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                fileInput.click();
            }
        }



        function downloadDocFile(docId) {
            const allDocs = getSubmittedDocs();
            const doc = allDocs.find(d => String(d.id) === String(docId));
            if (!doc) return;

            if (doc.fileDataUrl) {
                const a = document.createElement('a');
                a.href = doc.fileDataUrl;
                a.download = doc.fileName;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            } else {
                const blob = new Blob([`เอกสารสหกิจศึกษา: ${doc.docType}\nชื่อไฟล์: ${doc.fileName}\nผู้อัปโหลด: ${doc.studentName} (${doc.studentId})`], { type: 'text/plain;charset=utf-8' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = doc.fileName.includes('.') ? doc.fileName : `${doc.fileName}.txt`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }
        }



        async function handleStudentDocUpload() {
            const typeSelect = document.getElementById('std-doc-type-select');
            const fileInput = document.getElementById('std-doc-file-input');

            if (!fileInput.files || fileInput.files.length === 0) {
                alert('โปรดเลือกไฟล์เอกสารก่อนกดอัปโหลด');
                return;
            }

            const file = fileInput.files[0];
            const reader = new FileReader();

            reader.onload = async function(e) {
                const fileDataUrl = e.target.result;
                const savedSession = (sessionStorage.getItem('currentUser') || localStorage.getItem('currentUser'));
                const user = savedSession ? JSON.parse(savedSession) : {};
                const stdId = String(user.id || user.student_id || '6521655442');
                const stdName = user.name || 'นิสิต';

                const docType = typeSelect.value;
                const fileName = file.name;
                const nowStr = new Date().toLocaleDateString('th-TH') + ' ' + new Date().toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' }) + ' น.';

                const allDocs = getSubmittedDocs();
                const newDoc = {
                    id: Date.now(),
                    studentId: stdId,
                    studentName: stdName,
                    email: user.email || '',
                    docType: docType,
                    fileName: fileName,
                    fileDataUrl: fileDataUrl,
                    uploadDate: nowStr,
                    status: 'รอตรวจ'
                };
                allDocs.unshift(newDoc);
                saveSubmittedDocs(allDocs);
                sendNotification('advisor', 'all', `นิสิต ${stdName} (รหัส ${stdId}) ส่งเอกสารใหม่: ${docType}`);

                await dbUploadDocument(stdId, docType, fileName, fileDataUrl);

                renderStudentDocsList();
                renderStudentClassroomAssignments();

                const stdDocStatusEl = document.getElementById('std-doc-status');
                if (stdDocStatusEl) stdDocStatusEl.textContent = 'รอตรวจ';

                addNotification(`อัปโหลดเอกสาร "${docType}" เรียบร้อย ส่งให้อาจารย์ตรวจรับแล้ว`);
                alert(`อัปโหลดเอกสาร "${docType}" เรียบร้อยแล้ว! ส่งถึงอาจารย์ผู้สอนแล้ว`);
                fileInput.value = '';
            };

            reader.readAsDataURL(file);
        }

        let pendingPhotoDataUrl = null;
