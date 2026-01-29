$repoUrl = "https://raw.githubusercontent.com/walkerreza/MCPC_bedrock_bypass_trial/main"
$workDir = Join-Path $env:TEMP "MCPC_Bypass"

# Buat folder temp jika belum ada
if (-not (Test-Path $workDir)) { 
    New-Item -ItemType Directory -Force -Path $workDir | Out-Null 
}

$pythonScript = Join-Path $workDir "terminal_interface.py"

Write-Host "📥 Downloading terminal_interface.py from GitHub..." -ForegroundColor Cyan
try {
    Invoke-WebRequest -Uri "$repoUrl/terminal_interface.py" -OutFile $pythonScript -UseBasicParsing
} catch {
    Write-Host "❌ Gagal mendownload file: $_" -ForegroundColor Red
    exit
}

if (Test-Path $pythonScript) {
    Set-Location $workDir
    Write-Host "✅ Berhasil didownload!" -ForegroundColor Green
    Write-Host "🚀 Menjalankan Minecraft Bedrock Bypass Tool..." -ForegroundColor Cyan
    python $pythonScript
} else {
    Write-Host "❌ File terminal_interface.py gagal disimpan." -ForegroundColor Red
}
