import ConfigParser
import os

def loadAllSettings():
    global SETTINGS
    file = os.path.abspath(__file__)
    fname = os.path.join(file[:file.rfind('\\')], 'config.ini')
    loadSettings(fname, SETTINGS, 'Settings')

class Settings(object):
    def __init__(self):
        self.ip_address = ""
        self.port = 80
        self.ip_auto_detect = False
        self.ip_range_start = ""
        self.ip_range_end = ""
        self.auto_detect_timeout = 0.3
        self.auto_detect_model = "ANY"

def loadSettings(fname, obj, section, ignore=['valid']):
    """
    Generically deserializes a settings object
    from a specified ini file based on the predefined
    class variables.

    Returns:
        -1 if could not read file
        0 if no errors
        >0 positive number of errors if there were errors
    """
    errors = -1
    if os.path.isfile(fname):
        errors = 0
        Config = ConfigParser.ConfigParser()
        Config.read(fname)
        for key, val in obj.__dict__.items():
            if not key in ignore:
                try:
                    value = val
                    if type(val) is int:
                        value = Config.getint(section, key)
                    elif type(val) is bool:
                        value = Config.getboolean(section, key)
                    else:
                        value = Config.get(section, key)
                except:
                    errors = errors + 1
                obj.__dict__[key] = value
    obj.__dict__['valid'] = errors == 0
    return errors

SETTINGS = Settings()
