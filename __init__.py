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

    def Configure(self, ip_address="N/A", port=80, ip_auto_detect=True, auto_detect_model="ANY", auto_detect_timeout=1.0):
        x_start = 10
        x_padding = 60
        y_start = 10
        y_padding = 30
        label_padding = 3
        i = 0
        
        panel = eg.ConfigPanel()
        # IP Address
        wx.StaticText(panel, label="IP Address: ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        txt_ip = wx.TextCtrl(panel, -1, ip_address, (x_start + x_padding, y_start), (100, -1))
        
        i += 1
        # Port
        wx.StaticText(panel, label="Port: ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        spin = wx.SpinCtrl(panel, -1, "", (x_start + x_padding, y_start + (i * y_padding)), (80, -1))
        spin.SetRange(1,65535)
        spin.SetValue(int(port))
        
        while panel.Affirmed():
            panel.SetResult(txt_ip.GetValue(), spin.GetValue())
