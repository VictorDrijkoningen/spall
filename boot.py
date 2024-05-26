# pylint: skip-file

# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import network
import webrepl
import gc
import esp
import time

esp.osdebug(0)

gc.enable()

webrepl.start()

mode = 'LAN'
#mode = 'AP'

try:
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
        start = time.time()
        while not lan.isconnected():
            time.sleep(0.1)
            if (time.time() - start) > 10:
                raise TimeoutError
except:
    ap = network.WLAN(network.AP_IF)
    ap.config(essid='ERROR')
    ap.active(True)

gc.collect()