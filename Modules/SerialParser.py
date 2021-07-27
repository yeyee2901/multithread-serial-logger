from serial import Serial
from serial.serialutil import SerialException
import time

class SerialParser(Serial):

    # STATICS
    ID_COUNT = 0
    DEFAULT_DEVICE = "Arduino"

    def __init__(self, *args, **kwargs):

        # PRIVATES -----------------------------------
        self._data = ''
        self._ID = SerialParser.ID_COUNT
        SerialParser.ID_COUNT += 1
        # --------------------------------------------

        try:
            super().__init__(*args, **kwargs)
        except SerialException:
            print(f"[ERROR] Cannot initialize serial port: {self.port}")

        # on success open,
        # Tell arduino which ID it got allocated
        if self.isOpen():
            self.printParserMessage("Found new device. Sending message to device to confirm ID")

            # This is because on connection, Arduino will RESTART!
            # We have to wait before sending any data
            time.sleep(2)
            to_write = f"ID-{ self.getID() }\n"
            self.write(to_write.encode("utf-8"))

            self.printParserMessage(f"Device replied with: {self.getNewData()}")
        else:
            self.error_n_die()

    def getNewData(self) -> str:
        data = ''
        if self.isOpen():
            data = self.readline().decode("utf-8")
            data = f"{SerialParser.DEFAULT_DEVICE}#{self._ID},{data}"
        else:
            self.error_n_die()

        return data

    def getID(self) -> int:
        return self._ID


    # Generic error handler
    def error_n_die(self):
        self.printParserMessage("Cannot access port. Either arduino is disconnected or port error")
        self.close()

    def printParserMessage(self, msg:str):
        print(f"[SERIAL] {self.port}: {msg}")

if __name__ == "__main__":
    logger = SerialParser(port="/dev/ttyACM0", baudrate=9600)
    
    while True:
        print(f"{logger.getID()} sent: {logger.getNewData()}")

    print("Conection Lost")
