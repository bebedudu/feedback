# PowerShell compilation script for feedback.py
# Multi-monitor screenshot support included

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "    FEEDBACK APPLICATION COMPILATION" -ForegroundColor Cyan
Write-Host "    Multi-Monitor Screenshot Support" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if feedback.py exists
if (-not (Test-Path "feedback.py")) {
    Write-Host "ERROR: feedback.py not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Found feedback.py" -ForegroundColor Green

# Check Python installation
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found or not in PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install/upgrade required packages
Write-Host ""
Write-Host "📦 Installing/upgrading required packages..." -ForegroundColor Yellow

$packages = @(
    "pyinstaller>=5.0",
    "pillow>=9.0.0", 
    "pyautogui>=0.9.54",
    "pyperclip>=1.8.2",
    "pynput>=1.7.6",
    "plyer>=2.1.0",
    "pystray>=0.19.4",
    "psutil>=5.9.0",
    "requests>=2.28.0",
    "pygetwindow>=0.0.9",
    "pywin32>=304"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Cyan
    pip install $package --quiet
}

# Clean previous builds
Write-Host ""
Write-Host "🧹 Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "feedback.exe") { Remove-Item -Force "feedback.exe" }

# Create necessary directories
Write-Host "📁 Creating directory structure..." -ForegroundColor Yellow
$directories = @("assets", "assets\image", "assets\schedule", "logs", "screenshots")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created: $dir" -ForegroundColor Green
    }
}

# PyInstaller command with all necessary options
Write-Host ""
Write-Host "🔨 Compiling with PyInstaller..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Cyan

$pyinstallerArgs = @(
    "feedback.py",
    "--onefile",
    "--windowed",
    "--name=feedback",
    "--add-data=assets;assets",
    "--hidden-import=win32gui",
    "--hidden-import=win32ui", 
    "--hidden-import=win32api",
    "--hidden-import=win32con",
    "--hidden-import=PIL.Image",
    "--hidden-import=PIL.ImageDraw",
    "--hidden-import=pynput.keyboard",
    "--hidden-import=pynput.mouse",
    "--hidden-import=plyer.platforms.win.notification",
    "--hidden-import=pystray._win32",
    "--hidden-import=pygetwindow",
    "--hidden-import=ctypes.wintypes",
    "--exclude-module=matplotlib",
    "--exclude-module=numpy",
    "--exclude-module=scipy",
    "--exclude-module=pandas",
    "--clean",
    "--noconfirm"
)

# Add icon if it exists
if (Test-Path "assets\image\icon.ico") {
    $pyinstallerArgs += "--icon=assets\image\icon.ico"
    Write-Host "✅ Using custom icon" -ForegroundColor Green
}

try {
    & pyinstaller @pyinstallerArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Compilation successful!" -ForegroundColor Green
        
        # Copy executable to current directory
        if (Test-Path "dist\feedback.exe") {
            Copy-Item "dist\feedback.exe" "feedback.exe"
            $fileSize = (Get-Item "feedback.exe").Length / 1MB
            Write-Host "📦 Created: feedback.exe ($([math]::Round($fileSize, 1)) MB)" -ForegroundColor Green
            
            Write-Host ""
            Write-Host "================================================" -ForegroundColor Cyan
            Write-Host "    COMPILATION COMPLETED SUCCESSFULLY!" -ForegroundColor Green
            Write-Host "================================================" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "🚀 Features included:" -ForegroundColor Yellow
            Write-Host "   ✅ Multi-monitor screenshot support" -ForegroundColor Green
            Write-Host "   ✅ Keylogging functionality" -ForegroundColor Green
            Write-Host "   ✅ Clipboard monitoring" -ForegroundColor Green
            Write-Host "   ✅ System tray integration" -ForegroundColor Green
            Write-Host "   ✅ Auto-upload to GitHub" -ForegroundColor Green
            Write-Host "   ✅ Auto-update functionality" -ForegroundColor Green
            Write-Host "   ✅ Windows startup integration" -ForegroundColor Green
            Write-Host ""
            Write-Host "💡 Test the multi-monitor feature using:" -ForegroundColor Cyan
            Write-Host "   1. Run feedback.exe" -ForegroundColor White
            Write-Host "   2. Press PrtSc to show tray icon" -ForegroundColor White
            Write-Host "   3. Right-click → 'Test Multi-Monitor Screenshot'" -ForegroundColor White
            
        } else {
            Write-Host "❌ Executable not found in dist folder" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Compilation failed!" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error during compilation: $_" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"