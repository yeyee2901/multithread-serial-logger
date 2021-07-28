from serial.serialutil import SerialException
from . import SerialParser as ser

class Logger:

    def __init__(self, active_serial: ser.SerialParser,
                 logfile: str):

        # PRIVATES -------------------------------------
        self._logfile = f"./logfiles/{logfile}"
        # ----------------------------------------------

        self.serial = active_serial
        self.is_active = True

    # Continuously log data
    def logData(self) -> str:
        data = ""
        while self.is_active:
            try:
                with open(self._logfile, "a") as logfile:
                    data = self.serial.getNewData()
                    logfile.write(data)

            # Handle if device disconnected
            except (SerialException, KeyboardInterrupt):
                self.is_active = False
                print(f"[THREAD] Device disconnected, ending thread associated with the logger...")

        return data

    def printLoggingMessage(self, logfile:str, message:str):
        print(f"[LOGGER] {logfile}: {message}")
