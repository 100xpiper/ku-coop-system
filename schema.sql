-- ========================================================
-- DATABASE SCHEMA FOR COOPERATIVE EDUCATION SUPERVISION SYSTEM
-- Database System: PostgreSQL / Supabase
-- Target System: KU Cooperative Education System
-- ========================================================

-- Enable UUID Extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. USERS & AUTH WHITELIST TABLE
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('advisor', 'student', 'admin')),
    status VARCHAR(50) DEFAULT 'approved' CHECK (status IN ('pending', 'approved', 'rejected')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. ADVISORS TABLE
CREATE TABLE IF NOT EXISTS public.advisors (
    advisor_id VARCHAR(50) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL REFERENCES public.users(email) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    section VARCHAR(100) NOT NULL,
    department VARCHAR(255) DEFAULT 'ภาควิชาวิทยาการคอมพิวเตอร์',
    faculty VARCHAR(255) DEFAULT 'คณะวิทยาศาสตร์'
);

-- 3. STUDENTS TABLE
CREATE TABLE IF NOT EXISTS public.students (
    student_id VARCHAR(50) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL REFERENCES public.users(email) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    section VARCHAR(100) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    advisor_id VARCHAR(50) REFERENCES public.advisors(advisor_id) ON DELETE SET NULL,
    doc_status VARCHAR(50) DEFAULT 'รอตรวจ',
    supervision_status VARCHAR(50) DEFAULT 'รอนิเทศ',
    score INT DEFAULT 0,
    feedback TEXT DEFAULT '',
    photo_url TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. COOP DOCUMENTS TABLE
CREATE TABLE IF NOT EXISTS public.coop_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id VARCHAR(50) NOT NULL REFERENCES public.students(student_id) ON DELETE CASCADE,
    doc_type VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'รออาจารย์ตรวจ',
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. SUPERVISION EVIDENCE PHOTOS TABLE
CREATE TABLE IF NOT EXISTS public.supervision_photos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id VARCHAR(50) NOT NULL REFERENCES public.students(student_id) ON DELETE CASCADE,
    photo_url TEXT NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. APPOINTMENTS TABLE
CREATE TABLE IF NOT EXISTS public.appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    advisor_id VARCHAR(50) NOT NULL REFERENCES public.advisors(advisor_id) ON DELETE CASCADE,
    student_id VARCHAR(50) NOT NULL REFERENCES public.students(student_id) ON DELETE CASCADE,
    appt_date VARCHAR(100) NOT NULL,
    appt_time VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'นัดหมายสำเร็จ',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. IN-APP NOTIFICATIONS TABLE
CREATE TABLE IF NOT EXISTS public.notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ========================================================
-- INITIAL SEED DATA FOR TESTING
-- ========================================================

-- Insert Initial Users
INSERT INTO public.users (email, password_hash, full_name, role) VALUES
('wongsapat.u@ku.th', '1234', 'นายวงศพัทธ์ อุเทน', 'advisor'),
('poravee.w@ku.th', '1234', 'นายปรวี วงศ์สวัสดิ์สุริยะ', 'advisor'),
('somsak.r@ku.th', '1234', 'นายสมศักดิ์ รักดี', 'student'),
('taweesak.c@ku.th', '1234', 'นายทวีศักดิ์ ชัยชนะ', 'student'),
('adminku@ku.th', 'admin123', 'ผู้ดูแลระบบ (Admin)', 'admin')
ON CONFLICT (email) DO NOTHING;

-- Insert Initial Advisors
INSERT INTO public.advisors (advisor_id, email, full_name, section) VALUES
('1234', 'wongsapat.u@ku.th', 'นายวงศพัทธ์ อุเทน', 'หมู่ 700'),
('1235', 'poravee.w@ku.th', 'นายปรวี วงศ์สวัสดิ์สุริยะ', 'หมู่ 800')
ON CONFLICT (advisor_id) DO NOTHING;

-- Insert Initial Students
INSERT INTO public.students (student_id, email, full_name, section, company_name, advisor_id, doc_status, supervision_status, score, feedback) VALUES
('64010101', 'somsak.r@ku.th', 'นายสมศักดิ์ รักดี', 'หมู่ 700', 'บริษัท เมต้า โซลูชั่นส์ จำกัด', '1234', 'ครบถ้วน', 'นิเทศแล้ว', 95, 'นิสิตมีความตั้งใจสูง ปรับตัวกับทีมงานได้ดีเยี่ยม'),
('64010103', 'taweesak.c@ku.th', 'นายทวีศักดิ์ ชัยชนะ', 'หมู่ 700', 'บริษัท เทคซอส มีเดีย จำกัด', '1234', 'รอตรวจ', 'รอนิเทศ', 0, '')
ON CONFLICT (student_id) DO NOTHING;
