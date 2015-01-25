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

# EventGhost Constants
ACTION_EXECBUILTIN = 0x01
ACTION_BUTTON = 0x02

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

# CURSOR_CODES[zone][action]
CURSOR_CODES = {
    1: { 'Up': '7A859D62',
         'Down': '7A859C63',
         'Left': '7A859F60',
         'Right': '7A859E61',
         'Enter': '7A85DE21',
         'Return': '7A85AA55',
         'Level': '7A858679',
         'On Screen': '7A85847B',
         'Option': '7A856B14',
         'Top Menu': '7A85A0DF',
         'Pop Up Menu': '7A85A4DB' },
    2: { 'Up': '7A852B55',
         'Down': '7A852C52',
         'Left': '7A852D53',
         'Right': '7A852E50',
         'Enter': '7A852F51',
         'Return': '7A853C42',
         'Option': '7A856C12',
         'Top Menu': '7A85A1DF',
         'Pop Up Menu': '7A85A5DB' },
    }

#populated by the Setup Availability function
# Available zones/sources. These are to be generated based on availability
AVAILABLE_ZONES = []
AVAILABLE_SOURCES = []
AVAILABLE_INFO_SOURCES = []
AVAILABLE_FEATURE_SOURCES = []
AVAILABLE_INPUT_SOURCES = []

# Objects used in the GetInfo action
MENU_OBJECTS = [ 'Menu Layer', 'Menu Name' ]
LINE_OBJECTS = [ 'Line 1', 'Line 2', 'Line 3', 'Line 4', 'Line 5', 'Line 6', 'Line 7', 'Line 8', 'Current Line', 'Max Line' ]
GENERIC_PLAYBACK_OBJECTS = [ 'Playback Info', 'Repeat Mode', 'Shuffle', 'Artist', 'Album', 'Song' ] + MENU_OBJECTS + LINE_OBJECTS
ZONE_OBJECTS = [ 'Power', 'Sleep', 'Volume Level', 'Mute', 'Input Selection', 'Scene', 'Init Volume Mode', 'Init Volume Level', 'Max Volume Level' ]
MAIN_ZONE_OBJECTS = ZONE_OBJECTS + [ 'Straight', 'Enhancer', 'Sound Program', 'Treble', 'Bass' ]
NET_RADIO_OBJECTS = [ 'Playback Info', 'Station' ] + MENU_OBJECTS + LINE_OBJECTS
PANDORA_OBJECTS = [ 'Playback Info', 'Station', 'Album', 'Song' ] + MENU_OBJECTS + LINE_OBJECTS
SIRIUS_IR_OBJECTS = [ 'Playback Info', 'Artist', 'Channel', 'Title' ] + MENU_OBJECTS + LINE_OBJECTS
SIRIUS_OBJECTS = [ 'Antenna Strength', 'Category', 'Channel Number', 'Channel Name', 'Artist', 'Song', 'Composer' ]
SYSTEM_OBJECTS = [ 'Active Speakers', 'PreOut Levels' ]

"""
# A list of every single source we support
ALL_SOURCES = [ 'HDMI1', 'HDMI2', 'HDMI3', 'HDMI4', 'HDMI5', 'HDMI6', 'HDMI7', 'HDMI8', 'HDMI9',
                'AV1', 'AV2', 'AV3', 'AV4', 'AV5', 'AV6', 'AV7', 'AV8', 'AV9',
                'OPTICAL1', 'OPTICAL2', 'COAXIAL1', 'COAXIAL2', 'CD', 'LINE1', 'LINE2', 'LINE3',
                'V-AUX', 'TUNER', 'AUDIO', 'AUDIO1', 'AUDIO2', 'AUDIO3', 'AUDIO4',
                'DOCK', 'SIRIUS', 'PC', 'MULTICH', 'PHONO', 'iPod', 'Bluetooth',
                'UAW', 'NET', 'Rhapsody', 'Pandora', 'Napster',
                'NET RADIO', 'USB', 'iPod (USB)', 'SIRIUSInternetRadio' ]
"""
# Supported zone definitions
ALL_ZONES = [ 'Main Zone', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone A', 'Zone B', 'Zone C', 'Zone D' ]
ALL_ZONES_PLUS_ACTIVE = [ 'Active Zone' ] + ALL_ZONES
TWO_ZONES = [ 'Main Zone', 'Zone 2' ]
TWO_ZONES_PLUS_ACTIVE = [ 'Active Zone' ] + TWO_ZONES

"""
# All zones to check availability for
ZONE_CHECK = [ 'Main_Zone', 'Zone_2', 'Zone_3', 'Zone_4', 'Zone_A', 'Zone_B', 'Zone_C', 'Zone_D' ]
"""

"""
DEFUNCT

# All inputs to check availability for
INPUT_CHECK = [ 'HDMI_1', 'HDMI_2', 'HDMI_3', 'HDMI_4', 'HDMI_5', 'HDMI_6', 'HDMI_7', 'HDMI_8', 'HDMI_9',
                'AV_1', 'AV_2', 'AV_3', 'AV_4', 'AV_5', 'AV_6', 'AV_7', 'AV_8', 'AV_9',
                'OPTICAL_1', 'OPTICAL_2', 'OPTICAL_3', 'OPTICAL_4', 'COAXIAL_1', 'COAXIAL_2', 'COAXIAL_3', 'COAXIAL_4', 'CD', 'LINE_1', 'LINE_2', 'LINE_3', 'LINE_4',
                'V_AUX', 'Tuner', 'AUDIO', 'AUDIO_1', 'AUDIO_2', 'AUDIO_3', 'AUDIO_4',
                'DOCK', 'SIRIUS', 'PC', 'MULTI_CH', 'PHONO', 'iPod', 'Bluetooth',
                'UAW', 'NET', 'Rhapsody', 'Pandora', 'Napster', 'SERVER',
                'NET RADIO', 'USB', 'iPod_USB', 'SIRIUS_IR' ]

# A dict of mappings to go from INPUT_CHECK -> AVAILABLE_SOURCES
INPUT_MAPPINGS = { 'SERVER': 'PC',
                   'V_AUX': 'V-AUX',
                   'Tuner': 'TUNER',
                   'MULTI_CH': 'MULTICH',
                   'iPod_USB':'iPod (USB)',
                   'SIRIUS_IR': 'SIRIUSInternetRadio',
                   'NET_RADIO': 'NET RADIO'}

# Setup generic input mappings for HDMI, AV, and AUDIO
for i in range(1,10):
    INPUT_MAPPINGS['HDMI{0}'.format(i)] = 'HDMI{0}'.format(i)
    INPUT_MAPPINGS['AV{0}'.format(i)] = 'AV{0}'.format(i)
    if i <= 4:
        INPUT_MAPPINGS['AUDIO{0}'.format(i)] = 'AUDIO{0}'.format(i)
        INPUT_MAPPINGS['OPTICAL{0}'.format(i)] = 'OPTICAL{0}'.format(i)
        INPUT_MAPPINGS['COAXIAL{0}'.format(i)] = 'COAXIAL{0}'.format(i)
        INPUT_MAPPINGS['LINE{0}'.format(i)] = 'LINE{0}'.format(i)

# sources to directly copy over in mappings, because their names are the exact same
direct_copy = [ 'PHONO', 'iPod', 'Bluetooth', 'AUDIO', 'UAW', 'NET', 'Rhapsody', 'Pandora', 'Napster', 'NET RADIO', 'USB', 'DOCK', 'SIRIUS', 'PC', 'CD', 'SiriusXM', 'Spotify', 'AirPlay', 'V-AUX' ]
for item in direct_copy:
    INPUT_MAPPINGS[item] = item
"""
"""
# Sanity check for mappings, to ensure we have a mapping for every item
if len(INPUT_MAPPINGS.keys()) != len(INPUT_CHECK):
    print "Error, missing mappings for:"
    for key in INPUT_CHECK:
        if key not in INPUT_MAPPINGS:
            print '\t', key
"""


