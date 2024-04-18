# pylint: skip-file

# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import network
import webrepl
import gc

gc.enable()

webrepl.start()

mode = 'LAN'
#mode = 'AP'

if mode == 'AP':
    ap = network.WLAN(network.AP_IF)
    ap.config(essid='SPALL')
    ap.active(True)
else:
    with open(".env") as env_file:
        env = env_file.read().split(",")
    lan = network.WLAN(network.STA_IF)
    lan.active(True)
    lan.connect(env[0], env[1])
    while not lan.isconnected():
        pass


gc.collect()