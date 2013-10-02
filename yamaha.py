# Python Imports
from xml.dom import minidom
from threading import Thread, Timer
import time

# Local Imports
import globals
from helpers import *
from yamaha_xml import *

def increase_volume(zone=-1, inc=0.5):
    change_volume(zone, inc)

def decrease_volume(zone=-1, dec=0.5):
    change_volume(zone, -1 * dec)

def change_volume(zone=-1, diff=0.0):
    if abs(diff) == 0.5 or int(abs(diff)) in [1, 2, 5]:
        # Faster volume method which uses the built in methods
        param1 = 'Up' if diff > 0 else 'Down'
        param2 = ' {0} dB'.format(int(abs(diff))) if abs(diff) != 0.5 else ''
        zone_put_xml(zone, '<Volume><Lvl><Val>{0}{1}</Val><Exp></Exp><Unit></Unit></Lvl></Volume>'.format(param1, param2))
        # Sleep for a little amount of time to ensure we do not get "stuck" sending too many calls in short succession
        time.sleep(0.03)
    else:
        # Slower method that relies on get_volume() first
        set_volume(zone, (get_volume() / 10.0) + diff)

def get_volume():
    return get_status_int('Val')

def set_volume(zone=-1, value=-25.0):
    zone_put_xml(zone, '<Volume><Lvl><Val>{0}</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume>'.format(int(value * 10.0)))

def mute_on(zone=-1):
    zone_put_xml(zone, '<Volume><Mute>On</Mute></Volume>')

def mute_off(zone=-1):
    zone_put_xml(zone, '<Volume><Mute>Off</Mute></Volume>')

def get_mute(zone=-1):
    return get_status_param_is_on('Mute', zone)

def power_on(zone=-1):
    zone_put_xml(zone, '<Power_Control><Power>On</Power></Power_Control>')

def power_off(zone=-1):
    zone_put_xml(zone, '<Power_Control><Power>Off</Power></Power_Control>')

def power_standby(zone=-1):
    zone_put_xml(zone, '<Power_Control><Power>Standby</Power></Power_Control>')

def toggle_on_standby(zone=-1):
    zone_put_xml(zone, '<Power_Control><Power>On/Standby</Power></Power_Control>')

def toggle_mute(zone=-1):
    if get_mute(zone):
        mute_off(zone)
    else:
        mute_on(zone)

def change_source(source, zone=-1):
    zone_put_xml(zone, '<Input><Input_Sel>{0}</Input_Sel></Input>'.format(source))

def straight(zone=-1):
    zone_put_xml(zone, '<Surround><Program_Sel><Current><Straight>On</Straight><Sound_Program>Straight</Sound_Program></Current></Program_Sel></Surround>')

def surround_decode(zone=-1):
    zone_put_xml(zone, '<Surround><Program_Sel><Current><Straight>Off</Straight><Sound_Program>Surround Decoder</Sound_Program></Current></Program_Sel></Surround>')

def toggle_straight_decode(zone=-1):
    if get_straight(zone):
        surround_decode(zone)
    else:
        straight(zone)

def get_straight(zone=-1):
    return get_status_param_is_on('Straight', zone)

def set_enhancer(arg, zone=-1):
    zone_put_xml(zone, '<Surround><Program_Sel><Current><Enhancer>{0}</Enhancer></Current></Program_Sel></Surround>'.format(arg))

def get_enhancer(zone=-1):
    return get_status_param_is_on('Enhancer', zone)

def get_sound_program_name():
    return get_status_string('Sound_Program')

def get_source_number():
    return get_status_int('Src_Number')

def toggle_enhancer():
    if get_enhancer():
        set_enhancer("Off")
    else:
        set_enhancer("On")

def next_source():
    set_source_number(get_source_number() + 1)

def previous_source():
    set_source_number(get_source_number() - 1)

def set_source_number(num, zone=-1):
    zone_put_xml(zone, '<Input><Current_Input_Sel_Item><Src_Number>{0}</Src_Number></Current_Input_Sel_Item></Input>'.format(num))

def set_sleep(arg, zone=-1):
    zone_put_xml(zone, '<Power_Control><Sleep>{0}</Sleep></Power_Control>'.format(arg))

def set_radio_preset(preset):
    put_xml('<Tuner><Play_Control><Preset><Preset_Sel>{0}</Preset_Sel></Preset></Play_Control></Tuner>'.format(preset))

def get_radio_band():
    return get_tuner_string('Band')

def toggle_radio_amfm():
    if get_radio_band() == 'FM':
        set_radio_band('AM')
    else:
        set_radio_band('FM')

def set_radio_band(band):
    put_xml('<Tuner><Play_Control><Tuning><Band>{0}</Band></Tuning></Play_Control></Tuner>'.format(band))

def next_radio_preset():
    put_xml('<Tuner><Play_Control><Preset><Preset_Sel>Up', close_xml=True)

def prev_radio_preset():
    put_xml('<Tuner><Play_Control><Preset><Preset_Sel>Down', close_xml=True)

def modify_radio_preset(diff, turn_on, wrap):
    """
    Deprecated
    """
    oldpreset = get_tuner_int('Preset_Sel')
    preset = oldpreset + diff
    set_radio_preset(preset)
    if turn_on:
        is_on = is_radio_on()
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

def get_radio_preset_count(**kwargs):
    """
    Currently broken
    """
    xml = get_tuner_presets(**kwargs)
    if kwargs.get('print_xml', False):
        print xml
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

def is_radio_on():
    return get_status_string('Input_Sel') == "TUNER"

def auto_radio_freq(updown):
    put_xml('<Tuner><Play_Control><Auto_Freq>{0}</Auto_Freq></Play_Control></Tuner>'.format(updown))

def manual_radio_freq(updown):
    put_xml('<Tuner><Play_Control><Tuning><Freq>{0}</Freq></Tuning></Play_Control></Tuner>'.format(updown))

def set_radio_freq(freq):
    print "Not implemented!"

def set_scene(scene_num, zone=-1):
    zone_put_xml(zone, '<Scene><Scene_Sel>Scene {0}</Scene_Sel></Scene>'.format(scene_num))

def send_code(code):
    put_xml('<System><Misc><Remote_Signal><Receive><Code>{0}</Code></Receive></Remote_Signal></Misc></System>'.format(code))

def set_active_zone(zone):
    globals.active_zone = zone
    print "Active Zone: Zone", zone if zone > -1 else chr(-1 * zone)

def get_source_name(zone=-1):
    return get_status_string("Input_Sel", zone)

def get_availability_dict(items_to_check):
    xml = get_config()
    xmldoc = minidom.parseString(xml)
    res = {}
    for item in items_to_check:
        try:
            value = xmldoc.getElementsByTagName(item)[0].firstChild.data
        except:
            value = None
        res[item] = value
    return res
