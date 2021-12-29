from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .APC_mini_mle import APC_mini_mle

def create_instance(c_instance):
    return APC_mini_mle(c_instance)

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536,
                                             product_ids=[40],
                                             model_name='APC MINI MLE'),

            PORTS_KEY: [
                inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                outport(props=[SCRIPT, REMOTE])]}
