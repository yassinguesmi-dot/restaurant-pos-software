# Fix WSL Service Issues
# Run this if WSL is not starting

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  WSL Service Restart"  -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Shutting down WSL..." -ForegroundColor Yellow
wsl --shutdown
Start-Sleep -Seconds 5

Write-Host "✓ WSL shutdown complete" -ForegroundColor Green
Write-Host ""

Write-Host "Step 2: Checking WSL status..." -ForegroundColor Yellow
$distributions = wsl --list --verbose

Write-Host $distributions
Write-Host ""

Write-Host "Step 3: Starting Ubuntu 22.04..." -ForegroundColor Yellow
Write-Host ""

# Try to start WSL
$result = wsl -d Ubuntu-22.04 -- echo "WSL is now running!"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ WSL started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run:" -ForegroundColor Yellow
    Write-Host "  .\build_apk.ps1" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✗ WSL failed to start" -ForegroundColor Red
    Write-Host ""
    Write-Host "This might be a deeper system issue. Try:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option 1: Restart Windows Services" -ForegroundColor Cyan
    Write-Host "  1. Open Services (services.msc)" -ForegroundColor White
    Write-Host "  2. Find 'LxssManager' service" -ForegroundColor White
    Write-Host "  3. Right-click > Restart" -ForegroundColor White
    Write-Host ""
    Write-Host "Option 2: Reinstall WSL distribution" -ForegroundColor Cyan
    Write-Host "  wsl --unregister Ubuntu-22.04" -ForegroundColor White
    Write-Host "  wsl --install -d Ubuntu-22.04" -ForegroundColor White
    Write-Host ""
    Write-Host "Option 3: Use alternative build methods" -ForegroundColor Cyan
    Write-Host "  See QUICKSTART.md for Pydroid 3 method" -ForegroundColor White
    Write-Host ""
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
