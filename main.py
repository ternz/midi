from MIDIFileWriter import MIDIFileWriter

midi = MIDIFileWriter('test.mid')
midi.writeHeaderChunk(0, 1)
midi.createTrackChunkBuffer()
midi.playNote(0x3c)
midi.playNote(0x3e)
midi.playNote(0x40)
midi.playNote(0x41)
midi.playNote(0x43)
midi.playNote(0x45)
midi.playNote(0x47)
midi.playNote(0x48)
midi.flushTarckChunk()