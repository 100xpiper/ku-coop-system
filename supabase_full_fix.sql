-- ==============================================================================
-- สคริปต์ปรับปรุงฐานข้อมูล Supabase ให้พร้อมใช้งานจริง 100% (Production Ready)
-- โครงงาน: KU Cooperative Education Supervision System
-- วิธีใช้: คัดลอกโค้ดทั้งหมดนี้ไปวางใน Supabase Dashboard -> SQL Editor แล้วกด "Run"
-- ==============================================================================

-- 1. เพิ่มคอลัมน์ที่ขาดหายไปในตารางเดิม
ALTER TABLE IF EXISTS public.users ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'approved';
ALTER TABLE IF EXISTS public.users ADD COLUMN IF NOT EXISTS first_login BOOLEAN DEFAULT TRUE;

ALTER TABLE IF EXISTS public.students ADD COLUMN IF NOT EXISTS advisor_name VARCHAR(255);
ALTER TABLE IF EXISTS public.students ADD COLUMN IF NOT EXISTS company_lat VARCHAR(50);
ALTER TABLE IF EXISTS public.students ADD COLUMN IF NOT EXISTS company_lng VARCHAR(50);
ALTER TABLE IF EXISTS public.students ADD COLUMN IF NOT EXISTS semester VARCHAR(100) DEFAULT 'ภาคต้น 2569';
ALTER TABLE IF EXISTS public.students ADD COLUMN IF NOT EXISTS photo_url TEXT DEFAULT '';
ALTER TABLE IF EXISTS public.students ADD COLUMN IF NOT EXISTS score INT DEFAULT 0;
ALTER TABLE IF EXISTS public.students ADD COLUMN IF NOT EXISTS feedback TEXT DEFAULT '';

ALTER TABLE IF EXISTS public.advisors ADD COLUMN IF NOT EXISTS responsible_sections JSONB DEFAULT '[]'::jsonb;

-- 2. สร้างตารางใหม่ที่ยังขาดอยู่
-- 2.1 ตารางสั่งงาน / มอบหมายงานสหกิจศึกษา
CREATE TABLE IF NOT EXISTS public.coop_assignments (
    id VARCHAR(100) PRIMARY KEY,
    title TEXT,
    doc_type TEXT,
    section TEXT,
    semester TEXT,
    due_date TEXT,
    detail TEXT,
    advisor_name TEXT,
    payload JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2.2 ตารางบันทึกการติดตามงานประจำสัปดาห์ (16 สัปดาห์)
CREATE TABLE IF NOT EXISTS public.student_weekly_reports (
    id VARCHAR(100) PRIMARY KEY,
    student_id VARCHAR(50),
    project_name TEXT,
    week INT,
    issues TEXT,
    file_info JSONB,
    images JSONB,
    date_str TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. ปลดล็อก RLS (Row Level Security) เพื่อให้หน้าเว็บ (anon key) อ่าน-เขียนข้อมูลได้
ALTER TABLE IF EXISTS public.users DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.students DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.advisors DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.coop_documents DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.supervision_photos DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.appointments DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.coop_assignments DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.student_weekly_reports DISABLE ROW LEVEL SECURITY;

-- 4. สร้าง Storage Bucket สำหรับจัดเก็บไฟล์เอกสารและรูปภาพ
INSERT INTO storage.buckets (id, name, public)
VALUES ('coop-storage', 'coop-storage', true)
ON CONFLICT (id) DO UPDATE SET public = true;

-- 5. กำหนดสิทธิ์ให้ผู้ใช้งานอัปโหลดและดาวน์โหลดไฟล์ใน Storage Bucket ได้
DROP POLICY IF EXISTS "Public coop-storage Select" ON storage.objects;
CREATE POLICY "Public coop-storage Select" ON storage.objects FOR SELECT USING (bucket_id = 'coop-storage');

DROP POLICY IF EXISTS "Public coop-storage Insert" ON storage.objects;
CREATE POLICY "Public coop-storage Insert" ON storage.objects FOR INSERT WITH CHECK (bucket_id = 'coop-storage');

DROP POLICY IF EXISTS "Public coop-storage Update" ON storage.objects;
CREATE POLICY "Public coop-storage Update" ON storage.objects FOR UPDATE USING (bucket_id = 'coop-storage');

DROP POLICY IF EXISTS "Public coop-storage Delete" ON storage.objects;
CREATE POLICY "Public coop-storage Delete" ON storage.objects FOR DELETE USING (bucket_id = 'coop-storage');

-- 6. นำเข้าบัญชีเริ่มต้นของระบบ (หากยังไม่มีในระบบ)
INSERT INTO public.users (email, password_hash, full_name, role, status, first_login) VALUES
('adminku@ku.th', 'adminku123', 'ผู้ดูแลระบบ (Admin)', 'admin', 'approved', false),
('somchai.j@ku.th', 'Asd1234', 'อาจารย์ สมชาย แจ่มใส', 'advisor', 'approved', false),
('somying.ch@ku.th', 'Asd1234', 'อาจารย์ สมหญิง จงจิต', 'advisor', 'approved', false),
('somjit.m@ku.th', 'Asd1234', 'อาจารย์ สมจิต มั่งมี', 'advisor', 'approved', false),
('wongsapat.u@ku.th', '123456', 'นาย วงศพัทธ์ อุเทน', 'student', 'approved', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO public.advisors (advisor_id, email, full_name, section, department, faculty, responsible_sections) VALUES
('Q1111', 'somchai.j@ku.th', 'อาจารย์ สมชาย แจ่มใส', 'หมู่ 700, 800', 'ภาควิชาวิทยาการคอมพิวเตอร์', 'คณะวิทยาศาสตร์', '["700", "800"]'::jsonb),
('Q2222', 'somying.ch@ku.th', 'อาจารย์ สมหญิง จงจิต', 'หมู่ 701, 801', 'ภาควิชาวิทยาการคอมพิวเตอร์', 'คณะวิทยาศาสตร์', '["701", "801"]'::jsonb),
('Q3333', 'somjit.m@ku.th', 'อาจารย์ สมจิต มั่งมี', 'หมู่ 702, 802', 'ภาควิชาวิทยาการคอมพิวเตอร์', 'คณะวิทยาศาสตร์', '["702", "802"]'::jsonb)
ON CONFLICT (advisor_id) DO NOTHING;

INSERT INTO public.students (student_id, email, full_name, section, company_name, advisor_name, semester, doc_status, supervision_status, company_lat, company_lng) VALUES
('6521655442', 'wongsapat.u@ku.th', 'นาย วงศพัทธ์ อุเทน', 'หมู่ 800 (ภาคพิเศษ)', 'สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.)', 'อาจารย์ สมชาย แจ่มใส', 'ภาคต้น 2569', 'รอตรวจ', 'รอนิเทศ', '14.078440', '100.601560')
ON CONFLICT (student_id) DO NOTHING;
