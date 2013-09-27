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

active_zone = 0
smart_vol_up_start = None
smart_vol_down_start = None

# static / constants
ACTIONS = (   
    ("ToggleMute", "Toggle Mute", "Toggles mute state", "ToggleMute"),
    ("ToogleEnhancer", "Toggle Enhancer", "Toggles the enhancer on and off", "ToggleEnhancer"),
    ("NextRadioPreset", "Next Radio Preset", "Goes to next radio preset, or if radio is not on, it turns it on. Also wraps when you go past the last preset.", "NextRadioPreset"),
    ("PreviousRadioPreset", "Previous Radio Preset", "Goes to previous radio preset, or if radio is not on, it turns it on. Also wraps to the end when you go past the first preset.", "PreviousRadioPreset"),
    ("ToggleRadioAMFM", "Toggle Radio AM / FM", "Toggles radio between AM and FM", "ToggleRadioAMFM"),
    ("RadioAutoFreqUp", "Radio Auto Freq Up", "Auto increases the radio frequency", "RadioAutoFreqUp"),
    ("RadioAutoFreqDown", "Radio Auto Freq Down", "Auto decreases the radio frequency", "RadioAutoFreqDown"),
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

# NUMCHAR_CODES[zone][action]
NUMCHAR_CODES = {
    1: { '1': '7F0151AE',
         '2': '7F0152AD',
         '3': '7F0153AC',
         '4': '7F0154AB',
         '5': '7F0155AA',
         '6': '7F0156A9',
         '7': '7F0157A8',
         '8': '7F0158A7',
         '9': '7F0159A6',
         '0': '7F015AA5',
       '+10': '7F015BA4',
       'ENT': '7F015CA3' },
    2: { '1': '7F01718F',
         '2': '7F01728C',
         '3': '7F01738D',
         '4': '7F01748A',
         '5': '7F01758B',
         '6': '7F017688',
         '7': '7F017789',
         '8': '7F017886',
         '9': '7F017986',
         '0': '7F017A84',
       '+10': '7F017B85',
       'ENT': '7F017C82' }
}

# OPERATION_CODES[zone][action]
OPERATION_CODES = {
    1: { 'Play': '7F016897',
         'Stop': '7F016996',
         'Pause': '7F016798',
         'Search-': '7F016A95',
         'Search+': '7F016E94',
         'Skip-': '7F016C93',
         'Skip+': '7F016D92',
         'FM': '7F015827',
         'AM': '7F01552A' },
    2: { 'Play': '7F018876',
         'Stop': '7F018977',
         'Pause': '7F018779',
         'Search-': '7F018A74',
         'Search+': '7F018B75',
         'Skip-': '7F018C72',
         'Skip+': '7F018D73',
         'FM': '7F015927',
         'AM': '7F015628' }
}

# EventGhost Constants
ACTION_EXECBUILTIN = 0x01
ACTION_BUTTON = 0x02
