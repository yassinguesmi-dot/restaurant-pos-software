# APK Build Script for Windows PowerShell
# This script helps you build the APK using WSL from Windows

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Cafe216 POS APK Build (Windows)"  -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if WSL is installed
Write-Host "Checking WSL installation..." -ForegroundColor Yellow
$wslStatus = wsl --status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "WSL not installed or not configured properly" -ForegroundColor Red
    Write-Host ""
    Write-Host "To install WSL, run as Administrator:" -ForegroundColor Yellow
    Write-Host "  wsl --install -d Ubuntu-22.04" -ForegroundColor White
    Write-Host ""
    Write-Host "Then restart your computer and run this script again." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "See WSL_TROUBLESHOOTING.md for alternative build methods" -ForegroundColor Cyan
    pause
    exit 1
}

Write-Host "WSL is installed" -ForegroundColor Green

# Try to restart WSL service
Write-Host ""
Write-Host "Restarting WSL service..." -ForegroundColor Yellow
wsl --shutdown
Start-Sleep -Seconds 3

# Get current directory
$currentDir = Get-Location
$projectPath = $currentDir.Path

# Convert Windows path to WSL path
$wslPath = $projectPath -replace '^([A-Z]):', '/mnt/$1' -replace '\\', '/'
$wslPath = $wslPath.ToLower()

Write-Host "Project path (Windows): $projectPath" -ForegroundColor Cyan
Write-Host "Project path (WSL): $wslPath" -ForegroundColor Cyan

# Check if we're in the correct folder
if (Test-Path "main_kivy.py") {
    Write-Host ""
    Write-Host "Found main_kivy.py in current directory" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Cannot find main_kivy.py in current directory" -ForegroundColor Red
    Write-Host "Please run this script from the restaurant-pos-software (1) folder" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Building APK..."  -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Build commands for WSL
$buildCommands = "cd '$wslPath' && echo 'Starting build...' && buildozer -v android debug"

try {
    # Execute build in WSL
    Write-Host "Executing build in WSL Ubuntu..." -ForegroundColor Yellow
    Write-Host "(This may take 30-60 minutes on first build)" -ForegroundColor Yellow
    Write-Host ""
    
    wsl -d Ubuntu-22.04 bash -c $buildCommands
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=========================================" -ForegroundColor Green
        Write-Host "  BUILD SUCCESSFUL!"  -ForegroundColor Green
        Write-Host "=========================================" -ForegroundColor Green
        Write-Host ""
        
        # Check for APK file
        $apkPath = Join-Path $projectPath "bin\*.apk"
        $apkFiles = Get-ChildItem $apkPath -ErrorAction SilentlyContinue
        
        if ($apkFiles) {
            Write-Host "APK Location:" -ForegroundColor Cyan
            foreach ($apk in $apkFiles) {
                Write-Host "  $($apk.FullName)" -ForegroundColor White
                Write-Host "  Size: $([math]::Round($apk.Length / 1MB, 2)) MB" -ForegroundColor White
            }
            Write-Host ""
            Write-Host "To install on Android device:" -ForegroundColor Yellow
            Write-Host "  1. Copy APK to your device" -ForegroundColor White
            Write-Host "  2. Open the APK file on device" -ForegroundColor White
            Write-Host "  3. Allow installation from unknown sources" -ForegroundColor White
            Write-Host "  4. Install and enjoy!" -ForegroundColor White
        } else {
            Write-Host "APK file not found in expected location." -ForegroundColor Yellow
            Write-Host "Check the bin folder manually." -ForegroundColor Yellow
        }
    } else {
        Write-Host ""
        Write-Host "=========================================" -ForegroundColor Red
        Write-Host "  BUILD FAILED"  -ForegroundColor Red
        Write-Host "=========================================" -ForegroundColor Red
        Write-Host ""
        Write-Host "Common issues:" -ForegroundColor Yellow
        Write-Host "  1. WSL service issues - Try: wsl --shutdown, then restart" -ForegroundColor White
        Write-Host "  2. First build needs system dependencies installed" -ForegroundColor White
        Write-Host "  3. Network connectivity required for downloads" -ForegroundColor White
        Write-Host ""
        Write-Host "See APK_BUILD_GUIDE.md for detailed troubleshooting" -ForegroundColor Yellow
        Write-Host "See WSL_TROUBLESHOOTING.md for alternative methods" -ForegroundColor Cyan
    }
    
} catch {
    Write-Host ""
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "WSL may not be starting properly. Try:" -ForegroundColor Yellow
    Write-Host "  1. wsl --shutdown" -ForegroundColor White
    Write-Host "  2. Restart your computer" -ForegroundColor White
    Write-Host "  3. Run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "See WSL_TROUBLESHOOTING.md for alternative build methods" -ForegroundColor Cyan
}

Write-Host ""
pause
