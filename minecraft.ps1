$scriptPath = $PSScriptRoot
if (-not $scriptPath) { $scriptPath = Get-Location }
$pythonScript = Join-Path $scriptPath "terminal_interface.py"

if (Test-Path $pythonScript) {
    Write-Host "Menjalankan Minecraft Bedrock Bypass Tool..." -ForegroundColor Cyan
    python $pythonScript
} else {
    Write-Host "File terminal_interface.py tidak ditemukan di $scriptPath" -ForegroundColor Red
}
