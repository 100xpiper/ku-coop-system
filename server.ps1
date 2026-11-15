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
$SMTP_FROM_NAME = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("4Lij4Liw4Lia4Lia4LiZ4Li04LmA4LiX4Lio4Liq4Lir4LiB4Li04LiI4Lio4Li24LiB4Lip4LiyIEtV"))

function Send-CleanSmtpMail($toEmail, $subject, $htmlBody) {
    $mail = New-Object System.Net.Mail.MailMessage
    $fromAddr = New-Object System.Net.Mail.MailAddress($SMTP_USER, $SMTP_FROM_NAME, [System.Text.Encoding]::UTF8)
    $mail.From = $fromAddr
    $mail.To.Add($toEmail)
    $mail.Subject = $subject
    $mail.SubjectEncoding = [System.Text.Encoding]::UTF8
    $mail.Body = $htmlBody
    $mail.BodyEncoding = [System.Text.Encoding]::UTF8
    $mail.IsBodyHtml = $true

    $smtpClient = New-Object System.Net.Mail.SmtpClient("smtp.gmail.com", 587)
    $smtpClient.EnableSsl = $true
    $smtpClient.Credentials = New-Object System.Net.NetworkCredential($SMTP_USER, $SMTP_PASS)
    $smtpClient.Send($mail)
    $mail.Dispose()
    $smtpClient.Dispose()
}

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

            # --- POST /api/send-otp ---
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

                    $DEFENSE_EMAIL = "wongsapat.u@ku.th"
                    Write-Host "[OTP] Sending OTP $otpCode for $toEmail ($toName) -> to $DEFENSE_EMAIL ..." -ForegroundColor Cyan

                    $subject = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("4Lij4Lir4Lix4LiqIE9UUCDguYDguILguYnguLLguKrguLnguYjguKPguLDguJrguJrguJnguLTguYDguJfguKjguKrguKvguIHguLTguIjguKjguLbguIHguKnguLIgS1U6IA==")) + $otpCode
                    $templatePath = Join-Path $PSScriptRoot "templates\email_otp.html"
                    if (Test-Path $templatePath) {
                        $htmlBody = [System.IO.File]::ReadAllText($templatePath, [System.Text.Encoding]::UTF8)
                        $htmlBody = $htmlBody.Replace("{{TO_NAME}}", [string]$toName)
                        $htmlBody = $htmlBody.Replace("{{TO_EMAIL}}", [string]$toEmail)
                        $htmlBody = $htmlBody.Replace("{{OTP_CODE}}", [string]$otpCode)
                        $htmlBody = $htmlBody.Replace("{{DEFENSE_EMAIL}}", [string]$DEFENSE_EMAIL)
                    } else {
                        $htmlBody = "<h2>OTP Code: $otpCode</h2><p>For $toName ($toEmail)</p>"
                    }

                    Send-CleanSmtpMail $DEFENSE_EMAIL $subject $htmlBody

                    Write-Host "[OTP] Email sent successfully to $DEFENSE_EMAIL (for $toEmail)" -ForegroundColor Green
                    Write-JsonResponse $response @{ success = $true; forwardedTo = $DEFENSE_EMAIL }
                } catch {
                    $errMsg = $_.Exception.Message
                    Write-Host "[OTP] SMTP Error: $errMsg" -ForegroundColor Red
                    Write-JsonResponse $response @{ success = $false; error = $errMsg } 500
                }
                $response.Close()
                continue
            }

            # --- POST /api/send-reminder ---
            if ($urlPath -eq "/api/send-reminder" -and $request.HttpMethod -eq "POST") {
                try {
                    $reader   = New-Object System.IO.StreamReader($request.InputStream, [System.Text.Encoding]::UTF8)
                    $bodyText = $reader.ReadToEnd()
                    $body     = $bodyText | ConvertFrom-Json

                    $toEmail     = $body.studentEmail
                    $toName      = $body.studentName
                    $studentId   = $body.studentId
                    $advisorName = $body.advisorName
                    $title       = $body.title
                    $detail      = $body.detail
                    $dueDate     = $body.dueDate
                    $loginUrl    = $body.loginUrl

                    $DEFENSE_EMAIL = "wongsapat.u@ku.th"
                    Write-Host "[Reminder] Sending reminder to $DEFENSE_EMAIL (for $toEmail - $toName) ..." -ForegroundColor Cyan

                    $subjectPrefix = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("W+C5geC4iOC5ieC4h+C5gOC4leC4t+C4reC4meC4quC5iOC4h+C5gOC4reC4geC4quC4suC4o+C4quC4q+C4geC4tOC4iOC4qOC4tuC4geC4qeC4siBLVV0g"))
                    $subject = "$subjectPrefix $title"
                    $templatePath = Join-Path $PSScriptRoot "templates\email_reminder.html"
                    if (Test-Path $templatePath) {
                        $htmlBody = [System.IO.File]::ReadAllText($templatePath, [System.Text.Encoding]::UTF8)
                        $htmlBody = $htmlBody.Replace("{{TO_NAME}}", [string]$toName)
                        $htmlBody = $htmlBody.Replace("{{TO_EMAIL}}", [string]$toEmail)
                        $htmlBody = $htmlBody.Replace("{{STUDENT_ID}}", [string]$studentId)
                        $htmlBody = $htmlBody.Replace("{{ADVISOR_NAME}}", [string]$advisorName)
                        $htmlBody = $htmlBody.Replace("{{TITLE}}", [string]$title)
                        $htmlBody = $htmlBody.Replace("{{DETAIL}}", [string]$detail)
                        $htmlBody = $htmlBody.Replace("{{DUE_DATE}}", [string]$dueDate)
                        $htmlBody = $htmlBody.Replace("{{LOGIN_URL}}", [string]$loginUrl)
                        $htmlBody = $htmlBody.Replace("{{DEFENSE_EMAIL}}", [string]$DEFENSE_EMAIL)
                    } else {
                        $htmlBody = "<h2>Reminder: $title</h2><p>$detail</p><p>Due: $dueDate</p>"
                    }

                    Send-CleanSmtpMail $DEFENSE_EMAIL $subject $htmlBody

                    Write-Host "[Reminder] Email sent successfully to $DEFENSE_EMAIL (for $toEmail)" -ForegroundColor Green
                    Write-JsonResponse $response @{ success = $true; forwardedTo = $DEFENSE_EMAIL }
                } catch {
                    $errMsg = $_.Exception.Message
                    Write-Host "[Reminder] SMTP Error: $errMsg" -ForegroundColor Red
                    Write-JsonResponse $response @{ success = $false; error = $errMsg } 500
                }
                $response.Close()
                continue
            }

            # --- POST /api/send-first-login ---
            if ($urlPath -eq "/api/send-first-login" -and $request.HttpMethod -eq "POST") {
                try {
                    $reader   = New-Object System.IO.StreamReader($request.InputStream, [System.Text.Encoding]::UTF8)
                    $bodyText = $reader.ReadToEnd()
                    $body     = $bodyText | ConvertFrom-Json

                    $toEmail     = $body.studentEmail
                    $toName      = $body.studentName
                    $studentId   = $body.studentId
                    $advisorName = $body.advisorName
                    $initialPassword = $body.initialPassword
                    if (-not $initialPassword -or $initialPassword -eq $studentId) {
                        $initialPassword = "123456"
                    }
                    $loginUrl    = $body.loginUrl

                    $DEFENSE_EMAIL = "wongsapat.u@ku.th"
                    Write-Host "[FirstLogin] Sending first login email to $DEFENSE_EMAIL (for $toEmail - $toName) ..." -ForegroundColor Cyan

                    $subjectPrefix = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("4LmB4LiI4LmJ4LiH4LiC4LmJ4Lit4Lih4Li54Lil4LiB4Liy4Lij4LmA4LiC4LmJ4Liy4LmD4LiK4LmJ4LiH4Liy4LiZ4Lij4Liw4Lia4Lia4LiZ4Li04LmA4LiX4Lio4Liq4Lir4LiB4Li04LiI4Lio4Li24LiB4Lip4LiyIEtVICjguKrguLPguKvguKPguLHguJrguJnguLTguKrguLTguJXguYHguKPguIHguYDguILguYnguLIpIC0g"))
                    $subject = "$subjectPrefix $toName ($studentId)"
                    $templatePath = Join-Path $PSScriptRoot "templates\email_first_login.html"
                    if (Test-Path $templatePath) {
                        $htmlBody = [System.IO.File]::ReadAllText($templatePath, [System.Text.Encoding]::UTF8)
                        $htmlBody = $htmlBody.Replace("{{TO_NAME}}", [string]$toName)
                        $htmlBody = $htmlBody.Replace("{{STUDENT_ID}}", [string]$studentId)
                        $htmlBody = $htmlBody.Replace("{{ADVISOR_NAME}}", [string]$advisorName)
                        $htmlBody = $htmlBody.Replace("{{TO_EMAIL}}", [string]$toEmail)
                        $htmlBody = $htmlBody.Replace("{{INITIAL_PASSWORD}}", [string]$initialPassword)
                        $htmlBody = $htmlBody.Replace("{{LOGIN_URL}}", [string]$loginUrl)
                        $htmlBody = $htmlBody.Replace("{{DEFENSE_EMAIL}}", [string]$DEFENSE_EMAIL)
                    } else {
                        $htmlBody = "<h2>First Login Info</h2><p>Password: $initialPassword</p>"
                    }

                    Send-CleanSmtpMail $DEFENSE_EMAIL $subject $htmlBody

                    Write-Host "[FirstLogin] Email sent successfully to $DEFENSE_EMAIL (for $toEmail)" -ForegroundColor Green
                    Write-JsonResponse $response @{ success = $true; forwardedTo = $DEFENSE_EMAIL }
                } catch {
                    $errMsg = $_.Exception.Message
                    Write-Host "[FirstLogin] SMTP Error: $errMsg" -ForegroundColor Red
                    Write-JsonResponse $response @{ success = $false; error = $errMsg } 500
                }
                $response.Close()
                continue
            }

            # --- POST /api/send-notification ---
            if ($urlPath -eq "/api/send-notification" -and $request.HttpMethod -eq "POST") {
                try {
                    $reader   = New-Object System.IO.StreamReader($request.InputStream, [System.Text.Encoding]::UTF8)
                    $bodyText = $reader.ReadToEnd()
                    $body     = $bodyText | ConvertFrom-Json

                    $toEmail     = $body.toEmail
                    if (-not $toEmail) { $toEmail = $body.email }
                    $studentName = $body.studentName
                    $studentId   = $body.studentId
                    $advisorName = $body.advisorName
                    $notifType   = $body.type
                    $badgeText   = $body.badgeText
                    $badgeColor  = $body.badgeColor
                    $subject     = $body.subject
                    $notifTitle  = $body.notificationTitle
                    $detailsHtml = $body.detailsHtml
                    $actionUrl   = $body.actionUrl
                    $actionText  = $body.actionText

                    $DEFENSE_EMAIL = "wongsapat.u@ku.th"
                    Write-Host "[Notification] Sending $notifType notification to $toEmail & $DEFENSE_EMAIL ..." -ForegroundColor Cyan

                    $templatePath = Join-Path $PSScriptRoot "templates\email_notification.html"
                    if (Test-Path $templatePath) {
                        $htmlBody = [System.IO.File]::ReadAllText($templatePath, [System.Text.Encoding]::UTF8)
                        $htmlBody = $htmlBody.Replace("{{BADGE_TEXT}}", [string]$badgeText)
                        $htmlBody = $htmlBody.Replace("{{BADGE_COLOR}}", [string]$badgeColor)
                        $htmlBody = $htmlBody.Replace("{{NOTIFICATION_TITLE}}", [string]$notifTitle)
                        $htmlBody = $htmlBody.Replace("{{STUDENT_NAME}}", [string]$studentName)
                        $htmlBody = $htmlBody.Replace("{{STUDENT_ID}}", [string]$studentId)
                        $htmlBody = $htmlBody.Replace("{{ADVISOR_NAME}}", [string]$advisorName)
                        $htmlBody = $htmlBody.Replace("{{DETAILS_HTML}}", [string]$detailsHtml)
                        $htmlBody = $htmlBody.Replace("{{ACTION_URL}}", [string]$actionUrl)
                        $htmlBody = $htmlBody.Replace("{{ACTION_TEXT}}", [string]$actionText)
                        $htmlBody = $htmlBody.Replace("{{DEFENSE_EMAIL}}", [string]$DEFENSE_EMAIL)
                    } else {
                        $htmlBody = "<h2>$subject</h2><p>เรียน นิสิต $studentName</p><div>$detailsHtml</div>"
                    }

                    $recipients = @()
                    if ($toEmail -and $toEmail.Contains("@") -and -not $toEmail.EndsWith("example.com")) {
                        $recipients += $toEmail
                    }
                    if ($recipients -notcontains $DEFENSE_EMAIL) {
                        $recipients += $DEFENSE_EMAIL
                    }

                    foreach ($target in $recipients) {
                        try {
                            Send-CleanSmtpMail $target $subject $htmlBody
                            Write-Host "[Notification] Sent successfully to $target" -ForegroundColor Green
                        } catch {
                            $errText = $_.Exception.Message
                            Write-Host "[Notification] SMTP Error to $($target): $errText" -ForegroundColor Red
                        }
                    }

                    Write-JsonResponse $response @{ success = $true; recipients = $recipients }
                } catch {
                    $errMsg = $_.Exception.Message
                    Write-Host "[Notification] Error: $errMsg" -ForegroundColor Red
                    Write-JsonResponse $response @{ success = $false; error = $errMsg } 500
                }
                $response.Close()
                continue
            }

            # --- POST /api/send-email ---
            if ($urlPath -eq "/api/send-email" -and $request.HttpMethod -eq "POST") {
                try {
                    $reader   = New-Object System.IO.StreamReader($request.InputStream, [System.Text.Encoding]::UTF8)
                    $bodyText = $reader.ReadToEnd()
                    $body     = $bodyText | ConvertFrom-Json

                    $toEmail  = $body.to
                    if (-not $toEmail) { $toEmail = $body.email }
                    $subject  = $body.subject
                    $htmlBody = $body.htmlBody
                    if (-not $htmlBody) { $htmlBody = $body.html }
                    if (-not $htmlBody) { $htmlBody = $body.message }

                    if (-not $toEmail -or -not $subject) {
                        Write-JsonResponse $response @{ success = $false; error = "Missing to or subject" } 400
                        $response.Close()
                        continue
                    }

                    Write-Host "[SendEmail] Sending email to $toEmail" -ForegroundColor Cyan

                    Send-CleanSmtpMail $toEmail $subject $htmlBody

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

            # Fallback to docs/ folder if file not found in root
            if (-not (Test-Path $localPath -PathType Leaf)) {
                $docsPath = Join-Path (Join-Path $baseDir "docs") $decoded
                if (Test-Path $docsPath -PathType Leaf) {
                    $localPath = $docsPath
                }
            }

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
