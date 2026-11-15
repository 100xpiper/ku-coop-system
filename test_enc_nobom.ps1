
$txt = "รหัส OTP เข้าสู่ระบบนิเทศสหกิจศึกษา KU: 123456"
Write-Host "PS Output: $txt"
$bytes = [System.Text.Encoding]::UTF8.GetBytes($txt)
Write-Host "Byte len: $($bytes.Length)"
