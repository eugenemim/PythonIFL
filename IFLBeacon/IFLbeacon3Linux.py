__author__ = 'Eugene Mim'
# Eugene Mim
# IFLbeacon for Linux
# 06.12.19
import requests
import sched, time

classroom_id = ""

#post function
def ping():
    try:
        fetch_name()
        payload = {
            'classroom_id': classroom_id,
            }
        #httpbin.org used for testing purposes.
        r = requests.post("http://httpbin.org/post", data=payload)
        # r = requests.post("https://lighthouseprod.herokuapp.com/devices", data=payload)
        print r.text
    except:
        pass

#placeholder code until ID and naming convention is finished.
def fetch_name():
    global classroom_id

    #[ENTER ID CODE HERE]
    #LINE BELOW is a placeholder until ID methodology is decided.

    classroom_id = "unknown classroom"

#initial ping, then task here.
try:
    ping()
    pingtask = sched.scheduler(time.time, time.sleep)
except:
    pass

#60 second, ongoing loop
def ping_loop(sc):
    try:
        ping()
        pingtask.enter(60, 1, ping_loop, (sc,))
    except:
        pass

try:
    pingtask.enter(60, 1, ping_loop, (pingtask,))
    pingtask.run()
except:
    pass
