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
Write-Host " Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Green
Start-Process "http://localhost:$port"

$baseDir = $PSScriptRoot

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

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        try {
            $request = $context.Request
            $response = $context.Response

            $urlPath = $request.Url.LocalPath
            if ($urlPath -eq "/" -or [string]::IsNullOrWhiteSpace($urlPath)) {
                $urlPath = "/index.html"
            }

            $decoded = [System.Uri]::UnescapeDataString($urlPath).TrimStart('/')
            $localPath = Join-Path $baseDir $decoded

            if (Test-Path $localPath -PathType Leaf) {
                $ext = [System.IO.Path]::GetExtension($localPath).ToLower()
                $contentType = "application/octet-stream"
                if ($mimeTypes.ContainsKey($ext)) {
                    $contentType = $mimeTypes[$ext]
                }
                $response.ContentType = $contentType
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
