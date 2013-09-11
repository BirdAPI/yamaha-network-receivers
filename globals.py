# settings
ip_address=""
port=80
ip_auto_detect=True
auto_detect_model="ANY"
auto_detect_timeout=1.0
default_timeout=3.0

# runtime
FOUND_IP = None
MODEL = None

# static / constants
ACTIONS = (   
    ("ToggleMute", "Toggle Mute", "Toggles mute state", "ToggleMute"),
    ("ToogleEnhancer", "Toggle Enhancer", "Toggles the enhancer on and off", "ToggleEnhancer"),
    ("NextRadioPreset", "Next Radio Preset", "Goes to next radio preset, or if radio is not on, it turns it on. Also wraps when you go past the last preset.", "NextRadioPreset"),
    ("PreviousRadioPreset", "Previous Radio Preset", "Goes to previous radio preset, or if radio is not on, it turns it on. Also wraps to the end when you go past the first preset.", "PreviousRadioPreset"),
    ("ToggleRadioAMFM", "Toggle Radio AM / FM", "Toggles radio between AM and FM", "ToggleRadioAMFM"),
    ("RadioAutoFreqUp", "Radio Auto Freq Up", "Auto increases the radio frequency", "RadioAutoFreqUp"),
    ("RadioAtuoFreqDown", "Radio Auto Freq Down", "Auto decreases the radio frequency", "RadioAutoFreqDown"),
    ("RadioFreqUp", "Radio Freq Up", "Increases the radio frequency", "RadioFreqUp"),
    ("RadioFreqDown", "Radio Freq Down", "Decreases the radio frequency", "RadioFreqDown")
)  

ALL_MODELS = [ 'ANY', 
               '', 
               'RX-V867', 'RX-V1067', 'RX-V2067',
               '',
               'RX-V671', 'RX-V871',
               '',
               'RX-V473', 'RX-V573', 'RX-V673', 'RX-V773',
               '',
               'RX-V475', 'RX-V575', 'RX-V675', 'RX-V775' ]

# EventGhost Constants
ACTION_EXECBUILTIN = 0x01
ACTION_BUTTON = 0x02
