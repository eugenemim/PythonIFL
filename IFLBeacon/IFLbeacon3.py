__author__ = 'Mim'
# Eugene Mim
# IFLbeacon
# 06.07.18

import power
import wmi
import requests

#Assertion variables
c = wmi.WMI ()
skype = Skype4Py.Skype()
chrome_launched = None
skype_launched = None
charger_plugged_in = None
charger_plugged_in = None
system_time = None
foreground_window_text = None
foreground_window_tutormate = None
meraki_installed = None
district_name = ""
school_name = ""
teacher_name = ""
meraki_logged = None
classroom_id = ""
display_name = ""

#Charger code
def check_for_charger():
    try:
        ans = power.PowerManagement().get_providing_power_source_type()
        global charger_plugged_in
        if not ans:
            charger_plugged_in = True
        else:
            charger_plugged_in = False
    except:
        pass

#Assertion code

def WindowExists(classname):
    try:
        win32ui.FindWindow(classname, None)
    except win32ui.error:
        return False
    else:
        return True

#check to see if chrome is installed
def check_for_skype():
    global skype_launched
    try:
        if skype.Client.IsRunning:
            try:
                skype_launched = True
            except:
                pass
        elif skype.Client.IsRunning is False:
            try:
                skype_launched = False
            except:
                pass
    except:
        pass

#check to see if chrome is installed
def check_for_chrome():
    global chrome_launched
    try:
        if WindowExists("Chrome_WidgetWin_1") == True:
            try:
                chrome_launched = True
            except:
                pass
        elif WindowExists("Chrome_WidgetWin_1") == False:
            try:
                chrome_launched = False
            except:
                pass
    except:
        pass

#check system time
def check_time():
    global system_time
    try:
        timez = time.localtime()
        system_time = str(timez.tm_hour) + ":" + str(timez.tm_min)
    except:
        pass

#check if either tutormate tab or skype is in foreground. (should return false if kid is playing a game or a pop up appears)
def check_for_foreground_window():
    global foreground_window_text
    global foreground_window_tutormate
    try:
        foreground_window_text = GetWindowText(GetForegroundWindow())
        if "TutorMate" in foreground_window_text:
            foreground_window_tutormate = True
        elif "Skype" in foreground_window_text:
            foreground_window_tutormate = True
        else:
            foreground_window_tutormate=False
    except:
        pass

#check if meraki folder is installed
def check_meraki_folder():
        global meraki_installed
        try:
            meraki_installed = os.path.isdir("C:\Program Files (x86)\Meraki")
        except:
            pass

#post function
def ping():
    try:
        check_time()
        check_for_skype()
        check_for_chrome()
        check_for_charger()
        check_for_foreground_window()
        check_meraki_folder()
        fetch_lmi_name()
        payload = {
            'chrome_launched': chrome_launched,
            'skype_launched': skype_launched,
            'meraki_installed': meraki_installed,
            'charger_plugged_in': charger_plugged_in,
            'foreground_window_tutormate': foreground_window_tutormate,
            'district_name': district_name,
            'school_name': school_name,
            'teacher_name': teacher_name,
            'system_time': system_time,
            'classroom_id': classroom_id,
            }
        #httpbin.org used for testing purposes.
        r = requests.post("http://httpbin.org/post", data=payload)
        # r = requests.post("https://lighthouseprod.herokuapp.com/devices", data=payload)
        print r.text
    except:
        pass

#second try at assigning ID. if flat file is not configured, classroom ID is left blank and program does not ping. Checks this file for info every 60 seconds.
def try_flat_file():
    try:
        with open('C://lmi.txt') as d:
            if "}" in d.readline():
                with open('C://lmi.txt') as f:
                    global display_name
                    display_name = f.readline()
    except:
        pass

#checks for log me in display name in registry. If none found, looks for flat file(), if none in flat file, does not ping. checks every 60 seconds.
def fetch_lmi_name():
    try:
        global teacher_name, school_name, district_name, classroom_id, display_name
        display_name = ""
        proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
        proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()
        if proc_arch == 'x86' and not proc_arch64:
            arch_keys = {0}
        elif proc_arch == 'x86' or proc_arch == 'amd64':
            arch_keys = {_winreg.KEY_WOW64_32KEY, _winreg.KEY_WOW64_64KEY}
        else:
            raise Exception("Unhandled arch: %s" % proc_arch)
        try:
            for arch_key in arch_keys:
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\LogMeIn\V5", 0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)
                for i in xrange(0, _winreg.QueryInfoKey(key)[0]):
                    skey_name = _winreg.EnumKey(key, i)
                    skey = _winreg.OpenKey(key, skey_name)
                    try:
                        if  "}" in _winreg.QueryValueEx(skey, 'HostDescription')[0]:
                            display_name=_winreg.QueryValueEx(skey, 'HostDescription')[0]
                        if  "}" not in _winreg.QueryValueEx(skey, 'HostDescription')[0]:
                            display_name = ""
                    except OSError as e:
                        if e.errno == errno.ENOENT:
                            pass
                    finally:
                        skey.Close()
        except:
            pass
        if display_name == "":
            try_flat_file()
    except:
        pass

#function to chop up string into 4 variables
def mod_string():
    global teacher_name, school_name, district_name, classroom_id, display_name
    try:
        school_name = display_name[display_name.find(" ")+1:display_name.find("-")]
        teacher_name = display_name.split('-')[1]
        district_name = display_name[display_name.find("[")+1:display_name.find("]")]
        classroom_id = display_name[display_name.find("{")+1:display_name.find("}")]
    except:
        pass

#initial ping here.
try:
    fetch_lmi_name()
    if display_name != "":
        mod_string()
        if classroom_id != "":
            ping()

    pingtask = sched.scheduler(time.time, time.sleep)
except:
    pass
#60 second, ongoing loop
def ping_loop(sc):
    try:
        global display_name
        fetch_lmi_name()
        #makes sure display name is not empty before modding string
        if display_name != "":
            mod_string()
            #makes sure there is a classroom id to ping with. If no classroom id, does not ping
            if classroom_id != "":
                ping()
        #deletes display name if something is fishy
        if classroom_id == "":
            display_name = ""
        pingtask.enter(60, 1, ping_loop, (sc,))
    except:
        pass

try:
    pingtask.enter(60, 1, ping_loop, (pingtask,))
#activates loop
    pingtask.run()
except:
    pass
