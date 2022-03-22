from __future__ import with_statement, absolute_import, print_function, unicode_literals
from builtins import map
import time
from _Framework.Layer import Layer, SimpleLayerOwner
from _APC.ControlElementUtils import make_slider
import APC_Key_25.APC_Key_25 as APC_Key_25

NOTE_ON_STATUS = 144
NOTE_OFF_STATUS = 128
SHIFT_KEY = 98
CC_STATUS = 176

VOLUME_KEY = 68
PAN_KEY = 69
SEND_KEY = 70
DEVICE_KEY = 71

BAR_OFF = 0
BAR_ON = 1
BAR_BLINK = 2

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
            "bar": [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 5, 0, 1, 1],
                [1, 1, 1, 5, 0, 5, 1, 0],
                [0, 0, 0, 5, 5, 5, 1, 0],
                [0, 0, 0, 5, 0, 5, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "bpm": [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 5, 5, 5, 0, 0],
                [1, 1, 1, 5, 0, 5, 0, 0],
                [1, 0, 1, 5, 5, 5, 0, 0],
                [1, 1, 1, 5, 0, 1, 0, 1],
                [0, 0, 0, 5, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 0, 1]
            ],
            "tap": [
                [1, 1, 1, 0, 0, 1, 1, 1],
                [0, 1, 0, 0, 0, 1, 0, 1],
                [0, 1, 0, 5, 0, 1, 1, 1],
                [0, 1, 5, 0, 5, 1, 0, 0],
                [0, 0, 5, 5, 5, 1, 0, 0],
                [0, 0, 5, 0, 5, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "undo": [
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
            "edit": [
                [1, 1, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 0, 5, 5, 5],
                [1, 1, 0, 5, 1, 0, 5, 0],
                [1, 0, 0, 5, 1, 0, 5, 0],
                [1, 1, 5, 5, 1, 0, 5, 0],
                [0, 0, 5, 5, 0, 0, 0, 0],
                [0, 0, 5, 5, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "small1": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0]
            ],
            "small2": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small3": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small4": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0]
            ],
            "small5": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small6": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small7": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "small8": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small9": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "small0": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0]
            ],
            "on": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 1, 1, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],
                [1, 1, 1, 0, 1, 0, 1, 0]
            ],
            "off": [
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
        color = 1
        inc = 2
        if len(numberAsString) >= 3:
            inc = 1
        for char in numberAsString:
            letter = self.letters["small" + char]
            lastCol = 0
            if inc == 1:
                # No space between digits - use color to differentiate
                if color == 1:
                    color = 5
                else:
                    color = 1
            for rowNum, rowArr in enumerate(letter):
                for colNum, val in enumerate(rowArr):
                    if val == 1:
                        lastCol = max(lastCol, colNum)
                        if offset + colNum <= 7:
                            combined_letter[rowNum][offset + colNum] = color
            offset = offset + lastCol + inc
        self.paintLetter(combined_letter)


class ShiftedMenuMode(ModeBase):
    modeNum = 0

    def __init__(self, apc):
        ModeBase.__init__(self, apc)
        self.apc.show_message("menuMode")
        self.modes = [RecordBarsMode(apc), TapTempoMode(apc), MetronomeMode(apc), PaintMode(apc)]
        self.modeNum = 0
        # self.syncLights()

    def syncLights(self):
        self.apc.log_message("Mode name")
        self.apc.log_message(self.modes[self.modeNum].getName())
        self.apc.log_message("grid")
        self.apc.log_message(self.letters[self.modes[self.modeNum].getName()])
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
            if note == 65:
                self.exitMode()
                return
            if note == 64:
                self.apc.mode = self.modes[self.modeNum]
                self.apc.mode.syncLights()
                return
            if note == 66:
                self.modeNum = self.modeNum - 1
                if self.modeNum < 0:
                    self.modeNum = 0
                self.syncLights()
            if note == 67:
                self.modeNum = self.modeNum + 1
                if self.modeNum >= len(self.modes):
                    self.modeNum = len(self.modes) - 1
                self.syncLights()

        return False


class PaintMode(ModeBase):
    def __init__(self, apc):
        ModeBase.__init__(self, apc)
        self.grid = [
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
            if note == 65:
                self.gotoRootMenu()
                return
            if note < 64:
                trackIndex = self.apc.getTrackIndex(note)
                clipIndex = self.apc.getClipIndex(note)
                note = self.grid[clipIndex][trackIndex]
                if note == 0:
                    self.grid[clipIndex][trackIndex] = 1
                elif note == 1:
                    self.grid[clipIndex][trackIndex] = 3
                elif note == 3:
                    self.grid[clipIndex][trackIndex] = 5
                elif note == 5:
                    self.grid[clipIndex][trackIndex] = 0
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
        if self.apc.fixed_record_bar_length() > 1:
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
                self.apc.set_fixed_record_bar_length(self.apc.fixed_record_bar_length() + 1)
                self.syncLights()
            if note == 66 and self.apc.fixed_record_bar_length() > 1:
                self.apc.set_fixed_record_bar_length(self.apc.fixed_record_bar_length() - 1)
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
                self.apc.song().tempo = int(self.apc.song().tempo) + 1
                self.syncLights()
                return
            if note == 66:
                self.apc.song().tempo = int(self.apc.song().tempo) - 1
                self.syncLights()
                return
            if note == 65:
                self.gotoRootMenu()
                song = self.apc.song()
                # - round down tempo
                song.tempo = int(song.tempo)

            else:
                song = self.apc.song()
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


#class APC_mini_mle(APC_mini):
class APC_mini_mle(APC_Key_25):
    # @Overridden
    SESSION_HEIGHT = 8
    # @Overridden
    HAS_TRANSPORT = False

    RECORD_BAR_LENGTH = 4

    # Locals :
    shiftPressed = False
    __fixed_record_bar_length = RECORD_BAR_LENGTH
    lastShiftUpMillis = 0
    firstShiftClickedNote = -1
    lastShiftClickedNote = -1
    noteDoubleClickMillis = 0
    # TODO make mode configurable : 4 or 7 - 4 should be 1/8 + 1/8T; 7 should be 1/16 + 1/16T ?
    #  2 = 1/8   5= 1/16
    quantizeMode = 5
    mode = None

    # @Overridden
    def __init__(self, *a, **k):
        #super(APC_mini_mle, self).__init__(*a, **k)
        (super(APC_mini_mle, self).__init__)(*a, **k)
        with self.component_guard():
            self.register_disconnectable(SimpleLayerOwner(layer=Layer(_unused_buttons=(self.wrap_matrix(self._unused_buttons)))))

        self.log_message("MLEV5 in progress")
        self.set_fixed_record_bar_length(self.RECORD_BAR_LENGTH)
        self._suppress_send_midi = False
        self.mode = None
        self.rootMenu = ShiftedMenuMode(self)

    # @Overridden
    def _make_stop_all_button(self):
        return self.make_shifted_button(self._scene_launch_buttons[7])

    # @Overridden
    def _create_controls(self):
        super(APC_mini_mle, self)._create_controls()
        self._unused_buttons = list(map(self.make_shifted_button, self._scene_launch_buttons[5:7]))
        self._master_volume_control = make_slider(0, 56, name='Master_Volume')

    # @Overridden
    def _create_mixer(self):
        mixer = super(APC_mini_mle, self)._create_mixer()
        mixer.master_strip().layer = Layer(volume_control=(self._master_volume_control))
        return mixer

    # @Overridden
    def _product_model_id_byte(self):
        return 40

    ####

    def getTrackIndex(self, note):
        return int(note % 8)

    def getClipIndex(self, note):
        return 7 - int((note - self.getTrackIndex(note)) / 8)

    def _releaseShiftMenu(self, midi_bytes):

        song = self.song()
        note = midi_bytes[1]

        if note != SHIFT_KEY:
            return False

        self.shiftPressed = False

        # Double tap on shift key => show advanced menu
        now = int(round(time.time() * 1000))
        if now - self.lastShiftUpMillis < 500:
            self.mode = self.rootMenu
            self.mode.syncLights()

        self.lastShiftUpMillis = now

        if self.firstShiftClickedNote >= 0:
            firstNote = self.firstShiftClickedNote
            lastNote = self.lastShiftClickedNote
            self.firstShiftClickedNote = -1
            self.lastShiftClickedNote = -1
            fromTrackIndex = self.getTrackIndex(firstNote)
            fromTrack = song.tracks[fromTrackIndex]
            fromClipIndex = self.getClipIndex(firstNote)
            fromClipSlot = fromTrack.clip_slots[fromClipIndex]
            fromClip = fromClipSlot.clip
            if fromClip is not None:
                if lastNote < 0:
                    fromClipSlot.delete_clip()
                else:
                    toTrackIndex = self.getTrackIndex(lastNote)
                    toTrack = song.tracks[toTrackIndex]
                    toClipIndex = self.getClipIndex(lastNote)
                    toClipSlot = toTrack.clip_slots[toClipIndex]

                    # fromTrack.duplicate_clip_slot(fromClipIndex)
                    fromClipSlot.duplicate_clip_to(toClipSlot)

        self.show_message("")
        return False

    def _applyShiftMenu(self, midi_bytes):

        song = self.song()
        note = midi_bytes[1]

        if note == SHIFT_KEY:
            self.shiftPressed = True
            self.show_message("Shift + row 6 = metronome, row 7= undo")

        if note == 88 and self.shiftPressed:
            song.undo()
            return True

        if note == 87 and self.shiftPressed:
            song.tempo = round(song.tempo)
            song.metronome = not song.metronome
            return True

        # Double tap on note key => quantize
        now = int(round(time.time() * 1000))
        if note < 64:

            trackIndex = self.getTrackIndex(note)
            track = song.tracks[trackIndex]
            clipIndex = self.getClipIndex(note)
            clipSlot = track.clip_slots[clipIndex]
            if now - self.noteDoubleClickMillis < 500:
                if clipSlot.has_clip:
                    # and clipSlot.clip.is_midi_clip
                    self.log_message("APC quantize with mode " + str(self.quantizeMode))
                    clipSlot.clip.quantize(self.quantizeMode, 1)
                    return True

            if clipSlot.has_clip:
                self.noteDoubleClickMillis = now

        # Catch note selected with Shift
        if note < 64 and self.shiftPressed:
            if self.firstShiftClickedNote < 0:
                self.firstShiftClickedNote = note
                return True
            else:
                self.lastShiftClickedNote = note
                return True

        # Recording launch on one note
        if note < 64:
            trackIndex = self.getTrackIndex(note)
            track = song.tracks[trackIndex]
            clipIndex = self.getClipIndex(note)
            clipSlot = track.clip_slots[clipIndex]

            last_bars = self.fixed_record_bar_length()
            if last_bars == 0:
                last_bars = 8

            # Opinion oriented : fixed track's bars
            bars = last_bars
            if trackIndex == 0:
                bars = 1
            elif trackIndex == 1 or trackIndex == 2:
                bars = 2
            elif trackIndex == 3 or trackIndex == 4:
                bars = 4

            beatsPerBar = int(song.signature_numerator)
            beats = bars * beatsPerBar
            self.log_message("APC trackIndex: " + str(trackIndex) + " - " + str(beats))
            if not clipSlot.has_clip and not clipSlot.is_group_slot:
                track.arm = True
                clipSlot.fire(beats)
                return True
            else:
                song.session_record = False

        return False

    # @Overridden _do_send_midi
    def _do_send_midi(self, midi_bytes):
        # Override so that when custom mode takes over none of the usual updates (e.g. mouse click on clip on Mac)
        # will cause changes to lights
        if self.mode != None:
            return
        super(APC_mini_mle, self)._do_send_midi(midi_bytes)

    # Used by edit modes to echo edit ops as lighting messages unrelated to usual Live clip events
    def really_do_send_midi(self, midi_bytes):
        super(APC_mini_mle, self)._do_send_midi(midi_bytes)

    # @Overridden receive_midi
    def receive_midi(self, midi_bytes):

        self.log_message("APC receive_midi: " + str(midi_bytes))
        extra_conf_applied = False

        # Custom Modes
        if self.mode is not None:
            self.mode.custom_receive_midi(midi_bytes)
            return

        # Shift released or applied
        if midi_bytes[0] & 240 == NOTE_OFF_STATUS:
            extra_conf_applied = self._releaseShiftMenu(midi_bytes)
        elif midi_bytes[0] & 240 == NOTE_ON_STATUS:
            extra_conf_applied = self._applyShiftMenu(midi_bytes)

        # Transfer to Parent
        if not extra_conf_applied:
            super(APC_mini_mle, self).receive_midi(midi_bytes)

    def fixed_record_bar_length(self):
        return self.__fixed_record_bar_length

    def set_fixed_record_bar_length(self, barLength):
        self.__fixed_record_bar_length = barLength
