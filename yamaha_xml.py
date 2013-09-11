__author__ = 'Anthony Casagrande'

# Python Imports
from xml.dom import minidom
import httplib

# Local Imports
import globals
from helpers import *

def do_xml(xml, timeout=None, ip=None, port=None, return_result=False):
    '''
    Base function to send/receive xml using either GET or POST
    '''
    if ip is None:
        ip = globals.ip_address
    if port is None:
        port = globals.port
    if timeout is None:
        conn = httplib.HTTPConnection('{0}:{1}'.format(ip, port), timeout=float(globals.default_timeout))
    else:
        conn = httplib.HTTPConnection('{0}:{1}'.format(ip, port), timeout=float(timeout))
    headers = { "Content-type": "text/xml" }
    conn.request("POST", "/YamahaRemoteControl/ctrl", "", headers)
    conn.send(xml)
    if return_result:
        response = conn.getresponse()
        rval = response.read()
        conn.close()
        return rval
    else:
        conn.close()
        return True

def send_xml(xml, timeout=None, ip=None, port=None):
    '''
    Communicate with the receiver, but do not wait or return the results
    '''
    do_xml(xml, timeout, ip, port, return_result=False)

def put_xml(xml, timeout=None, ip=None, port=None):
    send_xml('<YAMAHA_AV cmd="PUT">{0}</YAMAHA_AV>'.format(xml), timeout, ip, port)

def zone_put_xml(zone, xml, timeout=None, ip=None, port=None):
    if zone < 2:
        put_xml('<Main_Zone>{0}</Main_Zone>'.format(xml), timeout, ip, port)
    else:
        put_xml('<Zone_{1}>{0}</Zone_{1}>'.format(xml, zone), timeout, ip, port)

def receive_xml(xml, timeout=None, ip=None, port=None):
    return do_xml(xml, timeout, ip, port, return_result=True)

def get_xml(xml, timeout=None, ip=None, port=None):
    return receive_xml('<YAMAHA_AV cmd="GET">{0}</YAMAHA_AV>'.format(xml), timeout, ip, port)

def zone_get_xml(zone, xml, timeout=None, ip=None, port=None):
    if zone < 2:
        return get_xml('<Main_Zone>{0}</Main_Zone>'.format(xml), timeout, ip, port)
    else:
        return get_xml('<Zone_{1}>{0}</Zone_{1}>'.format(xml, zone), timeout, ip, port)

def get_basic_status(zone=0, timeout=None, ip=None, port=None):
    return zone_get_xml(zone, '<Basic_Status>GetParam</Basic_Status>', timeout, ip, port)

def get_tuner_status(timeout=None, ip=None, port=None):
    return get_xml('<Tuner><Play_Info>GetParam</Play_Info></Tuner>', timeout, ip, port)

def get_tuner_presets(timeout=None, ip=None, port=None):
    return get_xml('<Tuner><Play_Control><Preset><Data>GetParam</Data></Preset></Play_Control></Tuner>', timeout, ip, port)

def get_config(timeout=None, ip=None, port=None):
    return get_xml('<System><Config>GetParam</Config></System>', timeout, ip, port)

def get_status_string(param, zone=0, timeout=None, ip=None, port=None):
    xml = get_basic_status(zone, timeout, ip, port)
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value

def get_status_param_is_on(param, zone=0):
    return get_status_string(param, zone) == "On"

def get_status_int(param, zone=0):
    return int(get_status_string(param, zone))

def get_config_string(param, timeout=None, ip=None, port=None):
    xml = get_config(timeout, ip, port)
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value

def get_config_param_is_on(param):
    return get_config_string(param) == "On"

def get_config_int(param):
    return int(get_config_string(param))

def get_tuner_string(param):
    xml = get_tuner_status()
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value

def get_tuner_param_is_on(param):
    return get_tuner_string(param) == "On"

def get_tuner_int(param):
    return int(get_tuner_string(param))
