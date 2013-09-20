import traceback
from threading import Thread
from datetime import datetime
import socket
from collections import *

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
            model = yamaha.get_config_string('Model_Name', float(globals.auto_detect_timeout), ip=ip)
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
    globals.FOUND_IP = None
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
        if globals.FOUND_IP is not None:
            break
        else:
            t.join()
    print "Found IP: {0} [{1}]".format(globals.FOUND_IP, globals.MODEL)
    return globals.FOUND_IP

def try_connect(ip):
    try:
        model = yamaha.get_config_string('Model_Name', float(globals.auto_detect_timeout), ip=ip)
        print '{0}: {1}'.format(ip, model)
        if globals.auto_detect_model.upper() == "ANY" \
                or globals.auto_detect_model == "" \
                or globals.auto_detect_model is None\
                or model.lower() == globals.auto_detect_model.lower():
            globals.FOUND_IP = ip
            globals.MODEL = model
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

def convert_zone_to_int(zone):
    if zone == 'Main Zone' or zone == 'Main_Zone' or zone == 'MZ':
        return 0
    else:
        return int(zone.replace('Zone_', '').replace('Zone', '').replace('Z', '').strip())

def open_to_close_tag(tag):
    index = tag.find(' ')
    if index == -1:
        index = len(tag) - 1
    return '</' + tag[1:index] + '>'

def close_xml_tags(xml):
    output = []
    stack = []
    xml_chars = deque(list(xml))
    c = None

    while len(xml_chars) > 0:
        while len(xml_chars) > 0 and c != '<':
            c = xml_chars.popleft()
            if c != '<':
                output.append(c)
        if c == '<':
            temp = [ '<' ]
            c = xml_chars.popleft()
            end_tag = c == '/'
            while c != '>':
                temp.append(c)
                c = xml_chars.popleft()
            temp.append('>')
            tag = ''.join(temp)
            if end_tag:
                other_tag = stack.pop()
                other_close_tag = open_to_close_tag(other_tag)
                while other_close_tag != tag:
                    output.append(other_close_tag)
                    other_tag = stack.pop()
                    other_close_tag = open_to_close_tag(other_tag)
            elif not tag.endswith('/>'):
                # Only add to stack if not self-closing
                stack.append(tag)
            output.append(tag)

    while len(stack) > 0:
        tag = stack.pop()
        output.append(open_to_close_tag(tag))

    return ''.join(output)
