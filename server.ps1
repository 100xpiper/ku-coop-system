$preferredPorts = @(8080, 8081, 8082, 3000)
$listener = $null
$port = $null

foreach ($p in $preferredPorts) {
    try {
        $l = New-Object System.Net.HttpListener
        $l.Prefixes.Add("http://localhost:$p/")
        $l.Prefixes.Add("http://127.0.0.1:$p/")
        $l.Start()
        $listener = $l
        $port = $p
        break
    } catch {
        # Port in use or not available, try next
    }
}

if (-not $listener) {
    try {
        $test = Invoke-WebRequest -Uri "http://localhost:8080/index.html" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($test.StatusCode -eq 200) {
            Write-Host "==========================================================" -ForegroundColor Green
            Write-Host " KU Coop Web Server is already running on http://localhost:8080" -ForegroundColor Green
            Write-Host " Opening web browser..." -ForegroundColor Cyan
            Write-Host "==========================================================" -ForegroundColor Green
            Start-Process "http://localhost:8080"
            exit 0
        }
    } catch {}

    Write-Host "Failed to start listener on ports: $($preferredPorts -join ', ')" -ForegroundColor Red
    exit 1
}

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " KU Coop Web Server started successfully!" -ForegroundColor Green
Write-Host " Access URL: http://localhost:$port" -ForegroundColor Cyan
Write-Host " OTP Email API: http://localhost:$port/api/send-otp" -ForegroundColor Cyan
Write-Host " Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Green
Start-Process "http://localhost:$port"

$baseDir = $PSScriptRoot

# --- SMTP Config ---
$SMTP_USER = "per.300846@gmail.com"
$SMTP_PASS = "bpbvozebtiqmmslk"
$SMTP_FROM_NAME = "ระบบนิเทศสหกิจศึกษา KU"

$mimeTypes = @{
    ".html" = "text/html; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json; charset=utf-8"
    ".png"  = "image/png"
    ".jpg"  = "image/jpeg"
    ".jpeg" = "image/jpeg"
    ".svg"  = "image/svg+xml"
    ".ico"  = "image/x-icon"
    ".md"   = "text/markdown; charset=utf-8"
}

function Write-JsonResponse($response, $obj, $statusCode = 200) {
    $response.StatusCode = $statusCode
    $response.ContentType = "application/json; charset=utf-8"
    $response.Headers.Add("Access-Control-Allow-Origin", "*")
    $response.Headers.Add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    $response.Headers.Add("Access-Control-Allow-Headers", "Content-Type")
    $json = $obj | ConvertTo-Json -Compress
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    $response.ContentLength64 = $bytes.Length
    $response.OutputStream.Write($bytes, 0, $bytes.Length)
}

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        try {
            $request  = $context.Request
            $response = $context.Response
            $urlPath  = $request.Url.LocalPath

            # --- Handle CORS preflight ---
            if ($request.HttpMethod -eq "OPTIONS") {
                $response.Headers.Add("Access-Control-Allow-Origin", "*")
                $response.Headers.Add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                $response.Headers.Add("Access-Control-Allow-Headers", "Content-Type")
                $response.StatusCode = 204
                $response.Close()
                continue
            }

            # --- POST /api/send-otp : ส่ง OTP Email ผ่าน Gmail SMTP ---
            if ($urlPath -eq "/api/send-otp" -and $request.HttpMethod -eq "POST") {
                try {
                    $reader   = New-Object System.IO.StreamReader($request.InputStream, [System.Text.Encoding]::UTF8)
                    $bodyText = $reader.ReadToEnd()
                    $body     = $bodyText | ConvertFrom-Json

                    $toEmail  = $body.email
                    $toName   = $body.name
                    $otpCode  = $body.otpCode

                    if (-not $toEmail -or -not $otpCode) {
                        Write-JsonResponse $response @{ success = $false; error = "Missing email or otpCode" } 400
                        $response.Close()
                        continue
                    }

                    Write-Host "[OTP] Sending OTP $otpCode to $toEmail ..." -ForegroundColor Cyan

                    $credential = New-Object System.Management.Automation.PSCredential(
                        $SMTP_USER,
                        (ConvertTo-SecureString $SMTP_PASS -AsPlainText -Force)
                    )

                    $subject = "รหัส OTP เข้าสู่ระบบนิเทศสหกิจศึกษา KU"
                    $htmlBody = @"
<div style="font-family:Arial,sans-serif;max-width:520px;margin:0 auto;padding:24px;">
  <div style="text-align:center;margin-bottom:20px;">
    <h2 style="color:#15803d;margin:0;">ระบบนิเทศสหกิจศึกษา</h2>
    <p style="color:#64748b;margin:4px 0;">มหาวิทยาลัยเกษตรศาสตร์</p>
  </div>
  <p>เรียน <strong>$toName</strong></p>
  <p>รหัส OTP สำหรับเข้าสู่ระบบของท่านคือ:</p>
  <div style="background:#f0fdf4;border:2px solid #16a34a;border-radius:12px;padding:28px;text-align:center;margin:20px 0;">
    <div style="font-size:40px;font-weight:bold;letter-spacing:8px;color:#15803d;font-family:monospace;">$otpCode</div>
  </div>
  <p>รหัสนี้มีอายุ <strong>5 นาที</strong> และใช้ได้ครั้งเดียว</p>
  <p>กรุณาอย่าเปิดเผยรหัสนี้แก่บุคคลอื่น</p>
  <hr style="border:none;border-top:1px solid #e2e8f0;margin:20px 0;">
  <p style="font-size:12px;color:#94a3b8;text-align:center;">ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์</p>
</div>
"@

                    Send-MailMessage `
                        -SmtpServer "smtp.gmail.com" `
                        -Port 587 `
                        -UseSsl `
                        -Credential $credential `
                        -From "$SMTP_FROM_NAME <$SMTP_USER>" `
                        -To $toEmail `
                        -Subject $subject `
                        -Body $htmlBody `
                        -BodyAsHtml `
                        -Encoding UTF8

                    Write-Host "[OTP] Email sent successfully to $toEmail" -ForegroundColor Green
                    Write-JsonResponse $response @{ success = $true }
                } catch {
                    $errMsg = $_.Exception.Message
                    Write-Host "[OTP] SMTP Error: $errMsg" -ForegroundColor Red
                    Write-JsonResponse $response @{ success = $false; error = $errMsg } 500
                }
                $response.Close()
                continue
            }


            # --- POST /api/send-first-login : ส่งอีเมลแจ้งแรกเข้าใช้งาน ผ่าน Gmail SMTP ---
            if ($urlPath -eq "/api/send-first-login" -and $request.HttpMethod -eq "POST") {
                try {
                    $reader   = New-Object System.IO.StreamReader($request.InputStream, [System.Text.Encoding]::UTF8)
                    $bodyText = $reader.ReadToEnd()
                    $body     = $bodyText | ConvertFrom-Json

                    $toEmail     = $body.email
                    $toName      = $body.name
                    $studentId   = $body.studentId
                    $advisorName = $body.advisorName
                    $loginUrl    = $body.loginUrl
                    if (-not $loginUrl) { $loginUrl = "http://localhost:8080/index.html" }

                    if (-not $toEmail) {
                        Write-JsonResponse $response @{ success = $false; error = "Missing email" } 400
                        $response.Close()
                        continue
                    }

                    Write-Host "[FirstLogin] Sending first login email to $toEmail ($toName) ..." -ForegroundColor Cyan

                    $credential = New-Object System.Management.Automation.PSCredential(
                        $SMTP_USER,
                        (ConvertTo-SecureString $SMTP_PASS -AsPlainText -Force)
                    )

                    $subject = "แจ้งข้อมูลการเข้าใช้งานระบบนิเทศสหกิจศึกษา KU (สำหรับนิสิตแรกเข้า) - $toName ($studentId)"
                    $htmlBody = @"
<div style="font-family:'Prompt','Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;padding:24px;background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;">
  <div style="background:#15803d;padding:24px;border-radius:8px 8px 0 0;text-align:center;color:#ffffff;">
    <h2 style="margin:0 0 6px 0;font-size:22px;">ระบบนิเทศสหกิจศึกษา</h2>
    <p style="margin:0;font-size:14px;opacity:0.9;">มหาวิทยาลัยเกษตรศาสตร์</p>
  </div>
  <div style="padding:24px;">
    <p style="font-size:16px;color:#1e293b;margin-top:0;">เรียน <strong>$toName</strong> (รหัสนิสิต: <strong>$studentId</strong>)</p>
    <p style="font-size:14px;color:#475569;line-height:1.6;">
      อาจารย์นิเทศ (<strong>$advisorName</strong>) ได้เพิ่มข้อมูลของท่านเข้าสู่ระบบนิเทศสหกิจศึกษา เรียบร้อยแล้ว ท่านสามารถเข้าใช้งานระบบเพื่อส่งเอกสารสหกิจศึกษา ตรวจสอบการนัดหมาย และติดตามความคืบหน้าได้ทันที
    </p>

    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:16px;margin:20px 0;">
      <h3 style="margin:0 0 10px 0;font-size:15px;color:#166534;">ข้อมูลสำหรับการเข้าสู่ระบบครั้งแรก</h3>
      <table style="width:100%;font-size:14px;color:#334155;border-collapse:collapse;">
        <tr>
          <td style="padding:6px 0;width:170px;font-weight:600;color:#15803d;">ชื่อผู้ใช้งาน (Username):</td>
          <td style="padding:6px 0;"><code>$toEmail</code> หรือ <code>$studentId</code></td>
        </tr>
        <tr>
          <td style="padding:6px 0;font-weight:600;color:#15803d;">รหัสผ่านแรกเข้า:</td>
          <td style="padding:6px 0;"><code style="background:#dcfce7;color:#166534;padding:2px 8px;border-radius:4px;font-weight:700;">$studentId</code></td>
        </tr>
      </table>
    </div>

    <div style="background:#f8fafc;border-left:4px solid #0284c7;padding:12px 16px;margin:20px 0;font-size:13.5px;color:#334155;">
      <strong>ขั้นตอนการเข้าสู่ระบบครั้งแรก:</strong>
      <ol style="margin:8px 0 0 0;padding-left:20px;line-height:1.7;">
        <li>กดปุ่มเข้าสู่ระบบด้านล่าง หรือเข้าผ่านลิงก์ของระบบ</li>
        <li>กรอกอีเมล (@ku.th) หรือรหัสนิสิต และรหัสผ่านแรกเข้า (รหัสนิสิต)</li>
        <li>ระบบจะส่งรหัส OTP 8 หลักไปยังอีเมลนี้ เพื่อยืนยันตัวตน</li>
        <li>ตั้งรหัสผ่านใหม่สำหรับการใช้งานประจำตัว</li>
      </ol>
    </div>

    <div style="text-align:center;margin:28px 0;">
      <a href="$loginUrl" style="display:inline-block;background:#15803d;color:#ffffff;text-decoration:none;font-size:15px;font-weight:600;padding:12px 32px;border-radius:8px;">เข้าสู่ระบบนิเทศสหกิจศึกษา</a>
    </div>

    <hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0;">
    <p style="font-size:12px;color:#94a3b8;text-align:center;margin:0;line-height:1.5;">
      ระบบนิเทศสหกิจศึกษา ภาควิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์<br>
      อีเมลนี้เป็นการแจ้งเตือนอัตโนมัติจากระบบ กรุณาอย่าตอบกลับ
    </p>
  </div>
</div>
"@

                    Send-MailMessage `
                        -SmtpServer "smtp.gmail.com" `
                        -Port 587 `
                        -UseSsl `
                        -Credential $credential `
                        -From "$SMTP_FROM_NAME <$SMTP_USER>" `
                        -To $toEmail `
                        -Subject $subject `
                        -Body $htmlBody `
                        -BodyAsHtml `
                        -Encoding UTF8

                    Write-Host "[FirstLogin] Email sent successfully to $toEmail" -ForegroundColor Green
                    Write-JsonResponse $response @{ success = $true }
                } catch {
                    $errMsg = $_.Exception.Message
                    Write-Host "[FirstLogin] SMTP Error: $errMsg" -ForegroundColor Red
                    Write-JsonResponse $response @{ success = $false; error = $errMsg } 500
                }
                $response.Close()
                continue
            }

            # --- POST /api/send-email : ส่งอีเมลทั่วไป ผ่าน Gmail SMTP ---
            if ($urlPath -eq "/api/send-email" -and $request.HttpMethod -eq "POST") {
                try {
                    $reader   = New-Object System.IO.StreamReader($request.InputStream, [System.Text.Encoding]::UTF8)
                    $bodyText = $reader.ReadToEnd()
                    $body     = $bodyText | ConvertFrom-Json

                    $toEmail  = $body.to
                    if (-not $toEmail) { $toEmail = $body.email }
                    $subject  = $body.subject
                    $htmlBody = $body.htmlBody
                    if (-not $htmlBody) { $htmlBody = $body.message }

                    if (-not $toEmail -or -not $subject) {
                        Write-JsonResponse $response @{ success = $false; error = "Missing to or subject" } 400
                        $response.Close()
                        continue
                    }

                    Write-Host "[SendEmail] Sending email to $toEmail" -ForegroundColor Cyan

                    $credential = New-Object System.Management.Automation.PSCredential(
                        $SMTP_USER,
                        (ConvertTo-SecureString $SMTP_PASS -AsPlainText -Force)
                    )

                    Send-MailMessage `
                        -SmtpServer "smtp.gmail.com" `
                        -Port 587 `
                        -UseSsl `
                        -Credential $credential `
                        -From "$SMTP_FROM_NAME <$SMTP_USER>" `
                        -To $toEmail `
                        -Subject $subject `
                        -Body $htmlBody `
                        -BodyAsHtml `
                        -Encoding UTF8

                    Write-Host "[SendEmail] Email sent successfully to $toEmail" -ForegroundColor Green
                    Write-JsonResponse $response @{ success = $true }
                } catch {
                    $errMsg = $_.Exception.Message
                    Write-Host "[SendEmail] SMTP Error: $errMsg" -ForegroundColor Red
                    Write-JsonResponse $response @{ success = $false; error = $errMsg } 500
                }
                $response.Close()
                continue
            }

            # --- Static File Serving ---
            if ($urlPath -eq "/" -or [string]::IsNullOrWhiteSpace($urlPath)) {
                $urlPath = "/index.html"
            }

            $decoded   = [System.Uri]::UnescapeDataString($urlPath).TrimStart('/')
            $localPath = Join-Path $baseDir $decoded

            if (Test-Path $localPath -PathType Leaf) {
                $ext         = [System.IO.Path]::GetExtension($localPath).ToLower()
                $contentType = "application/octet-stream"
                if ($mimeTypes.ContainsKey($ext)) { $contentType = $mimeTypes[$ext] }
                $response.ContentType = $contentType
                $response.AddHeader("Cache-Control", "no-cache, no-store, must-revalidate")
                $bytes = [System.IO.File]::ReadAllBytes($localPath)
                $response.ContentLength64 = $bytes.Length
                if ($request.HttpMethod -ne "HEAD") {
                    $response.OutputStream.Write($bytes, 0, $bytes.Length)
                }
            } else {
                $response.StatusCode = 404
                $errBytes = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found")
                $response.ContentLength64 = $errBytes.Length
                if ($request.HttpMethod -ne "HEAD") {
                    $response.OutputStream.Write($errBytes, 0, $errBytes.Length)
                }
            }
            $response.Close()
        } catch {
            try { $context.Response.Close() } catch {}
        }
    }
} finally {
    $listener.Stop()
    $listener.Close()
}
