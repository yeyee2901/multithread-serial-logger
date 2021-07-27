from . import ThreadWithReturn
from . import SerialParser
from . import Logger

class Handler(object):
    def __init__(self, new_port: str, logfile: str):
        self.connection = SerialParser.SerialParser(port=new_port, baudrate=9600)
        self.logger = Logger.Logger(self.connection, logfile, "w")
        self.thread = ThreadWithReturn.ThreadWithReturn(target=self.logger.logData)

    def isActive(self):
        return self.logger.serial.isOpen()

    def handleData(self):
        self.thread.start()

    def join(self):
        self.connection.close()
        self.thread.join()
