#from main import rtc
from lib.Config import Config
import lib.Config as conf
import uos
from helpers import get_readable_time, ensureFileExistance
#import traceback
from defines import *



class MyDebugger:
    log_file = Config.config.get("storage", "error_log_file_path", fb=PATH_ERROR_LOG_FILE)
    log_file_old = Config.config.get("storage", "error_log_old_file_path", fb=PATH_ERROR_LOG_OLD_FILE)
    size = Config.config.get("storage", "error_log_file_size", fb=MAX_ERROR_LOG_SIZE)
    
    @staticmethod
    def log(msg):
        try:
            datetime = get_readable_time(conf.rtc.datetime())
        except Exception as e2:
            datetime = "TIME UNKNOWN"
        
        print(datetime + ": " + msg)
        ensureFileExistance(MyDebugger.log_file)
        # Check the size of the log file
        if uos.stat(MyDebugger.log_file)[6] > MyDebugger.size:
            uos.rename(MyDebugger.log_file, MyDebugger.log_file_old)  # Archive the old log
        
        try:
            with open(MyDebugger.log_file, 'a') as f: # type: ignore
                f.write('--- Message on {} ---\n'.format(datetime))
                f.write(msg + '\n')
                f.write('\n')
        except Exception as log_error:
            print("Failed to log:", str(log_error))
    

    @staticmethod
    def logException(e):
        try:
            datetime = get_readable_time(conf.rtc.datetime())
        except Exception as e2:
            datetime = "TIME UNKNOWN"
        
        print(datetime + ": " + str(e))
        ensureFileExistance(MyDebugger.log_file)
        # Check the size of the log file
        if uos.stat(MyDebugger.log_file)[6] > MyDebugger.size:
            uos.rename(MyDebugger.log_file, MyDebugger.log_file_old)  # Archive the old log

        try:
            with open(MyDebugger.log_file, 'a') as f: # type: ignore
                f.write('--- Exception occurred on {} ---\n'.format(datetime))
                f.write(str(e) + '\n')
                #f.write(traceback.format_exc() + '\n') #TODO: Check if traceback can be implemented for micropython
                f.write('\n')
        except Exception as log_error:
            print("Failed to log exception:", str(log_error))

