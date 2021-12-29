# uncompyle6 version 3.8.1.dev0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.8.5 (default, Sep  4 2020, 02:22:02) 
# [Clang 10.0.0 ]
# Embedded file name: output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC_mini/__init__.py
# Compiled at: 2021-11-05 04:29:38
# Size of source mod 2**32: 697 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .APC_mini import APC_mini

def create_instance(c_instance):
    return APC_mini(c_instance)


def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536,
                          product_ids=[40],
                          model_name='APC MINI'), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[SCRIPT, REMOTE])]}
# okay decompiling __init__.pyc
