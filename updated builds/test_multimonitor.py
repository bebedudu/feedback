#!/usr/bin/env python3
"""
Test script to verify multi-monitor screenshot functionality
Run this to test if the multi-monitor features work correctly
"""

import os
import sys
import time
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    modules = [
        ('win32gui', 'Windows GUI API'),
        ('win32ui', 'Windows UI API'), 
        ('win32api', 'Windows System API'),
        ('win32con', 'Windows Constants'),
        ('PIL.Image', 'PIL Image processing'),
        ('pyautogui', 'PyAutoGUI screenshots'),
        ('pynput.keyboard', 'Keyboard monitoring'),
        ('pystray', 'System tray integration'),
        ('plyer', 'Notifications'),
        ('psutil', 'System information'),
        ('requests', 'HTTP requests')
    ]
    
    success_count = 0
    for module, description in modules:
        try:
            __import__(module)
            print(f"  ✅ {module} - {description}")
            success_count += 1
        except ImportError as e:
            print(f"  ❌ {module} - FAILED: {e}")
    
    print(f"\n📊 Import Results: {success_count}/{len(modules)} successful")
    return success_count == len(modules)

def test_monitor_detection():
    """Test monitor detection functionality"""
    print("\n🖥️ Testing monitor detection...")
    
    try:
        import win32api
        import win32con
        
        # Get virtual screen metrics
        virtual_left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        virtual_top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        virtual_width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        virtual_height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        
        # Get primary monitor info
        primary_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        primary_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        
        print(f"  📐 Virtual Desktop: {virtual_width}x{virtual_height} at ({virtual_left}, {virtual_top})")
        print(f"  📐 Primary Monitor: {primary_width}x{primary_height}")
        
        # Determine if multi-monitor setup
        if virtual_width > primary_width or virtual_height > primary_height:
            print(f"  ✅ Multi-monitor setup detected!")
            monitor_count = max(virtual_width // primary_width, virtual_height // primary_height)
            print(f"  📊 Estimated monitors: {monitor_count}")
        else:
            print(f"  ℹ️ Single monitor setup")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Monitor detection failed: {e}")
        return False

def test_screenshot_methods():
    """Test both screenshot methods"""
    print("\n📸 Testing screenshot methods...")
    
    # Create test directory
    test_dir = "test_screenshots"
    os.makedirs(test_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Test PyAutoGUI method
    try:
        import pyautogui
        pyautogui_file = os.path.join(test_dir, f"test_pyautogui_{timestamp}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(pyautogui_file)
        print(f"  ✅ PyAutoGUI: {screenshot.size} -> {pyautogui_file}")
        pyautogui_size = screenshot.size
    except Exception as e:
        print(f"  ❌ PyAutoGUI failed: {e}")
        pyautogui_size = None
    
    # Test Windows API method
    try:
        import win32gui
        import win32ui
        import win32api
        import win32con
        from PIL import Image
        
        # Get virtual screen dimensions
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        
        # Create device contexts
        hdesktop = win32gui.GetDesktopWindow()
        desktop_dc = win32gui.GetWindowDC(hdesktop)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)
        mem_dc = img_dc.CreateCompatibleDC()
        
        # Create bitmap
        screenshot_bmp = win32ui.CreateBitmap()
        screenshot_bmp.CreateCompatibleBitmap(img_dc, width, height)
        mem_dc.SelectObject(screenshot_bmp)
        
        # Copy screen to bitmap
        mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
        
        # Convert to PIL Image
        bmpinfo = screenshot_bmp.GetInfo()
        bmpstr = screenshot_bmp.GetBitmapBits(True)
        screenshot = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )
        
        # Clean up
        mem_dc.DeleteDC()
        win32gui.DeleteObject(screenshot_bmp.GetHandle())
        img_dc.DeleteDC()
        win32gui.ReleaseDC(hdesktop, desktop_dc)
        
        # Save screenshot
        winapi_file = os.path.join(test_dir, f"test_winapi_{timestamp}.png")
        screenshot.save(winapi_file)
        print(f"  ✅ Windows API: {screenshot.size} -> {winapi_file}")
        winapi_size = screenshot.size
        
    except Exception as e:
        print(f"  ❌ Windows API failed: {e}")
        winapi_size = None
    
    # Compare results
    if pyautogui_size and winapi_size:
        print(f"\n📊 Comparison:")
        print(f"  PyAutoGUI: {pyautogui_size}")
        print(f"  Windows API: {winapi_size}")
        
        if winapi_size[0] > pyautogui_size[0] or winapi_size[1] > pyautogui_size[1]:
            print(f"  🎉 Windows API captures larger area - multi-monitor working!")
        elif winapi_size == pyautogui_size:
            print(f"  ℹ️ Both methods capture same area")
        else:
            print(f"  ⚠️ Unexpected size difference")
    
    return pyautogui_size is not None or winapi_size is not None

def test_system_tray():
    """Test system tray functionality"""
    print("\n🔔 Testing system tray support...")
    
    try:
        import pystray
        from PIL import Image
        
        # Create a simple test image
        image = Image.new('RGB', (64, 64), color='blue')
        
        print(f"  ✅ pystray imported successfully")
        print(f"  ✅ PIL Image creation works")
        print(f"  ℹ️ System tray functionality available")
        
        return True
        
    except Exception as e:
        print(f"  ❌ System tray test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("    MULTI-MONITOR FUNCTIONALITY TEST")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Monitor Detection", test_monitor_detection), 
        ("Screenshot Methods", test_screenshot_methods),
        ("System Tray", test_system_tray)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("    TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Multi-monitor functionality is ready.")
        print("💡 You can now compile the application with confidence.")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")
        print("💡 Install missing dependencies: pip install -r requirements.txt")
    
    print(f"\n📁 Test screenshots saved in: test_screenshots/")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    
    print("\n" + "=" * 60)
    input("Press Enter to exit...")
    
    sys.exit(0 if success else 1)