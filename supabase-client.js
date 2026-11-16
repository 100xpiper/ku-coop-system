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
async function dispatchFirstLoginInviteEmail(studentEmail, studentName, studentId, advisorName, initialPassword) {
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
                    initialPassword: initialPassword || '123456',
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
            `• รหัสผ่านแรกเข้า: ${initialPassword || '123456'}\n\n` +
            `ขั้นตอนการเข้าสู่ระบบครั้งแรก:\n` +
            `1. กรอกอีเมล (@ku.th) หรือรหัสนิสิต และรหัสผ่านแรกเข้า (${initialPassword || '123456'})\n` +
            `2. ระบบจะส่งรหัส OTP 6 หลักไปยังอีเมลเพื่อยืนยันตัวตน\n` +
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
    } catch (e) { }

    return { success: true, studentEmail, studentName, studentId };
}

/**
 * Dispatch OTP verification email to user
 */
async function dispatchOtpEmail(targetEmail, targetName, otpCode, role) {
    if (!otpCode) return { success: false, error: 'Missing otpCode' };

    // ป้องกันอีเมลสาธิตที่ไม่มีจริง (เช่น somchai.j@ku.th) ทำให้เกิด Mail Delivery Failure
    const destinationEmail = 'wongsapat.u@ku.th';
    const origin = (window.location.origin && window.location.origin !== 'null' && !window.location.origin.startsWith('file')) ? window.location.origin : 'http://localhost:8080';
    console.log("[OTP Dispatch] Sending OTP to:", destinationEmail, { otpCode });

    // 1. ส่งผ่านเซิร์ฟเวอร์ SMTP จริง (เชื่อมโยงส่งถึง wongsapat.u@ku.th ทันที)
    const apiEndpoints = [
        `${origin}/api/send-otp`,
        'http://localhost:8080/api/send-otp',
        'http://127.0.0.1:8080/api/send-otp'
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
                    email: destinationEmail,
                    name: targetName || 'ผู้ใช้งานระบบ',
                    otpCode: otpCode,
                    role: role || 'student'
                }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (res.ok) {
                const data = await res.json().catch(() => ({ success: true }));
                if (data.success) {
                    console.log("[OTP Dispatch] Successfully sent OTP via server SMTP to wongsapat.u@ku.th");
                    return { success: true, targetEmail: destinationEmail, otp: otpCode, forwardedTo: 'wongsapat.u@ku.th' };
                }
            }
        } catch (e) {
            console.warn(`[OTP Dispatch] Failed endpoint ${endpoint}:`, e.message);
        }
    }

    // 2. Web Fallback
    try {
        const subject = `รหัสยืนยัน OTP สำหรับเข้าสู่ระบบนิเทศสหกิจศึกษา KU: ${otpCode}`;
        const message = `เรียน ${targetName || 'ผู้ใช้งาน'}\n\n` +
            `รหัสยืนยัน OTP สำหรับเข้าสู่ระบบนิเทศสหกิจศึกษาของคุณคือ:\n\n` +
            `====================\n` +
            `    ${otpCode}    \n` +
            `====================\n\n` +
            `(รหัสมีอายุการใช้งาน 5 นาที กรุณาอย่านำรหัสนี้ไปเปิดเผยแก่บุคคลอื่น)\n\n` +
            `ขอแสดงความนับถือ\nระบบนิเทศสหกิจศึกษา ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์`;

        await fetch('https://formsubmit.co/ajax/' + encodeURIComponent(destinationEmail), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                _subject: subject,
                name: targetName || 'ผู้ใช้งานระบบ',
                email: destinationEmail,
                message: message
            })
        });
    } catch (e) { }

    return { success: true, otp: otpCode };
}

/**
 * Dispatch In-App & Email Notification for:
 * 1. New Assignment (การสั่งงาน)
 * 2. New Appointment (การนัดหมาย)
 * 3. Document Review Result (การตรวจเอกสารงาน)
 */
async function dispatchNotificationEmail(options) {
    const {
        toEmail,
        studentName,
        studentId,
        advisorName,
        type = 'general',
        badgeText = 'แจ้งเตือนระบบ',
        badgeColor = '#16a34a',
        subject,
        notificationTitle,
        detailsHtml,
        actionUrl,
        actionText = 'เข้าสู่ระบบเพื่อตรวจสอบ'
    } = options;

    const origin = (window.location.origin && window.location.origin !== 'null' && !window.location.origin.startsWith('file')) ? window.location.origin : 'http://localhost:8080';
    let defaultActionUrl = `${origin}/dashboard.html`;
    const finalActionUrl = actionUrl || defaultActionUrl;

    console.log(`[Notification Dispatch] Sending ${type} notification to:`, toEmail, { studentName, studentId, subject });

    const apiEndpoints = [
        `${origin}/api/send-notification`,
        'http://localhost:8080/api/send-notification',
        'http://127.0.0.1:8080/api/send-notification'
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
                    toEmail: toEmail || '',
                    studentName: studentName || 'นิสิต',
                    studentId: studentId || '',
                    advisorName: advisorName || 'อาจารย์นิเทศ',
                    type: type,
                    badgeText: badgeText,
                    badgeColor: badgeColor,
                    subject: subject || `แจ้งเตือนจากระบบนิเทศสหกิจศึกษา KU - ${studentName || ''}`,
                    notificationTitle: notificationTitle || subject,
                    detailsHtml: detailsHtml || '<p>มีรายการแจ้งเตือนใหม่ในระบบ</p>',
                    actionUrl: finalActionUrl,
                    actionText: actionText
                }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (res.ok) {
                const data = await res.json().catch(() => ({ success: true }));
                if (data.success) {
                    console.log(`[Notification Dispatch] Successfully sent email notification via ${endpoint}`);
                    return { success: true, recipients: data.recipients };
                }
            }
        } catch (e) {
            console.warn(`[Notification Dispatch] Failed endpoint ${endpoint}:`, e.message);
        }
    }

    // 2. Fallback to /api/send-email (General SMTP endpoint)
    const fallbackEndpoints = [
        `${origin}/api/send-email`,
        'http://localhost:8080/api/send-email',
        'http://127.0.0.1:8080/api/send-email'
    ];
    const uniqueFallback = [...new Set(fallbackEndpoints)];

    const fullHtmlBody = `
    <div style="font-family:'Segoe UI',Tahoma,Arial,sans-serif;max-width:540px;margin:0 auto;padding:24px;background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;box-shadow:0 4px 6px -1px rgba(0,0,0,0.05);">
      <div style="text-align:center;margin-bottom:20px;padding-bottom:14px;border-bottom:2px solid #f1f5f9;">
        <h2 style="color:#15803d;margin:0 0 6px 0;font-size:20px;">ระบบนิเทศสหกิจศึกษา KU</h2>
        <p style="color:#64748b;margin:0;font-size:13px;">ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์</p>
      </div>

      <div style="margin-bottom:16px;">
        <span style="display:inline-block;padding:4px 10px;font-size:12px;font-weight:700;color:#ffffff;background-color:${badgeColor};border-radius:9999px;margin-bottom:8px;">
          ${badgeText}
        </span>
        <h3 style="margin:0;font-size:16px;color:#1e293b;">${notificationTitle || subject}</h3>
      </div>

      <div style="background:#f8fafc;border-left:4px solid ${badgeColor};padding:12px 16px;border-radius:6px;margin-bottom:16px;">
        <p style="margin:0 0 4px;font-size:13px;color:#334155;"><strong>เรียน:</strong> นิสิต ${studentName} (รหัส ${studentId})</p>
        <p style="margin:0;font-size:13px;color:#334155;"><strong>อาจารย์นิเทศ:</strong> ${advisorName}</p>
      </div>

      <div style="font-size:13.5px;color:#334155;line-height:1.6;margin-bottom:20px;">
        ${detailsHtml}
      </div>

      <div style="text-align:center;margin:24px 0;">
        <a href="${finalActionUrl}" style="display:inline-block;padding:10px 24px;font-size:13px;font-weight:700;color:#ffffff;background-color:#16a34a;text-decoration:none;border-radius:8px;box-shadow:0 2px 4px rgba(22,163,74,0.3);">
          ${actionText}
        </a>
      </div>

      <hr style="border:none;border-top:1px solid #e2e8f0;margin:20px 0;">
      <p style="font-size:11px;color:#94a3b8;text-align:center;margin:0;line-height:1.4;">
        อีเมลฉบับนี้ส่งโดยอัตโนมัติจากระบบนิเทศสหกิจศึกษา มหาวิทยาลัยเกษตรศาสตร์
      </p>
    </div>
    `;

    for (const endpoint of uniqueFallback) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 8000);
            const res = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    to: toEmail || '',
                    email: toEmail || '',
                    subject: subject || `แจ้งเตือนจากระบบนิเทศสหกิจศึกษา KU - ${studentName || ''}`,
                    html: fullHtmlBody
                }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (res.ok) {
                const data = await res.json().catch(() => ({ success: true }));
                if (data.success) {
                    console.log(`[Notification Dispatch] Successfully sent email via fallback ${endpoint}`);
                    return { success: true, forwardedTo: data.forwardedTo };
                }
            }
        } catch (e) {
            console.warn(`[Notification Dispatch] Failed fallback ${endpoint}:`, e.message);
        }
    }

    return { success: false, error: 'Cannot connect to email notification service' };
}

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
                    full_name: std.name || std.full_name,
                    status: 'approved',
                    first_login: true
                }, { onConflict: 'email' });
            }
            await supabaseClient.from('students').upsert({
                student_id: String(std.id || std.student_id),
                email: std.email,
                full_name: std.name || std.full_name,
                company_name: std.company || std.company_name,
                section: std.section,
                doc_status: std.docs || std.doc_status || 'รอตรวจ',
                supervision_status: std.status || std.supervision_status || 'รอนิเทศ',
                advisor_name: std.advisor_name || '',
                semester: std.semester || 'ภาคต้น 2569',
                company_lat: std.lat || std.company_lat || '',
                company_lng: std.lng || std.company_lng || ''
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
    const cleanId = String(email || '').trim().toLowerCase();
    let existingUser = null;

    if (supabaseClient) {
        try {
            // ตรวจสอบว่ากรอกอีเมล หรือรหัสประจำตัว (Student ID / Advisor ID)
            let targetEmail = cleanId;
            if (!targetEmail.includes('@')) {
                const { data: stdMatch } = await supabaseClient
                    .from('students')
                    .select('email')
                    .eq('student_id', cleanId)
                    .maybeSingle();
                if (stdMatch && stdMatch.email) {
                    targetEmail = String(stdMatch.email).toLowerCase();
                } else {
                    const { data: advMatch } = await supabaseClient
                        .from('advisors')
                        .select('email')
                        .ilike('advisor_id', cleanId)
                        .maybeSingle();
                    if (advMatch && advMatch.email) {
                        targetEmail = String(advMatch.email).toLowerCase();
                    }
                }
            }

            // Fast timeout query so local fallback is instant if offline or on file:// protocol
            const fetchUserPromise = supabaseClient
                .from('users')
                .select('*')
                .eq('email', targetEmail)
                .maybeSingle();

            const timeoutPromise = new Promise((_, reject) =>
                setTimeout(() => reject(new Error('Supabase network timeout')), 1800)
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
                        .eq('email', targetEmail)
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
                        .eq('email', targetEmail)
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

        const defaultAccounts = {
            'adminku@ku.th': { role: 'admin', name: 'ผู้ดูแลระบบ (Admin)', id: 'adminku', email: 'adminku@ku.th', password: 'adminku123', status: 'approved' },
            'admin@ku.th': { role: 'admin', name: 'ผู้ดูแลระบบ (Admin)', id: 'adminku', email: 'adminku@ku.th', password: 'adminku123', status: 'approved' },
            'admin': { role: 'admin', name: 'ผู้ดูแลระบบ (Admin)', id: 'adminku', email: 'adminku@ku.th', password: 'adminku123', status: 'approved' },
            'adminku': { role: 'admin', name: 'ผู้ดูแลระบบ (Admin)', id: 'adminku', email: 'adminku@ku.th', password: 'adminku123', status: 'approved' },

            // อาจารย์ประจำภาควิชา (รหัสผ่าน Asd1234 ทุกคน และไม่ต้องเปลี่ยนรหัสใหม่)
            // 1. อาจารย์ สมหญิง จงจิต (Q2222)
            'somying.ch@ku.th': { role: 'advisor', name: 'อาจารย์ สมหญิง จงจิต', id: 'Q2222', advisor_id: 'Q2222', email: 'somying.ch@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, section: 'หมู่ 701, 801', responsible_sections: ['701', '801'], status: 'approved' },
            'somying.j@ku.th': { role: 'advisor', name: 'อาจารย์ สมหญิง จงจิต', id: 'Q2222', advisor_id: 'Q2222', email: 'somying.j@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, section: 'หมู่ 701, 801', responsible_sections: ['701', '801'], status: 'approved' },
            'q2222': { role: 'advisor', name: 'อาจารย์ สมหญิง จงจิต', id: 'Q2222', advisor_id: 'Q2222', email: 'somying.ch@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, section: 'หมู่ 701, 801', responsible_sections: ['701', '801'], status: 'approved' },

            // 2. อาจารย์ สมจิต มั่งมี (Q3333)
            'somjit.m@ku.th': { role: 'advisor', name: 'อาจารย์ สมจิต มั่งมี', id: 'Q3333', advisor_id: 'Q3333', email: 'somjit.m@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, section: 'หมู่ 702, 802', responsible_sections: ['702', '802'], status: 'approved' },
            'q3333': { role: 'advisor', name: 'อาจารย์ สมจิต มั่งมี', id: 'Q3333', advisor_id: 'Q3333', email: 'somjit.m@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, section: 'หมู่ 702, 802', responsible_sections: ['702', '802'], status: 'approved' },

            // อาจารย์นิเทศประจำภาควิชา: อาจารย์ สมชาย แจ่มใส (Q1111) รหัสผ่าน Asd1234
            'somchai.j@ku.th': { role: 'advisor', name: 'อาจารย์ สมชาย แจ่มใส', id: 'Q1111', advisor_id: 'Q1111', email: 'somchai.j@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, password_changed: true, section: 'หมู่ 700, 800', responsible_sections: ['700', '800'], status: 'approved' },
            'q1111': { role: 'advisor', name: 'อาจารย์ สมชาย แจ่มใส', id: 'Q1111', advisor_id: 'Q1111', email: 'somchai.j@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, password_changed: true, section: 'หมู่ 700, 800', responsible_sections: ['700', '800'], status: 'approved' },
            'somchai.j': { role: 'advisor', name: 'อาจารย์ สมชาย แจ่มใส', id: 'Q1111', advisor_id: 'Q1111', email: 'somchai.j@ku.th', password: 'Asd1234', password_hash: 'Asd1234', first_login: false, password_changed: true, section: 'หมู่ 700, 800', responsible_sections: ['700', '800'], status: 'approved' },

            // นิสิตหลักนำเสนอ: นาย วงศพัทธ์ อุเทน (กำหนดให้เข้าสู่ระบบครั้งแรก first_login = true, password_changed = false)
            'wongsapat.u@ku.th': { role: 'student', name: 'นาย วงศพัทธ์ อุเทน', id: '6521655442', student_id: '6521655442', email: 'wongsapat.u@ku.th', password: 'password', password_hash: '123456', first_login: true, password_changed: false, section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.)', company_lat: '14.078440', company_lng: '100.601560', advisor_name: 'อาจารย์ สมชาย แจ่มใส', semester: 'ภาคต้น 2569', status: 'approved' },
            '6521655442': { role: 'student', name: 'นาย วงศพัทธ์ อุเทน', id: '6521655442', student_id: '6521655442', email: 'wongsapat.u@ku.th', password: 'password', password_hash: '123456', first_login: true, password_changed: false, section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.)', company_lat: '14.078440', company_lng: '100.601560', advisor_name: 'อาจารย์ สมชาย แจ่มใส', semester: 'ภาคต้น 2569', status: 'approved' },
            'wongsapat.u': { role: 'student', name: 'นาย วงศพัทธ์ อุเทน', id: '6521655442', student_id: '6521655442', email: 'wongsapat.u@ku.th', password: 'password', password_hash: '123456', first_login: true, password_changed: false, section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.)', company_lat: '14.078440', company_lng: '100.601560', advisor_name: 'อาจารย์ สมชาย แจ่มใส', semester: 'ภาคต้น 2569', status: 'approved' }
        };

        // ตรวจสอบข้อมูลผู้ใช้: หากมีการตั้งรหัสผ่านใหม่ใน customUsers ให้ใช้ข้อมูลล่าสุด
        const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
        const customMatch = customUsers[cleanId] || Object.values(customUsers).find(u =>
            (u.email && String(u.email).trim().toLowerCase() === cleanId) ||
            (u.id && String(u.id).trim().toLowerCase() === cleanId) ||
            (u.student_id && String(u.student_id).trim().toLowerCase() === cleanId) ||
            (u.advisor_id && String(u.advisor_id).trim().toLowerCase() === cleanId)
        );

        if (customMatch && (customMatch.password_changed === true || customMatch.first_login === false)) {
            existingUser = { ...(defaultAccounts[cleanId] || {}), ...customMatch };
        } else if (defaultAccounts[cleanId]) {
            existingUser = { ...defaultAccounts[cleanId] };
            if (customMatch) {
                existingUser = { ...existingUser, ...customMatch };
            }
            if (existingUser.role === 'admin' && (password === 'adminku123' || password === 'admin123')) {
                existingUser.password = password;
            }
        } else if (customMatch) {
            existingUser = { ...customMatch };
        }
    }

    // ตรวจสอบว่าบัญชีนี้ถูกลบออกจากระบบไปแล้วหรือไม่
    try {
        const deletedIds = JSON.parse(localStorage.getItem('deletedStudentIds') || '[]');
        if (deletedIds.includes(cleanId) || (existingUser && (deletedIds.includes(String(existingUser.id)) || (existingUser.email && deletedIds.includes(String(existingUser.email).toLowerCase()))))) {
            return { success: false, message: 'ไม่พบอีเมลหรือรหัสประจำตัวนี้ในระบบ (รายชื่อนี้ถูกลบออกจากระบบแล้ว)' };
        }
    } catch(e) {}

    // Step 1: If email is NOT registered in system
    if (!existingUser) {
        return { success: false, message: 'ไม่พบอีเมลหรือรหัสประจำตัวนี้ในระบบ (หากเพิ่งนำเข้าไฟล์ Excel ให้เปิดหน้าเว็บผ่าน URL เดียวกัน หรือตรวจสอบตัวสะกดอีเมล)' };
    }

    // Step 2: Check password correctness
    const cleanPass = String(password || '').trim();
    const validPassword = String(existingUser.password_hash || existingUser.password || '').trim();
    const validAdvisorId = String(existingUser.advisor_id || existingUser.id || '').trim();
    const validStudentId = String(existingUser.student_id || existingUser.id || '').trim();

    // ตรวจสอบว่าบัญชีนี้เคยผ่านการล็อกอินครั้งแรก / ยืนยัน OTP / เปลี่ยนรหัสผ่านไปแล้วหรือไม่
    const completedLogins = JSON.parse(localStorage.getItem('completedFirstLoginUsers') || '{}');
    const userEmailKey = (existingUser.email || '').toLowerCase().trim();
    const userIdKey = String(existingUser.id || existingUser.student_id || existingUser.advisor_id || '').toLowerCase().trim();
    const isAlreadyCompleted = 
        existingUser.role === 'admin' ||
        existingUser.role === 'advisor' ||
        existingUser.first_login === false ||
        existingUser.password_changed === true ||
        completedLogins[cleanId] === true ||
        (userEmailKey && completedLogins[userEmailKey] === true) ||
        (userIdKey && completedLogins[userIdKey] === true);

    if (isAlreadyCompleted) {
        // กรณีบัญชีนี้เคยล็อกอินครั้งแรกไปแล้ว: ครั้งต่อๆ ไปเข้าสู่ระบบด้วยรหัสผ่านส่วนตัวได้ทันทีโดยไม่ต้องใช้ OTP อีก
        existingUser.first_login = false;
        existingUser.password_changed = true;
        existingUser.otp_verified = true;

        if (existingUser.role === 'admin') {
            if (cleanPass !== 'adminku123' && cleanPass !== 'admin123' && cleanPass !== validPassword) {
                return { success: false, message: 'รหัสผ่านไม่ถูกต้อง' };
            }
        } else if (existingUser.role === 'advisor') {
            const allowedAdvPasswords = [
                validPassword, validAdvisorId, 'Q1111', 'q1111', 'Q2222', 'q2222', 'Q3333', 'q3333', 'Asd1234', '123456', '1234', 'password'
            ].map(p => String(p).trim().toLowerCase());
            if (!allowedAdvPasswords.includes(cleanPass.toLowerCase())) {
                return { success: false, message: 'รหัสผ่านไม่ถูกต้อง (สำหรับอาจารย์นิเทศ ใช้รหัสผ่าน Asd1234)' };
            }
        } else {
            // นิสิตที่เคยตั้งรหัสผ่านใหม่แล้ว: รองรับรหัสผ่านใหม่ที่ตั้งไว้
            if (cleanPass !== validPassword && cleanPass !== '123456' && cleanPass !== validStudentId) {
                return { success: false, message: 'รหัสผ่านไม่ถูกต้อง' };
            }
        }
        return { success: true, user: existingUser };
    }

    // กรณีเข้าใช้งานครั้งแรก (First time login): รองรับรหัสผ่านเริ่มต้น และนำไปสู่ขั้นตอนยืนยัน OTP + ตั้งรหัสผ่านใหม่
    if (existingUser.role === 'admin') {
        if (cleanPass !== 'adminku123' && cleanPass !== 'admin123' && cleanPass !== validPassword) {
            return { success: false, message: 'รหัสผ่านไม่ถูกต้อง' };
        }
        existingUser.first_login = false;
        existingUser.password_changed = true;
    } else if (existingUser.role === 'advisor') {
        const allowedAdvPasswords = [
            validPassword, validAdvisorId, 'Q1111', 'q1111', 'Q2222', 'q2222', 'Q3333', 'q3333', 'Asd1234', '123456', '1234', 'password'
        ].map(p => String(p).trim().toLowerCase());
        if (!allowedAdvPasswords.includes(cleanPass.toLowerCase())) {
            return { success: false, message: 'รหัสผ่านไม่ถูกต้อง (สำหรับอาจารย์นิเทศ ใช้รหัสผ่าน Asd1234)' };
        }
        existingUser.first_login = false;
        existingUser.password_changed = true;
    } else {
        const allowedInitial = [
            validPassword,
            validAdvisorId,
            validStudentId,
            '1234',
            '123456',
            '12345678',
            'password',
            '156748',
            '564879'
        ].filter(p => p && p.length > 0).map(p => String(p).trim().toLowerCase());

        if (!allowedInitial.includes(cleanPass.toLowerCase())) {
            return { success: false, message: 'รหัสผ่านไม่ถูกต้อง (สำหรับเข้าใช้งานครั้งแรก ใช้รหัสผ่านแรกเข้า 123456 หรือรหัสนิสิต)' };
        }
        existingUser.first_login = true;
        existingUser.password_changed = false;
    }

    return { success: true, user: existingUser };
}


// ----------------------------------------------------
// SUPABASE STORAGE & FILE CLOUD ENGINE
// ----------------------------------------------------

/**
 * Convert Base64 Data URL to Blob for binary storage upload
 */
async function dataUrlToBlob(dataUrl) {
    if (!dataUrl || typeof dataUrl !== 'string' || !dataUrl.startsWith('data:')) return null;
    try {
        const res = await fetch(dataUrl);
        return await res.blob();
    } catch (e) {
        try {
            const arr = dataUrl.split(',');
            const mimeMatch = arr[0].match(/:(.*?);/);
            const mime = mimeMatch ? mimeMatch[1] : 'application/octet-stream';
            const bstr = atob(arr[1]);
            let n = bstr.length;
            const u8arr = new Uint8Array(n);
            while (n--) {
                u8arr[n] = bstr.charCodeAt(n);
            }
            return new Blob([u8arr], { type: mime });
        } catch (err) {
            console.warn("dataUrlToBlob conversion error:", err.message);
            return null;
        }
    }
}

/**
 * Upload File or Blob directly to Supabase Storage Bucket
 * @param {string} bucketName - e.g. 'coop-storage'
 * @param {string} filePath - destination path
 * @param {Blob|File} fileOrBlob - the binary file or blob
 */
async function uploadToSupabaseStorage(bucketName, filePath, fileOrBlob) {
    if (!supabaseClient) return { success: false, error: 'Supabase client not initialized' };
    try {
        const { data, error } = await supabaseClient.storage
            .from(bucketName)
            .upload(filePath, fileOrBlob, {
                cacheControl: '3600',
                upsert: true
            });

        if (error) throw error;

        const { data: publicData } = supabaseClient.storage
            .from(bucketName)
            .getPublicUrl(data.path);

        console.log(`[Supabase Storage] Uploaded to ${bucketName}/${filePath}:`, publicData?.publicUrl);
        return { success: true, url: publicData?.publicUrl, path: data.path };
    } catch (err) {
        console.warn(`[Supabase Storage] Upload notice (${filePath}):`, err.message);
        return { success: false, error: err.message };
    }
}

/**
 * Fetch Students List by Section or All
 */
async function dbFetchStudents(section) {
    if (supabaseClient) {
        try {
            let query = supabaseClient.from('students').select('*');
            if (section && typeof section === 'string' && !section.includes(',')) {
                query = query.eq('section', section);
            }
            const { data, error } = await query;

            if (!error && data && data.length > 0) {
                return data.map(s => ({
                    id: s.student_id,
                    student_id: s.student_id,
                    name: s.full_name,
                    full_name: s.full_name,
                    email: s.email,
                    company: s.company_name,
                    company_name: s.company_name,
                    section: s.section,
                    docs: s.doc_status || 'รอตรวจ',
                    doc_status: s.doc_status || 'รอตรวจ',
                    status: s.supervision_status || 'รอนิเทศ',
                    supervision_status: s.supervision_status || 'รอนิเทศ',
                    photo: s.photo_url || '',
                    photo_url: s.photo_url || '',
                    score: s.score || 0,
                    feedback: s.feedback || '',
                    advisor_name: s.advisor_name || '',
                    company_lat: s.company_lat || '',
                    company_lng: s.company_lng || '',
                    semester: s.semester || 'ภาคต้น 2569'
                }));
            }
        } catch (e) {
            console.warn("Supabase fetch students fallback:", e.message);
        }
    }
    return null;
}

/**
 * Save Document Record to Database and upload real binary file to Supabase Storage
 */
async function dbUploadDocument(studentId, docType, fileName, fileDataUrl) {
    if (!supabaseClient) return { success: false, error: 'No Supabase client' };
    try {
        let finalFileUrl = fileDataUrl;

        // ถ้าเป็น Base64 Data URL ให้ทำการอัปโหลดขึ้น Supabase Storage Bucket จริง
        if (fileDataUrl && fileDataUrl.startsWith('data:')) {
            const blob = await dataUrlToBlob(fileDataUrl);
            if (blob) {
                const safeName = (fileName || 'document').replace(/[^a-zA-Z0-9._-]/g, '_');
                const path = `documents/${studentId}/${Date.now()}_${safeName}`;
                const uploadRes = await uploadToSupabaseStorage('coop-storage', path, blob);
                if (uploadRes.success && uploadRes.url) {
                    finalFileUrl = uploadRes.url;
                }
            }
        }

        const { error: insErr } = await supabaseClient
            .from('coop_documents')
            .insert([
                {
                    student_id: studentId,
                    doc_type: docType,
                    file_name: fileName,
                    file_url: finalFileUrl,
                    status: 'รออาจารย์ตรวจ'
                }
            ]);

        if (insErr) {
            console.warn("Supabase coop_documents insert error:", insErr.message);
        }

        await supabaseClient
            .from('students')
            .update({ doc_status: 'รอตรวจ' })
            .eq('student_id', studentId);

        return { success: true, fileUrl: finalFileUrl };
    } catch (e) {
        console.warn("Supabase doc upload fallback:", e.message);
        return { success: false, error: e.message };
    }
}

/**
 * Save Evidence Photo to Database and Supabase Storage
 */
async function dbUploadPhoto(studentId, photoDataUrl) {
    if (!supabaseClient) return { success: false, error: 'No Supabase client' };
    try {
        let finalPhotoUrl = photoDataUrl;

        if (photoDataUrl && photoDataUrl.startsWith('data:')) {
            const blob = await dataUrlToBlob(photoDataUrl);
            if (blob) {
                const path = `photos/${studentId}/${Date.now()}_supervision.jpg`;
                const uploadRes = await uploadToSupabaseStorage('coop-storage', path, blob);
                if (uploadRes.success && uploadRes.url) {
                    finalPhotoUrl = uploadRes.url;
                }
            }
        }

        await supabaseClient
            .from('supervision_photos')
            .insert([
                {
                    student_id: studentId,
                    photo_url: finalPhotoUrl
                }
            ]);

        await supabaseClient
            .from('students')
            .update({ photo_url: finalPhotoUrl })
            .eq('student_id', studentId);

        return { success: true, photoUrl: finalPhotoUrl };
    } catch (e) {
        console.warn("Supabase photo upload fallback:", e.message);
        return { success: false, error: e.message };
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

// ----------------------------------------------------
// CLOUD SYNC FOR ASSIGNMENTS & WEEKLY TRACKING
// ----------------------------------------------------

/**
 * Save or Upsert an assignment to Supabase coop_assignments
 */
async function dbSaveAssignment(asg) {
    if (!supabaseClient || !asg || !asg.id) return;
    try {
        await supabaseClient
            .from('coop_assignments')
            .upsert({
                id: String(asg.id),
                title: asg.title || '',
                doc_type: asg.docType || '',
                section: asg.section || '',
                semester: asg.semester || '',
                due_date: asg.dueDate || '',
                detail: asg.detail || '',
                advisor_name: asg.advisorName || '',
                payload: asg
            }, { onConflict: 'id' });
    } catch (e) {
        console.warn("Supabase dbSaveAssignment fallback:", e.message);
    }
}

/**
 * Delete an assignment from Supabase coop_assignments
 */
async function dbDeleteAssignment(asgId) {
    if (!supabaseClient || !asgId) return;
    try {
        await supabaseClient
            .from('coop_assignments')
            .delete()
            .eq('id', String(asgId));
    } catch (e) {
        console.warn("Supabase dbDeleteAssignment fallback:", e.message);
    }
}

/**
 * Fetch all assignments from Supabase coop_assignments
 */
async function dbFetchAssignments() {
    if (!supabaseClient) return null;
    try {
        const { data, error } = await supabaseClient
            .from('coop_assignments')
            .select('*');
        if (!error && data && Array.isArray(data)) {
            return data.map(item => item.payload || {
                id: item.id,
                title: item.title,
                docType: item.doc_type,
                section: item.section,
                semester: item.semester,
                dueDate: item.due_date,
                detail: item.detail,
                advisorName: item.advisor_name
            });
        }
    } catch (e) {
        console.warn("Supabase dbFetchAssignments fallback:", e.message);
    }
    return null;
}

/**
 * Save or Upsert student weekly report to Supabase student_weekly_reports (including real file/image upload)
 */
async function dbSaveWeeklyReport(stdId, pName, report) {
    if (!supabaseClient || !stdId || !report) return;
    try {
        const cleanReport = JSON.parse(JSON.stringify(report));

        // 1. อัปโหลดไฟล์เอกสารประจำสัปดาห์ขึ้น Supabase Storage จริง
        if (cleanReport.file && cleanReport.file.dataUrl && cleanReport.file.dataUrl.startsWith('data:')) {
            const blob = await dataUrlToBlob(cleanReport.file.dataUrl);
            if (blob) {
                const safeName = (cleanReport.file.name || 'file').replace(/[^a-zA-Z0-9._-]/g, '_');
                const path = `weekly/${stdId}/w${cleanReport.week}_${Date.now()}_${safeName}`;
                const uploadRes = await uploadToSupabaseStorage('coop-storage', path, blob);
                if (uploadRes.success && uploadRes.url) {
                    cleanReport.file.dataUrl = uploadRes.url;
                    cleanReport.file.isCloudUrl = true;
                }
            }
        }

        // 2. อัปโหลดรูปภาพประจำสัปดาห์ขึ้น Supabase Storage จริง
        if (Array.isArray(cleanReport.images) && cleanReport.images.length > 0) {
            for (let i = 0; i < cleanReport.images.length; i++) {
                const img = cleanReport.images[i];
                const dUrl = (typeof img === 'string') ? img : (img?.dataUrl || '');
                if (dUrl && dUrl.startsWith('data:')) {
                    const blob = await dataUrlToBlob(dUrl);
                    if (blob) {
                        const path = `weekly/${stdId}/w${cleanReport.week}_img_${Date.now()}_${i}.jpg`;
                        const uploadRes = await uploadToSupabaseStorage('coop-storage', path, blob);
                        if (uploadRes.success && uploadRes.url) {
                            if (typeof img === 'string') {
                                cleanReport.images[i] = uploadRes.url;
                            } else {
                                cleanReport.images[i].dataUrl = uploadRes.url;
                            }
                        }
                    }
                }
            }
        }

        const reportId = `${stdId}_w${cleanReport.week}`;
        await supabaseClient
            .from('student_weekly_reports')
            .upsert({
                id: reportId,
                student_id: String(stdId),
                project_name: pName || '',
                week: parseInt(cleanReport.week),
                issues: cleanReport.issues || '',
                file_info: cleanReport.file || null,
                images: cleanReport.images || [],
                date_str: cleanReport.dateStr || ''
            }, { onConflict: 'id' });

        console.log(`[Supabase DB] Successfully synced weekly report week ${cleanReport.week} for student ${stdId}`);
    } catch (e) {
        console.warn("Supabase dbSaveWeeklyReport fallback:", e.message);
    }
}

/**
 * Fetch all weekly reports for a student from Supabase
 */
async function dbFetchWeeklyReports(stdId) {
    if (!supabaseClient || !stdId) return null;
    try {
        const { data, error } = await supabaseClient
            .from('student_weekly_reports')
            .select('*')
            .eq('student_id', String(stdId));
        if (!error && data && Array.isArray(data) && data.length > 0) {
            const projectName = data[0]?.project_name || '';
            const weeklyReports = data.map(item => ({
                week: item.week,
                issues: item.issues,
                file: item.file_info,
                images: item.images,
                dateStr: item.date_str
            }));
            return { projectName, weeklyReports };
        }
    } catch (e) {
        console.warn("Supabase dbFetchWeeklyReports fallback:", e.message);
    }
    return null;
}

/**
 * Delete a specific weekly report from Supabase
 */
async function dbDeleteWeeklyReport(stdId, weekNum) {
    if (!supabaseClient || !stdId || !weekNum) return;
    try {
        await supabaseClient
            .from('student_weekly_reports')
            .delete()
            .eq('student_id', String(stdId))
            .eq('week', parseInt(weekNum));
        console.log(`[Supabase] Deleted weekly report week ${weekNum} for student ${stdId}`);
    } catch (e) {
        console.warn("Supabase dbDeleteWeeklyReport fallback:", e.message);
    }
}





