import os
import sys
import json
import socket
import smtplib
import webbrowser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import urllib.request
import subprocess
import re
import threading
import time

GLOBAL_TUNNEL_URL = None

# Configuration
PREFERRED_PORTS = [8080, 8081, 8082, 3000]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SMTP_USER = "per.300846@gmail.com"
SMTP_PASS = "bpbvozebtiqmmslk"
SMTP_FROM_NAME = "ระบบนิเทศสหกิจศึกษา KU"
DEFENSE_EMAIL = "wongsapat.u@ku.th"

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".csv": "text/csv; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
    ".txt": "text/plain; charset=utf-8"
}

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"

def send_smtp_email(to_email, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = formataddr((str(Header(SMTP_FROM_NAME, "utf-8")), SMTP_USER))
    msg["To"] = to_email

    part = MIMEText(html_body, "html", "utf-8")
    msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [to_email], msg.as_string())

class CoopServerHandler(SimpleHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def send_json_response(self, obj, status_code=200):
        data = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path).path
        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length)
        
        try:
            body = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}
        except Exception:
            body = {}

        # 1. API: /api/send-otp
        if parsed_path == "/api/send-otp":
            to_email = body.get("email")
            to_name = body.get("name") or "ผู้ใช้งาน"
            otp_code = body.get("otpCode")

            if not to_email or not otp_code:
                self.send_json_response({"success": False, "error": "Missing email or otpCode"}, 400)
                return

            print(f"[OTP] Sending OTP {otp_code} for {to_email} ({to_name}) -> to {DEFENSE_EMAIL} ...")
            try:
                subject = f"รหัส OTP เข้าสู่ระบบนิเทศสหกิจศึกษา KU: {otp_code}"
                template_path = os.path.join(BASE_DIR, "templates", "email_otp.html")
                if os.path.exists(template_path):
                    with open(template_path, "r", encoding="utf-8") as tf:
                        html_body = tf.read()
                    html_body = (html_body.replace("{{TO_NAME}}", str(to_name))
                                          .replace("{{TO_EMAIL}}", str(to_email))
                                          .replace("{{OTP_CODE}}", str(otp_code))
                                          .replace("{{DEFENSE_EMAIL}}", str(DEFENSE_EMAIL)))
                else:
                    html_body = f"<h2>รหัส OTP: {otp_code}</h2><p>สำหรับ {to_name} ({to_email})</p>"

                send_smtp_email(DEFENSE_EMAIL, subject, html_body)
                print(f"[OTP] Email sent successfully to {DEFENSE_EMAIL} (for {to_email})")
                self.send_json_response({"success": True, "forwardedTo": DEFENSE_EMAIL})
            except Exception as e:
                print(f"[OTP] SMTP Error: {e}")
                self.send_json_response({"success": False, "error": str(e)}, 500)
            return

        # 2. API: /api/send-reminder
        if parsed_path == "/api/send-reminder":
            to_email = body.get("studentEmail") or body.get("email")
            to_name = body.get("studentName") or "นิสิต"
            student_id = body.get("studentId") or "-"
            advisor_name = body.get("advisorName") or "อาจารย์นิเทศ"
            title = body.get("title") or "แจ้งเตือนการส่งงาน"
            detail = body.get("detail") or ""
            due_date = body.get("dueDate") or "-"
            lan_ip = get_lan_ip()
            login_url = body.get("loginUrl") or f"http://{lan_ip}:{self.server.server_port}"
            if "localhost" in login_url or "127.0.0.1" in login_url:
                login_url = login_url.replace("localhost", lan_ip).replace("127.0.0.1", lan_ip)

            print(f"[Reminder] Sending reminder to {DEFENSE_EMAIL} (for {to_email} - {to_name}) ...")
            try:
                subject = f"[แจ้งเตือนส่งงานสหกิจศึกษา KU] {title}"
                template_path = os.path.join(BASE_DIR, "templates", "email_reminder.html")
                if os.path.exists(template_path):
                    with open(template_path, "r", encoding="utf-8") as tf:
                        html_body = tf.read()
                    html_body = (html_body.replace("{{TO_NAME}}", str(to_name))
                                          .replace("{{TO_EMAIL}}", str(to_email))
                                          .replace("{{STUDENT_ID}}", str(student_id))
                                          .replace("{{ADVISOR_NAME}}", str(advisor_name))
                                          .replace("{{TITLE}}", str(title))
                                          .replace("{{DETAIL}}", str(detail))
                                          .replace("{{DUE_DATE}}", str(due_date))
                                          .replace("{{LOGIN_URL}}", str(login_url))
                                          .replace("{{DEFENSE_EMAIL}}", str(DEFENSE_EMAIL)))
                else:
                    html_body = f"<h2>{title}</h2><p>{detail}</p><p>กำหนดส่ง: {due_date}</p>"

                send_smtp_email(DEFENSE_EMAIL, subject, html_body)
                print(f"[Reminder] Email sent successfully to {DEFENSE_EMAIL} (for {to_email})")
                self.send_json_response({"success": True, "forwardedTo": DEFENSE_EMAIL})
            except Exception as e:
                print(f"[Reminder] SMTP Error: {e}")
                self.send_json_response({"success": False, "error": str(e)}, 500)
            return

        # 3. API: /api/send-first-login
        if parsed_path == "/api/send-first-login":
            to_email = body.get("studentEmail") or body.get("email")
            to_name = body.get("studentName") or "นิสิต"
            student_id = body.get("studentId") or "-"
            advisor_name = body.get("advisorName") or "อาจารย์นิเทศ"
            initial_password = body.get("initialPassword") or "123456"
            if initial_password == student_id or not initial_password:
                initial_password = "123456"
            lan_ip = get_lan_ip()
            login_url = body.get("loginUrl") or f"http://{lan_ip}:{self.server.server_port}"
            if "localhost" in login_url or "127.0.0.1" in login_url:
                login_url = login_url.replace("localhost", lan_ip).replace("127.0.0.1", lan_ip)

            print(f"[FirstLogin] Sending first login email to {DEFENSE_EMAIL} (for {to_email} - {to_name}) ...")
            try:
                subject = f"แจ้งข้อมูลการเข้าใช้งานระบบนิเทศสหกิจศึกษา KU (สำหรับนิสิตแรกเข้า) - {to_name} ({student_id})"
                template_path = os.path.join(BASE_DIR, "templates", "email_first_login.html")
                if os.path.exists(template_path):
                    with open(template_path, "r", encoding="utf-8") as tf:
                        html_body = tf.read()
                    html_body = (html_body.replace("{{TO_NAME}}", str(to_name))
                                          .replace("{{STUDENT_ID}}", str(student_id))
                                          .replace("{{ADVISOR_NAME}}", str(advisor_name))
                                          .replace("{{TO_EMAIL}}", str(to_email))
                                          .replace("{{INITIAL_PASSWORD}}", str(initial_password))
                                          .replace("{{LOGIN_URL}}", str(login_url))
                                          .replace("{{DEFENSE_EMAIL}}", str(DEFENSE_EMAIL)))
                else:
                    html_body = f"<h2>ข้อมูลแรกเข้าใช้งาน</h2><p>รหัสผ่านแรกเข้า: {initial_password}</p>"

                send_smtp_email(DEFENSE_EMAIL, subject, html_body)
                print(f"[FirstLogin] Email sent successfully to {DEFENSE_EMAIL} (for {to_email})")
                self.send_json_response({"success": True, "forwardedTo": DEFENSE_EMAIL})
            except Exception as e:
                print(f"[FirstLogin] SMTP Error: {e}")
                self.send_json_response({"success": False, "error": str(e)}, 500)
            return

        # 4. API: /api/send-email (Generic)
        if parsed_path == "/api/send-email":
            to_email = body.get("to") or body.get("email")
            subject = body.get("subject") or "แจ้งเตือนจากระบบนิเทศสหกิจศึกษา"
            html_body = body.get("htmlBody") or body.get("message") or ""

            if not to_email:
                self.send_json_response({"success": False, "error": "Missing to email"}, 400)
                return

            print(f"[SendEmail] Sending email to {to_email} ...")
            try:
                send_smtp_email(to_email, subject, html_body)
                print(f"[SendEmail] Email sent successfully to {to_email}")
                self.send_json_response({"success": True})
            except Exception as e:
                print(f"[SendEmail] SMTP Error: {e}")
                self.send_json_response({"success": False, "error": str(e)}, 500)
            return

        self.send_json_response({"error": "Endpoint not found"}, 404)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path == "/" or not path:
            path = "/index.html"

        decoded_path = urllib.parse.unquote(path).lstrip("/")
        local_path = os.path.join(BASE_DIR, decoded_path)

        # Fallback to docs/ folder
        if not os.path.exists(local_path) or os.path.isdir(local_path):
            docs_path = os.path.join(BASE_DIR, "docs", decoded_path)
            if os.path.exists(docs_path) and os.path.isfile(docs_path):
                local_path = docs_path

        if os.path.exists(local_path) and os.path.isfile(local_path):
            _, ext = os.path.splitext(local_path)
            content_type = MIME_TYPES.get(ext.lower(), "application/octet-stream")

            try:
                with open(local_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(content)
            except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                pass
            except Exception as e:
                try:
                    self.send_error(500, f"Error reading file: {e}")
                except Exception:
                    pass
        else:
            self.send_error(404, "File Not Found")

    def log_message(self, format, *args):
        # Only log non-static file requests to keep console clean
        try:
            msg = format % args
            if any(api in msg for api in ["/api/", "POST", "500", "404"]):
                super().log_message(format, *args)
        except Exception:
            pass

def start_cloudflared_tunnel(port):
    global GLOBAL_TUNNEL_URL
    cf_path = os.path.join(BASE_DIR, "tools", "cloudflared.exe")
    if not os.path.exists(cf_path):
        return None, None
    try:
        proc = subprocess.Popen(
            [cf_path, "tunnel", "--url", f"http://127.0.0.1:{port}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
    except Exception:
        return None, None

    tunnel_url = None
    t0 = time.time()
    while time.time() - t0 < 8:
        line = proc.stderr.readline()
        if not line:
            continue
        m = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if m:
            tunnel_url = m.group(0)
            GLOBAL_TUNNEL_URL = tunnel_url
            try:
                with open(os.path.join(BASE_DIR, "tools", "mobile_url.txt"), "w", encoding="utf-8") as f:
                    f.write(tunnel_url)
            except Exception:
                pass
            break

    def drain_pipe():
        try:
            for _ in proc.stderr:
                pass
        except Exception:
            pass
    threading.Thread(target=drain_pipe, daemon=True).start()
    return proc, tunnel_url

def main():
    lan_ip = get_lan_ip()
    port = None
    server = None
    tunnel_proc = None
    tunnel_url = None

    # Check if server is already running on port 8080
    try:
        req = urllib.request.urlopen("http://localhost:8080/index.html", timeout=1)
        if req.status == 200:
            existing_tunnel = None
            url_file = os.path.join(BASE_DIR, "tools", "mobile_url.txt")
            if os.path.exists(url_file):
                try:
                    with open(url_file, "r", encoding="utf-8") as f:
                        existing_tunnel = f.read().strip()
                except Exception:
                    pass

            print("=" * 66)
            print("  KU Coop Web Server is already running! (เซิร์ฟเวอร์กำลังทำงานอยู่แล้ว)")
            print("=" * 66)
            print(f"  [PC คอมพิวเตอร์เครื่องนี้]:        http://localhost:8080")
            if existing_tunnel:
                print(f"  [โทรศัพท์มือถือ (เปิดได้ทุกที่)]:   {existing_tunnel}")
            print(f"  [โทรศัพท์มือถือ (Wi-Fi เดียวกัน)]:   http://{lan_ip}:8080")
            print("=" * 66)
            print("  กำลังเปิดเว็บเบราว์เซอร์...")
            try:
                webbrowser.open("http://localhost:8080")
            except Exception:
                pass
            print("  เซิร์ฟเวอร์เปิดให้บริการอยู่แล้ว สามารถใช้งานได้ทันที")
            print("=" * 66)
            return
    except Exception:
        pass

    for p in PREFERRED_PORTS:
        try:
            # Bind to 0.0.0.0 so ALL interfaces (LAN / Wi-Fi) can access without admin rights!
            server = HTTPServer(('0.0.0.0', p), CoopServerHandler)
            port = p
            break
        except OSError:
            continue

    if not server:
        print(f"Error: Could not bind to any preferred port ({PREFERRED_PORTS})")
        sys.exit(1)

    # Start Cloudflare Tunnel for mobile access (HTTPS)
    tunnel_proc, tunnel_url = start_cloudflared_tunnel(port)

    print("=" * 66)
    print("  KU Coop Web Server started successfully! (เปิดเซิร์ฟเวอร์สำเร็จ)")
    print("=" * 66)
    print(f"  [PC คอมพิวเตอร์เครื่องนี้]:        http://localhost:{port}")
    if tunnel_url:
        print(f"  [โทรศัพท์มือถือ (เปิดได้ทุกที่)]:   {tunnel_url}")
    print(f"  [โทรศัพท์มือถือ (Wi-Fi เดียวกัน)]:   http://{lan_ip}:{port}")
    print("=" * 66)
    print("  กด Ctrl+C ในหน้าต่างนี้เพื่อหยุดการทำงานของเซิร์ฟเวอร์")
    print("=" * 66)

    try:
        webbrowser.open(f"http://localhost:{port}")
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        if tunnel_proc:
            try:
                tunnel_proc.terminate()
                tunnel_proc.wait(timeout=2)
            except Exception:
                pass
        server.server_close()

if __name__ == "__main__":
    main()
