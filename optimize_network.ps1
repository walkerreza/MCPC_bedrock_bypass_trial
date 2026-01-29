Write-Host "--- Memulai Optimasi Jaringan ---" -ForegroundColor Cyan
ipconfig /flushdns
netsh int ip reset
Write-Host "DNS Berhasil di-flush dan IP Reset selesai!" -ForegroundColor Green
Write-Host "Siap untuk menjalankan Minecraft/Bypass." -ForegroundColor Yellow

$scriptPath = $PSScriptRoot
if (-not $scriptPath) { $scriptPath = Get-Location }
$pythonScript = Join-Path $scriptPath "terminal_interface.py"

if (Test-Path $pythonScript) {
    Write-Host "Menjalankan Terminal Interface..." -ForegroundColor Cyan
    python $pythonScript
} else {
    Write-Host "File terminal_interface.py tidak ditemukan di $scriptPath" -ForegroundColor Red
}
