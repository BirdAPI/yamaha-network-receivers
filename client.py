# Python Imports
import wx.lib.agw.floatspin as FS
from datetime import datetime
import re

# Local Imports
import globals
from yamaha import *
from helpers import *

class SmartVolumeFinished(eg.ActionBase):
    def __call__(self):
        globals.smart_vol_up_start = None
        globals.smart_vol_down_start = None

class SmartVolumeUp(eg.ActionBase):
    def __call__(self, zone, step1, step2, wait):
        izone = convert_zone_to_int(zone)
        if globals.smart_vol_up_start is None:
            globals.smart_vol_up_start = datetime.now()
        diff = datetime.now() - globals.smart_vol_up_start
        if diff.seconds < float(wait):
            #print "Volume Up:", step1
            increase_volume(izone, step1)
        else:
            #print "Volume Up:", step2
            increase_volume(izone, step2)

    def Configure(self, zone='Active Zone', step1=0.5, step2=2.0, wait=2.0):
        panel = eg.ConfigPanel()

        zones = [ 'Active Zone', 'Main Zone', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone A', 'Zone B', 'Zone C', 'Zone D' ]
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Increase Amount (Step 1): ", pos=(10, 60))
        fs_step1 = FS.FloatSpin(panel, -1, pos=(10, 80), min_val=0.5, max_val=10,
            increment=0.5, value=float(step1), agwStyle=FS.FS_LEFT)
        fs_step1.SetFormat("%f")
        fs_step1.SetDigits(1)

        wx.StaticText(panel, label="Time between Step 1 to Step 2 (seconds): ", pos=(10, 110))
        fs_wait = FS.FloatSpin(panel, -1, pos=(10, 130), min_val=0.5, max_val=999,
            increment=0.1, value=float(wait), agwStyle=FS.FS_LEFT)
        fs_wait.SetFormat("%f")
        fs_wait.SetDigits(1)

        wx.StaticText(panel, label="Increase Amount (Step 2): ", pos=(10, 160))
        fs_step2 = FS.FloatSpin(panel, -1, pos=(10, 180), min_val=0.5, max_val=10,
            increment=0.5, value=float(step2), agwStyle=FS.FS_LEFT)
        fs_step2.SetFormat("%f")
        fs_step2.SetDigits(1)

        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], fs_step1.GetValue(), fs_step2.GetValue(), fs_wait.GetValue())

class SmartVolumeDown(eg.ActionBase):
    def __call__(self, zone, step1, step2, wait):
        izone = convert_zone_to_int(zone)
        if globals.smart_vol_down_start is None:
            globals.smart_vol_down_start = datetime.now()
        diff = datetime.now() - globals.smart_vol_down_start
        if diff.seconds < float(wait):
            decrease_volume(izone, step1)
        else:
            decrease_volume(izone, step2)

    def Configure(self, zone='Active Zone', step1=0.5, step2=2.0, wait=2.0):
        panel = eg.ConfigPanel()

        zones = [ 'Active Zone', 'Main Zone', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone A', 'Zone B', 'Zone C', 'Zone D' ]
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Decrease Amount (Step 1): ", pos=(10, 60))
        fs_step1 = FS.FloatSpin(panel, -1, pos=(10, 80), min_val=0.5, max_val=10,
            increment=0.5, value=float(step1), agwStyle=FS.FS_LEFT)
        fs_step1.SetFormat("%f")
        fs_step1.SetDigits(1)

        wx.StaticText(panel, label="Time between Step 1 to Step 2 (seconds): ", pos=(10, 110))
        fs_wait = FS.FloatSpin(panel, -1, pos=(10, 130), min_val=0.5, max_val=999,
            increment=0.1, value=float(wait), agwStyle=FS.FS_LEFT)
        fs_wait.SetFormat("%f")
        fs_wait.SetDigits(1)

        wx.StaticText(panel, label="Decrease Amount (Step 2): ", pos=(10, 160))
        fs_step2 = FS.FloatSpin(panel, -1, pos=(10, 180), min_val=0.5, max_val=10,
            increment=0.5, value=float(step2), agwStyle=FS.FS_LEFT)
        fs_step2.SetFormat("%f")
        fs_step2.SetDigits(1)

        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], fs_step1.GetValue(), fs_step2.GetValue(), fs_wait.GetValue())

class IncreaseVolume(eg.ActionBase):
    def __call__(self, zone, step):
        increase_volume(convert_zone_to_int(zone), float(step))

    def Configure(self, zone='Active Zone', step=0.5):
        panel = eg.ConfigPanel()

        zones = [ 'Active Zone', 'Main Zone', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone A', 'Zone B', 'Zone C', 'Zone D' ]
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Increase Amount (Step): ", pos=(10, 60))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 80), min_val=0.5, max_val=10,
            increment=0.5, value=float(step), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], floatspin.GetValue())

class DecreaseVolume(eg.ActionBase):
    def __call__(self, zone, step):
        decrease_volume(convert_zone_to_int(zone), float(step))

    def Configure(self, zone='Active Zone', step=0.5):
        panel = eg.ConfigPanel()

        zones = [ 'Active Zone', 'Main Zone', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone A', 'Zone B', 'Zone C', 'Zone D' ]
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Decrease Amount (Step): ", pos=(10, 60))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 80), min_val=0.5, max_val=10,
                                 increment=0.5, value=float(step), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], floatspin.GetValue())

class SetVolume(eg.ActionBase):
    def __call__(self, zone, vol):
        set_volume(convert_zone_to_int(zone), float(vol))

    def Configure(self, zone='Active Zone', vol=-50.0):
        panel = eg.ConfigPanel()

        zones = [ 'Active Zone', 'Main Zone', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone A', 'Zone B', 'Zone C', 'Zone D' ]
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Exact Volume (dB): ", pos=(10, 60))
        floatspin = FS.FloatSpin(panel, -1, pos=(10, 80), min_val=-100.0, max_val=50.0,
            increment=0.5, value=float(vol), agwStyle=FS.FS_LEFT)
        floatspin.SetFormat("%f")
        floatspin.SetDigits(1)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], floatspin.GetValue())

class SetActiveZone(eg.ActionBase):
    def __call__(self, zone):
        set_active_zone(convert_zone_to_int(zone))

    def Configure(self, zone='Main Zone'):
        panel = eg.ConfigPanel()
        zones = [ 'Main Zone', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone A', 'Zone B', 'Zone C', 'Zone D' ]
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()])

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
    def __call__(self, zone, source):
        izone = convert_zone_to_int(zone)
        change_source(source, izone)

    def Configure(self, zone="Active Zone", source="HDMI1"):
        panel = eg.ConfigPanel()

        zones = [ 'Active Zone', 'Main Zone', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone A', 'Zone B', 'Zone C', 'Zone D' ]
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)
        inputs = [ 'HDMI1', 'HDMI2', 'HDMI3', 'HDMI4', 'HDMI5', 'HDMI6', 'HDMI7', 'HDMI8', 'HDMI9',
                   'AV1', 'AV2', 'AV3', 'AV4', 'AV5', 'AV6', 'AV7', 'AV8', 'AV9',
                   'V-AUX', 'TUNER', 'AUDIO', 'AUDIO1', 'AUDIO2', 'AUDIO3', 'AUDIO4',
                   'DOCK', 'SIRIUS', 'PC', 'MULTICH', 'PHONO', 'iPod', 'Bluetooth',
                   'UAW', 'NET', 'Rhapsody', 'SIRIUSInternetRadio', 'Pandora', 'Napster',
                   'NET RADIO', 'USB', 'iPod (USB)' ]
        wx.StaticText(panel, label="Source Input: ", pos=(10, 60))
        choice_input = wx.Choice(panel, -1, (10, 80), choices=inputs)
        if source in inputs:
            choice_input.SetStringSelection(source)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], inputs[choice_input.GetCurrentSelection()])

class SetPowerStatus(eg.ActionBase):
    def __call__(self, zone, status):
        izone = convert_zone_to_int(zone)
        if status == 'Toggle On/Standby':
            toggle_on_standby(izone)
        elif status == 'On':
            power_on(izone)
        elif status == 'Standby':
            power_standby(izone)

    def Configure(self, zone="Active Zone", status="Toggle On/Standby"):
        panel = eg.ConfigPanel()

        zones = [ 'Active Zone', 'Main Zone', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone A', 'Zone B', 'Zone C', 'Zone D' ]
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        statuses = [ 'Toggle On/Standby', 'On', 'Standby' ]
        wx.StaticText(panel, label="Power Status: ", pos=(10, 60))
        choice = wx.Choice(panel, -1, (10, 80), choices=statuses)
        if status in statuses:
            choice.SetStringSelection(status)
        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], statuses[choice.GetCurrentSelection()])

class SetSurroundMode(eg.ActionBase):
    def __call__(self, mode):
        if mode == 'Toggle Straight/Surround Decode':
            toggle_straight_decode()
        elif mode == 'Straight':
            straight()
        elif mode == 'Surround Decode':
            surround_decode()

    def Configure(self, mode='Toggle Straight/Surround Decode'):
        panel = eg.ConfigPanel()

        modes = [ 'Toggle Straight/Surround Decode', 'Straight', 'Surround Decode' ]
        wx.StaticText(panel, label="Surround Mode: ", pos=(10, 10))
        choice = wx.Choice(panel, -1, (10, 30), choices=modes)
        if mode in modes:
            choice.SetStringSelection(mode)
        while panel.Affirmed():
            panel.SetResult(modes[choice.GetCurrentSelection()])

class CursorAction(eg.ActionBase):
    def __call__(self, action, zone):
        code = None
        izone = convert_zone_to_int(zone)
        if izone == -1:
            izone = globals.active_zone
        if izone in [0,1]:
            if action == 'Up':
                code = '7A859D62'
            elif action == 'Down':
                code = '7A859C63'
            elif action == 'Left':
                code = '7A859F60'
            elif action == 'Right':
                code = '7A859E61'
            elif action == 'Enter':
                code = '7A85DE21'
            elif action == 'Return':
                code = '7A85AA55'
            elif action == 'Level':
                code = '7A858679'
            elif action == 'On_Screen':
                code = '7A85847B'
            elif action == 'Option':
                code = '7A856B14'
            elif action == 'Top Menu':
                code = '7A85A0DF'
            elif action == 'Pop Up Menu':
                code = '7A85A4DB'
        if izone == 2:
            if action == 'Up':
                code = '7A852B55'
            elif action == 'Down':
                code = '7A852C52'
            elif action == 'Left':
                code = '7A852D53'
            elif action == 'Right':
                code = '7A852E50'
            elif action == 'Enter':
                code = '7A852F51'
            elif action == 'Return':
                code = '7A853C42'
            elif action == 'Option':
                code = '7A856C12'
            elif action == 'Top Menu':
                code = '7A85A1DF'
            elif action == 'Pop Up Menu':
                code = '7A85A5DB'
        if code is not None:
            send_code(code)

    def Configure(self, action="Up", zone="Active Zone"):
        panel = eg.ConfigPanel()

        zones = [ 'Active Zone', 'Main Zone', 'Zone 2' ]
        actions = [ 'Up', 'Down', 'Left', 'Right', 'Enter', 'Return', 'Option', 'Top Menu', 'Pop Up Menu' ]

        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Cursor Action: ", pos=(10, 60))
        choice_action = wx.Choice(panel, -1, (10, 80), choices=actions)
        if action in actions:
            choice_action.SetStringSelection(action)

        while panel.Affirmed():
            panel.SetResult(actions[choice_action.GetCurrentSelection()], zones[choice_zone.GetCurrentSelection()])

class OperationAction(eg.ActionBase):
    def __call__(self, action, zone):
        code = None
        izone = convert_zone_to_int(zone, convert_active=True)
        if izone in [0,1]:
            code = globals.OPERATION_CODES[1][action]
        if izone == 2:
            code = globals.OPERATION_CODES[2][action]

        if code is not None:
            send_code(code)
        else:
            # It is possible the user's active zone is not yet supported
            eg.PrintError("Zone {0} is not yet supported for this action".format(izone if izone > -1 else chr(-1 * izone)))

    def Configure(self, action="Play", zone="Active Zone"):
        panel = eg.ConfigPanel()

        zones = [ 'Active Zone', 'Main Zone', 'Zone 2' ]
        actions = [ 'Play', 'Stop', 'Pause', 'Search-', 'Search+', 'Skip-', 'Skip+', 'FM', 'AM' ]

        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Operation: ", pos=(10, 60))
        choice_action = wx.Choice(panel, -1, (10, 80), choices=actions)
        if action in actions:
            choice_action.SetStringSelection(action)

        while panel.Affirmed():
            panel.SetResult(actions[choice_action.GetCurrentSelection()], zones[choice_zone.GetCurrentSelection()])

class NumCharAction(eg.ActionBase):
    def __call__(self, action, zone):
        code = None
        izone = convert_zone_to_int(zone, convert_active=True)
        if izone in [0,1]:
            code = globals.NUMCHAR_CODES[1][action]
        if izone == 2:
            code = globals.NUMCHAR_CODES[2][action]

        if code is not None:
            send_code(code)
        else:
            # It is possible the user's active zone is not yet supported
            eg.PrintError("Zone {0} is not yet supported for this action".format(izone if izone > -1 else chr(-1 * izone)))

    def Configure(self, action="1", zone="Main Zone"):
        panel = eg.ConfigPanel()

        zones = [ 'Active Zone', 'Main Zone', 'Zone 2' ]
        actions = [ '1', '2', '3', '4', '5', '6', '7', '8', '9', '+10', 'ENT' ]

        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Action: ", pos=(10, 60))
        choice_action = wx.Choice(panel, -1, (10, 80), choices=actions)
        if action in actions:
            choice_action.SetStringSelection(action)

        while panel.Affirmed():
            panel.SetResult(actions[choice_action.GetCurrentSelection()], zones[choice_zone.GetCurrentSelection()])

class GetInfo(eg.ActionBase):
    def __call__(self, object, cat):
        zone = None
        #zone specific objects
        if object == "Input Selection":
            object = "Input_Sel"
        if object == "Scene":
            return "not complete"
        if object == "Sound Program":
            object = "Sound_Program"
        if cat == "Main Zone":
            zone = 1
        if cat.startswith("Zone"):
            zone = convert_zone_to_int(cat)
        if object == "Volume Level":
            val, unit = get_status_strings(["Val", "Unit"], zone)
            return "{0} {1}".format(float(val) / 10.0, unit)
        if zone is not None:
            return get_status_string(object,zone)

        #all the rest are zone agnostic
        #object, input, location to get_device_string
        section = "List_Info"
        if object in ["Menu Layer", "Menu Name", "Current Line", "Max Line"] \
                or object in ['Line {0}'.format(i) for i in range(9)]:
            object = object.replace(' ', '_')
        else:
            section = "Play_Info"

        if object == "FM Mode":
            object = "FM_Mode"
        elif object == "Frequency":
            try:
                val, unit, band = get_device_strings(["Val", "Unit", "Band"], cat, section)
                return "{0} {1}".format(float(val) / 100.0 if band == "FM" else val, unit)
            except:
                eg.PrintError("Input not active or unavailable with your model.")
                return None
        elif object == "Audio Mode":
            object = "Current"
        elif object == "Antenna Strength":
            object = "Antenna_Lvl"
        elif object == "Channel Number":
            object = "Ch_Number"
        elif object == "Channel Name":
            object = "Ch_Name"
        elif object == "Playback Info":
            object = "Playback_Info"
        elif object == "Repeat Mode":
            object = "Repeat"
        elif object == "Connect Information":
            object = "Connect_Info"

        try:
            return get_device_string(object, cat, section)
        except:
            eg.PrintError("Input not active or unavailable with your model.")


    def Configure(self, object="Power", cat="Main Zone"):
        panel = eg.ConfigPanel()

        self.cats = [ 'Main Zone', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone A', 'Zone B', 'Zone C', 'Zone D', 'Tuner', 'HD Radio', 'SIRIUS', 'iPod', 'Bluetooth', 'Rhapsody', 'SIRIUS IR', 'Pandora', 'PC', 'NET RADIO', 'Napster', 'USB', 'USB iPod']

        wx.StaticText(panel, label="Category: ", pos=(10, 10))
        self.choice_cat = wx.Choice(panel, -1, (10, 30), choices=self.cats)
        if cat in self.cats:
            self.choice_cat.SetStringSelection(cat)
        self.choice_cat.Bind(wx.EVT_CHOICE, self.CategoryChanged)

        self.objects = [ 'Power', 'Sleep', 'Volume Level', 'Mute', 'Input Selection', 'Scene', 'Straight', 'Enhancer', 'Sound Program']
        wx.StaticText(panel, label="Object: ", pos=(10, 60))
        self.choice_object = wx.Choice(panel, -1, (10, 80), choices=self.objects)
        self.CategoryChanged()
        if object in self.objects:
            self.choice_object.SetStringSelection(object)
            
        while panel.Affirmed():
            panel.SetResult(self.objects[self.choice_object.GetCurrentSelection()], self.cats[self.choice_cat.GetCurrentSelection()])

    def CategoryChanged(self, event=None):
        cat = self.cats[self.choice_cat.GetCurrentSelection()]
        if cat == "Main Zone":
            self.objects = [ 'Power', 'Sleep', 'Volume Level', 'Mute', 'Input Selection', 'Scene', 'Straight', 'Enhancer', 'Sound Program']
        elif cat[:4] == "Zone":
            self.objects = [ 'Power', 'Sleep', 'Volume Level', 'Mute', 'Input Selection', 'Scene']
        elif cat == "Tuner":
            self.objects = [ 'Band', 'Frequency', 'FM Mode']
        elif cat == "HD Radio":
            self.objects = [ 'Band', 'Frequency', 'Audio Mode']
        elif cat == "SIRIUS":
            self.objects = [ 'Antenna Strength', 'Category', 'Channel Number', 'Channel Name', 'Artist', 'Song', 'Composer']
        elif cat == "iPod":
            self.objects = [ 'Playback Info', 'Repeat Mode', 'Shuffle', 'Artist', 'Album', 'Song', 'Menu Layer', 'Menu Name', 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5', 'Line 6', 'Line 7', 'Line 8', 'Current Line', 'Max Line']
        elif cat == "Bluetooth":
            self.objects = [ 'Connect Information']
        elif cat == "Rhapsody":
            self.objects = [ 'Playback Info', 'Repeat Mode', 'Shuffle', 'Artist', 'Album', 'Song', 'Menu Layer', 'Menu Name', 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5', 'Line 6', 'Line 7', 'Line 8', 'Current Line', 'Max Line']
        elif cat == "SIRIUS IR":
            self.objects = [ 'Playback Info', 'Artist', 'Channel', 'Title', 'Menu Layer', 'Menu Name', 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5', 'Line 6', 'Line 7', 'Line 8', 'Current Line', 'Max Line']
        elif cat == "Pandora":
            self.objects = [ 'Playback Info', 'Station', 'Album', 'Song', 'Menu Layer', 'Menu Name', 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5', 'Line 6', 'Line 7', 'Line 8', 'Current Line', 'Max Line']
        elif cat == "PC":
            self.objects = [ 'Playback Info', 'Repeat Mode', 'Shuffle', 'Artist', 'Album', 'Song', 'Menu Layer', 'Menu Name', 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5', 'Line 6', 'Line 7', 'Line 8', 'Current Line', 'Max Line']
        elif cat == "NET RADIO":
            self.objects = [ 'Playback Info', 'Station', 'Menu Layer', 'Menu Name', 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5', 'Line 6', 'Line 7', 'Line 8', 'Current Line', 'Max Line']
        elif cat == "Napster":
            self.objects = [ 'Playback Info', 'Repeat Mode', 'Shuffle', 'Artist', 'Album', 'Song', 'Menu Layer', 'Menu Name', 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5', 'Line 6', 'Line 7', 'Line 8', 'Current Line', 'Max Line']
        elif cat == "USB":
            self.objects = [ 'Playback Info', 'Repeat Mode', 'Shuffle', 'Artist', 'Album', 'Song', 'Menu Layer', 'Menu Name', 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5', 'Line 6', 'Line 7', 'Line 8', 'Current Line', 'Max Line']
        elif cat == "USB iPod":
            self.objects = [ 'Playback Info', 'Repeat Mode', 'Shuffle', 'Artist', 'Album', 'Song', 'Menu Layer', 'Menu Name', 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5', 'Line 6', 'Line 7', 'Line 8', 'Current Line', 'Max Line']
        else:
            eg.PrintError("Unknown Category!")
        self.choice_object.Clear()
        self.choice_object.AppendItems(self.objects)
        self.choice_object.SetSelection(0) 

class AutoDetectIP(eg.ActionBase):
    def __call__(self):
        eg.result = auto_detect_ip_threaded()

class VerifyStaticIP(eg.ActionBase):
    def __call__(self):
        if globals.ip_auto_detect:
            eg.PrintError('Static IP is not enabled!')
            return False
        else:
            return setup_ip() is not None

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
            toggle_radio_amfm()
        elif msg == 'RadioAutoFeqUp':
            auto_radio_freq('Up')
        elif msg == 'RadioAutoFreqDown':
            auto_radio_freq('Down')
        elif msg == 'RadioFeqUp':
            manual_radio_freq('Up')
        elif msg == 'RadioFreqDown':
            manual_radio_freq('Down')

           