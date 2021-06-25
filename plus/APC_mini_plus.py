#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC_mini_plus/APC_mini_plus.py
#https://julienbayle.studio/PythonLiveAPI_documentation/Live10.1.19.xml
#https://nsuspray.github.io/Live_API_Doc/10.1.0.xml
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Layer import Layer, SimpleLayerOwner
from _APC.ControlElementUtils import make_slider
from APC_Key_25.APC_Key_25 import APC_Key_25
from APC_mini.APC_mini import APC_mini
import time

GRID_OFF = 0
GRID_GREEN = 1
GRID_GREEN_BLINK = 2
GRID_RED = 3
GRID_RED_BLINK = 4
GRID_YELLOW = 5
GRID_YELLOW_BLINK = 6

BAR_OFF = 0
BAR_ON = 1
BAR_BLINK = 2

NOTE_ON_STATUS = 144
NOTE_OFF_STATUS = 128
SHIFT_KEY = 98
UNDO_KEY = 88

UP_KEY = 64
DOWN_KEY = 65
LEFT_KEY = 66
RIGHT_KEY = 67
VOLUME_KEY = 68
PAN_KEY = 69
SEND_KEY = 70
DEVICE_KEY = 71

METRONOME_KEY = 87
DOUBLE_PRESS_TIMING_LIMIT = 500

class ShiftedMenuMode():

    BARS_ON_OFF = 63
    BARS_COL_INDEX = 7
    def __init__(self, apc):
        self.apc = apc

    def setMode(self):
        self.apc.log_message("Shifted Menu")
        for i in range(8):
            self.apc.setRightBarLed(i, BAR_BLINK)
        self.apc.updateArmedRow()
        self.apc.clear_lights()
        time.sleep(0.1)
        self.setBarsLeds()

    def setBarsLeds(self):
        for i in range(8):
            self.apc.setGridLed(7, i, GRID_OFF)
        if self.apc.fixedRecordLength:
            self.apc.setGridLed(7, 0, GRID_GREEN)
            for i in range(self.apc.recordLengthsIdx + 1):
                self.apc.setGridLed(7, 7 - i, GRID_YELLOW)
        else:
            self.apc.setGridLed(7, 0, GRID_RED)

    def custom_receive_midi(self, midi_bytes):
        note = midi_bytes[1]
        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            if note == self.BARS_ON_OFF:
                self.apc.fixedRecordLength = not self.apc.fixedRecordLength
                self.setBarsLeds()

            elif self.apc.getTrackIndex(note) == self.BARS_COL_INDEX:
                self.apc.recordLengthsIdx = 7 - self.apc.getClipIndex(note)
                self.setBarsLeds()

            elif note >= 64 and note <= 71:
                track = self.apc.getTrack(note)
                if track != False:
                    track.arm = not track.arm
                self.apc.updateArmedRow()


        elif midi_bytes[0] & 240 == NOTE_OFF_STATUS:
            if note == SHIFT_KEY:
                self.apc.shiftPressed = False
                self.apc.mode = None
                self.apc._update_hardware()

class APC_mini_plus(APC_mini):
    SESSION_HEIGHT = 8
    HAS_TRANSPORT = False
    shiftPressed = False
    deletingState = False
    clipHasBeenCopied = False
    metronomeMode = False
    toDeleteNote = 0
    previousNotePressedDown = 0
    previousNoteReleased = 0
    previousPressTime = int(round(time.time() * 1000))
    previousReleaseTime = int(round(time.time() * 1000))

    previousEncoderMode = 'volume'

    fixedRecordLength = False
    recordLengths = [1, 2, 4, 8, 16, 32, 64]
    recordLengthsIdx = 2

    def __init__(self, *a, **k):
        super(APC_mini_plus, self).__init__(*a, **k)
        self._suppress_send_midi = False
        self.mode = None
        self.rootMenu=ShiftedMenuMode(self)

    def getTrackIndex(self, note):
        return int(note % 8) + self._session._track_offset

    def getTrack(self, note):
        if len(self.song().tracks) > self.getTrackIndex(note):
            return self.song().tracks[self.getTrackIndex(note)]
        else:
            return False

    def getClipIndex(self, note):
        return 7 - int((note / 8)) + self._session._scene_offset

    def getClipSlot(self, note):
        return self.getTrack(note).clip_slots[self.getClipIndex(note)]

    def noteDoublePressed(self, note):
        return (self.previousNotePressedDown == note) and (int(round(time.time() * 1000)) - self.previousPressTime <= DOUBLE_PRESS_TIMING_LIMIT)

    def noteDoubleReleased(self, note):
        return (self.previousNoteReleased == note) and (int(round(time.time() * 1000)) - self.previousReleaseTime <= DOUBLE_PRESS_TIMING_LIMIT)

    def clear_lights(self):
        for i in range (64):
            self.send_midi((NOTE_ON_STATUS, i, 0))

    def _do_send_midi(self, midi_bytes):
        # Override so that when custom mode takes over none of the usual updates (e.g. mouse click on clip on Mac)
        # will cause changes to lights
        if self.mode != None:
            return
        self.send_midi(midi_bytes)

    def send_midi(self, midi_bytes):
        super(APC_mini_plus, self)._do_send_midi(midi_bytes)

    # turns on/off a grid's LED, (0, 0) represents the top left corner of the APC
    def setGridLed(self, x, y, state):
        if x >= 8 or y >= 8:
            self.log_message("Can't set grid LED, the coordinates are out of the 8x8 grid.")
            return
        elif state > 6:
            self.log_message("Can't set grid LED, given state does not exist.")
            return

        self.send_midi((NOTE_ON_STATUS, x + ((8 - (y + 1)) * 8), state))

    def setBottomBarLed(self, i, state):
        if i >= 8:
            self.log_message("Can't set bottom bar LED, the index is higher than 8.")
            return
        elif state > 2:
            self.log_message("Can't set bottom bar LED, given state does not exist.")
            return

        self.send_midi((NOTE_ON_STATUS, 64 + i, state))

    def setRightBarLed(self, i, state):
        if i >= 8:
            self.log_message("Can't set right bar LED, the index is higher than 8.")
            return
        elif state > 2:
            self.log_message("Can't set right bar LED, given state does not exist.")
            return

        self.send_midi((NOTE_ON_STATUS, 82 + i, state))

    def updateArmedRow(self):
        for i in range(8):
            track = self.getTrack(i)
            if track != False:
                if not track.clip_slots[0].is_group_slot:
                    if track.can_be_armed and self.getTrack(i).arm == True:
                        self.setBottomBarLed(self.getTrackIndex(i), BAR_ON)
                    else:
                        self.setBottomBarLed(self.getTrackIndex(i), BAR_OFF)

    def receive_midi(self, midi_bytes):
        if self.mode != None:
            self.mode.custom_receive_midi(midi_bytes)
            return
        note = midi_bytes[1]
        super(APC_mini_plus, self).receive_midi(midi_bytes)

        if midi_bytes[0] & 240 == NOTE_ON_STATUS:
            pressTime = int(round(time.time() * 1000))
            if note == SHIFT_KEY:
                self.previousEncoderMode = self._encoder_modes.selected_mode
                self._encoder_modes.selected_mode = 'pan'
                # So the mode LED doesnt always show pan
                self.send_midi((NOTE_ON_STATUS, PAN_KEY, BAR_OFF))
                if self.previousEncoderMode == 'volume':
                    self.send_midi((NOTE_ON_STATUS, VOLUME_KEY, BAR_ON))
                elif self.previousEncoderMode == 'pan':
                    self.send_midi((NOTE_ON_STATUS, PAN_KEY, BAR_ON))
                elif self.previousEncoderMode == 'send':
                    self.send_midi((NOTE_ON_STATUS, SEND_KEY, BAR_ON))
                elif self.previousEncoderMode == 'device':
                    self.send_midi((NOTE_ON_STATUS, DEVICE_KEY, BAR_ON))

                self.shiftPressed = True

            if self.shiftPressed:
                if note == UNDO_KEY:
                    self.song().undo()
                elif note == METRONOME_KEY:
                     self.metronomeMode = True
                elif note == VOLUME_KEY or note == PAN_KEY or note == SEND_KEY or note == DEVICE_KEY:
                    # so that encoder mode isnt set back to volume once shift is released
                    self.previousEncoderMode = self._encoder_modes.selected_mode
                elif note < 64:
                    if self.metronomeMode:
                        self.song().metronome = False
                        self.song().tap_tempo()
                        self.song().tempo = round(self.song().tempo)
                        return
                    if self.deletingState:
                        # copy the clip waiting to be deleted to another slot
                        self.getClipSlot(self.toDeleteNote).duplicate_clip_to(self.getClipSlot(note))
                        self.clipHasBeenCopied = True
                    else:
                        if self.getClipSlot(note).has_clip:
                            self.deletingState = True
                            self.clipHasBeenCopied = False
                            self.toDeleteNote = note
            else:
                if note < 64:
                    if not self.getClipSlot(note).has_clip and not self.getClipSlot(note).is_group_slot:
                        for trackToUnArm in self.song().tracks:
                            if not trackToUnArm.clip_slots[0].is_group_slot:
                                trackToUnArm.arm = False
                        self.getTrack(note).arm = True
                        if self.fixedRecordLength:
                            self.getClipSlot(note).fire(self.recordLengths[self.recordLengthsIdx])
                        else:
                           self.getClipSlot(note).fire()
                    else :
                        # The slot has a clip
                        if self.noteDoublePressed(note):
                            # double press has occured, start mdi overdubbing
                            for trackToUnArm in self.song().tracks:
                                if not trackToUnArm.clip_slots[0].is_group_slot:
                                    trackToUnArm.arm = False
                            self.getTrack(note).arm = True
                            self.song().session_record = True
                        else:
                            self.song().session_record = False
            self.previousNotePressedDown = note
            self.previousPressTime = pressTime
        if midi_bytes[0] & 240 == NOTE_OFF_STATUS:
            releaseTime = int(round(time.time() * 1000))
            if note == SHIFT_KEY:
                self._encoder_modes.selected_mode = self.previousEncoderMode
                self.shiftPressed = False
                self.deletingState = False
                self.clipHasBeenCopied = False
                self.metronomeMode = False
                if self.noteDoubleReleased(SHIFT_KEY):
                    self.mode = self.rootMenu
                    self.mode.setMode()
                    return

            if self.shiftPressed:
                if note == self.toDeleteNote:
                    if self.deletingState:
                        # Only delete clip if it has not been copied
                        if not self.clipHasBeenCopied:
                            self.getClipSlot(self.toDeleteNote).delete_clip()
                        self.deletingState = False
                elif note == METRONOME_KEY:
                    self.song().tempo = round(self.song().tempo) # fractionnal tempos annoy me
                    self.song().metronome = not self.song().metronome
                    self.metronomeMode = False
            self.previousNoteReleased = note
            self.previousReleaseTime = releaseTime

