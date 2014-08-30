# Python Imports
import wx.lib.agw.floatspin as FS

# Local Imports
import globals
from client import *
from yamaha import *

# expose some information about the plugin through an eg.PluginInfo subclass
eg.RegisterPlugin(
    name = "Yamaha RX-V Network Receiver",
    author = "Anthony Casagrande (BirdAPI), Jason Kloepping (Dragon470)",
    version = "1.0",
    kind = "external",
    # We don't auto load macros because they are not configured yet.
    createMacrosOnAdd = False,
    canMultiLoad = True,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=3382",
    description = "Control Yamaha RX-V network receivers."
)

class ActionPrototype(eg.ActionClass):
    def __call__(self):
        try:
            self.plugin.client.send_action(self.value, globals.ACTION_BUTTON)
        except:
            raise self.Exceptions.ProgramNotRunning

class YamahaRX(eg.PluginClass):
    def __init__(self):
        self.AddAction(SmartVolumeUp, clsName="Smart Volume Up", description="Increases the volume by step1 for a specified period of time, and then increases the volume by step2 each time after.")
        self.AddAction(SmartVolumeDown, clsName="Smart Volume Down", description="Decreases the volume by step1 for a specified period of time, and then decreases the volume by step2 each time after.")
        self.AddAction(SmartVolumeFinished, clsName="Smart Volume Finished", description="This MUST be called after a Smart Volume Up or Smart Volume Down in order to reset them for the next time.")
        self.AddAction(IncreaseVolume, clsName="Increase Volume", description="Increase the volume a specified amount on the specified zone.")
        self.AddAction(DecreaseVolume, clsName="Decrease Volume", description="Decrease the volume a specified amount on the specified zone.")
        self.AddAction(SetVolume, clsName="Set Exact Volume", description="Set the exact volume on the specified zone.")
        self.AddAction(SetScene, clsName="Set Scene", description="Change the scene number on the specified zone.")
        self.AddAction(SetSourceInput, clsName="Set Source Input", description="Set the source input on the specified zone.")
        self.AddAction(NextInput, clsName="Next Input", description="Set the source input on the specified zone to the next input in the specified list of inputs.")
        self.AddAction(PreviousInput, clsName="Previous Input", description="Set the source input on the specified zone to the previous input in the specified list of inputs.")
        self.AddAction(SetFeatureVideoOut, clsName="Feature Input Video Out", description="Set the source video output from a specified input.  For Main Zone only")
        self.AddAction(SetPowerStatus, clsName="Set Power Status", description="Set the power status for the receiver (Main Zone), or turn on/off additional zones.")
        self.AddAction(SetSurroundMode, clsName="Set Surround Mode", description="Choose between Surround Decode and Straight, or toggle between the two.")
        self.AddAction(Set7ChannelMode, clsName="Set 7 Channel Mode", description="Turn 7 Channel Stereo mode on and off. Usually turned 'On' after setting 'Surround Mode' to 'Surround Decode'.")  # McB 1/11/2014 - Turn 7-channel mode on and off
        self.AddAction(CursorAction, clsName="Cursor Action", description="Generic cursor action: Up, Down, Left, Right, Enter, Return, Level, On Screen, Option, Top Menu, Pop Up Menu")
        self.AddAction(SetSleepStatus, clsName="Set Sleep Status", description= "Set the sleep state for the receiver (Main Zone), or additional zones.")
        self.AddAction(NumCharAction, clsName="NumChar Action", description="Generic NumChar action: 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, +10, ENT")
        self.AddAction(OperationAction, clsName="Operation Action", description="Generic Operation action: Play, Stop, Pause, Search-, Search+, Skip-, Skip+, FM, AM")
        self.AddAction(SetActiveZone, clsName="Set Active Zone", description="Sets which zone is currently active. This affects any action that is based on 'Active Zone'.")
        self.AddActionsFromList(globals.ACTIONS, ActionPrototype)
        self.AddAction(GetInfo, clsName="Get Info", description="Gets various info from the receiver.")
        self.AddAction(GetAvailability, clsName="Get Availability", description="Gets the available input sources.")
        self.grp1 = self.AddGroup('Config', 'General configuration actions')
        self.grp1.AddAction(AutoDetectIP, clsName="Auto Detect IP", description="Runs the IP Address auto detection in case your receiver's ip address has changed since starting EventGhost.")
        self.grp1.AddAction(VerifyStaticIP, clsName="Verify Static IP", description="Checks whether there is a Yamaha AV Receiver at the other end of the static ip specified in the configuration.")
        #Add all actions again but hidden so they can be exposed for eg python scripts (not sure why adding clsName removes the ability to call the action outside the plugin)
        self.AddAction(SmartVolumeUp, hidden=True)
        self.AddAction(SmartVolumeDown, hidden=True)
        self.AddAction(SmartVolumeFinished, hidden=True)
        self.AddAction(IncreaseVolume, hidden=True)
        self.AddAction(DecreaseVolume, hidden=True)
        self.AddAction(SetVolume, hidden=True)
        self.AddAction(SetScene, hidden=True)
        self.AddAction(SetSourceInput, hidden=True)
        self.AddAction(NextInput, hidden=True)
        self.AddAction(SetFeatureVideoOut, hidden=True)
        self.AddAction(PreviousInput, hidden=True)
        self.AddAction(SetPowerStatus, hidden=True)
        self.AddAction(SetSurroundMode, hidden=True)
        self.AddAction(Set7ChannelMode, hidden=True) # McB 1/11/2014 - Turn 7-channel mode on and off
        self.AddAction(CursorAction, hidden=True)
        self.AddAction(SetSleepStatus, hidden=True)
        self.AddAction(NumCharAction, hidden=True)
        self.AddAction(OperationAction, hidden=True)
        self.AddAction(SetActiveZone, hidden=True)
        self.AddAction(GetInfo, hidden=True)
        self.AddAction(GetAvailability, hidden=True)
        self.grp1.AddAction(AutoDetectIP, hidden=True)
        self.grp1.AddAction(VerifyStaticIP, hidden=True)
        self.client = YamahaRXClient()
        
    def __start__(self, ip_address="", port=80, ip_auto_detect=True, auto_detect_model="ANY", auto_detect_timeout=1.0, default_timeout=3.0):
        globals.ip_address = ip_address
        globals.port = port
        globals.ip_auto_detect = ip_auto_detect
        globals.auto_detect_model = auto_detect_model
        globals.auto_detect_timeout = auto_detect_timeout
        ip = setup_ip()
        if ip is not None:
            setup_availability()

    def autoDetectChanged(self, event):
        if self.cb.GetValue():
            self.txt_ip.Hide()
            self.lbl_ip.Hide()
            
            self.lbl_model.Show()
            self.combo.Show()
        else:
            self.txt_ip.Show()
            self.lbl_ip.Show()
            
            self.lbl_model.Hide()
            self.combo.Hide()

            self.txt_ip.SetFocus()
            self.txt_ip.SetInsertionPoint(len(self.txt_ip.GetValue()))
        
    def Configure(self, ip_address="", port=80, ip_auto_detect=True, auto_detect_model="ANY", auto_detect_timeout=1.0, default_timeout=3.0):
        x_start = 10
        x_padding = 60
        y_start = 10
        y_padding = 22
        label_padding = 3
        i = 0

        if ip_address == "":
            # Default ip address to network prefix to save typing
            ip_address = get_network_prefix() + '.'
        
        panel = eg.ConfigPanel()

        lbl_net = wx.StaticText(panel, label="Network Settings: ", pos=(0, y_start + label_padding + (i * y_padding)))
        font = lbl_net.GetFont()
        font.SetPointSize(10)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        lbl_net.SetFont(font)
        
        i += 1
        # Auto Detect IP
        self.cb = wx.CheckBox(panel, -1, 'Auto Detect IP Address', (x_start, y_start + (i * y_padding)))
        self.cb.SetValue(ip_auto_detect)
        self.cb.Bind(wx.EVT_CHECKBOX, self.autoDetectChanged)
        
        i += 1
        # IP Address
        self.lbl_ip = wx.StaticText(panel, label="Static IP Address: ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        self.txt_ip = wx.TextCtrl(panel, -1, ip_address, (x_start + (x_padding * 2), y_start + (i * y_padding)), (100, -1))
        
        # Do not add to index, so they go over top each other
        # Models (Auto Detect)
        self.lbl_model = wx.StaticText(panel, label="AV Receiver Model (If you have multiple on network): ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        self.combo = wx.ComboBox(panel, -1, pos=(x_start + (x_padding * 4.5), y_start + (i * y_padding)), size=(100, -1), choices=globals.ALL_MODELS, style=wx.CB_DROPDOWN)
        self.combo.SetValue(auto_detect_model)
        
        i += 1
        lbl_adv = wx.StaticText(panel, label="Advanced Settings: ", pos=(0, y_start + label_padding + (i * y_padding)))
        font = lbl_adv.GetFont()
        font.SetPointSize(10)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        lbl_adv.SetFont(font)
        
        i += 1
        # Port
        wx.StaticText(panel, label="Port: ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        self.spin = wx.SpinCtrl(panel, -1, "", (x_start + x_padding, y_start + (i * y_padding)), (80, -1))
        self.spin.SetRange(1,65535)
        self.spin.SetValue(int(port))
        
        i += 1
        # Auto Detect Timeout
        wx.StaticText(panel, label="Auto Detect IP Timeout (seconds): ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        self.auto_time = FS.FloatSpin(panel, -1, pos=(x_start + (x_padding * 3), y_start + (i * y_padding)), min_val=0.1, max_val=10.0,
                                 increment=0.1, value=float(auto_detect_timeout), agwStyle=FS.FS_LEFT)
        self.auto_time.SetFormat("%f")
        self.auto_time.SetDigits(1)
        
        i += 1
        # Default Timeout
        wx.StaticText(panel, label="Default Timeout (seconds): ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        self.def_time = FS.FloatSpin(panel, -1, pos=(x_start + (x_padding * 3), y_start + (i * y_padding)), min_val=0.1, max_val=10.0,
                                 increment=0.1, value=float(default_timeout), agwStyle=FS.FS_LEFT)
        self.def_time.SetFormat("%f")
        self.def_time.SetDigits(1)
        
        # Call this once after setting everything up to change the visibility of things
        self.autoDetectChanged(None)

        while panel.Affirmed():
            panel.SetResult(self.txt_ip.GetValue(), self.spin.GetValue(), self.cb.GetValue(), str(self.combo.GetValue()), self.auto_time.GetValue(), self.def_time.GetValue())
        
