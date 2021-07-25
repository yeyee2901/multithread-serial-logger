from . import SerialParser as ser

class Logger:

    def __init__(self, active_serial: ser.SerialParser,
                 logfile: str, mode: str):

        # PRIVATES -------------------------------------
        self._logfile = logfile
        # ----------------------------------------------

        self.target_file = open(logfile, mode)
        self.serial = active_serial

    def logData(self) -> str:
        self.printLoggingMessage("","Getting data...")
        data = self.serial.getNewData()

        if self.target_file.writable() and self.serial.isOpen():
            self.printLoggingMessage(self._logfile, data)
            self.target_file.write(data)

        # Let's not forget to close the file
        else:
            self.printLoggingMessage(self._logfile, "Closing logfile")
            self.target_file.close()

        return data

    def printLoggingMessage(self, logfile:str, message:str):
        print(f"[LOGGER] {logfile}: {message}")
