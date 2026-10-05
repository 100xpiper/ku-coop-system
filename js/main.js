// --- Proto 2 Data Reset ---
        if (!localStorage.getItem('proto2_reset')) {
            localStorage.removeItem('systemAppointments');
            localStorage.removeItem('submittedDocs');
            localStorage.setItem('proto2_reset', 'true');
        }

        let selectedStudentExcelFile = null;
        let selectedAdvisorExcelFile = null;

        function handleStudentExcelSelected(event) {
            const file = event.target.files[0];
            if (file) {
                selectedStudentExcelFile = file;
                const label = document.getElementById('excel-student-file-name-label');
                if (label) {
                    label.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> เลือกไฟล์รายชื่อนิสิตแล้ว: ` + file.name;
                    label.parentElement.style.backgroundColor = '#dcfce7';
                    label.parentElement.style.border = '1.5px solid #22c55e';
                }
            }
        }

        function handleAdvisorExcelSelected(event) {
            const file = event.target.files[0];
            if (file) {
                selectedAdvisorExcelFile = file;
                const label = document.getElementById('excel-advisor-file-name-label');
                if (label) {
                    label.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> เลือกไฟล์รายชื่ออาจารย์แล้ว: ` + file.name;
                    label.parentElement.style.backgroundColor = '#dbeafe';
                    label.parentElement.style.border = '1.5px solid #3b82f6';
                }
            }
        }

        function findRowValue(row, possibleKeys) {
            if (!row) return '';
            const rowKeys = Object.keys(row);
            for (const key of possibleKeys) {
                if (row[key] !== undefined && row[key] !== null && row[key] !== '') {
                    return row[key].toString().trim();
                }
                const normKey = key.toLowerCase().replace(/[\s\-_]/g, '');
                const matchedKey = rowKeys.find(k => k.toLowerCase().replace(/[\s\-_]/g, '') === normKey);
                if (matchedKey && row[matchedKey] !== undefined && row[matchedKey] !== null && row[matchedKey] !== '') {
                    return row[matchedKey].toString().trim();
                }
            }
            return '';
        }

        function importStudentExcelFile() {
            if (!selectedStudentExcelFile) {
                alert('กรุณาคลิกเลือกไฟล์ Excel รายชื่อนิสิต (.xlsx) ก่อนกดนำเข้าข้อมูล');
                return;
            }

            const reader = new FileReader();
            reader.onload = async function(e) {
                try {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: 'array' });
                    const firstSheetName = workbook.SheetNames[0];
                    const worksheet = workbook.Sheets[firstSheetName];
                    const jsonRows = XLSX.utils.sheet_to_json(worksheet);

                    if (!jsonRows || jsonRows.length === 0) {
                        alert('ไม่พบข้อมูลรายชื่อในไฟล์ Excel ที่เลือก');
                        return;
                    }

                    let importedCount = 0;
                    const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');

                    for (const row of jsonRows) {
                        const emailRaw = findRowValue(row, ['อีเมลมหาวิทยาลัย', 'อีเมล', 'Email', 'email']);
                        if (!emailRaw) continue;
                        const email = String(emailRaw).toLowerCase();
                        if (!email) continue;

                        const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname']);
                        const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']);
                        const fullName = title ? `${title} ${name}`.trim() : name;
                        const studentId = findRowValue(row, ['รหัสนิสิต', 'รหัสประจำตัว', 'รหัสนักศึกษา', 'รหัส', 'ID', 'Student ID', 'StudentID', 'student_id']);
                        const sectionVal = findRowValue(row, ['หมู่เรียน', 'หมู่เรียนที่รับผิดชอบ', 'หมู่', 'Section', 'section']);
                        const section = sectionVal ? (sectionVal.includes('หมู่') ? sectionVal : `หมู่ ${sectionVal}`) : 'หมู่ 700';
                        const company = findRowValue(row, ['ชื่อสถานประกอบการ', 'สถานประกอบการ', 'Company', 'company']);
                        
                        // อ่านพิกัดแบบรวม (เช่น "14.076, 100.601") แล้วนำมาแยกเป็นละติจูดและลองจิจูด
                        const locationCoord = findRowValue(row, ['พิกัด', 'พิกัด GPS', 'GPS', 'Location', 'พิกัดจีพีเอส']);
                        let lat = null;
                        let lng = null;
                        if (locationCoord && locationCoord.includes(',')) {
                            const parts = locationCoord.split(',');
                            if (parts.length >= 2) {
                                lat = parseFloat(parts[0].trim());
                                lng = parseFloat(parts[1].trim());
                            }
                        }

                        const pass = findRowValue(row, ['รหัสผ่านชั่วคราว', 'รหัสผ่าน', 'Password', 'pass']);

                        const userObj = {
                            id: studentId,
                            student_id: studentId,
                            name: fullName,
                            email: email,
                            password: pass,
                            password_hash: pass,
                            role: 'student',
                            section: section,
                            company_name: company,
                            company_lat: lat || null,
                            company_lng: lng || null,
                            status: 'approved',
                            first_login: true
                        };

                        customUsers[email] = userObj;

                        if (typeof supabaseClient !== 'undefined' && supabaseClient) {
                            try {
                                await supabaseClient.from('users').upsert([{
                                    email: email,
                                    password_hash: pass,
                                    full_name: fullName,
                                    role: 'student',
                                    status: 'approved'
                                }], { onConflict: 'email' });

                                if (studentId) {
                                    const studentData = {
                                        student_id: studentId,
                                        email: email,
                                        full_name: fullName,
                                        section: section,
                                        company_name: company,
                                        doc_status: 'รอตรวจ',
                                        supervision_status: 'รอนิเทศ'
                                    };
                                    // หากในไฟล์ Excel มีค่าละติจูด/ลองจิจูด ให้ใส่เข้าไปใน payload ด้วย
                                    if (lat) studentData.company_lat = lat;
                                    if (lng) studentData.company_lng = lng;

                                    await supabaseClient.from('students').upsert([studentData], { onConflict: 'student_id' });
                                }
                            } catch (err) {
                                console.warn("Supabase upsert notice:", err.message);
                            }
                        }
                        importedCount++;
                    }

                    localStorage.setItem('customUsers', JSON.stringify(customUsers));
                    renderAdminUsersTable();
                    updateAdvisorStats();
                    alert(`นำเข้าข้อมูลนิสิตสหกิจศึกษาเข้าสู่ระบบเรียบร้อยแล้วจำนวน ${importedCount} รายการ!\n\nบัญชีนิสิตพร้อมให้นำอีเมลมหาวิทยาลัยและรหัสผ่านชั่วคราวไปล็อกอินเข้าใช้งานได้ทันที`);
                    const label = document.getElementById('excel-student-file-name-label');
                    if (label) {
                        label.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg> คลิกเพื่อเลือกไฟล์ Excel รายชื่อนิสิต (.xlsx)`;
                    }
                    selectedStudentExcelFile = null;

                } catch (err) {
                    console.error("Student Excel import error:", err);
                    alert('เกิดข้อผิดพลาดในการอ่านไฟล์ Excel รายชื่อนิสิต กรุณาตรวจสอบรูปแบบไฟล์แล้วลองใหม่อีกครั้ง');
                }
            };
            reader.readAsArrayBuffer(selectedStudentExcelFile);
        }

        function importAdvisorExcelFile() {
            if (!selectedAdvisorExcelFile) {
                alert('กรุณาคลิกเลือกไฟล์ Excel รายชื่ออาจารย์ (.xlsx) ก่อนกดนำเข้าข้อมูล');
                return;
            }

            const reader = new FileReader();
            reader.onload = async function(e) {
                try {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: 'array' });
                    const firstSheetName = workbook.SheetNames[0];
                    const worksheet = workbook.Sheets[firstSheetName];
                    const jsonRows = XLSX.utils.sheet_to_json(worksheet);

                    if (!jsonRows || jsonRows.length === 0) {
                        alert('ไม่พบข้อมูลรายชื่อในไฟล์ Excel ที่เลือก');
                        return;
                    }

                    let importedCount = 0;
                    const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');

                    for (const row of jsonRows) {
                        const emailRaw = findRowValue(row, ['อีเมลมหาวิทยาลัย', 'อีเมล', 'Email', 'email']);
                        if (!emailRaw) continue;
                        const email = String(emailRaw).toLowerCase();

                        const name = findRowValue(row, ['ชื่อ - นามสกุล', 'ชื่อ-นามสกุล', 'ชื่อนามสกุล', 'ชื่อ', 'Name', 'fullname']);
                        const title = findRowValue(row, ['คำนำหน้านาม', 'คำนำหน้า', 'Prefix', 'title']);
                        const fullName = title ? `${title} ${name}`.trim() : name;
                        const advisorId = findRowValue(row, ['รหัสประจำตัว', 'รหัสอาจารย์', 'รหัส', 'ID', 'Advisor ID', 'advisor_id']);
                        const section = findRowValue(row, ['หมู่เรียนที่รับผิดชอบ', 'หมู่เรียน', 'หมู่', 'Section', 'section']);
                        const pass = findRowValue(row, ['รหัสผ่านชั่วคราว', 'รหัสผ่าน', 'Password', 'pass']);

                        const userObj = {
                            id: advisorId,
                            advisor_id: advisorId,
                            name: fullName,
                            email: email,
                            password: pass,
                            password_hash: pass,
                            role: 'advisor',
                            section: section || 'หมู่ 700, หมู่ 800',
                            status: 'approved',
                            first_login: true
                        };

                        customUsers[email] = userObj;

                        if (typeof supabaseClient !== 'undefined' && supabaseClient) {
                            try {
                                await supabaseClient.from('users').upsert([{
                                    email: email,
                                    password_hash: pass,
                                    full_name: fullName,
                                    role: 'advisor',
                                    status: 'approved'
                                }], { onConflict: 'email' });

                                if (advisorId) {
                                    await supabaseClient.from('advisors').upsert([{
                                        advisor_id: advisorId,
                                        email: email,
                                        full_name: fullName,
                                        section: section
                                    }], { onConflict: 'advisor_id' });
                                }
                            } catch (err) {
                                console.warn("Supabase upsert notice:", err.message);
                            }
                        }
                        importedCount++;
                    }

                    localStorage.setItem('customUsers', JSON.stringify(customUsers));
                    renderAdminUsersTable();
                    updateAdvisorStats();
                    alert(`นำเข้าข้อมูลอาจารย์นิเทศเข้าสู่ระบบเรียบร้อยแล้วจำนวน ${importedCount} รายการ!\n\nบัญชีอาจารย์พร้อมให้นำอีเมลมหาวิทยาลัยและรหัสผ่านชั่วคราวไปล็อกอินเข้าใช้งานได้ทันที`);
                    const label = document.getElementById('excel-advisor-file-name-label');
                    if (label) {
                        label.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg> คลิกเพื่อเลือกไฟล์ Excel รายชื่ออาจารย์ (.xlsx)`;
                    }
                    selectedAdvisorExcelFile = null;

                } catch (err) {
                    console.error("Advisor Excel import error:", err);
                    alert('เกิดข้อผิดพลาดในการอ่านไฟล์ Excel รายชื่ออาจารย์ กรุณาตรวจสอบรูปแบบไฟล์แล้วลองใหม่อีกครั้ง');
                }
            };
            reader.readAsArrayBuffer(selectedAdvisorExcelFile);
        }

        function downloadStudentExcelTemplate() {
            const studentSample = [
                {
                    "รหัสนิสิต": "6521655442",
                    "คำนำหน้านาม": "นาย",
                    "ชื่อ - นามสกุล": "วงศพัทธ์ อุเทน",
                    "ชั้นปี": "4",
                    "ภาควิชา": "วิทยาการคอมพิวเตอร์",
                    "หลักสูตร": "ภาคพิเศษ",
                    "หมู่เรียน": "800",
                    "อีเมลมหาวิทยาลัย": "wongsapat.u@ku.th",
                    "เบอร์โทรศัพท์": "0948783020",
                    "ชื่อสถานประกอบการ": "สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.)",
                    "รหัสผ่านชั่วคราว": "156748"
                }
            ];
            const wb = XLSX.utils.book_new();
            const wsStudent = XLSX.utils.json_to_sheet(studentSample);
            XLSX.utils.book_append_sheet(wb, wsStudent, "รายชื่อนิสิต");
            XLSX.writeFile(wb, "Student_Import_Template.xlsx");
        }

        function downloadAdvisorExcelTemplate() {
            const advisorSample = [
                {
                    "รหัสประจำตัว": "Q1171",
                    "คำนำหน้านาม": "อาจารย์",
                    "ชื่อ - นามสกุล": "ปรวี วงศ์สวัสดิ์สุริยะ",
                    "หมู่เรียนที่รับผิดชอบ": "700, 800",
                    "อีเมลมหาวิทยาลัย": "poravee.w@ku.th",
                    "เบอร์โทรศัพท์": "034-300481 ถึง 4 ต่อ 7320",
                    "รหัสผ่านชั่วคราว": "564879"
                }
            ];
            const wb = XLSX.utils.book_new();
            const wsAdvisor = XLSX.utils.json_to_sheet(advisorSample);
            XLSX.utils.book_append_sheet(wb, wsAdvisor, "รายชื่ออาจารย์");
            XLSX.writeFile(wb, "Advisor_Import_Template.xlsx");
        }

        function clearImportedUsersByRole(roleTarget) {
            const roleTitle = roleTarget === 'student' ? 'นิสิตสหกิจศึกษา' : 'อาจารย์นิเทศ';
            if (confirm(`คุณต้องการลบ/รีเซ็ตรายชื่อ "${roleTitle}" ทั้งหมดออกจากระบบใช่หรือไม่?\n\n(บัญชีในประเภทอื่นๆ จะไม่ได้รับผลกระทบ)`)) {
                const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                const updatedUsers = {};
                Object.keys(customUsers).forEach(email => {
                    const u = customUsers[email];
                    if (u.role !== roleTarget) {
                        updatedUsers[email] = u;
                    }
                });
                localStorage.setItem('customUsers', JSON.stringify(updatedUsers));
                alert(`ลบ/รีเซ็ตรายชื่อ "${roleTitle}" ทั้งหมดเรียบร้อยแล้ว!`);
                location.reload();
            }
        }

        function clearAllImportedSystemUsers() {
            if (confirm('คุณต้องการลบ/รีเซ็ตรายชื่อผู้ใช้งานทั้งหมด (นิสิตและอาจารย์) ที่เคยอัปโหลดค้างไว้ออกจากระบบใช่หรือไม่?\n\n(บัญชีแอดมินยังคงอยู่ปกติ และจะไม่มีนิสิต/อาจารย์คนใดเข้าใช้ได้จนกว่าจะอัปโหลดไฟล์ Excel ใหม่)')) {
                localStorage.removeItem('customUsers');
                alert('ล้างข้อมูลรายชื่อผู้ใช้งานในระบบเรียบร้อยแล้ว!\n\nปัจจุบันในระบบจะเหลือเฉพาะบัญชีผู้ดูแลระบบ (Admin) เท่านั้น');
                location.reload();
            }
        }

