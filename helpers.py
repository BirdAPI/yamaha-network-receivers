import traceback
from threading import Thread
from datetime import datetime
import socket

from settings import *
import yamaha

def setup_ip():
    if SETTINGS.ip_auto_detect:
        ip = auto_detect_ip_threaded()
        if ip is not None:
            SETTINGS.ip_address = ip

def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def auto_detect_ip():
    start = datetime.now()
    found_ip = None
    ip_range = create_ip_range(SETTINGS.ip_range_start, SETTINGS.ip_range_end)
    for ip in ip_range:
        try:
            conf = yamaha.get_config(float(SETTINGS.auto_detect_timeout), ip=ip)
            model = yamaha.get_string_param('Model_Name', conf)
            print '{0}: {1}'.format(ip, model)
            if model.upper() == "ANY" or model == "" or model is None \
             or model.lower() == SETTINGS.auto_detect_model.lower():
                found_ip = ip
                break
        except:
            print '{0}: ...'.format(ip)
            #print traceback.format_exc()
    end = datetime.now()
    delta = end-start
    print "finished in", delta.total_seconds(), "seconds"
    return found_ip

_FOUND_IP = None
def auto_detect_ip_threaded():
    global _FOUND_IP
    _FOUND_IP = None
    start = datetime.now()
    threads = []

    # Get LAN IP in order to detect network prefix (eg 192.168.1)
    lan_ip = get_lan_ip()
    ip_range = create_ip_range(lan_ip[:lan_ip.rfind('.')] + '.1', lan_ip[:lan_ip.rfind('.')] + '.254')

    for ip in ip_range:
        t = Thread(target=try_connect, kwargs={'ip':ip})
        t.daemon = True
        threads.append(t)
        t.start()
    for t in threads:
        if _FOUND_IP is not None:
            break
        else:
            t.join()
    end = datetime.now()
    delta = end-start
    print "finished in", delta.total_seconds(), "seconds"
    print "Found IP:", _FOUND_IP
    return _FOUND_IP

def try_connect(ip):
    try:
        conf = yamaha.get_config(float(SETTINGS.auto_detect_timeout), ip=ip)
        model = yamaha.get_string_param('Model_Name', conf)
        print '{0}: {1}'.format(ip, model)
        if SETTINGS.auto_detect_model.upper() == "ANY" \
                or SETTINGS.auto_detect_model == "" \
                or SETTINGS.auto_detect_model is None\
                or model.lower() == SETTINGS.auto_detect_model.lower():
            global _FOUND_IP
            _FOUND_IP = ip
    except:
        #print '{0}: ...'.format(ip)
        pass

def create_ip_range(range_start, range_end):
    ip_range = []
    start = int(range_start[range_start.rfind('.')+1:])
    end = int(range_end[range_end.rfind('.')+1:])
    for i in range(start, end+1):
        ip = range_start[:range_start.rfind('.')+1] + str(i)
        ip_range.append(ip)
    return ip_range