#!/usr/bin/python

# Python Imports
from xml.dom import minidom
import time

# Local Imports
from yamaha import *

# EventGhost Constnats
ACTION_EXECBUILTIN = 0x01
ACTION_BUTTON = 0x02

def main():
    print "MAIN"
    
if __name__ == "__main__":
    main()
    
class YamahaRXClient:
    def __init__(self):
        print "Init"

    def send_action(self, msg = '', type = ACTION_EXECBUILTIN):
        if msg == 'VolumeUp':
            increase_volume()
        elif msg == 'VolumeDown':
            decrease_volume()
        elif msg.startswith('VolumeUp_'):
            increase_volume(float(msg.replace('VolumeUp_', '')))
        elif msg.startswith('VolumeDown_'):
            decrease_volume(float(msg.replace('VolumeDown_', '')))
        elif msg == 'ToggleMute':
            toggle_mute()
        elif msg == 'PowerOn':
            power_on()
        elif msg == 'PowerOff':
            power_off()
        elif msg == 'PowerStandby':
            power_standby()    
        elif msg == 'ToggleOnStandby':
            toggle_on_standby()  
        elif msg.startswith('Source_'):
            change_source(msg.replace('Source_', ''))
        elif msg == 'Straight':
            straight()
        elif msg == 'SurroundDecode':
            surround_decode()
        elif msg == 'ToggleStraightAndDecode':
            toggle_straight_decode()
        elif msg == 'ToggleEnhancer':
            toggle_enhancer()
        elif msg == 'PreviousSource':
            next_source()
        elif msg == 'NextSource':
            previous_source()
        elif msg == 'ToggleSleep':
            toggle_sleep()
        elif msg == 'NextRadioPreset':
            modify_radio_preset(1, True, True)
        elif msg == 'PreviousRadioPreset':
            modify_radio_preset(-1, True, True)
        elif msg == 'ToggleRadioAMFM':
            toggle_radio_amfm();
        elif msg == 'RadioAutoFeqUp':
            auto_radio_freq('Up')
        elif msg == 'RadioAutoFreqDown':
            auto_radio_freq('Down')
        elif msg == 'RadioFeqUp':
            manual_radio_freq('Up')
        elif msg == 'RadioFreqDown':
            manual_radio_freq('Down')
        elif msg.startswith('Scene'):
            set_scene(int(msg.replace('Scene', '')))
           