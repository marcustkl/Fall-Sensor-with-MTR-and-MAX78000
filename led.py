from __future__ import print_function
from mbientlab.metawear import MetaWear, libmetawear
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event

import sys

# connect to C5:DE:74:B6:AC:5F
address = "C5:DE:74:B6:AC:5F"
device = MetaWear(address)
device.connect()
print("Connected")

# create led pattern
pattern= LedPattern(repeat_count= Const.LED_REPEAT_INDEFINITELY)
libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.BLINK)
libmetawear.mbl_mw_led_write_pattern(device.board, byref(pattern), LedColor.GREEN)

# play the pattern
libmetawear.mbl_mw_led_play(device.board)

# wait 5s
sleep(5.0)

# remove the led pattern and stop playing
libmetawear.mbl_mw_led_stop_and_clear(device.board)
sleep(2.0)

print("Done")
# disconnect
device.disconnect()
sleep(1.0)