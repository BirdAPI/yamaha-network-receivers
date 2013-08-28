import traceback
from threading import Thread
from datetime import datetime
import socket

import globals
import yamaha

def setup_ip():
    if globals.ip_auto_detect:
        print "Searching for Yamaha Recievers ({0})...".format(globals.auto_detect_model)
        ip = auto_detect_ip_threaded()
        if ip is not None:
            globals.ip_address = ip
    else:
        print 'IP:', globals.ip_address

def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def auto_detect_ip():
    start = datetime.now()
    found_ip = None
    ip_range = create_ip_range(globals.ip_range_start, globals.ip_range_end)
    for ip in ip_range:
        try:
            conf = yamaha.get_config(float(globals.auto_detect_timeout), ip=ip)
            model = yamaha.get_string_param('Model_Name', conf)
            print '{0}: {1}'.format(ip, model)
            if model.upper() == "ANY" or model == "" or model is None \
                    or model.lower() == globals.auto_detect_model.lower():
                found_ip = ip
                break
        except:
            print '{0}: ...'.format(ip)
            #print traceback.format_exc()
    end = datetime.now()
    delta = end-start
    print "finished in", delta.total_seconds(), "seconds"
    return found_ip

def auto_detect_ip_threaded():
    globals._FOUND_IP = None
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
        if globals._FOUND_IP is not None:
            break
        else:
            t.join()
    print "Found IP:", globals._FOUND_IP
    return globals._FOUND_IP

def try_connect(ip):
    try:
        conf = yamaha.get_config(float(globals.auto_detect_timeout), ip=ip)
        model = yamaha.get_string_param('Model_Name', conf)
        print '{0}: {1}'.format(ip, model)
        if globals.auto_detect_model.upper() == "ANY" \
                or globals.auto_detect_model == "" \
                or globals.auto_detect_model is None\
                or model.lower() == globals.auto_detect_model.lower():
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