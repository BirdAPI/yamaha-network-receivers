__author__ = 'Anthony Casagrande'

import globals
from client import *
from yamaha import *

# expose some information about the plugin through an eg.PluginInfo subclass
eg.RegisterPlugin(
    name = "Yamaha RX Network Receiver",
    author = "Anthony Casagrande",
    version = "0.9",
    kind = "external",
    createMacrosOnAdd = True,
    url = "",
    description = "Adds actions to control Yamaha RX-*** network receiver.",
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
        self.AddAction(SetScene)
        self.AddAction(SetSourceInput)
        self.AddAction(SetPowerStatus)
        self.AddAction(SetSurroundMode)
        self.AddActionsFromList(globals.ACTIONS, ActionPrototype)
        self.client = YamahaRXClient()
        
    def __start__(self, ip_address="N/A", port=80, ip_auto_detect=True, auto_detect_model="ANY", auto_detect_timeout=1.0):
        globals.ip_address = ip_address
        globals.port = port
        globals.ip_auto_detect = ip_auto_detect
        globals.auto_detect_model = auto_detect_model
        globals.auto_detect_timeout = auto_detect_timeout
        setup_ip()

    def autoDetectChecked(self, event):
        self.txt_ip.SetValue("N/A")
        self.txt_ip.SetEditable(not self.cb.GetValue())
        
    def Configure(self, ip_address="N/A", port=80, ip_auto_detect=True, auto_detect_model="ANY", auto_detect_timeout=1.0):
        x_start = 10
        x_padding = 60
        y_start = 10
        y_padding = 30
        label_padding = 3
        i = 0
        
        panel = eg.ConfigPanel()
        
        # Auto Detect IP
        self.cb = wx.CheckBox(panel, -1, 'Auto Detect IP Address', (x_start, y_start + (i * y_padding)))
        self.cb.SetValue(ip_auto_detect)
        wx.EVT_CHECKBOX(panel, self.cb.GetId(), self.autoDetectChecked)
        
        i += 1
        # IP Address
        wx.StaticText(panel, label="Static IP Address: ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        self.txt_ip = wx.TextCtrl(panel, -1, ip_address, (x_start + (x_padding * 2), y_start + (i * y_padding)), (100, -1))
        
        i += 1
        # Port
        wx.StaticText(panel, label="Port: ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        self.spin = wx.SpinCtrl(panel, -1, "", (x_start + x_padding, y_start + (i * y_padding)), (80, -1))
        self.spin.SetRange(1,65535)
        self.spin.SetValue(int(port))
        
        i += 1
        # Models (Auto Detect)
        models = [ 'ANY', 'RX-V867', 'RX-V473', 'RX-V775' ]
        wx.StaticText(panel, label="AV Receiver Model (For Auto Detect IP): ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        index = -1 if not auto_detect_model in models else models.index(auto_detect_model)
        self.combo = wx.ComboBox(panel, -1, pos=(x_start + (x_padding * 4), y_start + (i * y_padding)), size=(150, -1), choices=models, style=wx.CB_DROPDOWN)
        
        while panel.Affirmed():
            panel.SetResult(self.txt_ip.GetValue(), self.spin.GetValue(), self.cb.GetValue(), self.combo.GetValue(), 1.0)
        
