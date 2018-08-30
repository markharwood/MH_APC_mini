#Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC_mini/APC_mini.py
from __future__ import with_statement
from _Framework.Layer import Layer, SimpleLayerOwner
from _APC.ControlElementUtils import make_slider
from APC_Key_25.APC_Key_25 import APC_Key_25
from APC_mini.APC_mini import APC_mini
import time

# TO Debug and see messages:
# tail -f ~/Library/Preferences/Ableton/Live\ 9.7.1/Log.txt

NOTE_ON_STATUS = 144
NOTE_OFF_STATUS = 128
SHIFT_KEY = 98
CC_STATUS = 176

class ModeBase():
    def __init__(self, apc):
        self.apc = apc
        self.rowStarts = [56, 48, 40, 32, 24, 16, 8, 0]
        self.letters = {

            "1": [
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0]
            ],
            "2": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 1, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0]
            ],
            "bar":[
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 5, 0, 1, 1],
                [1, 1, 1, 5, 0, 5, 1, 0],
                [0, 0, 0, 5, 5, 5, 1, 0],
                [0, 0, 0, 5, 0, 5, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "bpm":[
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 5, 5, 5, 0, 0],
                [1, 1, 1, 5, 0, 5, 0, 0],
                [1, 0, 1, 5, 5, 5, 0, 0],
                [1, 1, 1, 5, 0, 1, 0, 1],
                [0, 0, 0, 5, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 0, 1]
            ],
            "tap":[
                [1, 1, 1, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 1, 0, 1],
                [0, 1, 0, 5, 0, 1, 1, 1],
                [0, 1, 5, 0, 5, 1, 0, 0],
                [0, 0, 5, 5, 5, 1, 0, 0],
                [0, 0, 5, 0, 5, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "undo":[
                [1, 0, 1, 0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 1, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 1, 1, 0, 1, 1, 1, 0]
            ],
            "metronome": [
                [1, 0, 1, 0, 0, 1, 1, 1],
                [1, 1, 1, 0, 0, 0, 1, 0],
                [1, 1, 1, 5, 5, 0, 1, 0],
                [1, 0, 1, 5, 0, 0, 1, 0],
                [0, 0, 0, 5, 5, 0, 0, 0],
                [0, 0, 0, 5, 0, 0, 0, 0],
                [0, 0, 0, 5, 5, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "edit":[
                [1, 1, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 0, 5, 5, 5],
                [1, 1, 0, 5, 1, 0, 5, 0],
                [1, 0, 0, 5, 1, 0, 5, 0],
                [1, 1, 5, 5, 1, 0, 5, 0],
                [0, 0, 5, 5, 0, 0, 0, 0],
                [0, 0, 5, 5, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "small1":[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0]
            ],
            "small2":[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small3":[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small4":[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0]
            ],
            "small5":[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small6":[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small7":[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "small8":[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small9":[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small0":[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "on":[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 1, 1, 0, 1, 0, 1, 0]
            ],
            "off":[
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 5, 5, 0, 0, 0],
                [1, 1, 1, 5, 0, 1, 1, 0],
                [0, 0, 0, 5, 5, 1, 0, 0],
                [0, 0, 0, 5, 0, 1, 1, 0],
                [0, 0, 0, 5, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0]
            ]
        }
    def custom_receive_midi(self, midi_bytes):
        return True

    def clear_lights(self):
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 68, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 69, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 70, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 71, 0))

    def gotoRootMenu(self):
        self.apc.mode = self.apc.rootMenu
        self.apc.mode.syncLights()


    def exitMode(self):
        self.apc.mode = None
        # # Use this to refresh lights if have been monkeying around with them to do comms:
        self.apc._update_hardware()

        # Another way - only worked once...
        # self._refresh_displays()

        # Another way to refresh lights if have been monkeying around but seems slower and heavier reboot op
        # self.refresh_state()


    def paintLetter(self, letter):
        for rowNum, rowArr in enumerate(letter):
            rowStart = self.rowStarts[rowNum]
            for colNum, val in enumerate(rowArr):
                self.apc.really_do_send_midi((NOTE_ON_STATUS, rowStart + colNum, val))
                # if val == 1:
                #     self.apc.really_do_send_midi((NOTE_ON_STATUS, rowStart + colNum, 1))
                # else:
                #     self.apc.really_do_send_midi((NOTE_ON_STATUS, rowStart + colNum, 0))


    def paintNumber(self, number):
        numberAsString = str(number)
        offset = 0
        combined_letter = [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ]
        color=1
        inc = 2
        if len(numberAsString) >= 3:
            inc=1
        for char in numberAsString:
            letter = self.letters["small"+char]
            lastCol = 0
            if inc== 1:
                # No space between digits - use color to differentiate
                if color==1:
                    color = 5
                else:
                    color=1
            for rowNum, rowArr in enumerate(letter):
                for colNum, val in enumerate(rowArr):
                    if val == 1:
                        lastCol = max(lastCol, colNum)
                        if offset + colNum <= 7:
                            combined_letter[rowNum][offset+colNum]=color
            offset = offset+ lastCol+inc
        self.paintLetter(combined_letter)


class ShiftedMenuMode(ModeBase):
    def __init__(self, apc):
        ModeBase.__init__(self, apc)
        self.apc.show_message("menuMode")
        self.modes=[RecordBarsMode(apc), TapTempoMode(apc), MetronomeMode(apc), PaintMode(apc) ]
        self.modeNum=0
        # self.syncLights()

    def syncLights(self):
        self.apc.log_message("Mode name");
        self.apc.log_message(self.modes[self.modeNum].getName());
        self.apc.log_message("grid");
        self.apc.log_message(self.letters[self.modes[self.modeNum].getName()]);
        self.paintLetter(self.letters[self.modes[self.modeNum].getName()])

        # Set status of menu buttons
        self.clear_lights()

        self.apc.really_do_send_midi((NOTE_ON_STATUS, 64, 1))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 65, 1))
        # self.apc.really_do_send_midi((NOTE_ON_STATUS, 68, 0))
        # self.apc.really_do_send_midi((NOTE_ON_STATUS, 69, 0))
        # self.apc.really_do_send_midi((NOTE_ON_STATUS, 70, 0))
        # self.apc.really_do_send_midi((NOTE_ON_STATUS, 71, 0))
        if self.modeNum < len(self.modes) - 1:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, 67, 1))
        else:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, 67, 0))
        if self.modeNum > 0:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, 66, 1))
        else:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, 66, 0))

    def custom_receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]
            if note == 65 :
                self.exitMode()
                return
            if note == 64 :
                self.apc.mode=self.modes[self.modeNum]
                self.apc.mode.syncLights()
                return
            if note == 66 :
                self.modeNum =self.modeNum-1
                if self.modeNum < 0 :
                    self.modeNum = 0
                self.syncLights()
            if note == 67 :
                self.modeNum =self.modeNum+1
                if self.modeNum >= len(self.modes):
                    self.modeNum = len(self.modes) -1
                self.syncLights()

        return False

#   Dev class used to edit letters
class PaintMode(ModeBase):
    def __init__(self, apc):
        ModeBase.__init__(self, apc)
        self.grid=[
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ]

    def getName(self):
        return "edit"

    def syncLights(self):
        self.paintLetter(self.grid)
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 64, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 65, 1))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 66, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 67, 0))

    def custom_receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]
            if note == 65 :
                self.gotoRootMenu()
                return
            if note <64:
                trackIndex = self.apc.getTrackIndex(note)
                clipIndex= self.apc.getClipIndex(note)
                note = self.grid[clipIndex][trackIndex]
                if note ==0:
                    self.grid[clipIndex][trackIndex]=1
                elif note ==1:
                    self.grid[clipIndex][trackIndex]=3
                elif note ==3:
                    self.grid[clipIndex][trackIndex]=5
                elif note ==5:
                    self.grid[clipIndex][trackIndex]=0
                self.syncLights()
        return False

class RecordBarsMode(ModeBase):
    def __init__(self, apc):
        ModeBase.__init__(self, apc)
        # self.apc.__fixed_record_bar_length=2

    def getName(self):
        return "bar"

    def syncLights(self):
        self.paintNumber(self.apc.fixed_record_bar_length())
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 64, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 65, 1))
        if self.apc.fixed_record_bar_length()>1:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, 66, 1))
        else:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, 66, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 67, 1))

    def custom_receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]
            if note == 65:
                self.gotoRootMenu()
            if note == 67:
                self.apc.set_fixed_record_bar_length ( self.apc.fixed_record_bar_length() +1)
                self.syncLights()
            if note == 66 and self.apc.fixed_record_bar_length()>1:
                self.apc.set_fixed_record_bar_length ( self.apc.fixed_record_bar_length() -1)
                self.syncLights()
        return False

class TapTempoMode(ModeBase):
    def __init__(self, apc):
        ModeBase.__init__(self, apc)
        # self.apc.__fixed_record_bar_length=2

    def getName(self):
        return "bpm"

    def syncLights(self):
        song = self.apc.song()
        self.paintNumber(int(song.tempo))
        # self.apc.really_do_send_midi((NOTE_ON_STATUS, 64, 0))
        # self.apc.really_do_send_midi((NOTE_ON_STATUS, 65, 1))
        # if self.apc.fixed_record_bar_length() > 1:
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 64, 0))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 66, 1))
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 67, 1))
        # else:
        #     self.apc.really_do_send_midi((NOTE_ON_STATUS, 66, 0))
        # self.apc.really_do_send_midi((NOTE_ON_STATUS, 67, 1))

    def custom_receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]
            if note == 67:
                self.apc.song().tempo = int(self.apc.song().tempo)+1
                self.syncLights()
                return
            if note == 66:
                self.apc.song().tempo = int(self.apc.song().tempo)-1
                self.syncLights()
                return
            if note == 65:
                self.gotoRootMenu()
                song=self.apc.song()
                # - round down tempo
                song.tempo = int(song.tempo)

            else:
                song=self.apc.song()
                song.tap_tempo()
                # Tempo Tap key - round down tempo
                # song.tempo = int(song.tempo)
                self.syncLights()

        return False

class MetronomeMode(ModeBase):
    def __init__(self, apc):
        ModeBase.__init__(self, apc)

    def getName(self):
        return "metronome"

    def syncLights(self):
        song = self.apc.song()
        # self.apc.really_do_send_midi((NOTE_ON_STATUS, 64, 0))
        # self.apc.really_do_send_midi((NOTE_ON_STATUS, 65, 1))
        # if self.apc.fixed_record_bar_length() > 1:
        self.apc.really_do_send_midi((NOTE_ON_STATUS, 64, 0))

        self.apc.really_do_send_midi((NOTE_ON_STATUS, 66, 0))
        if song.metronome:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, 67, 2))
            self.paintLetter(self.letters["on"])
        else:
            self.apc.really_do_send_midi((NOTE_ON_STATUS, 67, 1))
            self.paintLetter(self.letters["off"])

        # else:
        #     self.apc.really_do_send_midi((NOTE_ON_STATUS, 66, 0))
        # self.apc.really_do_send_midi((NOTE_ON_STATUS, 67, 1))

    def custom_receive_midi(self, midi_bytes):
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]
            if note == 67:
                self.apc.song().metronome = not self.apc.song().metronome
                self.syncLights()
                return
            if note < 64:
                self.apc.song().metronome = not self.apc.song().metronome
                self.syncLights()
            if note == 65:
                self.gotoRootMenu()

        return False


# See http://julienbayle.net/PythonLiveAPI_documentation/Live9.6.xml
# Decompiled source for core scripts: https://github.com/gluon/AbletonLive9_RemoteScripts
class MH_APC_mini(APC_mini):
    SESSION_HEIGHT = 8
    HAS_TRANSPORT = False

    shiftPressed = False
    shiftPressedOnNoteKey = False
    __fixed_record_bar_length=2
    lastNote = 0
    firstShiftClickedNote = -1
    lastShiftClickedNote = -1

    lastShiftUpMillis=0

    def __init__(self, *a, **k):
        super(MH_APC_mini, self).__init__(*a, **k)
        self.set_fixed_record_bar_length(4)
        self.mode = None
        self.rootMenu=ShiftedMenuMode(self)


    def getTrackIndex(self, note):
        return int(note % 8)

    def getClipIndex(self, note):
        return 7 - int((note - self.getTrackIndex(note)) / 8)


    def _do_send_midi(self, midi_bytes):
        # Override so that when custom mode takes over none of the usual updates (e.g. mouse click on clip on Mac)
        # will cause changes to lights
        if self.mode != None:
            return
        super(MH_APC_mini, self)._do_send_midi(midi_bytes)


    # Used by edit modes to echo edit ops as lighting messages unrelated to usual Live clip events
    def really_do_send_midi(self, midi_bytes):
        super(MH_APC_mini, self)._do_send_midi(midi_bytes)


    def receive_midi(self, midi_bytes):

        # When in edit mode redirect incoming midi message to current editor
        if self.mode != None:
            self.mode.custom_receive_midi(midi_bytes)
            return

        song = self.song()
        # if midi_bytes[0] & 240 == NOTE_ON_STATUS or midi_bytes[0] & 240 == NOTE_OFF_STATUS:
        if midi_bytes[0] & 240 == NOTE_OFF_STATUS:
            note = midi_bytes[1]
            if note == SHIFT_KEY:
                self.shiftPressed = False

                now=  int(round(time.time() * 1000))
                # Double tap on shift key = show menu gesture
                if now - self.lastShiftUpMillis <500:
                    # Now flip mode to edit mode showing root menu
                    self.mode = self.rootMenu
                    self.mode.syncLights()

                self.lastShiftUpMillis = now



                self.show_message("")


                if self.firstShiftClickedNote >=0:
                    firstNote=self.firstShiftClickedNote
                    lastNote=self.lastShiftClickedNote
                    self.firstShiftClickedNote=-1
                    self.lastShiftClickedNote=-1
                    fromTrackIndex = self.getTrackIndex(firstNote)
                    fromTrack = song.tracks[fromTrackIndex]
                    fromClipIndex = self.getClipIndex(firstNote)
                    # self.log_message("armed="+str(track.arm)+" tr="+str(trackIndex)+" clip="+str(clipIndex))
                    fromClip = fromTrack.clip_slots[fromClipIndex].clip
                    if fromClip is not None:
                        if lastNote <0:
                            # Delete first clip
                            fromTrack.clip_slots[fromClipIndex].delete_clip()
                        else:
                            # Copy first clicked clip to last (BUT THIS ERRORS!!! HOW TO DO PROGRAMATICALLY??
                            fromTrack.duplicate_clip_slot(fromClipIndex)
                            # toTrackIndex = self.getTrackIndex(lastNote)
                            # toTrack = song.tracks[toTrackIndex]
                            # toClipIndex = self.getClipIndex(lastNote)
                            # toTrack.clip_slots[toClipIndex]=fromClip


        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            note = midi_bytes[1]
            if note == SHIFT_KEY:
                self.shiftPressed = True
                self.show_message("Shift + row 6 = menu, row 7= undo")
            else:
                self.lastNote = note
                # self.log_message("MIDI!" + str(note))
            if note  ==88 and self.shiftPressed:
                song.undo()
                return
            if note  ==87 and self.shiftPressed:
                self.song().metronome = not self.song().metronome

            if note <64:
                if self.shiftPressed:
                    if self.firstShiftClickedNote <0:
                        self.firstShiftClickedNote = note
                        return
                    else:
                        self.lastShiftClickedNote = note
                        return

                trackIndex = self.getTrackIndex(note)
                track = song.tracks[trackIndex]
                clipIndex= self.getClipIndex(note)
                # self.log_message("armed="+str(track.arm)+" tr="+str(trackIndex)+" clip="+str(clipIndex))
                clip = track.clip_slots[clipIndex].clip
                if clip is None:
                    for t in range(8):
                        track = song.tracks[t]
                        track.arm = (t == trackIndex)
                    # track.arm = True
                    # Start recording
                    bars = self.fixed_record_bar_length()
                    if bars == 0:
                        bars = 4
                    beatsPerBar = int(song.signature_numerator)
                    beats = bars * beatsPerBar

                    song.trigger_session_record(beats)  # MH
                    # self.log_message("Starting record")
                    # self.log_message("clip:"+str(7-int(note/8))+"-"+str(int(note%8))+" "+str(clip))
                    return
        # Don't seem to get any CC messages but Live intercepts them somehow
        # elif midi_bytes[0] & 240 == CC_STATUS:
        #     cc_no = midi_bytes[1]
        #     cc_value = midi_bytes[2]
        #     self.log_message("CC " + str(cc_no)+" v:"+str(cc_value))

        super(MH_APC_mini, self).receive_midi(midi_bytes)

    #MH
    def fixed_record_bar_length(self):
        return self.__fixed_record_bar_length

    #MH
    def set_fixed_record_bar_length(self, barLength):
        # self.log_message("LoopRecordTime" + str(barLength))
        self.__fixed_record_bar_length = barLength

