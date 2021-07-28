from . import ThreadWithReturn
from . import SerialParser
from . import Logger

class Handler(object):

    def __init__(self, new_port: str, logfile: str, baudrate = 9600):
        self.baudrate = baudrate
        self.connection = SerialParser.SerialParser(port=new_port, baudrate=self.baudrate)
        self.logger = Logger.Logger(self.connection, logfile)
        self.thread = ThreadWithReturn.ThreadWithReturn(target=self.logger.logData)

    def isActive(self):
        return self.logger.serial.isOpen()

    def handleData(self):
        self.thread.start()

    def join(self):
        self.connection.close()
        self.thread.join()
