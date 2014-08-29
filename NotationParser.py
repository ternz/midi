import sys
from collections import deque
from MIDIFileWriter import MIDIFileWriter

class NotationParser:
    __file = None
    __line = 0
    __buffer_size = 256
    __input_buffer = deque([], self.__buffer_size)
    __parenthesis = 0
    __midi_writer = None
    __state = 0
    __stack = []
    __notes = []

    def __init__(self, file=None, midiwriter=None):
        self.setInputFile(file)
        self.setMidiWriter(midiwriter)
        #self.__input_buffer = deque([], self.__buffer_size)

    def setInputFile(self, file):
        if type(file) == str:
            self.__file = open(file, "r")
        else:
            self.__file = file

    def setMidiWriter(self, writer):
        if type(writer) == str:
            self.__midi_writer = MIDIFileWriter(writer)
        else:
            self.__midi_writer = writer

    def getChar(self):
        if len(self.__input_buffer) == 0:
            self.__input_buffer.extend(self.__file.read(self.__buffer_size))
        if len(self.__input_buffer) != 0:
            return self.__input_buffer.popleft()
        else:
            return ''

    def error(self, msg):
        print msg
        sys.exit(0)

    def parse(self, f=None):
        if f is not None:
            self.setInputFile(f)

    def fms(c):
        if c in 'cdefgabCDEFGAB':
            pass

