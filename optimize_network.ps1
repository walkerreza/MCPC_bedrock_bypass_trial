Write-Host "--- Memulai Optimasi Jaringan ---" -ForegroundColor Cyan
ipconfig /flushdns
netsh int ip reset
Write-Host "DNS Berhasil di-flush dan IP Reset selesai!" -ForegroundColor Green
Write-Host "Siap untuk menjalankan Minecraft/Bypass." -ForegroundColor Yellow
