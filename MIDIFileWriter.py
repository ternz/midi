import struct
class MIDIFileWriter:
    __file = None
    __track_chunk_buffer = None
    __time_division = 960
    __big_endian = 1  #midi file is big-endian

    def __init__(self, file):
        if type(file) == str:
            self.__file = open(file, "wb+")
        else:
            self.__file = file

    def setTimeDivision(self, time):
        self.__time_division = time

    def setBigEndian(self, val):
        self.__big_endian = val

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
        bytes.reverse()
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
        bytes.reverse()
        return bytes

    def createTrackChunkBuffer(self):
        self.__track_chunk_buffer = bytearray()

    def writeBytes(self, bytes):
        self.__file.write(bytes)

    def writeValue(self, val, length):
        bytes = MIDIFileWriter.valueBytes(val, length)
        self.writeBytes(bytes)

    def writeVarLenValue(self, val):
        bytes = MIDIFileWriter.valLenValueBytes(val)
        self.writeBytes(bytes)

    def writeHeaderChunk(self, formatType, tracks, timeDivision = 0):
        if formatType not in range(0, 3):
            print "unknown format type\n"
            exit()
        self.writeBytes('MThd')  #Chunk ID
        self.writeValue(6, 4)    #Chunk size
        self.writeValue(formatType, 2)  #format type
        self.writeValue(tracks, 2)      #number of tracks
        if timeDivision == 0:
            timeDivision = self.__time_division
        self.writeValue(timeDivision, 2)  #time division

    def writeTrackChunk(self, size, eventData):
        self.writeBytes('MTrk');  #Chunk ID
        self.writeValue(size, 4); #Chunk size
        self.writeBytes(eventData); #tarck event data

    def pushMTrkEvent(self, deltaTime, event):
        self.__track_chunk_buffer.extend(self.valLenValueBytes(deltaTime))
        self.__track_chunk_buffer.extend(event)

    @staticmethod
    def midiEventBytes(type, channel, para1, para2):
        bytes = bytearray()
        val = channel | (type<<4)  #big endian
        bytes.append(val)
        bytes.append(para1)
        if para2 is not None:
            bytes.append(para2)
        return bytes

    @staticmethod
    def sysexEventBytes(type, length, data):
        bytes = bytearray()
        bytes.append(type)
        bytes.extend(MIDIFileWriter.valLenValueBytes(length))
        bytes.extend(data)
        return bytes

    @staticmethod
    def metaEventBytes(type, length, data):
        bytes = bytearray()
        bytes.append(0xFF)
        bytes.append(type)
        bytes.extend(MIDIFileWriter.valLenValueBytes(length))
        if data is not None:
            bytes.extend(data)
        return bytes

    def pushMidiEvent(self, deltaTime, type, channel, para1, para2):
        self.pushMTrkEvent(deltaTime, self.midiEventBytes(type, channel, para1, para2))

    def pushSysexEvent(self, deltaTime, type, length, data):
        self.pushMTrkEvent(deltaTime, self.sysexEventBytes(type, length, data))

    def pushMetaEvent(self, detalTime, type, length, data):
        self.pushMTrkEvent(detalTime, self.metaEventBytes(type, length, data))

    def flushTarckChunk(self):
        self.pushMetaEvent(0, 0x2f, 0, None)  #end of track event
        size = len(self.__track_chunk_buffer)
        self.writeTrackChunk(size, self.__track_chunk_buffer)
        self.__track_chunk_buffer = None

    def playNote(self, name, time=4, velocity=64, deltaTime=0, channel=0):
        if time not in (1, 2, 4, 8, 16, 32, 64):
            raise ValueError(time)
        duration = self.__time_division * 4 / time
        self.pushMidiEvent(deltaTime, 0x9, channel, name, velocity)
        self.pushMidiEvent(duration, 0x8, channel, name, velocity)
