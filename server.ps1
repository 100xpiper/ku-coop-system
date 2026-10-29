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
  <p>⏱️ รหัสนี้มีอายุ <strong>5 นาที</strong> และใช้ได้ครั้งเดียว</p>
  <p>⚠️ กรุณาอย่าเปิดเผยรหัสนี้แก่ผู้อื่น</p>
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
