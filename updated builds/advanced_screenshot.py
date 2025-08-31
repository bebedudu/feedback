import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyautogui
from PIL import Image, ImageTk
import os
from datetime import datetime
import threading
import keyboard
import json
import sys

# Windows-specific imports for better multi-monitor support
if sys.platform == "win32":
    import win32gui
    import win32ui
    import win32con
    import win32api

class MultiMonitorScreenshot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Multi-Monitor Screenshot Tool")
        self.root.geometry("500x400")
        
        # Load settings
        self.settings_file = "screenshot_settings.json"
        self.load_settings()
        
        # Setup GUI
        self.setup_gui()
        
        # Setup hotkey
        self.setup_hotkey()
        
    def load_settings(self):
        """Load settings from JSON file"""
        default_settings = {
            "save_path": os.path.expanduser("~/Pictures/Screenshots"),
            "file_format": "PNG",
            "hotkey": "ctrl+shift+s",
            "auto_save": True,
            "show_preview": True
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
            else:
                self.settings = default_settings
        except:
            self.settings = default_settings
            
        # Ensure save directory exists
        os.makedirs(self.settings["save_path"], exist_ok=True)
    
    def save_settings(self):
        """Save current settings to JSON file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def setup_gui(self):
        """Setup the main GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Multi-Monitor Screenshot Tool", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Screenshot button
        screenshot_btn = ttk.Button(main_frame, text="Take Screenshot", 
                                  command=self.take_screenshot_threaded,
                                  style="Accent.TButton")
        screenshot_btn.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Save path
        ttk.Label(settings_frame, text="Save Path:").grid(row=0, column=0, sticky=tk.W)
        self.path_var = tk.StringVar(value=self.settings["save_path"])
        path_entry = ttk.Entry(settings_frame, textvariable=self.path_var, width=40)
        path_entry.grid(row=0, column=1, padx=(5, 0))
        browse_btn = ttk.Button(settings_frame, text="Browse", 
                               command=self.browse_folder)
        browse_btn.grid(row=0, column=2, padx=(5, 0))
        
        # File format
        ttk.Label(settings_frame, text="Format:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.format_var = tk.StringVar(value=self.settings["file_format"])
        format_combo = ttk.Combobox(settings_frame, textvariable=self.format_var, 
                                   values=["PNG", "JPEG", "BMP"], state="readonly")
        format_combo.grid(row=1, column=1, sticky=tk.W, pady=(10, 0), padx=(5, 0))
        
        # Hotkey
        ttk.Label(settings_frame, text="Hotkey:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.hotkey_var = tk.StringVar(value=self.settings["hotkey"])
        hotkey_entry = ttk.Entry(settings_frame, textvariable=self.hotkey_var, width=20)
        hotkey_entry.grid(row=2, column=1, sticky=tk.W, pady=(10, 0), padx=(5, 0))
        
        # Checkboxes
        self.auto_save_var = tk.BooleanVar(value=self.settings["auto_save"])
        auto_save_cb = ttk.Checkbutton(settings_frame, text="Auto-save screenshots", 
                                      variable=self.auto_save_var)
        auto_save_cb.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        self.preview_var = tk.BooleanVar(value=self.settings["show_preview"])
        preview_cb = ttk.Checkbutton(settings_frame, text="Show preview after capture", 
                                    variable=self.preview_var)
        preview_cb.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Save settings button
        save_settings_btn = ttk.Button(settings_frame, text="Save Settings", 
                                      command=self.update_settings)
        save_settings_btn.grid(row=5, column=0, columnspan=2, pady=(15, 0))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to capture screenshots")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        # Monitor info
        self.update_monitor_info()
        
    def get_monitor_info_windows(self):
        """Get monitor information using Windows API"""
        try:
            monitors = []
            
            # Get virtual screen metrics
            virtual_left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            virtual_top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
            virtual_width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            virtual_height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            
            # Get primary monitor info
            primary_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
            primary_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
            
            # Add primary monitor
            monitors.append({
                'left': 0,
                'top': 0,
                'width': primary_width,
                'height': primary_height,
                'primary': True
            })
            
            # If virtual screen is larger than primary, we have multiple monitors
            if virtual_width > primary_width or virtual_height > primary_height:
                # Estimate additional monitors (this is a simplified approach)
                if virtual_width > primary_width:
                    # Likely side-by-side setup
                    secondary_width = virtual_width - primary_width
                    monitors.append({
                        'left': primary_width,
                        'top': 0,
                        'width': secondary_width,
                        'height': primary_height,
                        'primary': False
                    })
                
                if virtual_height > primary_height:
                    # Likely stacked setup
                    secondary_height = virtual_height - primary_height
                    monitors.append({
                        'left': 0,
                        'top': primary_height,
                        'width': primary_width,
                        'height': secondary_height,
                        'primary': False
                    })
            
            return monitors
        except Exception as e:
            print(f"Windows monitor info failed: {e}")
            return []
    
    def update_monitor_info(self):
        """Display information about connected monitors"""
        try:
            monitors = []
            
            # Try Windows-specific method first
            if sys.platform == "win32":
                monitors = self.get_monitor_info_windows()
            
            # Fallback to getting screen size info
            if not monitors:
                # Get basic screen info as fallback
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                monitors = [{'left': 0, 'top': 0, 'width': screen_width, 'height': screen_height, 'primary': True}]
            
            info_text = f"Detected {len(monitors)} monitor(s):\n"
            
            for i, monitor in enumerate(monitors):
                primary_text = " (Primary)" if monitor.get('primary', False) else ""
                info_text += f"Monitor {i+1}: {monitor['width']}x{monitor['height']} at ({monitor['left']}, {monitor['top']}){primary_text}\n"
            
            # Add virtual screen info for Windows
            if sys.platform == "win32":
                try:
                    virtual_width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
                    virtual_height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
                    info_text += f"\nVirtual Desktop: {virtual_width}x{virtual_height}"
                except:
                    pass
            
            # Add info label
            info_frame = ttk.LabelFrame(self.root, text="Monitor Information", padding="10")
            info_frame.grid(row=1, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))
            
            info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
            info_label.grid(row=0, column=0, sticky=tk.W)
            
        except Exception as e:
            print(f"Error getting monitor info: {e}")
            # Create a basic info frame even if monitor detection fails
            try:
                info_frame = ttk.LabelFrame(self.root, text="Monitor Information", padding="10")
                info_frame.grid(row=1, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))
                
                info_label = ttk.Label(info_frame, text="Monitor information unavailable", justify=tk.LEFT)
                info_label.grid(row=0, column=0, sticky=tk.W)
            except:
                pass
    
    def browse_folder(self):
        """Browse for save folder"""
        folder = filedialog.askdirectory(initialdir=self.path_var.get())
        if folder:
            self.path_var.set(folder)
    
    def update_settings(self):
        """Update settings from GUI"""
        self.settings["save_path"] = self.path_var.get()
        self.settings["file_format"] = self.format_var.get()
        self.settings["hotkey"] = self.hotkey_var.get()
        self.settings["auto_save"] = self.auto_save_var.get()
        self.settings["show_preview"] = self.preview_var.get()
        
        # Ensure save directory exists
        os.makedirs(self.settings["save_path"], exist_ok=True)
        
        self.save_settings()
        self.setup_hotkey()  # Update hotkey
        messagebox.showinfo("Settings", "Settings saved successfully!")
    
    def setup_hotkey(self):
        """Setup global hotkey for screenshot"""
        try:
            # Remove existing hotkey
            keyboard.unhook_all()
            
            # Add new hotkey
            keyboard.add_hotkey(self.settings["hotkey"], self.take_screenshot_threaded)
            self.status_var.set(f"Hotkey active: {self.settings['hotkey']}")
        except Exception as e:
            self.status_var.set(f"Hotkey error: {e}")
    
    def take_screenshot_threaded(self):
        """Take screenshot in a separate thread to avoid GUI freezing"""
        threading.Thread(target=self.take_screenshot, daemon=True).start()
    
    def take_screenshot_windows(self):
        """Windows-specific method to capture all monitors using Win32 API"""
        try:
            # Get the virtual screen dimensions (all monitors combined)
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
            
            return screenshot
            
        except Exception as e:
            print(f"Windows screenshot method failed: {e}")
            return None
    
    def take_screenshot(self):
        """Capture screenshot of all monitors"""
        try:
            self.status_var.set("Taking screenshot...")
            self.root.update()
            
            screenshot = None
            
            # Try Windows-specific method first (more reliable for multi-monitor)
            if sys.platform == "win32":
                try:
                    screenshot = self.take_screenshot_windows()
                except Exception as e:
                    print(f"Windows method failed, trying pyautogui: {e}")
            
            # Fallback to pyautogui method
            if screenshot is None:
                # Simple fallback - just take a screenshot of the entire screen
                # This may not capture all monitors perfectly but will work as basic fallback
                screenshot = pyautogui.screenshot()
            
            if screenshot is None:
                raise Exception("Failed to capture screenshot")
            
            if self.settings["auto_save"]:
                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.{self.settings['file_format'].lower()}"
                filepath = os.path.join(self.settings["save_path"], filename)
                
                # Save screenshot
                screenshot.save(filepath, self.settings["file_format"])
                self.status_var.set(f"Screenshot saved: {filename}")
                
                # Show success message
                self.root.after(0, lambda: messagebox.showinfo("Success", 
                    f"Screenshot saved to:\n{filepath}"))
            
            if self.settings["show_preview"]:
                self.show_preview(screenshot)
                
        except Exception as e:
            error_msg = f"Error taking screenshot: {e}"
            self.status_var.set(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
    
    def show_preview(self, screenshot):
        """Show preview of the captured screenshot"""
        try:
            # Create preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Screenshot Preview")
            preview_window.geometry("800x600")
            
            # Resize image for preview
            img_width, img_height = screenshot.size
            max_width, max_height = 780, 500
            
            if img_width > max_width or img_height > max_height:
                ratio = min(max_width/img_width, max_height/img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                preview_img = screenshot.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                preview_img = screenshot
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(preview_img)
            
            # Create label with image
            img_label = ttk.Label(preview_window, image=photo)
            img_label.image = photo  # Keep a reference
            img_label.pack(pady=10)
            
            # Buttons frame
            btn_frame = ttk.Frame(preview_window)
            btn_frame.pack(pady=10)
            
            # Save button
            def save_screenshot():
                try:
                    filename = filedialog.asksaveasfilename(
                        defaultextension=f".{self.settings['file_format'].lower()}",
                        filetypes=[
                            (f"{self.settings['file_format']} files", f"*.{self.settings['file_format'].lower()}"),
                            ("All files", "*.*")
                        ]
                    )
                    if filename:
                        screenshot.save(filename, self.settings["file_format"])
                        messagebox.showinfo("Success", f"Screenshot saved to:\n{filename}")
                        preview_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save screenshot: {e}")
            
            ttk.Button(btn_frame, text="Save As...", command=save_screenshot).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Close", command=preview_window.destroy).pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Failed to show preview: {e}")
    
    def run(self):
        """Start the application"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
    
    def on_closing(self):
        """Handle application closing"""
        try:
            keyboard.unhook_all()
            self.root.destroy()
        except:
            pass

if __name__ == "__main__":
    app = MultiMonitorScreenshot()
    app.run()