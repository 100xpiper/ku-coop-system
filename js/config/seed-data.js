// ==========================================================================
// seed-data.js - ฐานข้อมูลจำลองและฟังก์ชันเริ่มต้นข้อมูลผู้ใช้งาน (Seed Data)
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

function getSeedSystemData() {
    return {
        advisors: [
            {
                id: 'Q2222',
                advisor_id: 'Q2222',
                name: 'อาจารย์ สมหญิง จงจิต',
                email: 'somying.ch@ku.th',
                password: 'Asd1234',
                password_hash: 'Asd1234',
                first_login: false,
                role: 'advisor',
                section: 'หมู่ 701, หมู่ 801'
            },
            {
                id: 'Q3333',
                advisor_id: 'Q3333',
                name: 'อาจารย์ สมจิต มั่งมี',
                email: 'somjit.m@ku.th',
                password: 'Asd1234',
                password_hash: 'Asd1234',
                first_login: false,
                role: 'advisor',
                section: 'หมู่ 702, หมู่ 802'
            }
        ],
        students: [
            // 10 นิสิตในความดูแลของ อาจารย์ สมชาย แจ่มใส (5 หมู่ 700, 5 หมู่ 800)
            { id: '6521650101', student_id: '6521650101', name: 'นาย กิตติศักดิ์ พลอยประเสริฐ', email: 'kittisak.plo@ku.th', role: 'student', section: 'หมู่ 700 (ภาคปกติ)', company_name: 'บริษัท กสท โทรคมนาคม จำกัด (มหาชน)', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', semester: 'ภาคต้น 2569' },
            { id: '6521650102', student_id: '6521650102', name: 'นางสาว ชลธิชา พงษ์ศิริ', email: 'chonthicha.po@ku.th', role: 'student', section: 'หมู่ 700 (ภาคปกติ)', company_name: 'บริษัท สามารถคอร์ปอเรชั่น จำกัด (มหาชน)', advisor_name: '-', docs: 'ครบถ้วน', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521650103', student_id: '6521650103', name: 'นาย ธนวัฒน์ สุขสวัสดิ์', email: 'thanawat.suk@ku.th', role: 'student', section: 'หมู่ 700 (ภาคปกติ)', company_name: 'สำนักงานพัฒนาธุรกรรมทางอิเล็กทรอนิกส์ (ETDA)', advisor_name: '-', docs: 'รอตรวจ', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521650104', student_id: '6521650104', name: 'นางสาว ณัฐณิชา ทองใบ', email: 'natnicha.t@ku.th', role: 'student', section: 'หมู่ 700 (ภาคปกติ)', company_name: 'ธนาคารกสิกรไทย จำกัด (มหาชน)', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', semester: 'ภาคต้น 2569' },
            { id: '6521650105', student_id: '6521650105', name: 'นาย ปวริศร์ จันทรังสี', email: 'pawaris.j@ku.th', role: 'student', section: 'หมู่ 700 (ภาคปกติ)', company_name: 'บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน)', advisor_name: '-', docs: 'รอตรวจ', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            // หมู่ 800
            { id: '6521655443', student_id: '6521655443', name: 'นาย วรัญญู รัตนเดช', email: 'waranyoo.r@ku.th', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'บริษัท อโกด้า เซอร์วิสเซส จำกัด', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', semester: 'ภาคต้น 2569' },
            { id: '6521655444', student_id: '6521655444', name: 'นางสาว พิมลภัส ศรีมงคล', email: 'pimonpat.s@ku.th', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'บริษัท ไลน์ คอมพานี (ประเทศไทย) จำกัด', advisor_name: '-', docs: 'รอตรวจ', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521655445', student_id: '6521655445', name: 'นาย อัครพล ชื่นอารมณ์', email: 'akkarapol.c@ku.th', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'บริษัท ซีพี ออลล์ จำกัด (มหาชน)', advisor_name: '-', docs: 'ครบถ้วน', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521655446', student_id: '6521655446', name: 'นางสาว สุพรรณษา ใจดี', email: 'supansa.j@ku.th', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'ธนาคารไทยพาณิชย์ จำกัด (มหาชน) (SCB TechX)', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', semester: 'ภาคต้น 2569' },

            // 10 นิสิตในความดูแลของ อาจารย์ สมหญิง จงจิต (5 หมู่ 701, 5 หมู่ 801)
            { id: '6521650201', student_id: '6521650201', name: 'นาย ปัญญาวุฒิ เกิดผล', email: 'panyawut.k@ku.th', role: 'student', section: 'หมู่ 701 (ภาคปกติ)', company_name: 'บริษัท เบทาโกร จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', semester: 'ภาคต้น 2569' },
            { id: '6521650202', student_id: '6521650202', name: 'นางสาว กัญญาณัฐ วิทยา', email: 'kanyanat.w@ku.th', role: 'student', section: 'หมู่ 701 (ภาคปกติ)', company_name: 'บริษัท ปตท. สำรวจและผลิตปิโตรเลียม จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521650203', student_id: '6521650203', name: 'นาย ชวัลกร วงศ์ษา', email: 'chawankorn.w@ku.th', role: 'student', section: 'หมู่ 701 (ภาคปกติ)', company_name: 'การไฟฟ้าฝ่ายผลิตแห่งประเทศไทย (กฟผ.)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'รอตรวจ', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521650204', student_id: '6521650204', name: 'นางสาว ธันยพร สุริยะ', email: 'thanyaporn.s@ku.th', role: 'student', section: 'หมู่ 701 (ภาคปกติ)', company_name: 'บริษัท การบินไทย จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', semester: 'ภาคต้น 2569' },
            { id: '6521650205', student_id: '6521650205', name: 'นาย กานต์ดนัย ลิ้มประเสริฐ', email: 'karndanai.l@ku.th', role: 'student', section: 'หมู่ 701 (ภาคปกติ)', company_name: 'บริษัท เอสซีจี แพคเกจจิ้ง จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'รอตรวจ', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            // หมู่ 801
            { id: '6521655201', student_id: '6521655201', name: 'นาย กฤติน สิทธิชัย', email: 'krittin.s@ku.th', role: 'student', section: 'หมู่ 801 (ภาคพิเศษ)', company_name: 'ธนาคารกรุงไทย จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521655202', student_id: '6521655202', name: 'นางสาว นริศรา ชินวงศ์', email: 'narisara.c@ku.th', role: 'student', section: 'หมู่ 801 (ภาคพิเศษ)', company_name: 'บริษัท ช้อปปี้ (ประเทศไทย) จำกัด', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', semester: 'ภาคต้น 2569' },
            { id: '6521655203', student_id: '6521655203', name: 'นาย อภิวิชญ์ บุณยะ', email: 'apiwit.b@ku.th', role: 'student', section: 'หมู่ 801 (ภาคพิเศษ)', company_name: 'บริษัท บลูบิค กรุ๊ป จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'รอตรวจ', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521655204', student_id: '6521655204', name: 'นางสาว มณีรัตน์ มงคลศิลป์', email: 'maneerat.m@ku.th', role: 'student', section: 'หมู่ 801 (ภาคพิเศษ)', company_name: 'บริษัท แอดวานซ์ อินโฟร์ เซอร์วิส จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521655205', student_id: '6521655205', name: 'นาย พงศกร อัศวเมธี', email: 'pongsakorn.a@ku.th', role: 'student', section: 'หมู่ 801 (ภาคพิเศษ)', company_name: 'บริษัท ดับบลิวเอชเอ คอร์ปอเรชั่น จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', semester: 'ภาคต้น 2569' },

            // 10 นิสิตในความดูแลของ อาจารย์ สมจิต มั่งมี (5 หมู่ 702, 5 หมู่ 802)
            { id: '6521650301', student_id: '6521650301', name: 'นาย ธนาคาร เจริญสุข', email: 'thanakarn.c@ku.th', role: 'student', section: 'หมู่ 702 (ภาคปกติ)', company_name: 'บริษัท พีทีที ดิจิตอล โซลูชั่น จำกัด', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', semester: 'ภาคต้น 2569' },
            { id: '6521650302', student_id: '6521650302', name: 'นางสาว ภาวิณี บัวคลี่', email: 'pawinee.b@ku.th', role: 'student', section: 'หมู่ 702 (ภาคปกติ)', company_name: 'สถาบันวิจัยดาราศาสตร์แห่งชาติ (สดร.)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521650303', student_id: '6521650303', name: 'นาย รัชชานนท์ พิทักษ์', email: 'ratchanon.p@ku.th', role: 'student', section: 'หมู่ 702 (ภาคปกติ)', company_name: 'บริษัท จัสท์โค (ประเทศไทย) จำกัด', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'รอตรวจ', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521650304', student_id: '6521650304', name: 'นางสาว ชญานิศา รัตนโกสีย์', email: 'chayanisa.r@ku.th', role: 'student', section: 'หมู่ 702 (ภาคปกติ)', company_name: 'สถาบันวิจัยวิทยาศาสตร์และเทคโนโลยีแห่งประเทศไทย (วว.)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', semester: 'ภาคต้น 2569' },
            { id: '6521650305', student_id: '6521650305', name: 'นาย นพดล อินทรทัศน์', email: 'nopadol.i@ku.th', role: 'student', section: 'หมู่ 702 (ภาคปกติ)', company_name: 'สำนักงานนวัตกรรมแห่งชาติ (สนช.)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'รอตรวจ', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            // หมู่ 802
            { id: '6521655301', student_id: '6521655301', name: 'นาย ชยพล รัตนไพศาล', email: 'chayapol.r@ku.th', role: 'student', section: 'หมู่ 802 (ภาคพิเศษ)', company_name: 'บริษัท เกร็บ (ประเทศไทย) จำกัด', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521655302', student_id: '6521655302', name: 'นางสาว ศุภานัน ธนะสมบูรณ์', email: 'supanan.t@ku.th', role: 'student', section: 'หมู่ 802 (ภาคพิเศษ)', company_name: 'บริษัท ดิจิทัล เวนเจอร์ส จำกัด', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', semester: 'ภาคต้น 2569' },
            { id: '6521655303', student_id: '6521655303', name: 'นาย สุรเชษฐ์ เด่นดวง', email: 'surachet.d@ku.th', role: 'student', section: 'หมู่ 802 (ภาคพิเศษ)', company_name: 'บริษัท บีทีเอส กรุ๊ป โฮลดิ้งส์ จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'รอตรวจ', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521655304', student_id: '6521655304', name: 'นางสาว ณัฐริกา กองแก้ว', email: 'nattarika.k@ku.th', role: 'student', section: 'หมู่ 802 (ภาคพิเศษ)', company_name: 'ตลาดหลักทรัพย์แห่งประเทศไทย (SET)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'รอนิเทศ', semester: 'ภาคต้น 2569' },
            { id: '6521655305', student_id: '6521655305', name: 'นาย พชร ศิริวัฒน์', email: 'pachara.s@ku.th', role: 'student', section: 'หมู่ 802 (ภาคพิเศษ)', company_name: 'บริษัท กัลฟ์ เอ็นเนอร์จี ดีเวลลอปเมนท์ จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', semester: 'ภาคต้น 2569' },

            // ==========================================
            // ข้อมูลประวัติย้อนหลัง: ภาคการศึกษา 2568 (12 นิสิตรุ่นพี่)
            // ==========================================
            // ภาคปลาย 2568 (6 นิสิต - สถานะสำเร็จการฝึกงานครบถ้วน)
            { id: '6421650111', student_id: '6421650111', name: 'นาย ปริญญา เกียรติสกุล', email: 'parinya.kia@ku.th', role: 'student', section: 'หมู่ 700 (ภาคปกติ)', company_name: 'บริษัท บิตคับ ออนไลน์ จำกัด (Bitkub)', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 94, feedback: 'นิสิตมีทักษะการแก้ปัญหาดีเยี่ยม และปรับตัวเข้ากับงานได้รวดเร็ว', semester: 'ภาคปลาย 2568' },
            { id: '6421655112', student_id: '6421655112', name: 'นางสาว ณิชากานต์ พงษ์สถิตย์', email: 'nichakan.po@ku.th', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'บริษัท บลูบิค กรุ๊ป จำกัด (มหาชน)', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 91, feedback: 'มีผลงานระบบ Business Intelligence ชัดเจน สถานประกอบการชื่นชม', semester: 'ภาคปลาย 2568' },
            { id: '6421650213', student_id: '6421650213', name: 'นาย ธีรภัทร อัครเสถียร', email: 'teerapat.ak@ku.th', role: 'student', section: 'หมู่ 701 (ภาคปกติ)', company_name: 'บริษัท ทรานสฟอร์เมชั่น เทคโนโลยี จำกัด', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 89, feedback: 'ผลงานโครงงานผ่านเกณฑ์มาตรฐานในระดับดีมาก', semester: 'ภาคปลาย 2568' },
            { id: '6421655214', student_id: '6421655214', name: 'นางสาว อรนิชชา เลิศรัตนกุล', email: 'ornicha.le@ku.th', role: 'student', section: 'หมู่ 801 (ภาคพิเศษ)', company_name: 'บริษัท ไลน์ คอมพานี (ประเทศไทย) จำกัด', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 96, feedback: 'ผลงานระดับยอดเยี่ยม ได้รับข้อเสนอให้ร่วมงานต่อหลังจบการศึกษา', semester: 'ภาคปลาย 2568' },
            { id: '6421650315', student_id: '6421650315', name: 'นาย ภูมิพัฒน์ ศรีมณี', email: 'phumiphat.sr@ku.th', role: 'student', section: 'หมู่ 702 (ภาคปกติ)', company_name: 'ธนาคารไทยพาณิชย์ จำกัด (มหาชน) (SCB TechX)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 92, feedback: 'ปฏิบัติตามกฎระเบียบและส่งงานตรงเวลา มีมนุษยสัมพันธ์ดี', semester: 'ภาคปลาย 2568' },
            { id: '6421655316', student_id: '6421655316', name: 'นางสาว ธัญชนก รุ่งเรืองกิจ', email: 'thanchanok.ru@ku.th', role: 'student', section: 'หมู่ 802 (ภาคพิเศษ)', company_name: 'บริษัท อโกด้า เซอร์วิสเซส จำกัด', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 95, feedback: 'การสื่อสารภาษาอังกฤษดีเยี่ยม มีความรับผิดชอบในงานสูง', semester: 'ภาคปลาย 2568' },

            // ภาคต้น 2568 (6 นิสิต - สถานะสำเร็จการฝึกงานครบถ้วน)
            { id: '6421650121', student_id: '6421650121', name: 'นาย กรวิชญ์ สิทธิประเสริฐ', email: 'korawit.si@ku.th', role: 'student', section: 'หมู่ 700 (ภาคปกติ)', company_name: 'บริษัท จัสท์โค (ประเทศไทย) จำกัด', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 88, feedback: 'ผ่านการประเมินมาตรฐานสหกิจศึกษา ผลการปฏิบัติงานเป็นที่น่าพอใจ', semester: 'ภาคต้น 2568' },
            { id: '6421655122', student_id: '6421655122', name: 'นางสาว วริศรา เจริญธนากร', email: 'warisara.ch@ku.th', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'การไฟฟ้าฝ่ายผลิตแห่งประเทศไทย (กฟผ.)', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 93, feedback: 'ส่งรายงานสรุปผลงานครบถ้วนตรงเวลา มีความมุ่งมั่นตั้งใจสูง', semester: 'ภาคต้น 2568' },
            { id: '6421650223', student_id: '6421650223', name: 'นาย อรรถพล ธนโชติสิริ', email: 'attapol.th@ku.th', role: 'student', section: 'หมู่ 701 (ภาคปกติ)', company_name: 'บริษัท ช้อปปี้ (ประเทศไทย) จำกัด', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 90, feedback: 'พัฒนาตนเองได้รวดเร็ว สามารถทำงานร่วมกับทีมวิศวกรรมได้ดี', semester: 'ภาคต้น 2568' },
            { id: '6421655224', student_id: '6421655224', name: 'นางสาว กัญญารัตน์ ชาญณรงค์', email: 'kanyarat.ch@ku.th', role: 'student', section: 'หมู่ 801 (ภาคพิเศษ)', company_name: 'บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 87, feedback: 'ปฏิบัติงานได้ตามเป้าหมายของสถานประกอบการเรียบร้อยดี', semester: 'ภาคต้น 2568' },
            { id: '6421650325', student_id: '6421650325', name: 'นาย ปฏิภาณ วรเกียรติ', email: 'patiphan.wo@ku.th', role: 'student', section: 'หมู่ 702 (ภาคปกติ)', company_name: 'บริษัท ปตท. สำรวจและผลิตปิโตรเลียม จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 94, feedback: 'มีความคิดริเริ่มสร้างสรรค์ และส่งงานตรงต่อเวลาสม่ำเสมอ', semester: 'ภาคต้น 2568' },
            { id: '6421655326', student_id: '6421655326', name: 'นางสาว พัชรพร บูรณสมภพ', email: 'patcharaporn.bu@ku.th', role: 'student', section: 'หมู่ 802 (ภาคพิเศษ)', company_name: 'สำนักงานพัฒนาธุรกรรมทางอิเล็กทรอนิกส์ (ETDA)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 91, feedback: 'ทำงานเอกสารและการประสานงานได้เป็นระเบียบเรียบร้อยมาก', semester: 'ภาคต้น 2568' },

            // ==========================================
            // ข้อมูลประวัติย้อนหลัง: ภาคการศึกษา 2567 (12 นิสิตรุ่นพี่)
            // ==========================================
            // ภาคปลาย 2567 (6 นิสิต)
            { id: '6321650111', student_id: '6321650111', name: 'นาย วศิน พรหมมินทร์', email: 'wasin.p@ku.th', role: 'student', section: 'หมู่ 700 (ภาคปกติ)', company_name: 'บริษัท แสนสิริ จำกัด (มหาชน)', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 92, feedback: 'พัฒนาแอปพลิเคชันได้ตรงตามความต้องการ มีวินัยสูง', semester: 'ภาคปลาย 2567' },
            { id: '6321655112', student_id: '6321655112', name: 'นางสาว ปาณิสรา วัฒนโภคา', email: 'panisara.w@ku.th', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'บริษัท อโกด้า เซอร์วิสเซส จำกัด', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 95, feedback: 'ทักษะภาษาอังกฤษและการสื่อสารดีเยี่ยม ทำงานเป็นทีมได้ดี', semester: 'ภาคปลาย 2567' },
            { id: '6321650213', student_id: '6321650213', name: 'นาย ธนกร อมรเดชา', email: 'thanakorn.a@ku.th', role: 'student', section: 'หมู่ 701 (ภาคปกติ)', company_name: 'ธนาคารกสิกรไทย จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 90, feedback: 'เข้าใจขั้นตอนงาน Data Analytics รวดเร็ว', semester: 'ภาคปลาย 2567' },
            { id: '6321655214', student_id: '6321655214', name: 'นางสาว ศิริพร วิมลชัย', email: 'siriporn.w@ku.th', role: 'student', section: 'หมู่ 801 (ภาคพิเศษ)', company_name: 'บริษัท สามารถคอร์ปอเรชั่น จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 88, feedback: 'มีความกระตือรือร้นในการเรียนรู้เทคโนโลยีใหม่', semester: 'ภาคปลาย 2567' },
            { id: '6321650315', student_id: '6321650315', name: 'นาย กานต์ ธนะสิทธิ์', email: 'karn.t@ku.th', role: 'student', section: 'หมู่ 702 (ภาคปกติ)', company_name: 'บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 93, feedback: 'ส่งงานตรงเวลา มีความรับผิดชอบต่องานสูง', semester: 'ภาคปลาย 2567' },
            { id: '6321655316', student_id: '6321655316', name: 'นางสาว ชญานี เจริญชัย', email: 'chayanee.c@ku.th', role: 'student', section: 'หมู่ 802 (ภาคพิเศษ)', company_name: 'สำนักงานนวัตกรรมแห่งชาติ (สนช.)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 91, feedback: 'มีทักษะการประสานงานและเขียนรายงานวิจัยยอดเยี่ยม', semester: 'ภาคปลาย 2567' },

            // ภาคต้น 2567 (6 นิสิต)
            { id: '6321650121', student_id: '6321650121', name: 'นาย ภควัต จิตติพงศ์', email: 'pakawat.j@ku.th', role: 'student', section: 'หมู่ 700 (ภาคปกติ)', company_name: 'การไฟฟ้าฝ่ายผลิตแห่งประเทศไทย (กฟผ.)', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 89, feedback: 'ผลงานโครงงานผ่านการประเมินในเกณฑ์ดีมาก', semester: 'ภาคต้น 2567' },
            { id: '6321655122', student_id: '6321655122', name: 'นางสาว ณภัทร ชาญวณิช', email: 'naphat.c@ku.th', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'บริษัท บิตคับ ออนไลน์ จำกัด (Bitkub)', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 94, feedback: 'เชี่ยวชาญด้าน Smart Contract และระบบบล็อกเชน', semester: 'ภาคต้น 2567' },
            { id: '6321650223', student_id: '6321650223', name: 'นาย อิทธิพล เหมรัตน์', email: 'itthiphon.h@ku.th', role: 'student', section: 'หมู่ 701 (ภาคปกติ)', company_name: 'บริษัท เบทาโกร จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 87, feedback: 'เข้ากับเพื่อนร่วมงานได้ดี มีทักษะการสื่อสารดี', semester: 'ภาคต้น 2567' },
            { id: '6321655224', student_id: '6321655224', name: 'นางสาว นันท์นภัส บุญชู', email: 'nannaphat.b@ku.th', role: 'student', section: 'หมู่ 801 (ภาคพิเศษ)', company_name: 'บริษัท ไลน์ คอมพานี (ประเทศไทย) จำกัด', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 96, feedback: 'ผลงานโดดเด่น สถานประกอบการชื่นชมเป็นพิเศษ', semester: 'ภาคต้น 2567' },
            { id: '6321650325', student_id: '6321650325', name: 'นาย อภิเชษฐ์ ปรีชา', email: 'aphichet.p@ku.th', role: 'student', section: 'หมู่ 702 (ภาคปกติ)', company_name: 'สถาบันวิจัยวิทยาศาสตร์และเทคโนโลยีฯ', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 90, feedback: 'ปฏิบัติตามกฎระเบียบห้องแล็บอย่างเคร่งครัด', semester: 'ภาคต้น 2567' },
            { id: '6321655326', student_id: '6321655326', name: 'นางสาว สุพัชรา สิทธิกร', email: 'supatchara.s@ku.th', role: 'student', section: 'หมู่ 802 (ภาคพิเศษ)', company_name: 'บริษัท ปตท. สำรวจและผลิตปิโตรเลียม จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 93, feedback: 'วิเคราะห์ข้อมูลทางเทคนิคได้ละเอียดรอบคอบ', semester: 'ภาคต้น 2567' },

            // ==========================================
            // ข้อมูลประวัติย้อนหลัง: ภาคการศึกษา 2566 (12 นิสิตรุ่นพี่)
            // ==========================================
            // ภาคปลาย 2566 (6 นิสิต)
            { id: '6221650111', student_id: '6221650111', name: 'นาย ภาสกร กิจเจริญ', email: 'pasakorn.k@ku.th', role: 'student', section: 'หมู่ 700 (ภาคปกติ)', company_name: 'บริษัท กสท โทรคมนาคม จำกัด (มหาชน)', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 91, feedback: 'ดูแลระบบเครือข่ายได้ดี มีทักษะแก้ปัญหาเฉพาะหน้าดี', semester: 'ภาคปลาย 2566' },
            { id: '6221655112', student_id: '6221655112', name: 'นางสาว ชิดชนก วรพงศ์', email: 'chidchanok.w@ku.th', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'บริษัท ดิจิทัล เวนเจอร์ส จำกัด', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 93, feedback: 'สร้างสรรค์ฟีเจอร์ FinTech มีประโยชน์ต่อองค์กร', semester: 'ภาคปลาย 2566' },
            { id: '6221650213', student_id: '6221650213', name: 'นาย ศุภวิชญ์ เมธาวี', email: 'supawit.m@ku.th', role: 'student', section: 'หมู่ 701 (ภาคปกติ)', company_name: 'ธนาคารไทยพาณิชย์ จำกัด (มหาชน) (SCB TechX)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 90, feedback: 'เรียนรู้ระบบ Cloud และ DevOps ได้รวดเร็ว', semester: 'ภาคปลาย 2566' },
            { id: '6221655214', student_id: '6221655214', name: 'นางสาว วรรณภา ศรีสุข', email: 'wannapa.s@ku.th', role: 'student', section: 'หมู่ 801 (ภาคพิเศษ)', company_name: 'บริษัท แอดวานซ์ อินโฟร์ เซอร์วิส จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 89, feedback: 'ประสานงานลูกค้าองค์กรได้สุภาพเรียบร้อย', semester: 'ภาคปลาย 2566' },
            { id: '6221650315', student_id: '6221650315', name: 'นาย เอกราช ประเสริฐผล', email: 'ekkarat.p@ku.th', role: 'student', section: 'หมู่ 702 (ภาคปกติ)', company_name: 'ตลาดหลักทรัพย์แห่งประเทศไทย (SET)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 94, feedback: 'พัฒนาแดชบอร์ดติดตามข้อมูลหุ้นได้อย่างถูกต้อง', semester: 'ภาคปลาย 2566' },
            { id: '6221655316', student_id: '6221655316', name: 'นางสาว ปัทมา รุ่งเรือง', email: 'pattama.r@ku.th', role: 'student', section: 'หมู่ 802 (ภาคพิเศษ)', company_name: 'บริษัท เกร็บ (ประเทศไทย) จำกัด', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 92, feedback: 'ทัศนคติดีเยี่ยม มีความคิดเชิงตรรกะดี', semester: 'ภาคปลาย 2566' },

            // ภาคต้น 2566 (6 นิสิต)
            { id: '6221650121', student_id: '6221650121', name: 'นาย ธนภัทร สุวรรณโชติ', email: 'thanaphat.s@ku.th', role: 'student', section: 'หมู่ 700 (ภาคปกติ)', company_name: 'บริษัท พีทีที ดิจิตอล โซลูชั่น จำกัด', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 88, feedback: 'ทำงานระบบฐานข้อมูลได้ถูกต้องแม่นยำ', semester: 'ภาคต้น 2566' },
            { id: '6221655122', student_id: '6221655122', name: 'นางสาว มนัสชนก ยั่งยืน', email: 'manatsanok.y@ku.th', role: 'student', section: 'หมู่ 800 (ภาคพิเศษ)', company_name: 'บริษัท ซีพี ออลล์ จำกัด (มหาชน)', advisor_name: '-', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 91, feedback: 'ส่งรายงานตรงเวลา มีความมุ่งมั่นตั้งใจสูง', semester: 'ภาคต้น 2566' },
            { id: '6221650223', student_id: '6221650223', name: 'นาย พชรพล เกียรติสกุล', email: 'pacharapol.k@ku.th', role: 'student', section: 'หมู่ 701 (ภาคปกติ)', company_name: 'บริษัท การบินไทย จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 89, feedback: 'ช่วยเหลืองานทีมไอทีได้เป็นอย่างดี', semester: 'ภาคต้น 2566' },
            { id: '6221655224', student_id: '6221655224', name: 'นางสาว พิชญาภา อารีวัลย์', email: 'pichayapa.a@ku.th', role: 'student', section: 'หมู่ 801 (ภาคพิเศษ)', company_name: 'ธนาคารกรุงไทย จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมหญิง จงจิต', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 95, feedback: 'ผลงานระบบโมบายแบงก์กิ้งยอดเยี่ยม', semester: 'ภาคต้น 2566' },
            { id: '6221650325', student_id: '6221650325', name: 'นาย สหรัฐ อัครโยธิน', email: 'saharat.a@ku.th', role: 'student', section: 'หมู่ 702 (ภาคปกติ)', company_name: 'สำนักงานพัฒนาธุรกรรมทางอิเล็กทรอนิกส์ (ETDA)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 90, feedback: 'เข้าใจมาตรฐานความปลอดภัยไซเบอร์เป็นอย่างดี', semester: 'ภาคต้น 2566' },
            { id: '6221655326', student_id: '6221655326', name: 'นางสาว พิมลดา ธนารัตน์', email: 'pimonlada.t@ku.th', role: 'student', section: 'หมู่ 802 (ภาคพิเศษ)', company_name: 'บริษัท กัลฟ์ เอ็นเนอร์จี ดีเวลลอปเมนท์ จำกัด (มหาชน)', advisor_name: 'อาจารย์ สมจิต มั่งมี', docs: 'ครบถ้วน', status: 'นิเทศแล้ว', score: 93, feedback: 'มีทักษะการนำเสนอและการวิเคราะห์ข้อมูลที่ดีมาก', semester: 'ภาคต้น 2566' }
        ]
    };
}

function ensureSeedUsers() {
    try {
        let customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
        const seeds = getSeedSystemData();

        // ล้างข้อมูลนิสิตตัวอย่างสำหรับทดสอบอัดคลิป (ยกเว้น wongsapat.u)
        const removeDemoIds = ['6512345678', '6666666666', '6565432111'];
        const removeDemoEmails = ['somying.j@ku.th', 'jitdee.m@ku.th'];
        if (!localStorage.getItem('demo_students_cleared_v10')) {
            removeDemoIds.forEach(id => {
                delete customUsers[id];
            });
            removeDemoEmails.forEach(em => {
                delete customUsers[em];
            });
            Object.keys(customUsers).forEach(k => {
                const u = customUsers[k];
                if (u) {
                    const uId = String(u.id || u.student_id || '').trim();
                    const uEmail = String(u.email || '').toLowerCase().trim();
                    if (removeDemoIds.includes(uId) || removeDemoEmails.includes(uEmail)) {
                        delete customUsers[k];
                    }
                }
            });
            localStorage.setItem('demo_students_cleared_v10', 'true');
        }

        // กำหนดสถานะ purge เริ่มต้นให้เป็น true เพื่อไม่ให้ล้างบัญชี somchai.j ที่ผู้ใช้นำเข้าหรือตั้งค่าไว้
        if (!localStorage.getItem('initial_somchai_purged_v10')) {
            localStorage.setItem('initial_somchai_purged_v10', 'true');
        }

        // รีเซ็ตบัญชี wongsapat.u ให้กลับมาเป็นสถานะเข้าสู่ระบบแรกเข้าใหม่ (first_login = true, password_changed = false)
        if (!localStorage.getItem('wongsapat_reset_first_login_v8')) {
            const wUser = {
                role: 'student',
                name: 'นาย วงศพัทธ์ อุเทน',
                id: '6521655442',
                student_id: '6521655442',
                email: 'wongsapat.u@ku.th',
                password: 'password',
                password_hash: '123456',
                first_login: true,
                password_changed: false,
                section: 'หมู่ 800 (ภาคพิเศษ)',
                company_name: 'สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.)',
                company_lat: '14.078440',
                company_lng: '100.601560',
                advisor_name: 'อาจารย์ สมชาย ใจถนอม',
                semester: 'ภาคต้น 2569',
                status: 'approved'
            };
            const sUser = {
                role: 'advisor',
                name: 'อาจารย์ สมชาย ใจถนอม',
                id: 'Q1111',
                advisor_id: 'Q1111',
                email: 'somchai.j@ku.th',
                password: 'Q1111',
                password_hash: 'Q1111',
                first_login: true,
                password_changed: false,
                section: 'หมู่ 700, 800',
                responsible_sections: ['700', '800'],
                status: 'approved'
            };
            ['wongsapat.u@ku.th', '6521655442', 'wongsapat.u'].forEach(k => {
                customUsers[k] = Object.assign(customUsers[k] || {}, wUser);
                customUsers[k].first_login = true;
                customUsers[k].password_changed = false;
                customUsers[k].password = 'password';
                customUsers[k].password_hash = '123456';
            });
            ['somchai.j@ku.th', 'q1111', 'somchai.j'].forEach(k => {
                if (!customUsers[k] || customUsers[k].password_changed !== true) {
                    customUsers[k] = Object.assign(customUsers[k] || {}, sUser);
                    customUsers[k].first_login = true;
                    customUsers[k].password_changed = false;
                    customUsers[k].password_hash = 'Q1111';
                }
            });
            localStorage.setItem('customUsers', JSON.stringify(customUsers));
            localStorage.setItem('wongsapat_reset_first_login_v8', 'true');
        }

        // Ensure advisors exist with password Asd1234 and first_login false
        seeds.advisors.forEach(a => {
            const emailKey = a.email.toLowerCase().trim();
            if (!customUsers[emailKey]) {
                customUsers[emailKey] = a;
            } else {
                customUsers[emailKey].section = a.section;
                customUsers[emailKey].name = a.name;
                customUsers[emailKey].id = a.id;
                customUsers[emailKey].advisor_id = a.id;
            }
            customUsers[emailKey].password = 'Asd1234';
            customUsers[emailKey].password_hash = 'Asd1234';
            customUsers[emailKey].first_login = false;
        });

        // Ensure students exist with up-to-date semester, score, and status
        seeds.students.forEach(s => {
            const emailKey = s.email.toLowerCase().trim();
            if (!customUsers[emailKey]) {
                customUsers[emailKey] = s;
            } else {
                customUsers[emailKey].advisor_name = s.advisor_name;
                customUsers[emailKey].section = s.section;
                customUsers[emailKey].company_name = s.company_name;
                customUsers[emailKey].name = s.name;
                customUsers[emailKey].id = s.id;
                customUsers[emailKey].student_id = s.id;
                customUsers[emailKey].semester = s.semester;
                if (s.score !== undefined) customUsers[emailKey].score = s.score;
                if (s.feedback !== undefined) customUsers[emailKey].feedback = s.feedback;
                if (s.status !== undefined) customUsers[emailKey].status = s.status;
                if (s.docs !== undefined) customUsers[emailKey].docs = s.docs;
            }
        });

        localStorage.setItem('customUsers', JSON.stringify(customUsers));

        // Preload sample documents for historical students if not present
        let submittedDocs = JSON.parse(localStorage.getItem('submittedDocs') || '[]');
        const seededDocStudentIds = new Set(submittedDocs.map(d => String(d.studentId)));
        let docsAdded = false;

        seeds.students.filter(s => s.semester && (s.semester.includes('2568') || s.semester.includes('2567') || s.semester.includes('2566'))).forEach(s => {
            if (!seededDocStudentIds.has(String(s.id))) {
                submittedDocs.push({
                    id: 'doc-hist-' + s.id + '-1',
                    studentId: String(s.id),
                    email: s.email,
                    docType: 'แบบตอบรับนิสิตเข้าปฏิบัติงานสหกิจศึกษา (คู-01)',
                    fileName: `KU01_Acceptance_${s.id}.pdf`,
                    fileUrl: '',
                    status: 'ตรวจรับแล้ว',
                    uploadDate: s.semester.includes('ภาคต้น') ? '15 ก.ค. 2568' : '15 ธ.ค. 2568'
                });
                submittedDocs.push({
                    id: 'doc-hist-' + s.id + '-2',
                    studentId: String(s.id),
                    email: s.email,
                    docType: 'รายงานสรุปผลการปฏิบัติงานสหกิจศึกษาฉบับสมบูรณ์',
                    fileName: `Final_Report_${s.id}.pdf`,
                    fileUrl: '',
                    status: 'ตรวจรับแล้ว',
                    uploadDate: s.semester.includes('ภาคต้น') ? '25 ต.ค. 2568' : '25 มี.ค. 2569'
                });
                docsAdded = true;
            }
        });

        // Preload sample documents for 2569 students (current semester)
        // หมายเหตุ: ลบ Contribution Distribution ออกจาก seed แล้ว
        // กรอง Contribution Distribution ที่อาจค้างอยู่ใน localStorage ออก (migration)
        const contribKey = 'แบบฟอร์มยืนยันสัดส่วนการทำงานร่วมกัน (Contribution Distribution)';
        const beforeFilter = submittedDocs.length;
        submittedDocs = submittedDocs.filter(d =>
            !String(d.docType || '').includes('Contribution Distribution')
        );
        if (submittedDocs.length !== beforeFilter) docsAdded = true;

        const seededDocKeys = new Set(submittedDocs.map(d => `${d.studentId}_${d.docType}`));
        seeds.students.filter(s => !s.semester || s.semester.includes('2569')).forEach((s, idx) => {

            // Doc 2: Form 02 - แบบแจ้งยืนยันการนิเทศงานนิสิตสหกิจศึกษา
            const doc2 = 'Form 02 - แบบแจ้งยืนยันการนิเทศงานนิสิตสหกิจศึกษา';
            if (!seededDocKeys.has(`${s.id}_${doc2}`)) {
                submittedDocs.push({
                    id: 'doc-2569-' + s.id + '-2',
                    studentId: String(s.id),
                    email: s.email,
                    docType: doc2,
                    fileName: `Form02_SupervisionConfirmation_${s.id}.pdf`,
                    fileUrl: '',
                    status: s.status === 'นิเทศแล้ว' ? 'ตรวจรับแล้ว' : 'รอตรวจ',
                    uploadDate: '14 ต.ค. 2569'
                });
                docsAdded = true;
            }

            // Doc 3: Form 04 - แบบแจ้งรายละเอียดที่พัก
            const doc4 = 'Form 04 - แบบแจ้งรายละเอียดที่พักระหว่างการปฏิบัติงานสหกิจศึกษา';
            if (!seededDocKeys.has(`${s.id}_${doc4}`) && (s.docs === 'ครบถ้วน' || idx % 2 === 0)) {
                submittedDocs.push({
                    id: 'doc-2569-' + s.id + '-4',
                    studentId: String(s.id),
                    email: s.email,
                    docType: doc4,
                    fileName: `Form04_Accommodation_${s.id}.pdf`,
                    fileUrl: '',
                    status: 'ตรวจรับแล้ว',
                    uploadDate: '18 ต.ค. 2569'
                });
                docsAdded = true;
            }

            // Doc 4: Form 05 - แบบแจ้งรายละเอียดงาน ตำแหน่งงาน พนักงานที่ปรึกษา
            const doc5 = 'Form 05 - แบบแจ้งรายละเอียดงาน ตำแหน่งงาน พนักงานที่ปรึกษา';
            if (!seededDocKeys.has(`${s.id}_${doc5}`) && (s.docs === 'ครบถ้วน' || idx % 3 === 0)) {
                submittedDocs.push({
                    id: 'doc-2569-' + s.id + '-5',
                    studentId: String(s.id),
                    email: s.email,
                    docType: doc5,
                    fileName: `Form05_JobMentor_${s.id}.pdf`,
                    fileUrl: '',
                    status: idx % 2 === 0 ? 'ตรวจรับแล้ว' : 'รอตรวจ',
                    uploadDate: '20 ต.ค. 2569'
                });
                docsAdded = true;
            }

            // Doc 5: Form 06 - รายงานการปฏิบัติงานประจำสัปดาห์ (Weekly Report)
            const doc6 = 'Form 06 - รายงานการปฏิบัติงานประจำสัปดาห์ (Weekly Report)';
            if (!seededDocKeys.has(`${s.id}_${doc6}`) && idx % 2 === 0) {
                submittedDocs.push({
                    id: 'doc-2569-' + s.id + '-6',
                    studentId: String(s.id),
                    email: s.email,
                    docType: doc6,
                    fileName: `Weekly_Report_W01_${s.id}.pdf`,
                    fileUrl: '',
                    status: 'ตรวจรับแล้ว',
                    uploadDate: '22 ต.ค. 2569'
                });
                docsAdded = true;
            }

            // Doc 6: Form 11 - รายงานสรุปผลการปฏิบัติงานสหกิจศึกษา (Final Report)
            const doc11 = 'Form 11 - รายงานสรุปผลการปฏิบัติงานสหกิจศึกษา (Final Report)';
            if (!seededDocKeys.has(`${s.id}_${doc11}`) && idx % 3 === 0) {
                submittedDocs.push({
                    id: 'doc-2569-' + s.id + '-11',
                    studentId: String(s.id),
                    email: s.email,
                    docType: doc11,
                    fileName: `Final_Report_Draft_${s.id}.pdf`,
                    fileUrl: '',
                    status: 'รอตรวจ',
                    uploadDate: '23 ต.ค. 2569'
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
}
