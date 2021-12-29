# uncompyle6 version 3.8.1.dev0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.5 (default, Sep  4 2020, 02:22:02) 
# [Clang 10.0.0 ]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC_mini/APC_mini.py
# Compiled at: 2021-11-05 04:29:38
# Size of source mod 2**32: 1468 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import map
from _Framework.Layer import Layer, SimpleLayerOwner
from _APC.ControlElementUtils import make_slider
import APC_Key_25.APC_Key_25 as APC_Key_25

class APC_mini(APC_Key_25):
    SESSION_HEIGHT = 8
    HAS_TRANSPORT = False

    def __init__(self, *a, **k):
        (super(APC_mini, self).__init__)(*a, **k)
        with self.component_guard():
            self.register_disconnectable(SimpleLayerOwner(layer=Layer(_unused_buttons=(self.wrap_matrix(self._unused_buttons)))))

    def _make_stop_all_button(self):
        return self.make_shifted_button(self._scene_launch_buttons[7])

    def _create_controls(self):
        super(APC_mini, self)._create_controls()
        self._unused_buttons = list(map(self.make_shifted_button, self._scene_launch_buttons[5:7]))
        self._master_volume_control = make_slider(0, 56, name='Master_Volume')

    def _create_mixer(self):
        mixer = super(APC_mini, self)._create_mixer()
        mixer.master_strip().layer = Layer(volume_control=(self._master_volume_control))
        return mixer

    def _product_model_id_byte(self):
        return 40
# okay decompiling APC_mini.pyc
