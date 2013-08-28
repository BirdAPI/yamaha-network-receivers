#!/usr/bin/python

# Python Imports
import wx.lib.agw.floatspin as FS

# Local Imports
from settings import *
from yamaha import *
from helpers import *

# EventGhost Constants
ACTION_EXECBUILTIN = 0x01
ACTION_BUTTON = 0x02

def testing():
    print "TESTING"

def main():
    print "MAIN"
    setup_ip()

    testing()
    
if __name__ == "__main__":
    main()
    
class IncreaseVolume(eg.ActionBase):
    def __call__(self, step):
        increase_volume(float(step))

    def Configure(self, step=0.5):
        panel = eg.ConfigPanel()
        
        wx.StaticText(panel, label="Increase Amount (Step): ", pos=(10, 10))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 30), min_val=0.5, max_val=10,
                                 increment=0.5, value=float(step), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(floatspin.GetValue())
            
class DecreaseVolume(eg.ActionBase):
    def __call__(self, step):
        decrease_volume(float(step))

    def Configure(self, step=0.5):
        panel = eg.ConfigPanel()
        
        wx.StaticText(panel, label="Decrease Amount (Step): ", pos=(10, 10))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 30), min_val=0.5, max_val=10,
                                 increment=0.5, value=float(step), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(floatspin.GetValue())
            
class SetScene(eg.ActionBase):
    def __call__(self, scene):
        set_scene(int(scene))

    def Configure(self, scene=1):
        panel = eg.ConfigPanel()
        
        wx.StaticText(panel, label="Scene Number: ", pos=(10, 10))
        spin = wx.SpinCtrl(panel, -1, "", (10, 30), (80, -1))
        spin.SetRange(1,12)
        spin.SetValue(int(scene))
        while panel.Affirmed():
            panel.SetResult(spin.GetValue())
            
class SetSourceInput(eg.ActionBase):
    def __call__(self, source):
        change_source(source)

    def Configure(self, source="HDMI1"):
        panel = eg.ConfigPanel()
        
        inputs = [ 'HDMI1', 'HDMI2', 'HDMI3', 'HDMI4', 'HDMI5', 'HDMI6', 'HDMI7', 'HDMI8', 'HDMI9',
                   'AV1', 'AV2', 'AV3', 'AV4', 'AV5', 'AV6', 'AV7', 'AV8', 'AV9',
                   'V-AUX', 'TUNER' ]
        wx.StaticText(panel, label="Source Input: ", pos=(10, 10))
        choice = wx.Choice(panel, -1, (10, 30), choices=inputs)
        while panel.Affirmed():
            panel.SetResult(inputs[choice.GetCurrentSelection()])
    
class YamahaRXClient:
    def __init__(self):
        print "Init Yamaha Network Receivers"
        setup_ip()

    def send_action(self, msg = '', type = ACTION_EXECBUILTIN):
        if msg == 'ToggleMute':
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
           