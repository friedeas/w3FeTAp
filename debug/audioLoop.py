#!/usr/bin/env python3
import pyogg
import simpleaudio
import numpy # type: ignore

try: 
    def loadVorbisFile():
        print("Loading OGG file")
        filename = "../audio/1TR110-1_Kap8.1_Waehlton.ogg"

        # Read the file using VorbisFile
        print("Reading Ogg Vorbis file...")
        vorbis_file = pyogg.VorbisFile(filename)

        # Display summary information about the audio
        print("\nRead Ogg Vorbis file")
        print("Channels:\n  ", vorbis_file.channels)
        print("Frequency (samples per second):\n  ",vorbis_file.frequency)
        print("Buffer Length (bytes):\n  ", len(vorbis_file.buffer))
        return vorbis_file

    def prepareBuffer(vorbis_file):           
        # Using the data from the buffer in OpusFile, create a NumPy array        
        print("\nPrepare byte array buffer")
        buffer = numpy.ctypeslib.as_array(
            vorbis_file.buffer,
            (vorbis_file.buffer_length//
            2//
            vorbis_file.channels,
            vorbis_file.channels)
        )        
        return buffer

    def play(buffer, channels, frequency):
        # Play the audio
        print("Play audio")
        play_obj = simpleaudio.play_buffer(
            buffer,
            channels,
            2,
            frequency
        )
        return play_obj

    # Wait until sound has finished playing
    oggFile = loadVorbisFile()
    buffer = prepareBuffer(oggFile)
    while True:
        play_obj = play(buffer, oggFile.channels, oggFile.frequency)
        play_obj.wait_done()  
        print("Finished...repeat.")

except KeyboardInterrupt:
    print("Program aborted")
  
except Exception as error:
    print("Error or exception occurred, aborting program", error)
  
finally:
     simpleaudio.stop_all()