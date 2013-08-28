__author__ = 'Anthony Casagrande'

from client import *
from yamaha import *
import globals

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

ACTIONS = (   
    ("ToggleMute", "Toggle Mute", "Toggles mute state", "ToggleMute"),
    ("Straight", "Straight", "Straight", "Straight"),
    ("SurroundDecode", "Surround Decode", "Surround Decode", "SurroundDecode"),
    ("ToggleStraightAndDecode", "Toggle Straight And Decode", "Toggles between Straight and Sourround Decode", "ToggleStraightAndDecode"),
    ("ToogleEnhancer", "Toggle Enhancer", "Toggles the enhancer on and off", "ToggleEnhancer"),
    ("NextRadioPreset", "Next Radio Preset", "Goes to next radio preset, or if radio is not on, it turns it on. Also wraps when you go past the last preset.", "NextRadioPreset"),
    ("PreviousRadioPreset", "Previous Radio Preset", "Goes to previous radio preset, or if radio is not on, it turns it on. Also wraps to the end when you go past the first preset.", "PreviousRadioPreset"),
    ("ToggleRadioAMFM", "Toggle Radio AM / FM", "Toggles radio between AM and FM", "ToggleRadioAMFM"),
    ("RadioAutoFreqUp", "Radio Auto Freq Up", "Auto increases the radio frequency", "RadioAutoFreqUp"),
    ("RadioAtuoFreqDown", "Radio Auto Freq Down", "Auto decreases the radio frequency", "RadioAutoFreqDown"),
    ("RadioFreqUp", "Radio Freq Up", "Increases the radio frequency", "RadioFreqUp"),
    ("RadioFreqDown", "Radio Freq Down", "Decreases the radio frequency", "RadioFreqDown")
)    

class ActionPrototype(eg.ActionClass):
    def __call__(self):
        try:
            self.plugin.client.send_action(self.value, ACTION_BUTTON)
        except:
            raise self.Exceptions.ProgramNotRunning

class YamahaRX(eg.PluginClass):
    def __init__(self):
        self.AddAction(IncreaseVolume)
        self.AddAction(DecreaseVolume)
        self.AddAction(SetScene)
        self.AddAction(SetSourceInput)
        self.AddAction(SetPowerStatus)
        #self.AddActionsFromList(ACTIONS, ActionPrototype)
        self.client = YamahaRXClient()
        
    def __start__(self, ip_address="", port=80, ip_auto_detect=True, auto_detect_model="ANY", auto_detect_timeout=1.0):
        setup_ip()

    def Configure(self, ip_address="", port=80, ip_auto_detect=True, auto_detect_model="ANY", auto_detect_timeout=1.0):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, myString)
        panel.sizer.Add(textControl, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())
