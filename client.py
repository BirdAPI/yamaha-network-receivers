# Python Imports
import wx.lib.agw.floatspin as FS

# Local Imports
import globals
from yamaha import *
from helpers import *
    
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
        index = -1 if not source in inputs else inputs.index(source)
        choice = wx.Choice(panel, index, (10, 30), choices=inputs)
        while panel.Affirmed():
            panel.SetResult(inputs[choice.GetCurrentSelection()])
            
class SetPowerStatus(eg.ActionBase):
    def __call__(self, status):
        if status == 'Toggle On/Standby':
            toggle_on_standby()
        elif status == 'On':
            power_on()
        elif status == 'Off':
            power_off()
        elif status == 'Standby':
            power_standby()

    def Configure(self, status=""):
        panel = eg.ConfigPanel()
        
        statuses = [ 'Toggle On/Standby', 'On', 'Off', 'Standby' ]
        wx.StaticText(panel, label="Power Status: ", pos=(10, 10))
        index = -1 if not status in statuses else statuses.index(status)
        choice = wx.Choice(panel, index, (10, 30), choices=statuses)
        while panel.Affirmed():
            panel.SetResult(statuses[choice.GetCurrentSelection()])
            
class SetVolume(eg.ActionBase):
    def __call__(self, vol):
        set_volume(float(vol))

    def Configure(self, vol=-50.0):
        panel = eg.ConfigPanel()
        
        wx.StaticText(panel, label="Exact Volume (dB): ", pos=(10, 10))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 30), min_val=-100.0, max_val=50.0,
                                 increment=0.5, value=float(vol), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(floatspin.GetValue())
            
class SetSurroundMode(eg.ActionBase):
    def __call__(self, mode):
        if mode == 'Toggle Straight/Surround Decode':
            toggle_straight_decode()
        elif mode == 'Straight':
            straight()
        elif mode == 'Surround Decode':
            surround_decode()

    def Configure(self, mode=""):
        panel = eg.ConfigPanel()
        
        modes = [ 'Toggle Straight/Surround Decode', 'Straight', 'Surround Decode' ]
        wx.StaticText(panel, label="Surround Mode: ", pos=(10, 10))
        index = -1 if not mode in modes else modes.index(mode)
        choice = wx.Choice(panel, index, (10, 30), choices=modes)
        while panel.Affirmed():
            panel.SetResult(modes[choice.GetCurrentSelection()])
    
class YamahaRXClient:
    def __init__(self):
        pass
        
    def send_action(self, msg = '', type=globals.ACTION_EXECBUILTIN):
        if msg == 'ToggleMute':
            toggle_mute()
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
           