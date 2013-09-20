__author__ = 'Anthony Casagrande'

import wx.lib.agw.floatspin as FS

import globals
from client import *
from yamaha import *

# expose some information about the plugin through an eg.PluginInfo subclass
eg.RegisterPlugin(
    name = "Yamaha RX-V Network Receiver",
    author = "Anthony Casagrande (BirdAPI)",
    version = "0.9",
    kind = "external",
    createMacrosOnAdd = True,
    canMultiLoad = True,
    url = "https://github.com/BirdAPI/yamaha-network-receivers",
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
        self.AddAction(IncreaseVolume)
        self.AddAction(DecreaseVolume)
        self.AddAction(SetVolume)
        self.AddAction(SetScene)
        self.AddAction(SetSourceInput)
        self.AddAction(SetPowerStatus)
        self.AddAction(SetSurroundMode)
        self.AddAction(CursorAction)
        self.AddAction(NumCharAction)
        self.AddAction(OperationAction)
        self.AddAction(SetActiveZone)
        self.AddActionsFromList(globals.ACTIONS, ActionPrototype)
        self.client = YamahaRXClient()
        
    def __start__(self, ip_address="", port=80, ip_auto_detect=True, auto_detect_model="ANY", auto_detect_timeout=1.0, default_timeout=3.0):
        globals.ip_address = ip_address
        globals.port = port
        globals.ip_auto_detect = ip_auto_detect
        globals.auto_detect_model = auto_detect_model
        globals.auto_detect_timeout = auto_detect_timeout
        setup_ip()

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
        
    def Configure(self, ip_address="", port=80, ip_auto_detect=True, auto_detect_model="ANY", auto_detect_timeout=1.0, default_timeout=3.0):
        x_start = 10
        x_padding = 60
        y_start = 10
        y_padding = 22
        label_padding = 3
        i = 0
        
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
        
