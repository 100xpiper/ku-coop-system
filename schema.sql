-- ========================================================
-- DATABASE SCHEMA FOR COOPERATIVE EDUCATION SUPERVISION SYSTEM
-- Database System: PostgreSQL / Supabase
-- Target System: KU Cooperative Education System (01418499)
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
    first_login BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. ADVISORS TABLE
CREATE TABLE IF NOT EXISTS public.advisors (
    advisor_id VARCHAR(50) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL REFERENCES public.users(email) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    section VARCHAR(100) NOT NULL,
    department VARCHAR(255) DEFAULT 'ภาควิชาวิทยาการคอมพิวเตอร์',
    faculty VARCHAR(255) DEFAULT 'คณะวิทยาศาสตร์',
    responsible_sections JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. STUDENTS TABLE
CREATE TABLE IF NOT EXISTS public.students (
    student_id VARCHAR(50) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL REFERENCES public.users(email) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    section VARCHAR(100) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    advisor_id VARCHAR(50) REFERENCES public.advisors(advisor_id) ON DELETE SET NULL,
    advisor_name VARCHAR(255),
    company_lat VARCHAR(50) DEFAULT '14.076949',
    company_lng VARCHAR(50) DEFAULT '100.601563',
    semester VARCHAR(100) DEFAULT 'ภาคต้น 2569',
    doc_status VARCHAR(50) DEFAULT 'รอตรวจ',
    supervision_status VARCHAR(50) DEFAULT 'รอนิเทศ',
    score INT DEFAULT 0,
    feedback TEXT DEFAULT '',
    photo_url TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. COOP ASSIGNMENTS TABLE (งานที่อาจารย์สั่ง / มอบหมายงานสหกิจศึกษา)
CREATE TABLE IF NOT EXISTS public.coop_assignments (
    id VARCHAR(100) PRIMARY KEY,
    title TEXT NOT NULL,
    doc_type TEXT,
    section TEXT,
    semester TEXT,
    due_date TEXT,
    detail TEXT,
    advisor_name TEXT,
    payload JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. STUDENT WEEKLY REPORTS TABLE (รายงานการติดตามงานประจำสัปดาห์ 16 สัปดาห์)
CREATE TABLE IF NOT EXISTS public.student_weekly_reports (
    id VARCHAR(100) PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    project_name TEXT,
    week INT NOT NULL,
    issues TEXT,
    file_info JSONB,
    images JSONB,
    date_str TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. COOP DOCUMENTS TABLE (เอกสารการส่งงานของนิสิต)
CREATE TABLE IF NOT EXISTS public.coop_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id VARCHAR(50) NOT NULL,
    doc_type VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'รออาจารย์ตรวจ',
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. SUPERVISION EVIDENCE PHOTOS TABLE (รูปภาพหลักฐานการนิเทศงาน)
CREATE TABLE IF NOT EXISTS public.supervision_photos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id VARCHAR(50) NOT NULL,
    photo_url TEXT NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 8. APPOINTMENTS TABLE (ปฏิทินนัดหมายการนิเทศ)
CREATE TABLE IF NOT EXISTS public.appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    advisor_id VARCHAR(50) NOT NULL,
    student_id VARCHAR(50) NOT NULL,
    appt_date VARCHAR(100) NOT NULL,
    appt_time VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'นัดหมายสำเร็จ',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 9. IN-APP NOTIFICATIONS TABLE (การแจ้งเตือนในระบบ)
CREATE TABLE IF NOT EXISTS public.notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ========================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ปลดล็อก RLS เพื่อให้เว็บแอปพลิเคชัน (anon key) อ่านและเขียนข้อมูลได้
-- ========================================================
ALTER TABLE IF EXISTS public.users DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.students DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.advisors DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.coop_documents DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.supervision_photos DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.appointments DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.coop_assignments DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.student_weekly_reports DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.notifications DISABLE ROW LEVEL SECURITY;

-- ========================================================
-- INITIAL SEED DATA FOR TESTING
-- ========================================================

-- Insert Initial Users
INSERT INTO public.users (email, password_hash, full_name, role, status, first_login) VALUES
('adminku@ku.th', 'adminku123', 'ผู้ดูแลระบบ (Admin)', 'admin', 'approved', false),
('somchai.j@ku.th', 'Asd1234', 'อาจารย์ สมชาย แจ่มใส', 'advisor', 'approved', false),
('somying.ch@ku.th', 'Asd1234', 'อาจารย์ สมหญิง จงจิต', 'advisor', 'approved', false),
('somjit.m@ku.th', 'Asd1234', 'อาจารย์ สมจิต มั่งมี', 'advisor', 'approved', false),
('wongsapat.u@ku.th', '123456', 'นาย วงศพัทธ์ อุเทน', 'student', 'approved', true)
ON CONFLICT (email) DO UPDATE SET 
    full_name = EXCLUDED.full_name,
    role = EXCLUDED.role,
    status = EXCLUDED.status;

-- Insert Initial Advisors
INSERT INTO public.advisors (advisor_id, email, full_name, section, responsible_sections) VALUES
('Q1111', 'somchai.j@ku.th', 'อาจารย์ สมชาย แจ่มใส', 'หมู่ 700, หมู่ 800', '["700", "800"]'::jsonb),
('Q2222', 'somying.ch@ku.th', 'อาจารย์ สมหญิง จงจิต', 'หมู่ 701, หมู่ 801', '["701", "801"]'::jsonb),
('Q3333', 'somjit.m@ku.th', 'อาจารย์ สมจิต มั่งมี', 'หมู่ 702, หมู่ 802', '["702", "802"]'::jsonb)
ON CONFLICT (advisor_id) DO UPDATE SET
    full_name = EXCLUDED.full_name,
    section = EXCLUDED.section,
    responsible_sections = EXCLUDED.responsible_sections;

-- Insert Initial Student (wongsapat.u)
INSERT INTO public.students (student_id, email, full_name, section, company_name, advisor_id, advisor_name, semester, doc_status, supervision_status, company_lat, company_lng) VALUES
('6521655442', 'wongsapat.u@ku.th', 'นาย วงศพัทธ์ อุเทน', 'หมู่ 800 (ภาคพิเศษ)', 'สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.)', 'Q1111', 'อาจารย์ สมชาย แจ่มใส', 'ภาคต้น 2569', 'ครบถ้วน', 'รอนิเทศ', '14.076949', '100.601563')
ON CONFLICT (student_id) DO UPDATE SET
    full_name = EXCLUDED.full_name,
    section = EXCLUDED.section,
    company_name = EXCLUDED.company_name,
    advisor_id = EXCLUDED.advisor_id,
    advisor_name = EXCLUDED.advisor_name,
    company_lat = EXCLUDED.company_lat,
    company_lng = EXCLUDED.company_lng;
