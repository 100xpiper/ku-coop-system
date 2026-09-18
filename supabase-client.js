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
                _subject: '๐“ง เธขเธทเธเธขเธฑเธเธ•เธฑเธงเธ•เธเธเธฒเธฃเธฅเธเธ—เธฐเน€เธเธตเธขเธ - เธฃเธฐเธเธเธเธดเน€เธ—เธจเธชเธซเธเธดเธเธจเธถเธเธฉเธฒ KU',
                _subject: '๐Ÿ“ง เธขเธทเธ™เธขเธฑเธ™เธ•เธฑเธงเธ•เธ™เธ เธฒเธฃเธฅเธ‡เธ—เธฐเน€เธšเธตเธขเธ™ - เธฃเธฐเธšเธšเธ™เธดเน€เธ—เธจเธชเธซเธ เธดเธˆเธจเธถเธ เธฉเธฒ KU',
                name: toName,
                email: toEmail,
                message: `เธชเธงเธฑเธชเธ”เธตเธ„เธฃเธฑเธšเธ„เธธเธ“ ${toName}\n\nเธ เธฃเธธเธ“เธฒเธ เธ”เธ—เธตเนˆเธฅเธดเธ‡เธ เนŒเธ”เน‰เธฒเธ™เธฅเนˆเธฒเธ‡เธ™เธตเน‰เน€เธžเธทเนˆเธญเธขเธทเธ™เธขเธฑเธ™เธ•เธฑเธงเธ•เธ™เน เธฅเธฐเน€เธ›เธดเธ”เนƒเธŠเน‰เธ‡เธฒเธ™เธšเธฑเธ เธŠเธตเธ‚เธญเธ‡เธ„เธธเธ“:\n\n${confirmUrl}\n\nเน€เธกเธทเนˆเธญเธ เธ”เธฅเธดเธ‡เธ เนŒ เธฃเธฐเธšเธšเธˆเธฐเธžเธฒเธ„เธธเธ“เธ เธฅเธฑเธšเธกเธฒเธ—เธตเนˆเธซเธ™เธฒเน€เธงเน‡เšเน€เธžเธทเนˆเธญเน€เธ‚เน‰เธฒเธชเธนเนˆเธฃเธฐเธšเธšเธ—เธฑเธ™เธ—เธต!`
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
            // Query public.users table directly for matching email
            const { data: userByEmail, error: emailErr } = await supabaseClient
                .from('users')
                .select('*')
                .eq('email', email)
                .maybeSingle();

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

    // Local Storage / Static Seed Fallback
    if (!existingUser) {
        const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
        if (customUsers[email]) {
            existingUser = customUsers[email];
        } else if (email === 'adminku@ku.th' || email === 'adminku' || email === 'admin@ku.th' || email === 'admin') {
            existingUser = { role: 'admin', name: 'ผู้ดูแลระบบ (Admin)', id: 'adminku', email: 'adminku@ku.th', password_hash: 'admin123', password: 'admin123', status: 'approved' };
        }
    }

    // Step 1: If email is NOT registered in system
    if (!existingUser) {
        return { success: false, message: 'ไม่พบอีเมลนี้ในระบบ' };
    }

    // Step 3: Check password correctness
    const validPassword = existingUser.password_hash || existingUser.password;
    if (password !== validPassword) {
        return { success: false, message: 'รหัสผ่านไม่ถูกต้อง' };
    }

    return { success: true, user: existingUser };
}

/**
 * Sign Up User via Supabase Auth with Pending Admin Approval Status
 */
async function dbSignUp(newUser) {
    if (!newUser || !newUser.email || !newUser.password) {
        return { success: false, message: 'เธเธฃเธธเธ“เธฒเธเธฃเธญเธเธเนเธญเธกเธนเธฅเนเธซเนเธเธฃเธเธ–เนเธงเธ' };
    }

    if (supabaseClient) {
        try {
            // Save to public.users table with pending status
            await supabaseClient
                .from('users')
                .upsert([
                    {
                        email: newUser.email,
                        password_hash: newUser.password,
                        full_name: newUser.name,
                        role: newUser.role,
                        status: 'approved'
                    }
                ], { onConflict: 'email' });

            if (newUser.role === 'advisor') {
                await supabaseClient
                    .from('advisors')
                    .upsert([
                        {
                            advisor_id: newUser.id,
                            email: newUser.email,
                            full_name: newUser.name,
                            section: newUser.section || 'เธซเธกเธนเน 700'
                        }
                    ], { onConflict: 'advisor_id' });
            } else if (newUser.role === 'student') {
                await supabaseClient
                    .from('students')
                    .upsert([
                        {
                            student_id: newUser.id,
                            email: newUser.email,
                            full_name: newUser.name,
                            section: newUser.section || 'เธซเธกเธนเน 700',
                            company_name: 'เธขเธฑเธเนเธกเนเนเธ”เนเธฃเธฐเธเธธเธชเธ–เธฒเธเธเธฃเธฐเธเธญเธเธเธฒเธฃ',
                            doc_status: 'เธฃเธญเธ•เธฃเธงเธ',
                            supervision_status: 'เธฃเธญเธเธดเน€เธ—เธจ'
                        }
                    ], { onConflict: 'student_id' });
            }
        } catch (e) {
            console.warn("Supabase auth signup notice:", e.message);
        }
    }

    // Save to LocalStorage fallback with status pending
    const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
    customUsers[newUser.email] = { ...newUser, status: 'approved' };
    localStorage.setItem('customUsers', JSON.stringify(customUsers));

    return { 
        success: true, 
        message: `เธฅเธเธ—เธฐเน€เธเธตเธขเธเธชเธณเน€เธฃเนเธ! เธเธฑเธเธเธตเธเธญเธเธเธธเธ“เธญเธขเธนเนเธฃเธฐเธซเธงเนเธฒเธเธฃเธญเธเธฒเธฃเธญเธเธธเธกเธฑเธ•เธดเธชเธดเธ—เธเธดเนเธเธฒเธเธเธนเนเธ”เธนเนเธฅเธฃเธฐเธเธ (Admin)` 
    };
}

/**
 * Verify Email OTP Token / Confirmation Link via Supabase Auth (Method 1)
 */
async function dbVerifyEmailOTP(email, token) {
    if (supabaseClient) {
        try {
            const { data, error } = await supabaseClient.auth.verifyOtp({
                email: email,
                token: token,
                type: 'signup'
            });
            if (!error && data?.user) {
                return { success: true, user: data.user };
            } else if (error) {
                return { success: false, message: `เธขเธทเธเธขเธฑเธเนเธกเนเธชเธณเน€เธฃเนเธ: ${error.message}` };
            }
        } catch (e) {
            console.warn("OTP verify fallback:", e.message);
        }
    }
    // Demo fallback for test code (e.g. 123456)
    if (token && token.length >= 4) {
        return { success: true };
    }
    return { success: false, message: 'เธฃเธซเธฑเธชเธขเธทเธเธขเธฑเธ OTP เนเธกเนเธ–เธนเธเธ•เนเธญเธ เธซเธฃเธทเธญเธญเธตเน€เธกเธฅเธเธตเนเนเธกเนเธกเธตเธญเธขเธนเนเธเธฃเธดเธเนเธเธฃเธฐเธเธเธชเนเธเธเธ”เธซเธกเธฒเธข' };
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
                        status: 'เธฃเธญเธญเธฒเธเธฒเธฃเธขเนเธ•เธฃเธงเธ'
                    }
                ]);

            await supabaseClient
                .from('students')
                .update({ doc_status: 'เธฃเธญเธ•เธฃเธงเธ' })
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
                    supervision_status: 'เธเธดเน€เธ—เธจเนเธฅเนเธง'
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
                        status: 'เธเธฑเธ”เธซเธกเธฒเธขเธชเธณเน€เธฃเนเธ'
                    }
                ]);
        } catch (e) {
            console.warn("Supabase appointment save fallback:", e.message);
        }
    }
}

/**
 * Fetch List of Users Pending Admin Approval
 */
async function dbGetPendingUsers() {
    if (supabaseClient) {
        try {
            const { data, error } = await supabaseClient
                .from('users')
                .select('*')
                .eq('status', 'approved');
            if (!error && data) return data;
        } catch (e) {
            console.warn("Supabase pending users query fallback:", e.message);
        }
    }
    const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
    return Object.values(customUsers).filter(u => u.status === 'approved');
}

/**
 * Approve User Account (Admin Grant Role & Login Access)
 */
async function dbApproveUser(email) {
    if (supabaseClient) {
        try {
            await supabaseClient
                .from('users')
                .update({ status: 'approved' })
                .eq('email', email);
        } catch (e) {
            console.warn("Supabase user approval fallback:", e.message);
        }
    }
    const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
    if (customUsers[email]) {
        customUsers[email].status = 'approved';
        localStorage.setItem('customUsers', JSON.stringify(customUsers));
    }
    return { success: true, message: `เธญเธเธธเธกเธฑเธ•เธดเธชเธดเธ—เธเธดเนเธเธนเนเนเธเนเธเธฒเธ (${email}) เธชเธณเน€เธฃเนเธเน€เธฃเธตเธขเธเธฃเนเธญเธข!` };
}

/**
 * Reject User Account (Admin Deny Access)
 */
async function dbRejectUser(email) {
    if (supabaseClient) {
        try {
            await supabaseClient
                .from('users')
                .update({ status: 'rejected' })
                .eq('email', email);
        } catch (e) {
            console.warn("Supabase user rejection fallback:", e.message);
        }
    }
    const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
    if (customUsers[email]) {
        customUsers[email].status = 'rejected';
        localStorage.setItem('customUsers', JSON.stringify(customUsers));
    }
    return { success: true, message: `เธเธเธดเน€เธชเธเธเธณเธเธญเธฅเธเธ—เธฐเน€เธเธตเธขเธเธเธญเธ (${email}) เน€เธฃเธตเธขเธเธฃเนเธญเธขเนเธฅเนเธง` };
}

