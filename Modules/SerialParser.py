from serial import Serial
from serial.serialutil import SerialException

DEFAULT_BAUDRATE = 9600
DEFAULT_PORT = "/dev/ttyACM0"
DEFAULT_TIMEOUT = 100

class SerialParser(Serial):

    def __init__(self, PORT=DEFAULT_PORT, BAUD=DEFAULT_BAUDRATE, timeout_ms=DEFAULT_TIMEOUT):
        self.is_Active = False

        try:
            self.open_port = Serial(port=PORT, baudrate=BAUD, timeout=timeout_ms)
            self.SUCCESS_OPEN = True

        except SerialException as e:
            print("Cannot open serial port, try again")
            print(f"Cause: {e}")

    def readline(self):
        data = str(self.readline())

        # automatically parse comma separated values
        if "," in data:
            return data.split(",")
        else:
            return data
