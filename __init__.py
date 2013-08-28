__author__ = 'Anthony Casagrande'

from client import *
from yamaha import *

# expose some information about the plugin through an eg.PluginInfo subclass

eg.RegisterPlugin(
    name = "Yamaha RX Network Receiver",
    author = "Anthony Casagrande",
    version = "0.7",
    kind = "external",
    createMacrosOnAdd = True,
    url = "",
    description = "Adds actions to control Yamaha RX-*** network receiver.",
)

ACTIONS = (   
    ("ToggleMute", "Toggle Mute", "Toggles mute state", "ToggleMute"),
    ("PowerOff", "Power Off", "Powers off machine", "PowerOff"),
    ("PowerStandby", "Power Standby", "Turns machine to standby", "PowerStandby"),
    ("PowerOn", "Power On", "Powers on machine", "PowerOn"),
    ("ToggleOnStandby", "Toggle On / Standby", "Toggles machine between on and standby", "ToggleOnStandby"),
    ("Source_HDMI1", "Source HDMI1", "Changes source to HDMI1", "Source_HDMI1"),
    ("Source_HDMI2", "Source HDMI2", "Changes source to HDMI2", "Source_HDMI2"),
    ("Source_HDMI3", "Source HDMI3", "Changes source to HDMI3", "Source_HDMI3"),
    ("Source_HDMI4", "Source HDMI4", "Changes source to HDMI4", "Source_HDMI4"),
    ("Source_HDMI5", "Source HDMI5", "Changes source to HDMI5", "Source_HDMI5"),
    ("Source_HDMI6", "Source HDMI6", "Changes source to HDMI6", "Source_HDMI6"),
    ("Source_HDMI7", "Source HDMI7", "Changes source to HDMI7", "Source_HDMI7"),
    ("Source_HDMI8", "Source HDMI8", "Changes source to HDMI8", "Source_HDMI8"),
    ("Source_HDMI9", "Source HDMI9", "Changes source to HDMI9", "Source_HDMI9"),
    ("Source_V-AUX", "Source V-AUX", "Changes source to V-AUX", "Source_V-AUX"),
    ("Source_AV1", "Source AV1", "Changes source to AV1", "Source_AV1"),
    ("Source_AV2", "Source AV2", "Changes source to AV2", "Source_AV2"),
    ("Source_AV3", "Source AV3", "Changes source to AV3", "Source_AV3"),
    ("Source_AV4", "Source AV4", "Changes source to AV4", "Source_AV4"),
    ("Source_AV5", "Source AV5", "Changes source to AV5", "Source_AV5"),
    ("Source_AV6", "Source AV6", "Changes source to AV6", "Source_AV6"),
    ("Source_TUNER", "Source Tuner", "Changes source to radio", "Source_TUNER"),
    ("Straight", "Straight", "Straight", "Straight"),
    ("SurroundDecode", "Surround Decode", "Surround Decode", "SurroundDecode"),
    ("ToggleStraightAndDecode", "Toggle Straight And Decode", "Toggles between Straight and Sourround Decode", "ToggleStraightAndDecode"),
    ("ToogleEnhancer", "Toggle Enhancer", "Toggles the enhancer on and off", "ToggleEnhancer"),
    #("NextSource", "Next Source", "Goes to the next source", "NextSource"),
    #("PreviousSource", "Previous Source", "Goes to the previous source", "PreviousSource"),
    #("ToggleSleep", "Toggle Sleep", "Toggles sleep mode", "ToggleSleep"),
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
        self.AddActionsFromList(ACTIONS, ActionPrototype)
        self.client = YamahaRXClient()
