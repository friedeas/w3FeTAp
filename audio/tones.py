#!/usr/bin/env python3

import pyogg
import simpleaudio
import numpy # type: ignore
import threading
import time

class DialTone():
    def _load_vorbis_file(self):
        print("Loading dile tone")
        filename = "audio/1TR110-1_Kap8.1_Waehlton.ogg"
        # Read the file using VorbisFile
        print("Reading Ogg Vorbis file: " + filename)
        vorbis_file = pyogg.VorbisFile(filename)
        return vorbis_file
    
    def _prepare_buffer(self, vorbis_file):           
        # Using the data from the buffer in OpusFile, create a NumPy array        
        print("Prepare byte array buffer for dial tone audio")
        buffer = numpy.ctypeslib.as_array(
            vorbis_file.buffer,
            (vorbis_file.buffer_length//
            2//
            vorbis_file.channels,
            vorbis_file.channels)
        )        
        return buffer
    
    def _do_play(self):
        # Play the audio
        print("Play audio")        
        play_obj = simpleaudio.play_buffer(
            self._buffer,
            self._oggFile.channels,
            2,
            self._oggFile.frequency
        )
        return play_obj
    
    def __init__(self):
        self._oggFile = self._load_vorbis_file()
        self._buffer = self._prepare_buffer(self._oggFile)
    
    def playThread(self):
        t = threading.current_thread()        
        self._play_obj = self._do_play()
        while getattr(t, "do_run", True):
            time.sleep(0.0001)        
            if(not self._play_obj.is_playing()):
                break
        if(getattr(t, "do_run", True)):
            print("Finished...repeat.")
            self.play()

    def play(self):
        self._playThread = threading.Thread(target=self.playThread)
        self._playThread.start()
        
    def stop(self):
        print("Try to stop playback")
        if(self._playThread is not None):
            self._playThread.do_run = False
        if(self._play_obj != None):
            self._play_obj.stop()
        simpleaudio.stop_all()