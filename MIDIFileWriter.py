import struct
class MIDIFileWriter:
    __file = None

    def __init__(self, file):
        if type(file) == str:
            self.__file = open(file, "wb+")
        else:
            self.__file = file

    @staticmethod
    def valueBytes(val, length):
        if length > 4:
            flag = 'l'
        elif length > 2:
            flag = 'i'
        else:
            flag = 'h'
        s = struct.pack(flag, val)
        bytes = bytearray(s)
        l = len(bytes)
        while(l>length):
            bytes.pop()
            l -= 1
        while(l<length):
            bytes.append(0)
            l += 1
        return bytes;

    @staticmethod
    def valLenValueBytes(val):
        bytes = bytearray()
        flag = False
        while(val not in range(0, 128)):
            abyte = val & 0x7f
            if flag:
                abyte |= 0x80
            else:
                flag = True
            bytes.append(abyte)
            val = val >> 7
        if val != 0:
            if flag:
                val |= 0x80
            bytes.append(val)
        elif not flag:
            bytes.append(val)
        return bytes

    def writeBytes(self, bytes):
        self.__file.write(bytes)

    def writeValue(self, val, length):
        bytes = MIDIFileWriter.valueBytes(val, length)
        self.writeBytes(bytes)

    def writeVarLenValue(self, val):
        bytes = MIDIFileWriter.valLenValueBytes(val)
        self.writeBytes(bytes)

    def writeHeaderChunk(self, formatType, tracks, timeDivision):
        if formatType not in range(0, 3):
            print "unknown format type\n"
            exit()
        self.writeBytes('MThd')  #Chunk ID
        self.writeValue(6, 4)    #Chunk size
        self.writeValue(formatType, 2)  #format type
        self.writeValue(tracks, 2)      #number of tracks
        self.writeValue(timeDivision, 2)  #time division

    def writeTrackChunk(self, size, eventData):
        self.writeBytes('MTrk');  #Chunk ID
        self.writeValue(size, 4); #Chunk size
        self.writeBytes(eventData); #tarck event data

    def pushMTrkEvent(self, deltaTime, event):
        pass

    @staticmethod
    def midiEventBytes(type, channel, para1, para2):
        val = type | (channel<<4)
        val |= para1 << 8
        val |= para2 << 16
        return MIDIFileWriter.valueBytes(val, 3)

    @staticmethod
    def sysexEventBytes(type, length, data):
        bytes = bytearray()
        bytes.append(type)
        bytes.append(MIDIFileWriter.valLenValueBytes(length))
        bytes.append(data)
        return bytes

    @staticmethod
    def metaEventBytes(type, length, data):
        pass

