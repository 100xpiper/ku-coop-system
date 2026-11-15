$SMTP_USER = 'per.300846@gmail.com'
$SMTP_PASS = 'bpbvozebtiqmmslk'
$credential = New-Object System.Management.Automation.PSCredential($SMTP_USER, (ConvertTo-SecureString $SMTP_PASS -AsPlainText -Force))
try {
    Write-Host 'Testing SMTP connection to smtp.gmail.com:587...'
    Send-MailMessage -SmtpServer 'smtp.gmail.com' -Port 587 -UseSsl -Credential $credential -From "ระบบนิเทศสหกิจศึกษา KU <$SMTP_USER>" -To 'wongsapat.u@ku.th' -Subject 'ทดสอบระบบส่ง OTP สหกิจศึกษา KU' -Body 'ทดสอบส่งรหัส OTP เข้าสู่ wongsapat.u@ku.th สำเร็จ' -Encoding UTF8
    Write-Host 'SMTP TEST SUCCESSFUL!' -ForegroundColor Green
} catch {
    Write-Host "SMTP Error: $($_.Exception.Message)" -ForegroundColor Red
}
