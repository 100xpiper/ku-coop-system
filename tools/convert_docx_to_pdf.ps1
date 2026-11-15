$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pyScript = Join-Path $scriptDir "convert_docx_to_pdf.py"
& "$HOME\.local\bin\uv.exe" run --with pywin32 python $pyScript
