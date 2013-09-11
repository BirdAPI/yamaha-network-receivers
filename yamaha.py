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
        get_xml('<Main_Zone>{0}</Main_Zone>'.format(xml), timeout, ip, port)
    else:
        get_xml('<Zone_{1}>{0}</Zone_{1}>'.format(xml, zone), timeout, ip, port)

def get_basic_status(zone=0, timeout=None, ip=None, port=None):
    return zone_get_xml(zone, '<Basic_Status>GetParam</Basic_Status>', timeout, ip, port)

def get_tuner_status(timeout=None, ip=None, port=None):
    return get_xml('<Tuner><Play_Info>GetParam</Play_Info></Tuner>', timeout, ip, port)

def get_tuner_presets(timeout=None, ip=None, port=None):
    return get_xml('<Tuner><Play_Control><Preset><Data>GetParam</Data></Preset></Play_Control></Tuner>', timeout, ip, port)

def get_config(timeout=None, ip=None, port=None):
    return get_xml('<System><Config>GetParam</Config></System>', timeout, ip, port)

def increase_volume(zone=0, inc=0.5):
    zone_put_xml(zone, '<Volume><Lvl><Val>{0}</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume>'.format(int(get_volume() + 10.0 * inc)))

def decrease_volume(zone=0, dec=0.5):
    zone_put_xml(zone, '<Volume><Lvl><Val>{0}</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume>'.format(int(get_volume() - 10.0 * dec)))

def change_volume(zone=0, diff=0.0):
    zone_put_xml(zone, '<Volume><Lvl><Val>{0}</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume>'.format(int(get_volume() + 10.0 * diff)))

def get_volume():
    return get_int_param('Val')

def set_volume(zone=0, value=-25.0):
    zone_put_xml(zone, '<Volume><Lvl><Val>{0}</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume>'.format(int(value * 10.0)))

def mute_on(zone=0):
    zone_put_xml(zone, '<Volume><Mute>On</Mute></Volume>')

def mute_off(zone=0):
    zone_put_xml(zone, '<Volume><Mute>Off</Mute></Volume>')

def get_mute(zone=0):
    return get_is_param_on('Mute')

def power_on(zone=0):
    zone_put_xml(zone, '<Power_Control><Power>On</Power></Power_Control>')

def power_off(zone=0):
    zone_put_xml(zone, '<Power_Control><Power>Off</Power></Power_Control>')

def power_standby(zone=0):
    zone_put_xml(zone, '<Power_Control><Power>Standby</Power></Power_Control>')

def toggle_on_standby(zone=0):
    zone_put_xml(zone, '<Power_Control><Power>On/Standby</Power></Power_Control>')

def toggle_mute(zone=0):
    if get_mute(zone):
        mute_off(zone)
    else:
        mute_on(zone)

def change_source(source, zone=0):
    zone_put_xml(zone, '<Input><Input_Sel>{0}</Input_Sel></Input>'.format(source))

def straight(zone=0):
    zone_put_xml(zone, '<Surround><Program_Sel><Current><Straight>On</Straight><Sound_Program>Straight</Sound_Program></Current></Program_Sel></Surround>')

def surround_decode(zone=0):
    zone_put_xml(zone, '<Surround><Program_Sel><Current><Straight>Off</Straight><Sound_Program>Surround Decoder</Sound_Program></Current></Program_Sel></Surround>')

def toggle_straight_decode(zone=0):
    if get_straight(zone):
        surround_decode(zone)
    else:
        straight(zone)

def get_straight(zone=0):
    return get_is_param_on('Straight')

def set_enhancer(arg, zone=0):
    zone_put_xml(zone, '<Surround><Program_Sel><Current><Enhancer>{0}</Enhancer></Current></Program_Sel></Surround>'.format(arg))

def get_enhancer(zone=0):
    return get_is_param_on('Enhancer')

def get_sound_program_name():
    return get_string_param('Sound_Program')

def get_source_number():
    return get_int_param('Src_Number')

def get_is_param_on(param):
    return get_string_param(param) == "On"

def get_int_param(param):
    return int(get_string_param(param))

def get_string_param(param, xml=None):
    if xml is None:
        xml = get_basic_status()
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value

def get_is_tuner_param_on(param):
    return get_string_tuner_param(param) == "On"

def get_int_tuner_param(param):
    return int(get_string_tuner_param(param))

def get_string_tuner_param(param):
    xml = get_tuner_status()
    xmldoc = minidom.parseString(xml)
    value = xmldoc.getElementsByTagName(param)[0].firstChild.data
    return value

def toggle_enhancer():
    if get_enhancer():
        set_enhancer("Off")
    else:
        set_enhancer("On")

def next_source():
    set_source_number(get_source_number() + 1)

def previous_source():
    set_source_number(get_source_number() - 1)

def set_source_number(num, zone=0):
    zone_put_xml(zone, '<Input><Current_Input_Sel_Item><Src_Number>{0}</Src_Number></Current_Input_Sel_Item></Input>'.format(num))

def set_sleep(arg, zone=0):
    zone_put_xml(zone, '<Power_Control><Sleep>On</Sleep></Power_Control>')

def toggle_sleep():
    if (get_is_param_on('Sleep')):
        set_sleep('Off')
    else:
        set_sleep('On')

def set_radio_preset(preset):
    put_xml('<Tuner><Play_Control><Preset><Preset_Sel>{0}</Preset_Sel></Preset></Play_Control></Tuner>'.format(preset))

def get_radio_band():
    return get_string_tuner_param('Band')

def toggle_radio_amfm():
    if get_radio_band() == 'FM':
        set_radio_band('AM')
    else:
        set_radio_band('FM')

def set_radio_band(band):
    put_xml('<Tuner><Play_Control><Tuning><Band>{0}</Band></Tuning></Play_Control></Tuner>'.format(band))

def modify_radio_preset(diff, turn_on, wrap):
    oldpreset = get_int_tuner_param('Preset_Sel')
    preset = oldpreset + diff
    set_radio_preset(preset)
    if turn_on:
        is_on = is_radio_on
        if not is_on:
            change_source('TUNER')
    if wrap and (not turn_on or is_on):
        count = get_radio_preset_count()
        if diff > 0 and preset > count:
            preset = 1
            set_radio_preset(preset)
        elif diff < 0 and preset < 1:
            preset = count
            set_radio_preset(preset)

def is_radio_on():
    return get_string_param('Input_Sel') == "TUNER"

def auto_radio_freq(updown):
    put_xml('<Tuner><Play_Control><Auto_Freq>{0}</Auto_Freq></Play_Control></Tuner>'.format(updown))

def manual_radio_freq(updown):
    put_xml('<Tuner><Play_Control><Tuning><Freq>{0}</Freq></Tuning></Play_Control></Tuner>'.format(updown))

def set_radio_freq(freq):
    print "Not implemented!"

def get_radio_preset_count():
    xml = get_tuner_presets()
    xmldoc = minidom.parseString(xml)
    count = 0
    done = False
    while not done and count <= 40:
        num = "Number_{0}".format(count + 1)
        value = xmldoc.getElementsByTagName(num)[0].getElementsByTagName('Status')[0].firstChild.data
        if value == 'Exist':
            count += 1
        else:
            done = True
    return count

def set_scene(scene_num, zone=0):
    zone_put_xml(zone, '<Scene><Scene_Sel>Scene {0}</Scene_Sel></Scene>'.format(scene_num))

def send_code(code):
    put_xml('<System><Misc><Remote_Signal><Receive><Code>{0}</Code></Receive></Remote_Signal></Misc></System>'.format(code))
