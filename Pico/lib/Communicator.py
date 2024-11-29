from helpers import get_UART_instance, waitForRespnese
from lib.Config import Config
from machine import UART
from defines import *
import time

class ControllerNotExists(Exception):
    def __init__(self, controller):
        self.message = f"Controller {controller} does not exist in configuration file"

        super().__init__(self.message)

class ControllerError(Exception):
    def __init__(self, controller, resp, req="", **kwargs):
        self.controller = controller
        self.resp = resp #Resp is already stripped of new line character
        self.code = resp[3:5] if resp[3:5] in CONTROLLER_ERROR_CODES else None
        self.message = f"External Controller {self.controller} responded with Error {CONTROLLER_ERROR_CODES[self.code]['name'] if self.code else ''}\n"
        self.message += f"Error Code: {self.code}\n" if self.code else f"Response: {self.resp}\n"
        if (self.code): self.message += f"Message: {CONTROLLER_ERROR_CODES[self.code]['message']}\n"
        if (req != ""): self.message += f"Request: {req}\n"
        for key, value in kwargs.items():
            self.message += f"{key}: {value}\n"

        super().__init__(self.message)

    def getCode(self):
        return int(self.code) if self.code else -1

class ControllerNoResponseError(Exception):
    def __init__(self, controller):
        self.controller = controller
        self.message = f"External Controller {self.controller} did not respond\n"
        super().__init__(self.message)

class Communicator:
    # Dictionary to hold instances by alias
    _instances = {}

    def __new__(cls, alias):
        if alias in cls._instances:
            return cls._instances[alias]  # Return existing instance if alias is found
        # Otherwise, create a new instance
        instance = super(Communicator, cls).__new__(cls)
        cls._instances[alias] = instance  # Store new instance by alias
        return instance

    def __init__(self, alias):
        self.alias = alias  # Initialize with the alias
        self.config = Config.getControllerConfigByAlias(self.alias)
        if self.config is None: raise ControllerNotExists("Controller "+alias+" not found in Configuration")
        #print(self.config.get("uart", "bus"))
        self.uart = get_UART_instance(**self.config.get("uart")) #type: ignore
        self.rxBuffer = bytearray(100)
    def writeCommand(self, command): #Sends command and waits until response is available
        #self.uart.write('\n')
        #self.uart.flush()
        #self.uart.read() #Clear RX Buffer
        self.uart.write(command+"\n")
        self.uart.flush()
        waitForRespnese(self.uart, UART_WAIT_FOR_RESPONSE)
    def req(self, alias):
        res = None
        for i in range(0, self.config.get("retries", fb=CONTROLLER_DEFAULT_RETRY_ATTEMPTS)): # type: ignore
            command="/req "+alias
            self.writeCommand(command)
            print(f"Request Attempt {str(i)} Command: {command}")
            try: #TODO: Replace try-catch with more elegant .decode error parameter
                res = self.uart.readline().decode('utf-8').rstrip()
            except Exception as e: #Catch decode Error, caused by poor connection
                print(f"Request Attempt {str(i)} failed")
                pass
            if (res and res[0:len(CONTROLLER_ERROR_PREFIX)] != CONTROLLER_ERROR_PREFIX): return res
            time.sleep_ms(CONTROLLER_DEFAULT_DELAY_ATTEMPTS)
        if res is None: raise ControllerNoResponseError(self.alias)
        raise ControllerError(self.alias, res, command)
    
    def setup(self, id, alias, *args):
        #time.sleep(1)
        res = None
        for i in range(0, self.config.get("retries", fb=CONTROLLER_DEFAULT_RETRY_ATTEMPTS)): # type: ignore
            command = "/setup "+id+","+alias+","+','.join(str(arg) for arg in args)
            print(f"Setup Attempt {str(i)} Command: {command}")
            self.writeCommand(command)
            try:
                res = self.uart.readline().decode('utf-8').rstrip()
            except Exception as e: #Catch decode Error, caused by poor connection
                print(f"Setup Attempt {str(i)} failed")
                #time.sleep(5) #Test wether failed setup causes reset
                pass
            else:
                print(f"Response: {res}")
                if res == "OK": return
            time.sleep_ms(CONTROLLER_DEFAULT_DELAY_ATTEMPTS)
        if res is None: raise ControllerNoResponseError(self.alias)
        raise ControllerError(self.alias, res, command)

    def reset(self):
        self.uart.write("/reset")

    def list(self):
        numBytes = 0
        out = ""
        command = "/list"
        self.writeCommand(command)
        if self.uart.any():
            numBytes = self.uart.readinto(self.rxBuffer)
        try:
            out = self.rxBuffer[:numBytes].decode('utf-8')
        except Exception as e: #Catch decode Error, caused by poor connection
             raise ControllerNoResponseError(self.alias) 
        return out
        
            
