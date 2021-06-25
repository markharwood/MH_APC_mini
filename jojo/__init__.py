#Embedded file name: /Users/versonator/Jenkins/live/Binary/Core_Release_64_static/midi-remote-scripts/APC_mini/__init__.py

# module name chance, copied from midiscripts.net
from APC_mini_jojo import APC_mini_jojo

# original module thing
#from _Framework.Capabilities import CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT, REMOTE, controller_id, inport, outport

# copied from midiscripts.net
from _Framework.Capabilities import controller_id, inport, outport
from _Framework.Capabilities import CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC
from _Framework.Capabilities import SCRIPT, AUTO_LOAD_KEY
# this was missing, why? just add it as well
from _Framework.Capabilities import REMOTE


def create_instance(c_instance):
    return APC_mini_jojo(c_instance)


# format change copied from midiscripts.net
def get_capabilities():
    return {
        CONTROLLER_ID_KEY: controller_id(
            vendor_id=2536, product_ids=[40],
            model_name="APC MINI J0J0"),
        PORTS_KEY: [
            inport(props=[NOTES_CC, SCRIPT, REMOTE]),
            outport(props=[SCRIPT, REMOTE])]
    }
