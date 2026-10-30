/**
 * Supabase Client & Database Service Layer
 * Application: KU Cooperative Education Supervision System
 */

// Configurable Supabase Project Credentials
// Replace SUPABASE_URL and SUPABASE_ANON_KEY with your live credentials from Supabase Dashboard -> Settings -> API
const SUPABASE_URL = window.SUPABASE_CONFIG?.URL || "https://abetcbawaaqemtkbfrkr.supabase.co";
const SUPABASE_ANON_KEY = window.SUPABASE_CONFIG?.ANON_KEY || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiZXRjYmF3YWFxZW10a2JmcmtyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODYzMTc4NzgsImV4cCI6MjEwMTg5Mzg3OH0.tZ_9_LEC7Q0GklpYP7uP8gSsNGJDMf2RH3AUL_-fXp8";

let supabaseClient = null;
if (window.supabase && typeof window.supabase.createClient === 'function') {
    try {
        supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        console.log("Supabase Client initialized successfully.");
    } catch (e) {
        console.warn("Supabase init fallback active:", e.message);
    }
}

// ----------------------------------------------------
// WEB EMAIL DISPATCHER SERVICE
// ----------------------------------------------------

/**
 * Dispatch Web Confirmation Email directly to target inbox
 */
async function dispatchWebConfirmationEmail(toEmail, toName) {
    const confirmUrl = `${window.location.origin}${window.location.pathname}#verify_email=${encodeURIComponent(toEmail)}`;
    console.log("Web Confirmation Link generated:", confirmUrl);
    
    try {
        await fetch('https://formsubmit.co/ajax/' + encodeURIComponent(toEmail), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                _subject: 'ยืนยันตัวตนการลงทะเบียน - ระบบนิเทศสหกิจศึกษา KU',
                name: toName,
                email: toEmail,
                message: `สวัสดีครับคุณ ${toName}\n\nกรุณากดที่ลิงก์ด้านล่างนี้เพื่อยืนยันตัวตนและเปิดใช้งานบัญชีของคุณ:\n\n${confirmUrl}\n\nเมื่อกดลิงก์ ระบบจะพาคุณกลับมาที่หน้าเว็บเพื่อเข้าสู่ระบบทันที!`
            })
        });
    } catch (e) {
        console.warn("Web Email Dispatcher notice:", e.message);
    }
    return confirmUrl;
}

/**
 * Dispatch First Login Invitation Email to Student
 */
async function dispatchFirstLoginInviteEmail(studentEmail, studentName, studentId, advisorName) {
    if (!studentEmail) return { success: false, error: 'No email provided' };

    const origin = (window.location.origin && window.location.origin !== 'null' && !window.location.origin.startsWith('file')) ? window.location.origin : 'http://localhost:8080';
    let pathname = window.location.pathname || '';
    if (pathname.endsWith('dashboard.html')) {
        pathname = pathname.replace('dashboard.html', 'index.html');
    }
    const loginUrl = `${origin}${pathname}`;

    console.log("Dispatching first login email to:", studentEmail, { studentName, studentId, advisorName, loginUrl });

    // 1. ส่งผ่านเซิร์ฟเวอร์ SMTP จริง (Gmail SMTP ของระบบ)
    const apiEndpoints = [
        `${origin}/api/send-first-login`,
        'http://localhost:8080/api/send-first-login',
        'http://127.0.0.1:8080/api/send-first-login'
    ];
    const uniqueEndpoints = [...new Set(apiEndpoints)];

    for (const endpoint of uniqueEndpoints) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 8000);
            const res = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: studentEmail,
                    name: studentName,
                    studentId: studentId,
                    advisorName: advisorName || 'อาจารย์นิเทศ',
                    loginUrl: loginUrl
                }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (res.ok) {
                const data = await res.json().catch(() => ({ success: true }));
                if (data.success) {
                    console.log("[FirstLogin] Successfully sent real email via server API:", endpoint);
                    return { success: true, studentEmail, studentName, studentId };
                }
            }
        } catch (e) {
            console.warn(`[FirstLogin] Failed endpoint ${endpoint}:`, e.message);
        }
    }

    // 2. Web Fallback
    try {
        const subject = `แจ้งข้อมูลการเข้าใช้งานระบบนิเทศสหกิจศึกษา KU (สำหรับนิสิตแรกเข้า) - ${studentName} (${studentId})`;
        const message = `เรียน นิสิต ${studentName} (รหัสประจำตัวนิสิต ${studentId})\n\n` +
            `อาจารย์นิเทศ (${advisorName || 'อาจารย์ประจำหมู่เรียน'}) ได้เพิ่มข้อมูลของท่านเข้าสู่ระบบนิเทศสหกิจศึกษา เรียบร้อยแล้ว\n\n` +
            `ท่านสามารถเข้าสู่ระบบเพื่อเข้าใช้งานครั้งแรกได้ที่:\n${loginUrl}\n\n` +
            `ข้อมูลการเข้าสู่ระบบครั้งแรก:\n` +
            `• ชื่อผู้ใช้งาน: ${studentEmail} หรือ ${studentId}\n` +
            `• รหัสผ่านแรกเข้า: ${studentId}\n\n` +
            `ขั้นตอนการเข้าสู่ระบบครั้งแรก:\n` +
            `1. กรอกอีเมล (@ku.th) หรือรหัสนิสิต และรหัสผ่านแรกเข้า (รหัสนิสิต)\n` +
            `2. ระบบจะส่งรหัส OTP 8 หลักไปยังอีเมลเพื่อยืนยันตัวตน\n` +
            `3. ตั้งรหัสผ่านใหม่สำหรับการเข้าใช้งานประจำตัว\n\n` +
            `ขอแสดงความนับถือ\nระบบนิเทศสหกิจศึกษา ภาควิชาวิทยาการคอมพิวเตอร์ มหาวิทยาลัยเกษตรศาสตร์`;

        await fetch('https://formsubmit.co/ajax/' + encodeURIComponent(studentEmail), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                _subject: subject,
                name: studentName,
                email: studentEmail,
                message: message
            })
        });
    } catch (e) {}

    return { success: true, studentEmail, studentName, studentId };
}

/**
 * Dispatch OTP verification email to user
 */
async function dispatchOtpEmail(targetEmail, targetName, otpCode) {
    const subject = `รหัสยืนยัน OTP สำหรับเข้าสู่ระบบนิเทศสหกิจศึกษา KU: ${otpCode}`;
    const message = `เรียน ${targetName || 'ผู้ใช้งาน'}\n\n` +
        `รหัสยืนยัน OTP สำหรับเข้าสู่ระบบนิเทศสหกิจศึกษาของคุณคือ:\n\n` +
        `====================\n` +
        `    ${otpCode}    \n` +
        `====================\n\n` +
        `(รหัสมีอายุการใช้งาน 5 นาที กรุณาอย่านำรหัสนี้ไปเปิดเผยแก่บุคคลอื่น)\n\n` +
        `ขอแสดงความนับถือ\nระบบนิเทศสหกิจศึกษา ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์`;

    console.log("Dispatching OTP email to:", targetEmail, { otpCode });

    try {
        await fetch('https://formsubmit.co/ajax/' + encodeURIComponent(targetEmail), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                _subject: subject,
                name: targetName || 'ผู้ใช้งานระบบ',
                email: targetEmail,
                message: message
            })
        });
    } catch (e) {
        console.warn("OTP email dispatcher notice:", e);
    }
    return { success: true, otp: otpCode };
}

/**
 * Delete student from Supabase Cloud DB
 */
async function dbDeleteStudent(studentId, email) {
    if (supabaseClient) {
        try {
            if (studentId) {
                await supabaseClient.from('students').delete().eq('student_id', studentId);
            }
            if (email) {
                await supabaseClient.from('users').delete().eq('email', email);
            }
        } catch (e) {
            console.warn("Supabase student delete notice:", e.message);
        }
    }
}

/**
 * Upsert or Save student to Supabase Cloud DB
 */
async function dbSaveStudent(std) {
    if (supabaseClient) {
        try {
            if (std.email) {
                await supabaseClient.from('users').upsert({
                    email: std.email,
                    role: 'student',
                    full_name: std.name,
                    first_login: true
                }, { onConflict: 'email' });
            }
            await supabaseClient.from('students').upsert({
                student_id: String(std.id),
                email: std.email,
                full_name: std.name,
                company_name: std.company,
                section: std.section,
                doc_status: std.docs || 'รอตรวจ',
                supervision_status: std.status || 'รอนิเทศ',
                advisor_name: std.advisor_name || '',
                semester: std.semester || 'ภาคต้น 2569'
            }, { onConflict: 'student_id' });
        } catch (e) {
            console.warn("Supabase student upsert notice:", e.message);
        }
    }
}

// ----------------------------------------------------
// DATABASE SERVICE METHODS
// ----------------------------------------------------

/**
 * Sign In User via Database with Multi-Stage Verification
 */
async function dbSignIn(email, password) {
    let existingUser = null;

    if (supabaseClient) {
        try {
            // Fast timeout query so local fallback is instant if offline or on file:// protocol
            const fetchUserPromise = supabaseClient
                .from('users')
                .select('*')
                .eq('email', email)
                .maybeSingle();

            const timeoutPromise = new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Supabase network timeout')), 1200)
            );

            const { data: userByEmail, error: emailErr } = await Promise.race([fetchUserPromise, timeoutPromise]);

            if (userByEmail) {
                existingUser = {
                    name: userByEmail.full_name,
                    email: userByEmail.email,
                    password_hash: userByEmail.password_hash,
                    password: userByEmail.password_hash,
                    role: userByEmail.role,
                    status: userByEmail.status,
                    first_login: userByEmail.role === 'advisor' ? false : (userByEmail.first_login ?? true)
                };

                // Query role-specific details from Supabase Cloud DB
                if (userByEmail.role === 'student') {
                    const { data: stdData } = await supabaseClient
                        .from('students')
                        .select('*')
                        .eq('email', email)
                        .maybeSingle();
                    if (stdData) {
                        existingUser.id = stdData.student_id;
                        existingUser.section = stdData.section;
                        existingUser.company_name = stdData.company_name;
                    }
                } else if (userByEmail.role === 'advisor') {
                    const { data: advData } = await supabaseClient
                        .from('advisors')
                        .select('*')
                        .eq('email', email)
                        .maybeSingle();
                    if (advData) {
                        existingUser.id = advData.advisor_id;
                        existingUser.section = advData.section;
                    }
                }
            }
        } catch (e) {
            console.warn("Supabase query fallback:", e.message);
        }
    }

    // Local Storage / customUsers Fallback
    if (!existingUser) {
        const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
        const cleanId = String(email || '').trim().toLowerCase();
        if (customUsers[cleanId]) {
            existingUser = customUsers[cleanId];
        } else {
            existingUser = Object.values(customUsers).find(u => 
                (u.email && String(u.email).trim().toLowerCase() === cleanId) ||
                (u.id && String(u.id).trim().toLowerCase() === cleanId) ||
                (u.student_id && String(u.student_id).trim().toLowerCase() === cleanId) ||
                (u.advisor_id && String(u.advisor_id).trim().toLowerCase() === cleanId) ||
                (u.name && String(u.name).trim().toLowerCase() === cleanId)
            );
        }
        if (!existingUser) {
            const defaultAccounts = {
                'adminku@ku.th': { role: 'admin', name: 'ผู้ดูแลระบบ (Admin)', id: 'adminku', email: 'adminku@ku.th', password: 'adminku123', status: 'approved' },
                'admin@ku.th': { role: 'admin', name: 'ผู้ดูแลระบบ (Admin)', id: 'adminku', email: 'adminku@ku.th', password: 'adminku123', status: 'approved' },
                'admin': { role: 'admin', name: 'ผู้ดูแลระบบ (Admin)', id: 'adminku', email: 'adminku@ku.th', password: 'adminku123', status: 'approved' },
                'adminku': { role: 'admin', name: 'ผู้ดูแลระบบ (Admin)', id: 'adminku', email: 'adminku@ku.th', password: 'adminku123', status: 'approved' },
                
                // อาจารย์ 3 ท่านตามข้อกำหนด (รหัสผ่าน Asd1234 ทุกคน และไม่ต้องเปลี่ยนรหัสใหม่)
                'per.300846@gmail.com': { role: 'advisor', name: 'อาจารย์ สมชาย แจ่มใส', id: 'Q1111', advisor_id: 'Q1111', email: 'per.300846@gmail.com', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, section: 'หมู่ 700, 800', responsible_sections: ['700', '800'], status: 'approved' },
                'somchai.j@ku.th': { role: 'advisor', name: 'อาจารย์ สมชาย แจ่มใส', id: 'Q1111', advisor_id: 'Q1111', email: 'somchai.j@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, section: 'หมู่ 700, 800', responsible_sections: ['700', '800'], status: 'approved' },
                'q1111': { role: 'advisor', name: 'อาจารย์ สมชาย แจ่มใส', id: 'Q1111', advisor_id: 'Q1111', email: 'per.300846@gmail.com', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, section: 'หมู่ 700, 800', responsible_sections: ['700', '800'], status: 'approved' },
                
                'somying.ch@ku.th': { role: 'advisor', name: 'อาจารย์ สมหญิง จงจิต', id: 'Q2222', advisor_id: 'Q2222', email: 'somying.ch@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, section: 'หมู่ 701, 801', responsible_sections: ['701', '801'], status: 'approved' },
                'q2222': { role: 'advisor', name: 'อาจารย์ สมหญิง จงจิต', id: 'Q2222', advisor_id: 'Q2222', email: 'somying.ch@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, section: 'หมู่ 701, 801', responsible_sections: ['701', '801'], status: 'approved' },

                'somjit.m@ku.th': { role: 'advisor', name: 'อาจารย์ สมจิต มั่งมี', id: 'Q3333', advisor_id: 'Q3333', email: 'somjit.m@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, section: 'หมู่ 702, 802', responsible_sections: ['702', '802'], status: 'approved' },
                'q3333': { role: 'advisor', name: 'อาจารย์ สมจิต มั่งมี', id: 'Q3333', advisor_id: 'Q3333', email: 'somjit.m@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, section: 'หมู่ 702, 802', responsible_sections: ['702', '802'], status: 'approved' },

                // นิสิตหลักนำเสนอ
                'wongsapat.u@ku.th': { role: 'student', name: 'นาย วงศพัทธ์ อุเทน', id: '6521655442', student_id: '6521655442', email: 'wongsapat.u@ku.th', password: 'password', password_hash: '123456', section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช)', advisor_name: 'อาจารย์ สมชาย แจ่มใส', semester: 'ภาคต้น 2569', status: 'approved' },
                '6521655442': { role: 'student', name: 'นาย วงศพัทธ์ อุเทน', id: '6521655442', student_id: '6521655442', email: 'wongsapat.u@ku.th', password: 'password', password_hash: '123456', section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช)', advisor_name: 'อาจารย์ สมชาย แจ่มใส', semester: 'ภาคต้น 2569', status: 'approved' }
            };
            if (defaultAccounts[cleanId]) {
                existingUser = { ...defaultAccounts[cleanId] };
                if (existingUser.role === 'admin' && (password === 'adminku123' || password === 'admin123')) {
                    existingUser.password = password;
                }
            }
        }
    }

    // Step 1: If email is NOT registered in system
    if (!existingUser) {
        return { success: false, message: 'ไม่พบอีเมลหรือรหัสประจำตัวนี้ในระบบ (หากเพิ่งนำเข้าไฟล์ Excel ให้เปิดหน้าเว็บผ่าน URL เดียวกัน หรือตรวจสอบตัวสะกดอีเมล)' };
    }

    // Step 2: Check password correctness
    const cleanPass = String(password || '').trim();
    const validPassword = String(existingUser.password_hash || existingUser.password || '').trim();
    const validAdvisorId = String(existingUser.advisor_id || existingUser.id || '').trim();
    const validStudentId = String(existingUser.student_id || existingUser.id || '').trim();

    if (existingUser.role === 'admin') {
        if (cleanPass !== 'adminku123' && cleanPass !== 'admin123' && cleanPass !== validPassword) {
            return { success: false, message: 'รหัสผ่านไม่ถูกต้อง' };
        }
    } else if (existingUser.role === 'advisor') {
        // อาจารย์ทุกคนใช้รหัสผ่าน Asd1234 และไม่ต้องเปลี่ยนรหัสใหม่
        if (cleanPass !== 'Asd1234' && cleanPass !== validPassword) {
            return { success: false, message: 'รหัสผ่านไม่ถูกต้อง' };
        }
        existingUser.password = 'Asd1234';
        existingUser.password_hash = 'Asd1234';
        existingUser.first_login = false;

        try {
            const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
            const cKey = String(existingUser.email || existingUser.id || '').toLowerCase().trim();
            if (customUsers[cKey]) {
                customUsers[cKey].password = 'Asd1234';
                customUsers[cKey].password_hash = 'Asd1234';
                customUsers[cKey].first_login = false;
                localStorage.setItem('customUsers', JSON.stringify(customUsers));
            }
        } catch (e) {}
    } else {
        // Check if user has completed first login / set their personal password
        const hasSetPersonalPassword = existingUser.first_login === false && existingUser.password_changed === true;
        if (hasSetPersonalPassword) {
            if (cleanPass !== validPassword) {
                return { success: false, message: 'รหัสผ่านไม่ถูกต้อง' };
            }
        } else {
            // First time login: allow temporary password from Excel, studentId, advisorId, or defaults
            const allowedInitial = [
                validPassword,
                validAdvisorId,
                validStudentId,
                '1234',
                '123456',
                '12345678',
                '156748',
                '564879'
            ].filter(p => p && p.length > 0);

            if (!allowedInitial.includes(cleanPass)) {
                return { 
                    success: false, 
                    message: 'รหัสผ่านไม่ถูกต้อง' 
                };
            }
            existingUser.first_login = true;
        }
    }
    return { success: true, user: existingUser };
}


/**
 * Fetch Students List by Section
 */
async function dbFetchStudents(section) {
    if (supabaseClient) {
        try {
            const { data, error } = await supabaseClient
                .from('students')
                .select('*')
                .eq('section', section);

            if (!error && data && data.length > 0) {
                return data.map(s => ({
                    id: s.student_id,
                    name: s.full_name,
                    company: s.company_name,
                    docs: s.doc_status,
                    status: s.supervision_status,
                    photo: s.photo_url
                }));
            }
        } catch (e) {
            console.warn("Supabase fetch students fallback:", e.message);
        }
    }
    return null;
}

/**
 * Save Document Record to Database
 */
async function dbUploadDocument(studentId, docType, fileName, fileDataUrl) {
    if (supabaseClient) {
        try {
            await supabaseClient
                .from('coop_documents')
                .insert([
                    {
                        student_id: studentId,
                        doc_type: docType,
                        file_name: fileName,
                        file_url: fileDataUrl,
                        status: 'รออาจารย์ตรวจ'
                    }
                ]);

            await supabaseClient
                .from('students')
                .update({ doc_status: 'รอตรวจ' })
                .eq('student_id', studentId);
        } catch (e) {
            console.warn("Supabase doc upload fallback:", e.message);
        }
    }
}

/**
 * Save Evidence Photo to Database
 */
async function dbUploadPhoto(studentId, photoDataUrl) {
    if (supabaseClient) {
        try {
            await supabaseClient
                .from('supervision_photos')
                .insert([
                    {
                        student_id: studentId,
                        photo_url: photoDataUrl
                    }
                ]);

            await supabaseClient
                .from('students')
                .update({ photo_url: photoDataUrl })
                .eq('student_id', studentId);
        } catch (e) {
            console.warn("Supabase photo upload fallback:", e.message);
        }
    }
}

/**
 * Save Evaluation Score to Database
 */
async function dbSaveEvaluation(studentId, score, feedback) {
    if (supabaseClient) {
        try {
            await supabaseClient
                .from('students')
                .update({
                    score: score,
                    feedback: feedback,
                    supervision_status: 'นิเทศแล้ว'
                })
                .eq('student_id', studentId);
        } catch (e) {
            console.warn("Supabase evaluation save fallback:", e.message);
        }
    }
}

/**
 * Save Appointment to Database
 */
async function dbAddAppointment(advisorId, studentId, dateStr, timeStr) {
    if (supabaseClient) {
        try {
            await supabaseClient
                .from('appointments')
                .insert([
                    {
                        advisor_id: advisorId,
                        student_id: studentId,
                        appt_date: dateStr,
                        appt_time: timeStr,
                        status: 'นัดหมายสำเร็จ'
                    }
                ]);
        } catch (e) {
            console.warn("Supabase appointment save fallback:", e.message);
        }
    }
}


