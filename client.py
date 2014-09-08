# Python Imports
import wx.lib.agw.floatspin as FS
from datetime import datetime
import re
import time
from threading import Thread

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

        zones = get_available_zones(True, globals.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Increase Amount (Step 1): ", pos=(10, 60))
        fs_step1 = FS.FloatSpin(panel, -1, pos=(170, 57), min_val=0.5, max_val=10,
            increment=0.5, value=float(step1), agwStyle=FS.FS_LEFT)
        wx.StaticText(panel, label="dB", pos=(270, 60))
        fs_step1.SetFormat("%f")
        fs_step1.SetDigits(1)

        wx.StaticText(panel, label="Time between Step 1 to Step 2: ", pos=(10, 100))
        fs_wait = FS.FloatSpin(panel, -1, pos=(170, 97), min_val=0.5, max_val=999,
            increment=0.1, value=float(wait), agwStyle=FS.FS_LEFT)
        wx.StaticText(panel, label="Seconds", pos=(270, 100))
        fs_wait.SetFormat("%f")
        fs_wait.SetDigits(1)

        wx.StaticText(panel, label="Increase Amount (Step 2): ", pos=(10, 140))
        fs_step2 = FS.FloatSpin(panel, -1, pos=(170, 137), min_val=0.5, max_val=10,
            increment=0.5, value=float(step2), agwStyle=FS.FS_LEFT)
        wx.StaticText(panel, label="dB", pos=(270, 140))

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

        zones = get_available_zones(True, globals.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        wx.StaticText(panel, label="Decrease Amount (Step 1): ", pos=(10, 60))
        fs_step1 = FS.FloatSpin(panel, -1, pos=(170, 57), min_val=0.5, max_val=10,
            increment=0.5, value=float(step1), agwStyle=FS.FS_LEFT)
        wx.StaticText(panel, label="dB", pos=(270, 60))
        fs_step1.SetFormat("%f")
        fs_step1.SetDigits(1)

        wx.StaticText(panel, label="Time between Step 1 to Step 2: ", pos=(10, 100))
        fs_wait = FS.FloatSpin(panel, -1, pos=(170, 97), min_val=0.5, max_val=999,
            increment=0.1, value=float(wait), agwStyle=FS.FS_LEFT)
        wx.StaticText(panel, label="Seconds", pos=(270, 100))
        fs_wait.SetFormat("%f")
        fs_wait.SetDigits(1)

        wx.StaticText(panel, label="Decrease Amount (Step 2): ", pos=(10, 140))
        fs_step2 = FS.FloatSpin(panel, -1, pos=(170, 137), min_val=0.5, max_val=10,
            increment=0.5, value=float(step2), agwStyle=FS.FS_LEFT)
        wx.StaticText(panel, label="dB", pos=(270, 140))
        fs_step2.SetFormat("%f")
        fs_step2.SetDigits(1)

        while panel.Affirmed():
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], fs_step1.GetValue(), fs_step2.GetValue(), fs_wait.GetValue())

class IncreaseVolume(eg.ActionBase):
    def __call__(self, zone, step):
        increase_volume(convert_zone_to_int(zone), float(step))

    def Configure(self, zone='Active Zone', step=0.5):
        panel = eg.ConfigPanel()

        zones = get_available_zones(True, globals.AVAILABLE_ZONES)
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

        zones = get_available_zones(True, globals.AVAILABLE_ZONES)
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

        zones = get_available_zones(True, globals.AVAILABLE_ZONES)
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
        zones = get_available_zones(False, globals.AVAILABLE_ZONES) # Don't include active zone!
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
        if source =="Tuner":        #special case.  I don't know why
            source = "TUNER"
        change_source(source, izone)

    def Configure(self, zone="Active Zone", source="HDMI1"):
        panel = eg.ConfigPanel()

        zones = get_available_zones(True, globals.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)
        inputs = globals.AVAILABLE_SOURCES
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

        zones = get_available_zones(True, globals.AVAILABLE_ZONES)
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

class SetSleepStatus(eg.ActionBase):
    def __call__(self, zone, status):
        izone = convert_zone_to_int(zone)
        set_sleep(status, izone)

    def Configure(self, zone="Active Zone", status="Off"):
        panel = eg.ConfigPanel()

        zones = get_available_zones(True, globals.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (10, 30), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        statuses = [ 'Off', '30 min', '60 min', '90 min', '120 min', 'Last' ]
        wx.StaticText(panel, label="Sleep Status: ", pos=(10, 60))
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

class Set7ChannelMode(eg.ActionBase): # McB 1/11/2014 - Turn 7-channel mode on and off
    def __call__(self, mode):
        if mode == 'On':
            channel7_on()
        elif mode == 'Off':
            channel7_off()

    def Configure(self, mode='On'):
        panel = eg.ConfigPanel()

        modes = [ 'On', 'Off' ]
        wx.StaticText(panel, label="7-Channel Mode: ", pos=(10, 10))
        choice = wx.Choice(panel, -1, (10, 30), choices=modes)
        if mode in modes:
            choice.SetStringSelection(mode)
        while panel.Affirmed():
            panel.SetResult(modes[choice.GetCurrentSelection()])

class CursorAction(eg.ActionBase):
    def __call__(self, action, zone):
        code = None
        izone = convert_zone_to_int(zone, convert_active=True)
        if izone in [0,1]:
            code = globals.CURSOR_CODES[1][action]
        if izone == 2:
            # Not all of the actions are supported for zone 2
            code = globals.CURSOR_CODES[2].get(action, None)

        if code is not None:
            send_code(code)
        else:
            # It is possible the user's active zone is not yet supported
            eg.PrintError("Zone {0} is not yet supported for this action".format(izone if izone > -1 else chr(-1 * izone)))

    def Configure(self, action="Up", zone="Active Zone"):
        panel = eg.ConfigPanel()

        zones = get_available_zones(True, globals.TWO_ZONES_PLUS_ACTIVE, limit=2)
        actions = globals.CURSOR_CODES[1].keys()

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

        zones = get_available_zones(True, globals.TWO_ZONES_PLUS_ACTIVE, limit=2)
        actions = globals.OPERATION_CODES[1].keys()

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

        zones = get_available_zones(True, globals.TWO_ZONES_PLUS_ACTIVE, limit=2)
        actions = sorted(globals.NUMCHAR_CODES[1].keys(), key=lambda k: int(k) if len(k) == 1 else 10 + len(k))

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
                val, unit, band, exp = get_device_strings(["Val", "Unit", "Band", "Exp"], cat, section)
                if int(exp) == 0:
                    real_val = int(val)
                else:
                    real_val = float(val) / pow(10, int(exp))
                return "{0} {1}".format(real_val, unit)
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

        self.cats = globals.AVAILABLE_ZONES + globals.AVAILABLE_INFO_SOURCES

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
            self.objects = globals.MAIN_ZONE_OBJECTS
        elif cat.startswith("Zone"):
            self.objects = globals.ZONE_OBJECTS
        elif cat == "Tuner" or cat == "TUNER":
            self.objects = [ 'Band', 'Frequency', 'FM Mode']
        elif cat == "HD Radio":
            self.objects = [ 'Band', 'Frequency', 'Audio Mode']
        elif cat == "SIRIUS" or cat == "SiriusXM" or cat == "Spotify":
            self.objects = globals.SIRIUS_OBJECTS
        elif cat == "iPod":
            self.objects = globals.GENERIC_PLAYBACK_OBJECTS
        elif cat == "Bluetooth":
            self.objects = [ 'Connect Information']
        elif cat == "Rhapsody":
            self.objects = globals.GENERIC_PLAYBACK_OBJECTS
        elif cat == "SIRIUSInternetRadio":
            self.objects = globals.SIRIUS_IR_OBJECTS
        elif cat == "Pandora":
            self.objects = globals.PANDORA_OBJECTS
        elif cat == "PC" or "SERVER":
            self.objects = globals.GENERIC_PLAYBACK_OBJECTS
        elif cat == "NET RADIO" or cat == "NET_RADIO":
            self.objects = globals.NET_RADIO_OBJECTS
        elif cat == "Napster":
            self.objects = globals.GENERIC_PLAYBACK_OBJECTS
        elif cat == "USB":
            self.objects = globals.GENERIC_PLAYBACK_OBJECTS
        elif cat == "iPod (USB)" or cat == "iPod_USB" or cat == "Airplay":
            self.objects = globals.GENERIC_PLAYBACK_OBJECTS
        else:
            eg.PrintError("Unknown Category!")
        self.choice_object.Clear()
        self.choice_object.AppendItems(self.objects)
        self.choice_object.SetSelection(0) 

class GetAvailability(eg.ActionBase):
    def __call__(self):
        setup_availability()
        print 'Zones:', globals.AVAILABLE_ZONES
        print 'Inputs:', globals.AVAILABLE_SOURCES
        return list(globals.AVAILABLE_SOURCES)

class AutoDetectIP(eg.ActionBase):
    def __call__(self):
        ip = auto_detect_ip_threaded()
        if ip is not None:
            setup_availability()
        return ip

class VerifyStaticIP(eg.ActionBase):
    def __call__(self):
        if globals.ip_auto_detect:
            eg.PrintError('Static IP is not enabled!')
            return False
        else:
            ip = setup_ip()
            if ip is not None:
                setup_availability()
            return ip is not None

class NextInput(eg.ActionBase):
    def __call__(self, zone, inputs):
        izone = convert_zone_to_int(zone, convert_active=True)
        src = get_source_name(izone)
        index = inputs.index(src) if src in inputs else -1
        self._next_input(izone, index, inputs)

    def _next_input(self, izone, cur_index, inputs):
        next_index = 0
        if cur_index != -1:
            if cur_index < len(inputs) - 1:
                next_index = cur_index + 1
            else:
                next_index = 0
        else:
            # Current source not in the user's list. Change to the first item?
            next_index = 0
            print "Warning: Current source was not in the list of sources. Changing to first source in list."
        print "Switching input to", inputs[next_index]
        change_source(inputs[next_index], izone)

        t = Thread(target=self._verify_input, args=[izone, next_index, inputs])
        t.start()

    def _verify_input(self, izone, index, inputs, wait=0.3):
        time.sleep(wait)
        src = get_source_name(izone)
        if src != inputs[index]:
            eg.PrintError("Source input did not change! Your receiver may not have this input.")
            print "Skipping to next input."
            self._next_input(izone, index, inputs)

    def Configure(self, zone='Active Zone', inputs=['HDMI1']):
        panel = eg.ConfigPanel()

        zones = get_available_zones(True, globals.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (45, 7), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        y = 45
        x_start = 10
        x = x_start
        num_per_row = 5
        x_padding = 80
        y_padding = 20

        sources = globals.AVAILABLE_SOURCES
        self.cbs = []
        for i in range(len(sources)):
            if i > 0 and i % num_per_row == 0:
                x = x_start
                y += y_padding
            cb = wx.CheckBox(panel, -1, sources[i], (x, y))
            cb.SetValue(sources[i] in inputs)
            self.cbs.append(cb)
            x += x_padding

        # Futile attempt at setting a scrollbar, not working
        # panel.SetScrollbar(wx.VERTICAL, 0, 95, 100)

        while panel.Affirmed():
            res = []
            for i in range(len(self.cbs)):
                if self.cbs[i].GetValue():
                    res.append(sources[i])
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], res)

class PreviousInput(eg.ActionBase):
    def __call__(self, zone, inputs):
        izone = convert_zone_to_int(zone, convert_active=True)
        src = get_source_name(izone)
        index = inputs.index(src) if src in inputs else -1
        self._prev_input(izone, index, inputs)

    def _prev_input(self, izone, cur_index, inputs):
        prev_index = 0
        if cur_index != -1:
            if cur_index > 0:
                prev_index = cur_index - 1
            else:
                prev_index = len(inputs) - 1
        else:
            # Current source not in the user's list. Change to the first item?
            prev_index = 0
            print "Warning: Current source was not in the list of sources. Changing to first source in list."
        print "Switching input to", inputs[prev_index]
        change_source(inputs[prev_index], izone)

        t = Thread(target=self._verify_input, args=[izone, prev_index, inputs])
        t.start()

    def _verify_input(self, izone, index, inputs, wait=0.3):
        time.sleep(wait)
        src = get_source_name(izone)
        if src != inputs[index]:
            eg.PrintError("Source input did not change! Your receiver may not have this input.")
            print "Skipping to previous input."
            self._prev_input(izone, index, inputs)

    def Configure(self, zone='Active Zone', inputs=['HDMI1']):
        panel = eg.ConfigPanel()

        zones = get_available_zones(True, globals.AVAILABLE_ZONES)
        wx.StaticText(panel, label="Zone: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (45, 7), choices=zones)
        if zone in zones:
            choice_zone.SetStringSelection(zone)

        y = 45
        x_start = 10
        x = x_start
        num_per_row = 5
        x_padding = 80
        y_padding = 20

        sources = globals.AVAILABLE_SOURCES
        self.cbs = []
        for i in range(len(sources)):
            if i > 0 and i % num_per_row == 0:
                x = x_start
                y += y_padding
            cb = wx.CheckBox(panel, -1, sources[i], (x, y))
            cb.SetValue(sources[i] in inputs)
            self.cbs.append(cb)
            x += x_padding

        # Futile attempt at setting a scrollbar, not working
        # panel.SetScrollbar(wx.VERTICAL, 0, 95, 100)

        while panel.Affirmed():
            res = []
            for i in range(len(self.cbs)):
                if self.cbs[i].GetValue():
                    res.append(sources[i])
            panel.SetResult(zones[choice_zone.GetCurrentSelection()], res)

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
        elif msg == 'NextRadioPreset':
            next_radio_preset()
        elif msg == 'PreviousRadioPreset':
            prev_radio_preset()
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

class SetFeatureVideoOut(eg.ActionBase):

    def __call__(self, Feature, Source):
        feature_video_out(Feature, Source)
        
    def Configure(self, Feature="Tuner", Source="Off"):
        panel = eg.ConfigPanel()
        self.Source = Source

        wx.StaticText(panel, label="Feature Input: ", pos=(10, 10))
        choice_zone = wx.Choice(panel, -1, (95, 7), choices=globals.AVAILABLE_INFO_SOURCES)
        if Feature in globals.AVAILABLE_INFO_SOURCES:
            choice_zone.SetStringSelection(Feature)

        y = 45
        x_start = 10
        x = x_start
        num_per_row = 5
        x_padding = 80
        y_padding = 20

        sources = ['Off'] + globals.AVAILABLE_INPUT_SOURCES
        self.cbs = []
        for i in range(len(sources)):
            if i > 0 and i % num_per_row == 0:
                x = x_start
                y += y_padding
            cb = wx.CheckBox(panel, -1, sources[i], (x, y))
            if Source == sources[i]:
                cb.SetValue(True)
            else:
                cb.SetValue(False)
            cb.Bind(wx.EVT_CHECKBOX, lambda evt, temp=i: self.SourceChanged(evt, temp))
            self.cbs.append(cb)
            x += x_padding

        while panel.Affirmed():
            for i in range(len(self.cbs)):
                if self.cbs[i].GetValue():
                    res = sources[i]
            panel.SetResult(globals.AVAILABLE_INFO_SOURCES[choice_zone.GetCurrentSelection()], res)
            
    def SourceChanged(self, event, item):
        sources = ['Off'] + globals.AVAILABLE_INPUT_SOURCES
        self.Source = sources[item]
        for i in range(len(sources)):
            if i == item:
                self.cbs[i].SetValue(True)
            else:
                self.cbs[i].SetValue(False)

class SetDisplayDimmer(eg.ActionBase):

    def __call__(self, level):
        levels = ['100%','75%','50%','25%','10%']
        lev = levels.index(level)
        DisplayDimmer(int(lev)*-1)

    def Configure(self, level='100%'):
        panel = eg.ConfigPanel()

        levels = ['100%','75%','50%','25%','10%']
        wx.StaticText(panel, label="Brightness: ", pos=(10, 10))
        choice_level = wx.Choice(panel, -1, (10, 50), choices=levels)
        if level in levels:
            choice_level.SetStringSelection(level)
        while panel.Affirmed():
            panel.SetResult(levels[choice_level.GetCurrentSelection()])
            
class SetAudioIn(eg.ActionBase):

    def __call__(self, Audio, Source):
        source_audio_in(Audio, Source)
        
    def Configure(self, Audio="HDMI1", Source="HDMI_1"):
        panel = eg.ConfigPanel()
        self.Source = Source[:-2] + Source[-1:]
        print self.Source
        self.VidChoices = []
        PosChoices = ['HDMI1', 'HDMI2', 'HDMI3', 'HDMI4', 'HDMI5', 'HDMI6', 'HDMI7', 'HDMI8', 'HDMI9', 'AV1', 'AV2']
        for x in PosChoices:
            if x in globals.AVAILABLE_SOURCES:
                self.VidChoices.append(x)
        wx.StaticText(panel, label="Video Input: ", pos=(10, 10))
        self.choice_video = wx.Choice(panel, -1, (95, 7), choices=self.VidChoices)
        if self.Source in self.VidChoices:
            self.choice_video.SetStringSelection(self.Source)
        self.choice_video.Bind(wx.EVT_CHOICE, self.VidChanged)
        
        PosSources = ['AV1', 'AV2', 'AV3', 'AV4', 'AV5', 'AV6', 'AV7', 'AV8', 'AV9', 'AUDIO1', 'AUDIO2']
        self.AudChoices = [self.Source]
        for x in PosSources:
            if x in globals.AVAILABLE_SOURCES:
                self.AudChoices.append(x)
        wx.StaticText(panel, label="Audio Input: ", pos=(10, 40))
        self.choice_audio = wx.Choice(panel, -1, (95, 37), choices=self.AudChoices)
        if Audio in self.AudChoices:
            self.choice_audio.SetStringSelection(Audio)
         
        while panel.Affirmed():
            vid = self.VidChoices[self.choice_video.GetCurrentSelection()]
            vid = vid[:-1] + "_" + vid[-1:]
            panel.SetResult(self.AudChoices[self.choice_audio.GetCurrentSelection()], vid)
            
    def VidChanged(self, event):
        self.AudChoices[0] = self.VidChoices[self.choice_video.GetCurrentSelection()]
        self.choice_audio.Clear()
        self.choice_audio.AppendItems(self.AudChoices)
        self.choice_audio.SetSelection(0)