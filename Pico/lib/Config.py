from lib.SafeDict import SafeDict
from defines import *
from helpers import read_json
from machine import RTC

class Config:
    config = SafeDict(read_json(PATH_CONFIG))
    lookup_ld = SafeDict(read_json(PATH_LOOKUP_LOGGING_DEVICES))

    @staticmethod
    def getControllerConfigByAlias(contr_alias):
        contr = Config.config.get("controllers", contr_alias)
        if contr is not None:
            return SafeDict(contr)
        return None
    
rtc = RTC() #Is properly initialized in main.py