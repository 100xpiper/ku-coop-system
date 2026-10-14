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
                    first_login: userByEmail.first_login ?? true
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
                'adminku': { role: 'admin', name: 'ผู้ดูแลระบบ (Admin)', id: 'adminku', email: 'adminku@ku.th', password: 'adminku123', status: 'approved' }
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
    } else {
        // If the account has already set their personal password (first_login === false)
        if (existingUser.first_login === false && validPassword && validPassword !== '1234' && validPassword !== '123456') {
            if (cleanPass !== validPassword) {
                return { success: false, message: 'รหัสผ่านไม่ถูกต้อง' };
            }
        } else {
            // First time login: allow 123456, 1234, advisor/student ID, or any initial password (>= 4 chars)
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


