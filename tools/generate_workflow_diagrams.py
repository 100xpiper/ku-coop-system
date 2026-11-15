import os
from PIL import Image, ImageDraw, ImageFont

def draw_arrow(draw, start, end, arrow_size=10, width=2, color=(0, 0, 0)):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=width)
    
    # Calculate arrowhead points
    if x1 == x2: # Vertical arrow
        if y2 > y1: # Down
            points = [(x2, y2), (x2 - arrow_size // 2, y2 - arrow_size), (x2 + arrow_size // 2, y2 - arrow_size)]
        else: # Up
            points = [(x2, y2), (x2 - arrow_size // 2, y2 + arrow_size), (x2 + arrow_size // 2, y2 + arrow_size)]
    elif y1 == y2: # Horizontal arrow
        if x2 > x1: # Right
            points = [(x2, y2), (x2 - arrow_size, y2 - arrow_size // 2), (x2 - arrow_size, y2 + arrow_size // 2)]
        else: # Left
            points = [(x2, y2), (x2 + arrow_size, y2 - arrow_size // 2), (x2 + arrow_size, y2 + arrow_size // 2)]
    else:
        points = [(x2, y2)]
    draw.polygon(points, fill=color)

def generate_workflow_image(output_path, steps):
    width, height = 1200, 870
    img = Image.new("RGB", (width, height), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    # 1. Draw light grid background
    grid_size = 20
    grid_color = "#EFEFEF"
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # Fonts
    font_path = "C:/Windows/Fonts/tahoma.ttf"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/angsana.ttc"

    font_text = ImageFont.truetype(font_path, 18)

    # Grid box parameters
    box_w, box_h = 310, 130
    cols_x = [60, 445, 830]
    rows_y = [40, 245, 450, 655]

    # Map 10 steps to coordinates (col_idx, row_idx)
    # Row 0: 1 -> 2 -> 3
    # Row 1: 6 <- 5 <- 4
    # Row 2: 7 -> 8 -> 9
    # Row 3:           10
    layout = [
        (0, 0), # Step 1: col 0, row 0
        (1, 0), # Step 2: col 1, row 0
        (2, 0), # Step 3: col 2, row 0
        (2, 1), # Step 4: col 2, row 1
        (1, 1), # Step 5: col 1, row 1
        (0, 1), # Step 6: col 0, row 1
        (0, 2), # Step 7: col 0, row 2
        (1, 2), # Step 8: col 1, row 2
        (2, 2), # Step 9: col 2, row 2
        (2, 3), # Step 10: col 2, row 3
    ]

    # Draw boxes and text
    for idx, (col_i, row_i) in enumerate(layout):
        bx = cols_x[col_i]
        by = rows_y[row_i]

        # Fill white box with black border
        draw.rectangle([bx, by, bx + box_w, by + box_h], fill="#FFFFFF", outline="#000000", width=2)

        # Draw step text inside box
        lines = steps[idx]
        total_text_h = len(lines) * 26
        start_y = by + (box_h - total_text_h) // 2

        for l_idx, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_text)
            line_w = bbox[2] - bbox[0]
            line_x = bx + (box_w - line_w) // 2
            line_y = start_y + l_idx * 26
            draw.text((line_x, line_y), line, fill="#000000", font=font_text)

    # Draw connecting arrows
    # 1 -> 2 (right)
    draw_arrow(draw, (cols_x[0] + box_w, rows_y[0] + box_h // 2), (cols_x[1], rows_y[0] + box_h // 2))
    # 2 -> 3 (right)
    draw_arrow(draw, (cols_x[1] + box_w, rows_y[0] + box_h // 2), (cols_x[2], rows_y[0] + box_h // 2))
    # 3 -> 4 (down)
    draw_arrow(draw, (cols_x[2] + box_w // 2, rows_y[0] + box_h), (cols_x[2] + box_w // 2, rows_y[1]))
    # 4 -> 5 (left)
    draw_arrow(draw, (cols_x[2], rows_y[1] + box_h // 2), (cols_x[1] + box_w, rows_y[1] + box_h // 2))
    # 5 -> 6 (left)
    draw_arrow(draw, (cols_x[1], rows_y[1] + box_h // 2), (cols_x[0] + box_w, rows_y[1] + box_h // 2))
    # 6 -> 7 (down)
    draw_arrow(draw, (cols_x[0] + box_w // 2, rows_y[1] + box_h), (cols_x[0] + box_w // 2, rows_y[2]))
    # 7 -> 8 (right)
    draw_arrow(draw, (cols_x[0] + box_w, rows_y[2] + box_h // 2), (cols_x[1], rows_y[2] + box_h // 2))
    # 8 -> 9 (right)
    draw_arrow(draw, (cols_x[1] + box_w, rows_y[2] + box_h // 2), (cols_x[2], rows_y[2] + box_h // 2))
    # 9 -> 10 (down)
    draw_arrow(draw, (cols_x[2] + box_w // 2, rows_y[2] + box_h), (cols_x[2] + box_w // 2, rows_y[3]))

    # Save image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    print(f"Generated: {output_path}")

# Student Workflow
student_steps = [
    ["1. นิสิตเปิดเข้าสู่เว็บแอปพลิเคชัน", "KU Smart Internship"],
    ["2. กรอกอีเมลมหาวิทยาลัย (@ku.th)", "และรหัสผ่านเพื่อเข้าสู่ระบบ"],
    ["3. รับรหัส OTP 8 หลัก ทางอีเมล", "กรอกยืนยันตัวตนสำเร็จ"],
    ["4. บังคับเปลี่ยนรหัสผ่านส่วนบุคคล", "ตามเกณฑ์ความปลอดภัย 4 ข้อ"],
    ["5. หน้า Dashboard แสดงข้อมูล", "และสถานะการส่งเอกสาร"],
    ["6. ดาวน์โหลดแบบฟอร์มเปล่า", "FORM-00 ถึง FORM-11"],
    ["7. กรอกข้อมูลและอัปโหลด", "เอกสารรายงานเข้าสู่ระบบ"],
    ["8. ตรวจสอบสถานะการตรวจรับ", "และอ่านข้อคิดเห็นสะท้อนกลับ"],
    ["9. บันทึกและตั้งค่าพิกัด GPS", "สถานประกอบการของตนเอง"],
    ["10. แสดง Dynamic QR Code", "ให้อาจารย์สแกนตรวจนิเทศ"]
]

# Advisor Workflow
advisor_steps = [
    ["1. อาจารย์เข้าสู่ระบบด้วยอีเมล", "@ku.th และยืนยันรหัส OTP 8 หลัก"],
    ["2. เลือกห้องเรียนที่รับผิดชอบ", "หมู่ 700 ภาคปกติ หรือหมู่ 800"],
    ["3. ตรวจสอบรายชื่อนิสิตในกลุ่ม", "และข้อมูลสถานที่ฝึกงาน"],
    ["4. ตรวจสอบตารางแมทริกซ์", "สถานะการส่งเอกสารภาพรวม"],
    ["5. ตรวจรับเอกสารรายฉบับ", "อนุมัติหรือตีกลับพร้อม Feedback"],
    ["6. สร้างภาระงานและมอบหมายงาน", "ติดตามรายชื่อผู้ส่งงาน"],
    ["7. วางแผนและบันทึกกำหนดการ", "การออกตรวจนิเทศลงในปฏิทิน"],
    ["8. เมื่อถึงสถานที่ฝึกงาน เปิดกล้องสด", "สแกน Dynamic QR ของนิสิต"],
    ["9. ระบบตรวจสอบ Geofencing", "รัศมี 500 ม. เช็คอินสำเร็จ"],
    ["10. อัปโหลดภาพหลักฐานสองชั้น", "และประเมินคะแนนเกณฑ์รูบริก"]
]

# Admin Workflow
admin_steps = [
    ["1. ผู้ดูแลระบบเข้าสู่ระบบ", "ด้วยบัญชีสิทธิ์แอดมิน (Admin)"],
    ["2. ตรวจสอบแดชบอร์ดสถิติ", "ภาพรวมนิเทศงานแบบเรียลไทม์"],
    ["3. นำเข้าไฟล์ Excel รายชื่อนิสิต", "ข้อมูลสถานประกอบการและอาจารย์"],
    ["4. ตรวจสอบความถูกต้องของข้อมูล", "ผ่านตารางพรีวิวขนาดใหญ่ 100%"],
    ["5. ยืนยันบันทึกและจัดเก็บข้อมูล", "ลงสู่ฐานข้อมูล Supabase Cloud"],
    ["6. กรองข้อมูลตามภาคการศึกษา", "และค้นหารายชื่อนิสิตรายคน"],
    ["7. ตรวจสอบและปรับปรุง", "ตำแหน่งพิกัด GPS สถานประกอบการ"],
    ["8. บริหารจัดการบัญชีผู้ใช้งาน", "กำหนดสิทธิ์ และรีเซ็ตรหัสผ่าน"],
    ["9. ตรวจสอบสถานะการออกนิเทศ", "และผลการประเมินของอาจารย์"],
    ["10. ประมวลผลและส่งออกรายงาน", "สรุปผลการนิเทศเป็น Excel/PDF"]
]

if __name__ == "__main__":
    out_dir = "screenshots/workflows"
    generate_workflow_image(os.path.join(out_dir, "workflow_student.png"), student_steps)
    generate_workflow_image(os.path.join(out_dir, "workflow_advisor.png"), advisor_steps)
    generate_workflow_image(os.path.join(out_dir, "workflow_admin.png"), admin_steps)
