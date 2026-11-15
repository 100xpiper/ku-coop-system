# -*- coding: utf-8 -*-
import os
import re

DASHBOARD_FILE = 'dashboard.html'
SUPABASE_FILE = 'supabase-client.js'
ADMIN_EXCEL_FILE = 'js/admin-excel.js'
TEMPLATE_CSV = 'Student_Import_Template.csv'

# ==============================================================================
# 1. NEW CLEAN SEED DATA & ENSURE SEED USERS REPLACEMENT
# ==============================================================================
NEW_SEED_AND_ENSURE_CODE = '''        function getSeedSystemData() {
            return {
                advisors: [
                    {
                        id: 'Q1111',
                        advisor_id: 'Q1111',
                        name: 'อาจารย์ สมชาย แจ่มใส',
                        email: 'somchai.j@ku.th',
                        password: 'Q1111',
                        password_hash: 'Q1111',
                        first_login: false,
                        password_changed: true,
                        role: 'advisor',
                        section: 'หมู่ 700, หมู่ 800',
                        responsible_sections: ['700', '800'],
                        status: 'approved'
                    },
                    {
                        id: 'Q2222',
                        advisor_id: 'Q2222',
                        name: 'อาจารย์ สมหญิง จงจิต',
                        email: 'somying.ch@ku.th',
                        password: 'Asd1234',
                        password_hash: 'Asd1234',
                        first_login: false,
                        password_changed: true,
                        role: 'advisor',
                        section: 'หมู่ 701, หมู่ 801',
                        responsible_sections: ['701', '801'],
                        status: 'approved'
                    },
                    {
                        id: 'Q3333',
                        advisor_id: 'Q3333',
                        name: 'อาจารย์ สมจิต มั่งมี',
                        email: 'somjit.m@ku.th',
                        password: 'Asd1234',
                        password_hash: 'Asd1234',
                        first_login: false,
                        password_changed: true,
                        role: 'advisor',
                        section: 'หมู่ 702, หมู่ 802',
                        responsible_sections: ['702', '802'],
                        status: 'approved'
                    }
                ],
                students: [
                    // ===== อาจารย์ สมชาย แจ่มใส (หมู่ 800 ภาคพิเศษ, หมู่ 700 ภาคปกติ) =====
                    {
                        id: '6521655442',
                        student_id: '6521655442',
                        name: 'นาย วงศพัทธ์ อุเทน',
                        email: 'wongsapat.u@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคพิเศษ',
                        section: 'หมู่ 800 (ภาคพิเศษ)',
                        company_name: 'สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.)',
                        company: 'สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.)',
                        company_lat: '14.076949',
                        company_lng: '100.601563',
                        advisor_name: 'อาจารย์ สมชาย แจ่มใส',
                        advisor: 'อาจารย์ สมชาย แจ่มใส',
                        docs: 'ครบถ้วน',
                        status: 'รอนิเทศ',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    },
                    {
                        id: '6521655189',
                        student_id: '6521655189',
                        name: 'นางสาว ณิชมน เกียรติสกุล',
                        email: 'nichamon.k@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคพิเศษ',
                        section: 'หมู่ 800 (ภาคพิเศษ)',
                        company_name: 'บริษัท ไลน์ คอมพานี (ประเทศไทย) จำกัด (อาคารเกษร ทาวเวอร์)',
                        company: 'บริษัท ไลน์ คอมพานี (ประเทศไทย) จำกัด (อาคารเกษร ทาวเวอร์)',
                        company_lat: '13.744882',
                        company_lng: '100.540835',
                        advisor_name: 'อาจารย์ สมชาย แจ่มใส',
                        advisor: 'อาจารย์ สมชาย แจ่มใส',
                        docs: 'ครบถ้วน',
                        status: 'นิเทศแล้ว',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    },
                    {
                        id: '6521655210',
                        student_id: '6521655210',
                        name: 'นาย วรเมธ รัตนโกสินทร์',
                        email: 'worameth.r@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคพิเศษ',
                        section: 'หมู่ 800 (ภาคพิเศษ)',
                        company_name: 'ธนาคารกสิกรไทย จำกัด (มหาชน) (KBTG แจ้งวัฒนะ)',
                        company: 'ธนาคารกสิกรไทย จำกัด (มหาชน) (KBTG แจ้งวัฒนะ)',
                        company_lat: '13.910638',
                        company_lng: '100.551134',
                        advisor_name: 'อาจารย์ สมชาย แจ่มใส',
                        advisor: 'อาจารย์ สมชาย แจ่มใส',
                        docs: 'รอตรวจ',
                        status: 'รอนิเทศ',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    },
                    {
                        id: '6521650123',
                        student_id: '6521650123',
                        name: 'นาย กิตติศักดิ์ เจริญกิจ',
                        email: 'kittisak.c@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคปกติ',
                        section: 'หมู่ 700 (ภาคปกติ)',
                        company_name: 'บริษัท อโกด้า เซอร์วิสเซส จำกัด (เซ็นทรัลเวิลด์)',
                        company: 'บริษัท อโกด้า เซอร์วิสเซส จำกัด (เซ็นทรัลเวิลด์)',
                        company_lat: '13.746884',
                        company_lng: '100.539265',
                        advisor_name: 'อาจารย์ สมชาย แจ่มใส',
                        advisor: 'อาจารย์ สมชาย แจ่มใส',
                        docs: 'ครบถ้วน',
                        status: 'นิเทศแล้ว',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    },
                    {
                        id: '6521650145',
                        student_id: '6521650145',
                        name: 'นางสาว ชลธิชา พงษ์ศิริ',
                        email: 'chonthicha.p@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคปกติ',
                        section: 'หมู่ 700 (ภาคปกติ)',
                        company_name: 'บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน)',
                        company: 'บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน)',
                        company_lat: '13.761924',
                        company_lng: '100.570142',
                        advisor_name: 'อาจารย์ สมชาย แจ่มใส',
                        advisor: 'อาจารย์ สมชาย แจ่มใส',
                        docs: 'ครบถ้วน',
                        status: 'รอนิเทศ',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    },

                    // ===== อาจารย์ สมหญิง จงจิต (หมู่ 701 ภาคปกติ, หมู่ 801 ภาคพิเศษ) =====
                    {
                        id: '6521650211',
                        student_id: '6521650211',
                        name: 'นางสาว ธนพร วัฒนกุล',
                        email: 'thanaporn.w@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคปกติ',
                        section: 'หมู่ 701 (ภาคปกติ)',
                        company_name: 'ธนาคารไทยพาณิชย์ จำกัด (มหาชน) สำนักงานใหญ่ รัชโยธิน',
                        company: 'ธนาคารไทยพาณิชย์ จำกัด (มหาชน) สำนักงานใหญ่ รัชโยธิน',
                        company_lat: '13.826629',
                        company_lng: '100.565893',
                        advisor_name: 'อาจารย์ สมหญิง จงจิต',
                        advisor: 'อาจารย์ สมหญิง จงจิต',
                        docs: 'ครบถ้วน',
                        status: 'นิเทศแล้ว',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    },
                    {
                        id: '6521650234',
                        student_id: '6521650234',
                        name: 'นาย ปัญญาวุฒิ เกิดผล',
                        email: 'panyawut.k@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคปกติ',
                        section: 'หมู่ 701 (ภาคปกติ)',
                        company_name: 'บริษัท ปตท. สำรวจและผลิตปิโตรเลียม จำกัด (มหาชน)',
                        company: 'บริษัท ปตท. สำรวจและผลิตปิโตรเลียม จำกัด (มหาชน)',
                        company_lat: '13.820251',
                        company_lng: '100.559384',
                        advisor_name: 'อาจารย์ สมหญิง จงจิต',
                        advisor: 'อาจารย์ สมหญิง จงจิต',
                        docs: 'รอตรวจ',
                        status: 'รอนิเทศ',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    },
                    {
                        id: '6521655222',
                        student_id: '6521655222',
                        name: 'นาย กฤติน สิทธิชัย',
                        email: 'krittin.s@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคพิเศษ',
                        section: 'หมู่ 801 (ภาคพิเศษ)',
                        company_name: 'บริษัท เอสซีบี เทคเอกซ์ จำกัด (SCB TechX)',
                        company: 'บริษัท เอสซีบี เทคเอกซ์ จำกัด (SCB TechX)',
                        company_lat: '13.826629',
                        company_lng: '100.565893',
                        advisor_name: 'อาจารย์ สมหญิง จงจิต',
                        advisor: 'อาจารย์ สมหญิง จงจิต',
                        docs: 'ครบถ้วน',
                        status: 'รอนิเทศ',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    },
                    {
                        id: '6521655255',
                        student_id: '6521655255',
                        name: 'นางสาว กัญญาณัฐ วิทยา',
                        email: 'kanyanat.w@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคพิเศษ',
                        section: 'หมู่ 801 (ภาคพิเศษ)',
                        company_name: 'บริษัท สามารถคอร์ปอเรชั่น จำกัด (มหาชน)',
                        company: 'บริษัท สามารถคอร์ปอเรชั่น จำกัด (มหาชน)',
                        company_lat: '13.896742',
                        company_lng: '100.573214',
                        advisor_name: 'อาจารย์ สมหญิง จงจิต',
                        advisor: 'อาจารย์ สมหญิง จงจิต',
                        docs: 'ครบถ้วน',
                        status: 'นิเทศแล้ว',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    },

                    // ===== อาจารย์ สมจิต มั่งมี (หมู่ 702 ภาคปกติ, หมู่ 802 ภาคพิเศษ) =====
                    {
                        id: '6521650312',
                        student_id: '6521650312',
                        name: 'นาย พีรพัฒน์ ศิริชัย',
                        email: 'peerapat.s@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคปกติ',
                        section: 'หมู่ 702 (ภาคปกติ)',
                        company_name: 'บริษัท โทรคมนาคมแห่งชาติ จำกัด (มหาชน) (NT แจ้งวัฒนะ)',
                        company: 'บริษัท โทรคมนาคมแห่งชาติ จำกัด (มหาชน) (NT แจ้งวัฒนะ)',
                        company_lat: '13.884500',
                        company_lng: '100.578600',
                        advisor_name: 'อาจารย์ สมจิต มั่งมี',
                        advisor: 'อาจารย์ สมจิต มั่งมี',
                        docs: 'ครบถ้วน',
                        status: 'นิเทศแล้ว',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    },
                    {
                        id: '6521650345',
                        student_id: '6521650345',
                        name: 'นางสาว ภัทรภรณ์ รุ่งเรือง',
                        email: 'pattaraporn.r@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคปกติ',
                        section: 'หมู่ 702 (ภาคปกติ)',
                        company_name: 'การไฟฟ้าฝ่ายผลิตแห่งประเทศไทย (กฟผ.)',
                        company: 'การไฟฟ้าฝ่ายผลิตแห่งประเทศไทย (กฟผ.)',
                        company_lat: '13.807831',
                        company_lng: '100.499824',
                        advisor_name: 'อาจารย์ สมจิต มั่งมี',
                        advisor: 'อาจารย์ สมจิต มั่งมี',
                        docs: 'รอตรวจ',
                        status: 'รอนิเทศ',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    },
                    {
                        id: '6521655318',
                        student_id: '6521655318',
                        name: 'นาย ธนวัฒน์ สุขสวัสดิ์',
                        email: 'thanawat.s@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคพิเศษ',
                        section: 'หมู่ 802 (ภาคพิเศษ)',
                        company_name: 'สำนักงานพัฒนาธุรกรรมทางอิเล็กทรอนิกส์ (ETDA)',
                        company: 'สำนักงานพัฒนาธุรกรรมทางอิเล็กทรอนิกส์ (ETDA)',
                        company_lat: '13.884120',
                        company_lng: '100.569420',
                        advisor_name: 'อาจารย์ สมจิต มั่งมี',
                        advisor: 'อาจารย์ สมจิต มั่งมี',
                        docs: 'ครบถ้วน',
                        status: 'รอนิเทศ',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    },
                    {
                        id: '6521655342',
                        student_id: '6521655342',
                        name: 'นางสาว ศิริพร รัตนเดช',
                        email: 'siriporn.r@ku.th',
                        role: 'student',
                        year: '4',
                        department: 'วิทยาการคอมพิวเตอร์',
                        curriculum: 'ภาคพิเศษ',
                        section: 'หมู่ 802 (ภาคพิเศษ)',
                        company_name: 'บริษัท เบทาโกร จำกัด (มหาชน)',
                        company: 'บริษัท เบทาโกร จำกัด (มหาชน)',
                        company_lat: '13.883410',
                        company_lng: '100.571230',
                        advisor_name: 'อาจารย์ สมจิต มั่งมี',
                        advisor: 'อาจารย์ สมจิต มั่งมี',
                        docs: 'ครบถ้วน',
                        status: 'นิเทศแล้ว',
                        semester: 'ภาคต้น 2569',
                        initialPassword: 'password',
                        password: 'password',
                        password_hash: '123456',
                        first_login: false,
                        password_changed: true
                    }
                ]
            };
        }

        function ensureSeedUsers() {
            try {
                // ล้างข้อมูลแคชเก่าในเครื่องเมื่อเปิดใช้งานชุดข้อมูลสะอาดใหม่สำหรับวันสอบ
                const CURRENT_DATA_VERSION = 'v20261116_defense_clean';
                if (localStorage.getItem('system_students_version') !== CURRENT_DATA_VERSION) {
                    localStorage.removeItem('customUsers');
                    localStorage.removeItem('deletedStudentIds');
                    localStorage.removeItem('submittedDocs');
                    localStorage.setItem('system_students_version', CURRENT_DATA_VERSION);
                }

                let customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
                const deletedStudentIds = new Set(JSON.parse(localStorage.getItem('deletedStudentIds') || '[]').map(x => String(x).toLowerCase().trim()));
                const seeds = getSeedSystemData();

                // 1. ตั้งค่าบัญชีอาจารย์ทั้ง 3 ท่าน
                seeds.advisors.forEach(a => {
                    const emailKey = a.email.toLowerCase().trim();
                    const idKey = a.id.toLowerCase().trim();
                    customUsers[emailKey] = { ...(customUsers[emailKey] || {}), ...a };
                    customUsers[idKey] = customUsers[emailKey];
                });

                // 2. ตั้งค่าบัญชีนิสิต (เฉพาะที่ไม่เคยถูกสั่งลบ)
                seeds.students.forEach(s => {
                    const stdId = String(s.id || s.student_id || '').toLowerCase().trim();
                    const emailKey = String(s.email || '').toLowerCase().trim();
                    if (deletedStudentIds.has(stdId) || deletedStudentIds.has(emailKey)) {
                        return; // ถูกสั่งลบแล้ว ห้ามฟื้นคืนชีพ!
                    }
                    if (!customUsers[emailKey]) {
                        customUsers[emailKey] = s;
                        customUsers[stdId] = s;
                    } else {
                        // คงข้อมูลเดิมที่อัปเดตไว้ แต่รับค่าสำคัญ
                        customUsers[emailKey] = { ...s, ...customUsers[emailKey] };
                        customUsers[stdId] = customUsers[emailKey];
                    }
                });

                localStorage.setItem('customUsers', JSON.stringify(customUsers));

                // 3. เตรียมเอกสารประกอบการตรวจนิเทศ
                let submittedDocs = JSON.parse(localStorage.getItem('submittedDocs') || '[]');
                const seededDocStudentIds = new Set(submittedDocs.map(d => String(d.studentId)));
                let docsAdded = false;

                seeds.students.forEach(s => {
                    const stdId = String(s.id);
                    if (deletedStudentIds.has(stdId.toLowerCase()) || deletedStudentIds.has(s.email.toLowerCase())) return;

                    if (!seededDocStudentIds.has(stdId)) {
                        submittedDocs.push({
                            id: 'doc-' + stdId + '-1',
                            studentId: stdId,
                            studentName: s.name,
                            email: s.email,
                            docType: 'แบบตอบรับนิสิตเข้าปฏิบัติงานสหกิจศึกษา (คู-01)',
                            fileName: `KU01_Acceptance_${stdId}.pdf`,
                            fileUrl: '',
                            status: 'ตรวจรับแล้ว',
                            uploadDate: '15 ก.ค. 2569'
                        });
                        submittedDocs.push({
                            id: 'doc-' + stdId + '-2',
                            studentId: stdId,
                            studentName: s.name,
                            email: s.email,
                            docType: 'แผนปฏิบัติงานสหกิจศึกษา (คู-02)',
                            fileName: `KU02_WorkPlan_${stdId}.pdf`,
                            fileUrl: '',
                            status: s.status === 'นิเทศแล้ว' ? 'ตรวจรับแล้ว' : 'รอตรวจ',
                            uploadDate: '25 ก.ค. 2569'
                        });
                        submittedDocs.push({
                            id: 'doc-' + stdId + '-3',
                            studentId: stdId,
                            studentName: s.name,
                            email: s.email,
                            docType: 'รายงานสรุปผลการปฏิบัติงานสหกิจศึกษาฉบับสมบูรณ์',
                            fileName: `Final_Report_${stdId}.pdf`,
                            fileUrl: '',
                            status: s.status === 'นิเทศแล้ว' ? 'ตรวจรับแล้ว' : 'รอตรวจ',
                            uploadDate: '10 ต.ค. 2569'
                        });
                        docsAdded = true;
                    }
                });

                if (docsAdded) {
                    localStorage.setItem('submittedDocs', JSON.stringify(submittedDocs));
                }
            } catch (e) {
                console.error("Error in ensureSeedUsers:", e);
            }
        }'''

# ==============================================================================
# 2. ENHANCED confirmDeleteStudent
# ==============================================================================
NEW_CONFIRM_DELETE_CODE = '''        async function confirmDeleteStudent(studentId, studentName) {
            const isConfirm = confirm(`คุณต้องการลบรายชื่อนิสิต "${studentName}" (รหัส ${studentId}) ออกจากระบบหรือไม่?\\n\\nเมื่อลบแล้ว รายชื่อจะถูกนำออกจากระบบอย่างถาวรเสมือนข้อมูลจริง`);
            if (!isConfirm) return;

            const stdIdStr = String(studentId).trim();
            let deletedIds = JSON.parse(localStorage.getItem('deletedStudentIds') || '[]');
            if (!deletedIds.includes(stdIdStr)) deletedIds.push(stdIdStr);

            let customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
            let deletedEmail = null;
            Object.keys(customUsers).forEach(k => {
                const u = customUsers[k];
                if (u && (String(u.id) === stdIdStr || String(u.student_id) === stdIdStr || String(k).trim() === stdIdStr)) {
                    if (u.email) {
                        deletedEmail = u.email.toLowerCase().trim();
                        if (!deletedIds.includes(deletedEmail)) deletedIds.push(deletedEmail);
                    }
                    delete customUsers[k];
                }
            });
            if (deletedEmail && customUsers[deletedEmail]) {
                delete customUsers[deletedEmail];
            }
            localStorage.setItem('deletedStudentIds', JSON.stringify(deletedIds));
            localStorage.setItem('customUsers', JSON.stringify(customUsers));

            // ลบเอกสารที่เกี่ยวข้องกับนิสิตนี้
            let docs = JSON.parse(localStorage.getItem('submittedDocs') || '[]');
            docs = docs.filter(d => String(d.studentId) !== stdIdStr);
            localStorage.setItem('submittedDocs', JSON.stringify(docs));

            // ลบออกจาก studentsData ในหน่วยความจำทันที
            Object.keys(studentsData).forEach(sec => {
                studentsData[sec] = (studentsData[sec] || []).filter(s => String(s.id) !== stdIdStr);
            });

            if (typeof dbDeleteStudent === 'function') {
                try { await dbDeleteStudent(studentId, deletedEmail); } catch(e){}
            }

            loadDynamicStudentsData();
            if (typeof renderAdminUsersTable === 'function') renderAdminUsersTable();
            if (typeof renderStudentList === 'function') renderStudentList();
            if (typeof updateAdvisorStats === 'function') updateAdvisorStats();
            if (typeof populateAdvisorStudentSelects === 'function') populateAdvisorStudentSelects();
            if (typeof renderQrStudentSelectOptions === 'function') renderQrStudentSelectOptions();

            alert(`ลบรายชื่อนิสิต "${studentName}" (รหัส ${studentId}) ออกจากระบบเรียบร้อยแล้ว`);
        }'''

def update_dashboard():
    with open(DASHBOARD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace getSeedSystemData and ensureSeedUsers
    idx1 = content.find('function getSeedSystemData() {')
    idx3 = content.find('async function syncDatabaseUsers()')
    assert idx1 != -1 and idx3 != -1, "Could not find getSeedSystemData / syncDatabaseUsers"

    content = content[:idx1] + NEW_SEED_AND_ENSURE_CODE + '\n\n        ' + content[idx3:]

    # 2. Replace confirmDeleteStudent
    del_start = content.find('async function confirmDeleteStudent(studentId, studentName) {')
    del_end = content.find('function renderAdminTableRowsOnly()')
    assert del_start != -1 and del_end != -1, "Could not find confirmDeleteStudent block"

    content = content[:del_start] + NEW_CONFIRM_DELETE_CODE + '\n\n        ' + content[del_end:]

    # 3. Add Delete Button to Advisor student cards in renderStudentList
    target_adv_card_btn = '''<button class="btn-primary" style="padding: 6px; font-size: 11px; font-weight: 600; grid-column: span 2; background-color: #4f46e5; border-color: #4f46e5; display: flex; align-items: center; justify-content: center; gap: 5px;" onclick="sendFirstLoginInviteToStudent('${std.id}', '${std.name}', '${std.email}', this, '${std.initialPassword || std.password || std.id}')">
                                <span>ส่งอีเมลแจ้งแรกเข้าใช้งาน</span>
                            </button>'''

    replacement_adv_card_btn = '''<button class="btn-primary" style="padding: 6px; font-size: 11px; font-weight: 600; background-color: #4f46e5; border-color: #4f46e5; display: flex; align-items: center; justify-content: center; gap: 5px;" onclick="sendFirstLoginInviteToStudent('${std.id}', '${std.name}', '${std.email}', this, '${std.initialPassword || std.password || std.id}')">
                                <span>ส่งอีเมลแจ้งแรกเข้า</span>
                            </button>
                            <button class="btn-primary" style="padding: 6px; font-size: 11px; font-weight: 600; background-color: #dc2626; border-color: #dc2626; color: #fff; display: flex; align-items: center; justify-content: center; gap: 4px;" onclick="confirmDeleteStudent('${std.id}', '${std.name}')" title="ลบรายชื่อนิสิตนี้ออกจากระบบ">
                                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                                <span>ลบรายชื่อ</span>
                            </button>'''

    if target_adv_card_btn in content:
        content = content.replace(target_adv_card_btn, replacement_adv_card_btn, 1)
        print("Added delete button to advisor student card in renderStudentList")
    else:
        print("Warning: target_adv_card_btn not found directly, checking regex")

    # 4. In saveAdvisorNewStudentConfirmed: un-delete student if added
    target_save_adv = "localStorage.setItem('customUsers', JSON.stringify(customUsers));"
    un_delete_snippet = """localStorage.setItem('customUsers', JSON.stringify(customUsers));
                // หากนิสิตคนนี้เคยถูกลบ ให้ปลดออกจาก deletedStudentIds ทันที
                try {
                    let dIds = JSON.parse(localStorage.getItem('deletedStudentIds') || '[]');
                    dIds = dIds.filter(x => x !== String(stdId).trim() && x !== String(email).trim().toLowerCase());
                    localStorage.setItem('deletedStudentIds', JSON.stringify(dIds));
                } catch(e) {}"""
    if target_save_adv in content:
        content = content.replace(target_save_adv, un_delete_snippet, 1)
        print("Added un-delete logic to saveAdvisorNewStudentConfirmed")

    with open(DASHBOARD_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Dashboard.html updated successfully!")

def update_supabase_client():
    with open(SUPABASE_FILE, 'r', encoding='utf-8') as f:
        text = f.read()

    # Ensure Somchai Jaithanom is updated to Somchai Jaemsai and passwords are clean
    text = text.replace('อาจารย์ สมชาย ใจถนอม', 'อาจารย์ สมชาย แจ่มใส')
    text = text.replace("'first_login': true, 'password_changed': false", "'first_login': false, 'password_changed': true")
    
    # Check if student is in deletedStudentIds
    target_check = "    // Step 1: If email is NOT registered in system"
    replacement_check = """    // ตรวจสอบว่าบัญชีนี้ถูกลบออกจากระบบไปแล้วหรือไม่
    try {
        const deletedIds = JSON.parse(localStorage.getItem('deletedStudentIds') || '[]');
        if (deletedIds.includes(cleanId) || (existingUser && (deletedIds.includes(String(existingUser.id)) || (existingUser.email && deletedIds.includes(String(existingUser.email).toLowerCase()))))) {
            return { success: false, message: 'ไม่พบอีเมลหรือรหัสประจำตัวนี้ในระบบ (รายชื่อนี้ถูกลบออกจากระบบแล้ว)' };
        }
    } catch(e) {}

    // Step 1: If email is NOT registered in system"""

    if target_check in text and 'deletedStudentIds' not in text:
        text = text.replace(target_check, replacement_check, 1)
        print("Added deletedStudentIds check to dbSignIn in supabase-client.js")

    with open(SUPABASE_FILE, 'w', encoding='utf-8') as f:
        f.write(text)
    print("supabase-client.js updated successfully!")

def update_admin_excel():
    with open(ADMIN_EXCEL_FILE, 'r', encoding='utf-8') as f:
        text = f.read()

    # When importing students in admin-excel, un-delete them if previously deleted
    target_import = "customUsers[email] = userObj;"
    replacement_import = """customUsers[email] = userObj;
                // ปลดล็อกออกจาก deletedStudentIds เมื่อมีการนำเข้าใหม่
                try {
                    let dIds = JSON.parse(localStorage.getItem('deletedStudentIds') || '[]');
                    const sid = String(userObj.student_id || userObj.id || '').trim();
                    dIds = dIds.filter(x => x !== sid && x !== email.toLowerCase());
                    localStorage.setItem('deletedStudentIds', JSON.stringify(dIds));
                } catch(e) {}"""
    if target_import in text and 'deletedStudentIds' not in text:
        text = text.replace(target_import, replacement_import)
        print("Added un-delete to admin-excel.js import")

    with open(ADMIN_EXCEL_FILE, 'w', encoding='utf-8') as f:
        f.write(text)
    print("admin-excel.js updated successfully!")

def update_template_csv():
    new_csv = """รหัสนิสิต,คำนำหน้านาม,ชื่อ - นามสกุล,ชั้นปี,ภาควิชา,หลักสูตร,หมู่เรียน,อาจารย์ที่ปรึกษา,ภาคการศึกษา,ปีการศึกษา,อีเมลมหาวิทยาลัย,เบอร์โทรศัพท์,ชื่อสถานประกอบการ,พิกัด,รหัสผ่านชั่วคราว
6521655442,นาย,วงศพัทธ์ อุเทน,4,วิทยาการคอมพิวเตอร์,ภาคพิเศษ,800,อ. สมชาย แจ่มใส,ต้น,69,wongsapat.u@ku.th,0948783020,สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.),"14.076949, 100.601563",123456
6521655189,นางสาว,ณิชมน เกียรติสกุล,4,วิทยาการคอมพิวเตอร์,ภาคพิเศษ,800,อ. สมชาย แจ่มใส,ต้น,69,nichamon.k@ku.th,0845678904,บริษัท ไลน์ คอมพานี (ประเทศไทย) จำกัด,"13.744882, 100.540835",123456
6521650123,นาย,กิตติศักดิ์ เจริญกิจ,4,วิทยาการคอมพิวเตอร์,ภาคปกติ,700,อ. สมชาย แจ่มใส,ต้น,69,kittisak.c@ku.th,0812345671,บริษัท อโกด้า เซอร์วิสเซส จำกัด (เซ็นทรัลเวิลด์),"13.746884, 100.539265",123456
6521650211,นางสาว,ธนพร วัฒนกุล,4,วิทยาการคอมพิวเตอร์,ภาคปกติ,701,อ. สมหญิง จงจิต,ต้น,69,thanaporn.w@ku.th,0823456782,ธนาคารไทยพาณิชย์ จำกัด (มหาชน) สำนักงานใหญ่,"13.826629, 100.565893",123456
6521650312,นาย,พีรพัฒน์ ศิริชัย,4,วิทยาการคอมพิวเตอร์,ภาคปกติ,702,อ. สมจิต มั่งมี,ต้น,69,peerapat.s@ku.th,0834567893,บริษัท โทรคมนาคมแห่งชาติ จำกัด (มหาชน) (NT แจ้งวัฒนะ),"13.884500, 100.578600",123456
"""
    with open(TEMPLATE_CSV, 'w', encoding='utf-8') as f:
        f.write(new_csv)
    print("Student_Import_Template.csv updated successfully!")

if __name__ == '__main__':
    update_dashboard()
    update_supabase_client()
    update_admin_excel()
    update_template_csv()
    print("ALL UPDATES APPLIED!")
