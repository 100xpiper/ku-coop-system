#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KU Coop Web Server & Email API
ระบบนิเทศสหกิจศึกษา ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์
"""

import os
import sys
import json
import smtplib
import socket
import webbrowser
import subprocess
import threading
import time
import re
import shutil
import urllib.parse
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote, urlparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Global state for mobile tunnel
GLOBAL_TUNNEL_URL = None
TUNNEL_PROCESS = None

# SMTP Configuration
SMTP_USER = "per.300846@gmail.com"
SMTP_PASS = "bpbvozebtiqmmslk"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
FROM_NAME = "ระบบนิเทศสหกิจศึกษา KU"
DEFENSE_EMAIL = "wongsapat.u@ku.th"

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css":  "text/css; charset=utf-8",
    ".js":   "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg":  "image/svg+xml",
    ".ico":  "image/x-icon",
    ".md":   "text/markdown; charset=utf-8",
    ".pdf":  "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".csv":  "text/csv; charset=utf-8"
}

def get_lan_ip():
    """ค้นหา IPv4 ภายในวงแลน / Wi-Fi"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.1.103"

def send_clean_smtp_mail(to_email, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{Header(FROM_NAME, 'utf-8').encode()} <{SMTP_USER}>"
    msg["To"] = to_email
    msg["Subject"] = Header(subject, "utf-8").encode()
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [to_email], msg.as_string())

class KUCoopHandler(BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            body = json.loads(raw_body.decode("utf-8"))
        except Exception:
            body = {}

        # 1. POST /api/send-otp
        if parsed.path == "/api/send-otp":
            email = body.get("email", body.get("toEmail", ""))
            otp = body.get("otp", body.get("otpCode", ""))
            name = body.get("name", body.get("toName", "ผู้ใช้งานระบบนิเทศสหกิจศึกษา KU"))

            if not email or not otp:
                return self.send_json({"success": False, "error": "Email and OTP are required"}, 400)

            print(f"[OTP] Sending OTP {otp} to {DEFENSE_EMAIL} (for {email}) ...")
            subject = f"รหัส OTP เข้าสู่ระบบนิเทศสหกิจศึกษา KU: {otp}"

            tpl_path = os.path.join(BASE_DIR, "templates", "email_otp.html")
            if os.path.isfile(tpl_path):
                with open(tpl_path, "r", encoding="utf-8") as f:
                    html_body = f.read()
                html_body = html_body.replace("{{TO_NAME}}", str(name)).replace("{{NAME}}", str(name))
                html_body = html_body.replace("{{TO_EMAIL}}", str(email)).replace("{{ORIGINAL_EMAIL}}", str(email))
                html_body = html_body.replace("{{OTP_CODE}}", str(otp)).replace("{{OTP}}", str(otp))
                html_body = html_body.replace("{{DEFENSE_EMAIL}}", DEFENSE_EMAIL)
            else:
                html_body = f"<h2>OTP Verification</h2><p>Your OTP code is: <b>{otp}</b></p>"

            recipients = [DEFENSE_EMAIL]
            if email and "@" in email and email != DEFENSE_EMAIL and not email.endswith("example.com"):
                recipients.append(email)

            sent_any = False
            for target in recipients:
                try:
                    send_clean_smtp_mail(target, subject, html_body)
                    print(f"[OTP] Sent successfully to {target}")
                    sent_any = True
                except Exception as e:
                    print(f"[OTP] SMTP Error to {target}: {e}")

            if sent_any:
                return self.send_json({"success": True, "forwardedTo": DEFENSE_EMAIL, "recipients": recipients})
            else:
                return self.send_json({"success": False, "error": "SMTP send failed"}, 500)

        # 2. POST /api/send-reminder
        elif parsed.path == "/api/send-reminder":
            to_email = body.get("studentEmail", "")
            student_name = body.get("studentName", "")
            student_id = body.get("studentId", "")
            missing_docs = body.get("missingDocs", [])
            advisor_name = body.get("advisorName", "")

            print(f"[Reminder] Sending document reminder to {DEFENSE_EMAIL} (for {to_email} - {student_name}) ...")
            subject = f"แจ้งเตือนการส่งเอกสารสหกิจศึกษาคงค้าง - {student_name} ({student_id})"

            docs_list_html = "".join([f"<li style='margin-bottom:6px;'>{doc}</li>" for doc in missing_docs])
            tpl_path = os.path.join(BASE_DIR, "templates", "email_reminder.html")
            if os.path.isfile(tpl_path):
                with open(tpl_path, "r", encoding="utf-8") as f:
                    html_body = f.read()
                html_body = html_body.replace("{{STUDENT_NAME}}", str(student_name))
                html_body = html_body.replace("{{STUDENT_ID}}", str(student_id))
                html_body = html_body.replace("{{ADVISOR_NAME}}", str(advisor_name))
                html_body = html_body.replace("{{MISSING_DOCS}}", docs_list_html)
                html_body = html_body.replace("{{DEFENSE_EMAIL}}", DEFENSE_EMAIL)
            else:
                html_body = f"<h2>Document Reminder</h2><p>Student: {student_name}</p><ul>{docs_list_html}</ul>"

            try:
                send_clean_smtp_mail(DEFENSE_EMAIL, subject, html_body)
                print(f"[Reminder] Sent successfully to {DEFENSE_EMAIL} (for {to_email})")
                return self.send_json({"success": True, "forwardedTo": DEFENSE_EMAIL})
            except Exception as e:
                print(f"[Reminder] SMTP Error: {e}")
                return self.send_json({"success": False, "error": str(e)}, 500)

        # 3. POST /api/send-first-login
        elif parsed.path == "/api/send-first-login":
            to_email = body.get("studentEmail", "")
            to_name = body.get("studentName", "")
            student_id = body.get("studentId", "")
            advisor_name = body.get("advisorName", "")
            initial_password = body.get("initialPassword", "")
            if not initial_password or initial_password == student_id:
                initial_password = "123456"
            login_url = body.get("loginUrl", "http://localhost:8080")

            print(f"[FirstLogin] Sending first login email to {DEFENSE_EMAIL} (for {to_email} - {to_name}) ...")
            subject = f"แจ้งข้อมูลการเข้าใช้งานระบบนิเทศสหกิจศึกษา KU (สำหรับนิสิตแรกเข้า) - {to_name} ({student_id})"

            tpl_path = os.path.join(BASE_DIR, "templates", "email_first_login.html")
            if os.path.isfile(tpl_path):
                with open(tpl_path, "r", encoding="utf-8") as f:
                    html_body = f.read()
                html_body = html_body.replace("{{TO_NAME}}", str(to_name))
                html_body = html_body.replace("{{STUDENT_ID}}", str(student_id))
                html_body = html_body.replace("{{ADVISOR_NAME}}", str(advisor_name))
                html_body = html_body.replace("{{TO_EMAIL}}", str(to_email))
                html_body = html_body.replace("{{INITIAL_PASSWORD}}", str(initial_password))
                html_body = html_body.replace("{{LOGIN_URL}}", str(login_url))
                html_body = html_body.replace("{{DEFENSE_EMAIL}}", DEFENSE_EMAIL)
            else:
                html_body = f"<h2>First Login Info</h2><p>Password: {initial_password}</p>"

            try:
                send_clean_smtp_mail(DEFENSE_EMAIL, subject, html_body)
                print(f"[FirstLogin] Email sent successfully to {DEFENSE_EMAIL} (for {to_email})")
                return self.send_json({"success": True, "forwardedTo": DEFENSE_EMAIL})
            except Exception as e:
                print(f"[FirstLogin] SMTP Error: {e}")
                return self.send_json({"success": False, "error": str(e)}, 500)

        # 4. POST /api/send-notification (สำหรับแจ้งเตือน นัดหมาย, สั่งงาน, ตรวจเอกสาร)
        elif parsed.path == "/api/send-notification":
            to_email = body.get("toEmail") or body.get("to") or body.get("email") or ""
            student_name = body.get("studentName", "นิสิต")
            student_id = body.get("studentId", "")
            advisor_name = body.get("advisorName", "อาจารย์นิเทศ")
            notif_type = body.get("type", "general")
            badge_text = body.get("badgeText", "แจ้งเตือนระบบ")
            badge_color = body.get("badgeColor", "#16a34a")
            subject = body.get("subject", f"แจ้งเตือนจากระบบนิเทศสหกิจศึกษา KU - {student_name}")
            notif_title = body.get("notificationTitle", subject)
            details_html = body.get("detailsHtml", "<p>มีรายการแจ้งเตือนใหม่ในระบบ</p>")
            action_url = body.get("actionUrl", f"http://localhost:{self.server.server_port}/dashboard.html")
            action_text = body.get("actionText", "เข้าสู่ระบบเพื่อตรวจสอบ")

            print(f"[Notification] Dispatching {notif_type} notification for {student_name} ({student_id}) to {to_email} and {DEFENSE_EMAIL} ...")

            tpl_path = os.path.join(BASE_DIR, "templates", "email_notification.html")
            if os.path.isfile(tpl_path):
                with open(tpl_path, "r", encoding="utf-8") as f:
                    html_body = f.read()
                html_body = html_body.replace("{{BADGE_TEXT}}", str(badge_text))
                html_body = html_body.replace("{{BADGE_COLOR}}", str(badge_color))
                html_body = html_body.replace("{{NOTIFICATION_TITLE}}", str(notif_title))
                html_body = html_body.replace("{{STUDENT_NAME}}", str(student_name))
                html_body = html_body.replace("{{STUDENT_ID}}", str(student_id))
                html_body = html_body.replace("{{ADVISOR_NAME}}", str(advisor_name))
                html_body = html_body.replace("{{DETAILS_HTML}}", str(details_html))
                html_body = html_body.replace("{{ACTION_URL}}", str(action_url))
                html_body = html_body.replace("{{ACTION_TEXT}}", str(action_text))
                html_body = html_body.replace("{{DEFENSE_EMAIL}}", DEFENSE_EMAIL)
            else:
                html_body = f"<h2>{subject}</h2><p>เรียน นิสิต {student_name}</p><div>{details_html}</div>"

            recipients = []
            if to_email and "@" in to_email and not to_email.endswith("example.com"):
                recipients.append(to_email)
            if DEFENSE_EMAIL not in recipients:
                recipients.append(DEFENSE_EMAIL)

            sent_any = False
            for target in recipients:
                try:
                    send_clean_smtp_mail(target, subject, html_body)
                    print(f"[Notification] Sent successfully to {target}")
                    sent_any = True
                except Exception as e:
                    print(f"[Notification] SMTP Error to {target}: {e}")

            if sent_any:
                return self.send_json({"success": True, "recipients": recipients})
            else:
                return self.send_json({"success": False, "error": "SMTP send failed for all recipients"}, 500)

        # 5. POST /api/send-email
        elif parsed.path == "/api/send-email":
            to_email = body.get("to") or body.get("email")
            subject = body.get("subject", "แจ้งเตือนจากระบบนิเทศสหกิจศึกษา KU")
            html_body = body.get("html") or body.get("body") or "<p>แจ้งเตือนจากระบบ</p>"

            print(f"[SendEmail] Forwarding email to {DEFENSE_EMAIL} (target was {to_email}) ...")
            try:
                send_clean_smtp_mail(DEFENSE_EMAIL, subject, html_body)
                return self.send_json({"success": True, "forwardedTo": DEFENSE_EMAIL})
            except Exception as e:
                print(f"[SendEmail] SMTP Error: {e}")
                return self.send_json({"success": False, "error": str(e)}, 500)

        else:
            return self.send_json({"error": "Endpoint not found"}, 404)

    def do_GET(self):
        self.handle_static_request(send_body=True)

    def do_HEAD(self):
        self.handle_static_request(send_body=False)

    def handle_static_request(self, send_body=True):
        parsed = urlparse(self.path)
        clean_path = unquote(parsed.path).lstrip("/")

        # API get server url
        if clean_path == "api/get-server-url":
            data = {
                "tunnel_url": GLOBAL_TUNNEL_URL,
                "local_url": f"http://localhost:{self.server.server_port}",
                "lan_url": f"http://{get_lan_ip()}:{self.server.server_port}",
                "github_pages": "https://100xpiper.github.io/ku-coop-system/"
            }
            return self.send_json(data)

        if not clean_path or clean_path == "/":
            clean_path = "index.html"

        # Check in BASE_DIR
        file_path = os.path.normpath(os.path.join(BASE_DIR, clean_path))
        if not file_path.startswith(BASE_DIR):
            self.send_error(403, "Forbidden")
            return

        if not os.path.isfile(file_path):
            # Check in docs/
            docs_path = os.path.normpath(os.path.join(BASE_DIR, "docs", clean_path))
            if os.path.isfile(docs_path):
                file_path = docs_path

        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file_path)
            content_type = MIME_TYPES.get(ext.lower(), "application/octet-stream")

            try:
                with open(file_path, "rb") as f:
                    data = f.read()

                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.send_cors_headers()
                self.end_headers()

                if send_body:
                    self.wfile.write(data)
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_response(404)
            err_msg = b"404 Not Found"
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(err_msg)))
            self.send_cors_headers()
            self.end_headers()
            if send_body:
                self.wfile.write(err_msg)

    def log_message(self, format, *args):
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def find_adb():
    candidates = [
        r"C:\Users\per30\AppData\Local\Android\Sdk\platform-tools\adb.exe",
        "adb"
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
        elif shutil.which(p):
            return p
    return None

def start_adb_watcher(port):
    """ตรวจจับโทรศัพท์มือถือผ่านสาย USB และสั่ง adb reverse ให้อัตโนมัติ"""
    adb_exe = find_adb()
    if not adb_exe:
        return

    def watcher():
        configured_devices = set()
        while True:
            try:
                res = subprocess.run([adb_exe, "devices"], capture_output=True, text=True, timeout=3)
                current_devices = set()
                for line in res.stdout.splitlines():
                    parts = line.strip().split()
                    if len(parts) >= 2 and parts[1] == "device":
                        current_devices.add(parts[0])

                for dev in current_devices:
                    if dev not in configured_devices:
                        subprocess.run([adb_exe, "-s", dev, "reverse", f"tcp:{port}", f"tcp:{port}"], capture_output=True, timeout=3)
                        subprocess.run([adb_exe, "-s", dev, "reverse", "tcp:3000", "tcp:3000"], capture_output=True, timeout=3)
                        configured_devices.add(dev)
                        print("\n" + "=" * 66)
                        print(f"  [สาย USB]: เชื่อมต่อโทรศัพท์ ({dev}) สำเร็จเรียบร้อย!")
                        print(f"  --> เปิดเบราว์เซอร์ Chrome บนโทรศัพท์ แล้วพิมพ์: http://localhost:{port}")
                        print("=" * 66 + "\n")

                # Clear disconnected devices
                configured_devices.intersection_update(current_devices)
            except Exception:
                pass
            time.sleep(3)

    t = threading.Thread(target=watcher, daemon=True)
    t.start()

def update_mobile_access_page(tunnel_url, port):
    """อัปเดตหน้า mobile-access.html และดาวน์โหลดภาพ QR Code"""
    qr_file = os.path.join(BASE_DIR, "mobile-qr.png")
    try:
        qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(tunnel_url)}"
        req = urllib.request.urlopen(qr_api, timeout=4)
        with open(qr_file, "wb") as f:
            f.write(req.read())
    except Exception:
        pass

    access_html = os.path.join(BASE_DIR, "mobile-access.html")
    if os.path.isfile(access_html):
        try:
            with open(access_html, "r", encoding="utf-8") as f:
                content = f.read()
            content = re.sub(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', tunnel_url, content)
            with open(access_html, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            pass

def start_cloudflared_tunnel(port):
    """เปิดอุโมงค์ Cloudflare HTTPS สำหรับโทรศัพท์มือถือเข้าถึงได้จากทุกที่"""
    global GLOBAL_TUNNEL_URL, TUNNEL_PROCESS
    cf_path = os.path.join(BASE_DIR, "tools", "cloudflared.exe")
    if not os.path.isfile(cf_path):
        return None

    try:
        proc = subprocess.Popen(
            [cf_path, "tunnel", "--url", f"http://127.0.0.1:{port}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        TUNNEL_PROCESS = proc
    except Exception:
        return None

    def worker():
        global GLOBAL_TUNNEL_URL
        tunnel_url = None
        t0 = time.time()
        while time.time() - t0 < 12:
            line = proc.stderr.readline()
            if not line:
                continue
            m = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if m:
                tunnel_url = m.group(0)
                break

        if tunnel_url:
            GLOBAL_TUNNEL_URL = tunnel_url
            try:
                with open(os.path.join(BASE_DIR, "tools", "mobile_url.txt"), "w", encoding="utf-8") as f:
                    f.write(tunnel_url)
            except Exception:
                pass

            update_mobile_access_page(tunnel_url, port)

            print("\n" + "=" * 66)
            print("  [โทรศัพท์มือถือ - เปิดได้ทุกที่ ทุกระบบ ไม่ต้องเสียบสาย]:")
            print(f"  --> ลิงก์ตรง: {tunnel_url}")
            print(f"  --> หรือเปิดหน้า QR Code สแกนผ่านมือถือ: http://localhost:{port}/mobile-access.html")
            print("=" * 66 + "\n")

        try:
            for _ in proc.stderr:
                pass
        except Exception:
            pass

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return proc

def main():
    preferred_ports = [8080, 8081, 8082, 3000]
    chosen_port = None
    server = None

    for p in preferred_ports:
        try:
            server = HTTPServer(("0.0.0.0", p), KUCoopHandler)
            chosen_port = p
            break
        except OSError:
            continue

    if not server:
        if is_port_in_use(8080):
            print("==========================================================")
            print(" KU Coop Web Server is already running on http://localhost:8080")
            print(" Opening web browser...")
            print("==========================================================")
            webbrowser.open("http://localhost:8080")
            sys.exit(0)
        else:
            print("Failed to start server on ports:", preferred_ports)
            sys.exit(1)

    lan_ip = get_lan_ip()

    print("=" * 66)
    print("  KU Coop Web Server started successfully! (เปิดเซิร์ฟเวอร์สำเร็จ)")
    print("=" * 66)
    print(f"  1. [PC คอมพิวเตอร์เครื่องนี้]:        http://localhost:{chosen_port}")
    print(f"  2. [ออนไลน์ GitHub Pages (เปิดได้ทันที)]: https://100xpiper.github.io/ku-coop-system/")
    print(f"  3. [Wi-Fi วงเดียวกัน]:              http://{lan_ip}:{chosen_port}")
    print("=" * 66)
    print("  กด Ctrl+C ในหน้าต่างนี้เพื่อหยุดการทำงานของเซิร์ฟเวอร์")
    print("=" * 66)

    # Start mobile background helpers
    start_adb_watcher(chosen_port)
    start_cloudflared_tunnel(chosen_port)

    try:
        webbrowser.open(f"http://localhost:{chosen_port}")
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping KU Coop Web Server...")
        if TUNNEL_PROCESS:
            try:
                TUNNEL_PROCESS.terminate()
                TUNNEL_PROCESS.wait(timeout=2)
            except Exception:
                pass
        server.server_close()
        sys.exit(0)

if __name__ == "__main__":
    main()
