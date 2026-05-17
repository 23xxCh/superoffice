"""
SuperOffice Office Automation - COM automation for Microsoft Office
Based on OfficeMCP project
"""

import os
import sys
import win32com.client
import win32api
import win32con
import win32process
import win32gui
import win32clipboard
from win32com.client import GetActiveObject, CDispatch
import pythoncom
import subprocess
import webbrowser
import json
from pathlib import Path

# Default root folder
DEFAULT_ROOT = r"D:\@SuperOffice"


class TheOfficer:
    """Manages Windows Office COM automation"""

    MicrosoftApplications = [
        'Word', 'Excel', 'PowerPoint',
        'Visio', 'Access', 'MSProject',
        'Outlook', 'Publisher', "OneNote",
        "Kwps", "Ket", "Kwpp"  # WPS Office
    ]

    ProgIDs = {
        'Word': 'Word.Application',
        'Excel': 'Excel.Application',
        'PowerPoint': 'PowerPoint.Application',
        'Access': 'Access.Application',
        'Outlook': 'Outlook.Application',
        'Visio': 'Visio.Application',
        'MSProject': 'MSProject.Application',
        'Publisher': 'Publisher.Application',
        'OneNote': 'OneNote.Application',
        'Kwps': 'Kwps.Application',  # WPS Writer
        'Ket': 'Ket.Application',    # WPS Spreadsheets
        'Kwpp': 'Kwpp.Application',  # WPS Presentation
    }

    def __init__(self, root_folder=None):
        self.root_folder = root_folder or DEFAULT_ROOT
        os.makedirs(self.root_folder, exist_ok=True)
        self.apps = {}

    def _get_progid(self, app_name):
        """Get COM ProgID for application"""
        return self.ProgIDs.get(app_name, f"{app_name}.Application")

    def _get_running_app(self, progid):
        """Try to get a running instance"""
        try:
            return win32com.client.GetActiveObject(progid)
        except:
            return None

    def _create_app(self, progid):
        """Create a new instance"""
        return win32com.client.Dispatch(progid)

    def get_app(self, app_name):
        """Get or create Office application instance"""
        if app_name in self.apps:
            return self.apps[app_name]

        progid = self._get_progid(app_name)

        # Try to attach to running instance first
        app = self._get_running_app(progid)
        if app is None:
            # Create new instance
            app = self._create_app(progid)

        self.apps[app_name] = app
        return app

    def is_app_available(self, app_name):
        """Check if app is installed via registry"""
        try:
            import winreg
            key_path = f"SOFTWARE\\Classes\\{self._get_progid(app_name)}"
            key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path)
            winreg.CloseKey(key)
            return True
        except:
            return False

    def get_available_apps(self):
        """Return list of available Office apps"""
        available = []
        for app in self.MicrosoftApplications:
            if self.is_app_available(app):
                available.append(app)
        return available

    def get_running_apps(self):
        """Return list of running Office apps"""
        running = []
        for app_name in self.MicrosoftApplications:
            try:
                progid = self._get_progid(app_name)
                app = win32com.client.GetActiveObject(progid)
                running.append(app_name)
            except:
                pass
        return running

    def launch_app(self, app_name, visible=True):
        """Launch an Office application"""
        app = self.get_app(app_name)
        app.Visible = visible
        return f"{app_name} launched"

    def set_visible(self, app_name, visible):
        """Set app visibility"""
        app = self.get_app(app_name)
        app.Visible = visible
        return f"{app_name} visibility set to {visible}"

    def quit_app(self, app_name, force=False):
        """Quit an Office application"""
        if app_name in self.apps:
            app = self.apps[app_name]
            try:
                if force:
                    # Force kill process
                    pid = app.ProcessID
                    subprocess.run(['taskkill', '/PID', str(pid), '/F'])
                else:
                    app.Quit()
                del self.apps[app_name]
            except Exception as e:
                return f"Error: {str(e)}"
        return f"{app_name} quit"

    def speak(self, text, volume=100, rate=0):
        """Speak text using Windows SAPI"""
        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Volume = volume
            speaker.Rate = rate
            speaker.Speak(text)
            return "Speech completed"
        except Exception as e:
            return f"Error: {str(e)}"

    def beep(self, frequency=1000, duration=500):
        """Play system beep"""
        import winsound
        winsound.Beep(frequency, duration)
        return "Beep played"

    def screenshot(self, save_path=None):
        """Capture full screen"""
        try:
            import win32ui
            import win32gui
            import win32con
            from PIL import Image

            hwnd = win32gui.GetDesktopWindow()
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top

            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()

            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            saveDC.SelectObject(saveBitMap)

            result = saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            img = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )

            if save_path is None:
                save_path = os.path.join(self.root_folder, "screenshot.png")

            img.save(save_path)

            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)

            return f"Screenshot saved to {save_path}"
        except Exception as e:
            return f"Error: {str(e)}"

    def download_image(self, url, save_path):
        """Download image from URL"""
        try:
            import urllib.request

            if not save_path:
                filename = url.split('/')[-1]
                save_path = os.path.join(self.root_folder, filename)

            urllib.request.urlretrieve(url, save_path)
            return f"Image saved to {save_path}"
        except Exception as e:
            return f"Error: {str(e)}"

    def run_python(self, code, data=""):
        """Execute Python code with Officer in namespace"""
        try:
            namespace = {
                'Officer': self,
                'data': data,
                'output': None,
                '__name__': '__main__'
            }
            exec(code, namespace)
            result = namespace.get('output', 'Code executed')
            return {"success": True, "output": str(result)}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Singleton instance
_officer = None


def get_officer():
    """Get singleton officer instance"""
    global _officer
    if _officer is None:
        _officer = TheOfficer()
    return _officer


# MCP Tool Functions (to be called by AI agent)
def available_apps():
    """Get list of available Office apps"""
    officer = get_officer()
    return officer.get_available_apps()


def running_apps():
    """Get list of running Office apps"""
    officer = get_officer()
    return officer.get_running_apps()


def is_app_available(app_name="Word"):
    """Check if app is available"""
    officer = get_officer()
    return officer.is_app_available(app_name)


def launch_app(app_name, visible=True):
    """Launch an Office app"""
    officer = get_officer()
    return officer.launch_app(app_name, visible)


def quit_app(app_name, force=False):
    """Quit an Office app"""
    officer = get_officer()
    return officer.quit_app(app_name, force)


def speak(text, volume=100, rate=0):
    """Speak text"""
    officer = get_officer()
    return officer.speak(text, volume, rate)


def run_python(code, data=""):
    """Execute Python code"""
    officer = get_officer()
    return officer.run_python(code, data)


def screenshot(save_path=None):
    """Take screenshot"""
    officer = get_officer()
    return officer.screenshot(save_path)


def download_image(url, save_path=None):
    """Download image"""
    officer = get_officer()
    return officer.download_image(url, save_path)


if __name__ == "__main__":
    # Test
    officer = get_officer()
    print("Available apps:", officer.get_available_apps())
    print("Running apps:", officer.get_running_apps())