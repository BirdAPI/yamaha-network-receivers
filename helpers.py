# Python Imports
import traceback
from threading import Thread
from datetime import datetime
import socket
from collections import *

# Local Imports
import globals
import yamaha

def setup_ip():
    """
    If auto detect ip is enabled, this function will attempt to configure the ip
    address, otherwise if static ip is enabled, this function will
    verify whether a yamaha receiver can be found at the given static ip.
    """
    if globals.ip_auto_detect:
        print "Searching for Yamaha Recievers ({0})...".format(globals.auto_detect_model)
        ip = auto_detect_ip_threaded()
        if ip is not None:
            globals.ip_address = ip
            return ip
    else:
        try:
            model = yamaha.get_config_string('Model_Name', timeout=globals.auto_detect_timeout, ip=globals.ip_address, print_error=False)
            print "Found Yamaha Receiver: {0} [{1}]".format(globals.ip_address, model)
            return globals.ip_address
        except:
            eg.PrintError("Yamaha Receiver Not Found [{0}]!".format(globals.ip_address))
    return None

def get_lan_ip():
    """
    Attempts to open a socket connection to Google's DNS
    servers in order to determine the local IP address
    of this computer. Eg, 192.168.1.100
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.100"

def get_network_prefix():
    """
    Returns the network prefix, which is the local IP address
    without the last segment, Eg: 192.168.1.100 -> 192.168.1
    """
    lan_ip = get_lan_ip()
    return lan_ip[:lan_ip.rfind('.')]

def auto_detect_ip_threaded():
    """
    Blasts the network with requests, attempting to find any and all yamaha receivers
    on the local network. First it detects the user's local ip address, eg 192.168.1.100.
    Then, it converts that to the network prefix, eg 192.168.1, and then sends a request
    to every ip on that subnet, eg 192.168.1.1 -> 192.168.1.254. It does each request on
    a separate thread in order to avoid waiting for the timeout for every 254 requests
    one by one.
    """
    globals.FOUND_IP = None
    threads = []

    # Get network prefix (eg 192.168.1)
    net_prefix = get_network_prefix()
    ip_range = create_ip_range(net_prefix + '.1', net_prefix + '.254')

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
    if globals.FOUND_IP is not None:
        print "Found Yamaha Receiver IP: {0} [{1}]".format(globals.FOUND_IP, globals.MODEL)
    else:
        eg.PrintError("Yamaha Receiver Was Not Found!")
    return globals.FOUND_IP

def try_connect(ip):
    """
    Used with the auto-detect-ip functions, determines if a yamaha receiver is
    waiting at the other end of the given ip address.
    """
    try:
        model = yamaha.get_config_string('Model_Name', timeout=globals.auto_detect_timeout, ip=ip, print_error=False)
        print '{0}: {1}'.format(ip, model)
        if globals.auto_detect_model in ["ANY", "", None] or model.upper() == globals.auto_detect_model.upper():
            globals.FOUND_IP = ip
            globals.MODEL = model
    except:
        pass

def create_ip_range(range_start, range_end):
    """
    Given a start ip, eg 192.168.1.1, and an end ip, eg 192.168.1.254,
    generate a list of all of the ips within that range, including
    the start and end ips.
    """
    ip_range = []
    start = int(range_start[range_start.rfind('.')+1:])
    end = int(range_end[range_end.rfind('.')+1:])
    for i in range(start, end+1):
        ip = range_start[:range_start.rfind('.')+1] + str(i)
        ip_range.append(ip)
    return ip_range

def convert_zone_to_int(zone, convert_active=False):
    """
    Convert a zone name into the integer value that it represents:
    Examples:
    Active Zone: -1
    Main Zone: 0
    Zone 2: 2
    Zone A: -65 (this is the negative version of the integer that represents this letter: 'A' -> 65, thus -65)
    """
    if zone == 'Main Zone' or zone == 'Main_Zone' or zone == 'MZ':
        return 0
    elif 'active' in zone.lower():
        # -1 means active zone
        if convert_active:
            return globals.active_zone
        else:
            return -1
    else:
        z = zone.replace('Zone_', '').replace('Zone', '').replace('Z', '').strip()
        if z in [ 'A', 'B', 'C', 'D' ]:
            return -1 * ord(z)
        return int(z)

def open_to_close_tag(tag):
    """
    Given an opening xml tag, return the matching close tag
    eg. '<YAMAHA_AV cmd="PUT"> becomes </YAMAHA_AV>
    """
    index = tag.find(' ')
    if index == -1:
        index = len(tag) - 1
    return '</' + tag[1:index] + '>'

def close_xml_tags(xml):
    """
    Automagically takes an input xml string and returns that string
    with all of the xml tags properly closed. It can even handle when
    the open tag is in the middle of the string and not the end.
    """
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

def setup_availability():
    """
    Query the receiver to see which zones and inputs it supports.
    Should be called after a successful ip check.
    """
    res = yamaha.get_availability_dict(globals.INPUT_CHECK + globals.ZONE_CHECK)

    zones = []
    for zone in globals.ZONE_CHECK:
        if res[zone] is not None and res[zone] != '0':
            zones.append(zone)

    inputs = []
    for input in globals.INPUT_CHECK:
        if res[input] is not None and res[input] != '0':
            inputs.append(input)

    globals.AVAILABLE_ZONES = [ zone.replace('_', ' ') for zone in zones ]
    globals.AVAILABLE_SOURCES = [ globals.INPUT_MAPPINGS[input] for input in inputs ]
