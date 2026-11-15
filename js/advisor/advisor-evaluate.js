// ==========================================================================
// advisor-evaluate.js - ระบบแบบประเมินผลและให้คะแนนการนิเทศงาน (100 คะแนน)
// โครงการ: KU Science Smart Internship Supervision Platform (01418499)
// ผู้จัดทำ: นาย วงศพัทธ์ อุเทน (รหัสนิสิต 6521655442)
// ==========================================================================

function openEvalModalFromResult() {
            if (!currentSelectedStudentId) return;
            let stdName = 'นิสิต';
            const allStds = getAllSystemStudents();
            const stdObj = allStds.find(s => String(s.id) === String(currentSelectedStudentId));
            if (stdObj) stdName = stdObj.name;

            document.getElementById('eval-student-name').textContent = `${stdName} (${currentSelectedStudentId})`;
            document.getElementById('modal-eval-form').style.display = 'flex';
        }

        async function saveEvaluationForm() {
            const s1 = parseInt(document.getElementById('eval-score-1').value) || 0;
            const s2 = parseInt(document.getElementById('eval-score-2').value) || 0;
            const s3 = parseInt(document.getElementById('eval-score-3').value) || 0;
            const total = s1 + s2 + s3;
            const feedback = document.getElementById('eval-feedback').value;

            const allStds = getAllSystemStudents();
            const std = allStds.find(s => String(s.id) === String(currentSelectedStudentId));
            if (std) {
                std.status = 'นิเทศแล้ว';
                std.score = total;
                renderStudentList();
            }

            // Update in customUsers as well
            const customUsers = JSON.parse(localStorage.getItem('customUsers') || '{}');
            Object.values(customUsers).forEach(u => {
                if (String(u.id || u.student_id) === String(currentSelectedStudentId)) {
                    u.status = 'นิเทศแล้ว';
                    u.score = total;
                    u.feedback = feedback;
                }
            });
            localStorage.setItem('customUsers', JSON.stringify(customUsers));

            // Save Evaluation to Supabase DB
            await dbSaveEvaluation(currentSelectedStudentId, total, feedback);

            const scoreEl = document.getElementById('std-score-val');
            if (scoreEl) scoreEl.textContent = `${total} / 100`;
            const feedEl = document.getElementById('std-feedback-val');
            if (feedEl) feedEl.textContent = feedback;

            addNotification(`การประเมินนิเทศงานเสร็จสิ้น คะแนนรวม: ${total}/100`);
            alert(`บันทึกผลการประเมินดิจิทัลลง Database (Supabase) เรียบร้อย คะแนนรวม ${total}/100`);
            closeModal('modal-eval-form');
            updateAdvisorStats();
        }
