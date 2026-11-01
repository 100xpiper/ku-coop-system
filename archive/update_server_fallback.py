with open('server.ps1', 'r', encoding='utf-8') as f:
    text = f.read()

target = """            $decoded   = [System.Uri]::UnescapeDataString($urlPath).TrimStart('/')
            $localPath = Join-Path $baseDir $decoded"""

replacement = """            $decoded   = [System.Uri]::UnescapeDataString($urlPath).TrimStart('/')
            $localPath = Join-Path $baseDir $decoded

            # Fallback to docs/ folder if file not found in root
            if (-not (Test-Path $localPath -PathType Leaf)) {
                $docsPath = Join-Path (Join-Path $baseDir "docs") $decoded
                if (Test-Path $docsPath -PathType Leaf) {
                    $localPath = $docsPath
                }
            }"""

if target in text:
    text = text.replace(target, replacement, 1)
    with open('server.ps1', 'w', encoding='utf-8') as f:
        f.write(text)
    print("server.ps1 updated successfully with docs fallback!")
else:
    print("Target not found in server.ps1!")
