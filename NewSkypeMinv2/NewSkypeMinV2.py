__author__ = 'Mim'
# Eugene Mim
# NewSkypeMinV2
# 12.13.18

import win32gui, win32con
import time
import re
import win32com.client
import win32ui
from win32gui import GetWindowText, GetForegroundWindow
import ctypes
import pyHook, pythoncom
import keyboard
from multiprocessing import Process
import os
import wmi
import webbrowser
from threading import Thread
from queue import Queue
import time
import psutil
import sys



class WindowMgr:
        #Encapsulates some calls to the winapi for window management
    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name = None):
        #find a window by its class_name
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        #Pass to win32gui.EnumWindows() to check all the opened windows
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        #put the window in the foreground
        win32gui.SetForegroundWindow(self._handle)

    def show_window(self):
        #maximize window
        win32gui.ShowWindow(self._handle, win32con.SW_MAXIMIZE)


def WindowExists(classname):
    try:
        win32ui.FindWindow(classname, None)
    except win32ui.error:
        return False
    else:
        return True

url = 'https://www.tutormate.org/activities/splash?state=beginning'
c = wmi.WMI()
w = WindowMgr()
shell = win32com.client.Dispatch("WScript.Shell")
counter = 0
chrome_launched = False
shortcut_pressed = 0
duplicate_counter = 0

def check_for_duplicate():
    global duplicate_counter
    duplicatecounter = 0
    for process in psutil.process_iter():
        # print (process.name())
        if "NewSkypeMinV2.exe" in str(process.name):
            # print ("found instance")
            duplicate_counter = duplicate_counter + 1
            if duplicate_counter > 2:
                # print ("exiting app")
                sys.exit(1)
                # print("whatthefuck")

def check_for_chrome():
    try:
        for process in psutil.process_iter():
            # print (process.name())
            if "chrome.exe" in str(process.name):
                chrome_launched = True
                break
            else:
                chrome_launched = False
                continue
        if chrome_launched == False:
            webbrowser.open(url)
            chrome_launched = True
    except:
        pass

def waitforpress(threadname, q):
    try:
        q.put(0)
        #read variable "a" modify by thread 2
        while True:
            time.sleep(.1)
            if keyboard.is_pressed('f8'):
                q.put(1)
                # print ("shortcut pressed")
                time.sleep(120)
                # print ("shortcut unpressed")
                q.put(0)
    except:
        pass


def thread2(threadname, q):
    try:
        global check_for_chrome
        while True:
            ctypes.windll.user32.keybd_event(0x12, 0, 0x0002, 0)
            time.sleep(45)
            if q.empty() == False:
                a = q.get()
            if a == 0:
                w.find_window_wildcard(".*Chrome.*")
                counter = 0
                while ("Chrome" not in GetWindowText(GetForegroundWindow())):
                    time.sleep(.2)
                    ctypes.windll.user32.keybd_event(0x12, 0, 0, 0)
                    time.sleep(.2)
                    ctypes.windll.user32.keybd_event(0x1B, 0, 0, 0)
                    time.sleep(.2)
                    ctypes.windll.user32.keybd_event(0x1B, 0, 0x0002, 0)
                    time.sleep(.2)
                    ctypes.windll.user32.keybd_event(0x12, 0, 0x0002, 0)
                    time.sleep(.2)
                    counter = counter + 1
                    if counter > 4:
                        counter = 0
                        check_for_chrome()
                        break
                time.sleep(.5)
                w.show_window()
                time.sleep(.5)
    except:
        pass

check_for_duplicate()
queue = Queue()
waitforpress = Thread( target=waitforpress, args=("Thread-1", queue) )
thread2 = Thread( target=thread2, args=("Thread-2", queue) )
thread2.setDaemon(True)
waitforpress.setDaemon(True)
waitforpress.start()
thread2.start()
waitforpress.join()
thread2.join()
