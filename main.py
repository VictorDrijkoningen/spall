# pylint: skip-file
import machine
import urequests as requests
import time
import uasyncio as asyncio
import gc
import json
from microdot import Microdot, send_file
from ws import with_websocket


try:
    import ssd1306
except:
    import mip
    mip.install('ssd1306')

with open(".env") as f:
        env = f.read().split(",")


def update(force_update = False):
    with open("VERSION") as file:
        spall_version = file.read()
        githubversion = requests.get(env[2]).text
        if spall_version != githubversion or force_update:
            print(spall_version.split("-")[0]+" / "+ str(githubversion).split("-")[0])
            with open('VERSION', 'w') as f:
                  f.write(githubversion)
            with open('main.py', 'w') as f:
                  f.write(requests.get(env[3]).text)
            with open('boot.py', 'w') as f:
                  f.write(requests.get(env[4]).text)
            print('done updating')
    return spall_version


async def do_display():
    return
    i2c = machine.SoftI2C(sda=machine.Pin(22), scl=machine.Pin(21))
    display = ssd1306.SSD1306_I2C(128,64, i2c)
    display.text(fileversion.split("-")[0], 0,0,1)
    display.show()
    while True:
        x = 56
        y = 32
        display.text("-", x,y,1)
        display.show()
        display.text("-", x,y,0)
        await asyncio.sleep(1.5)
        display.text("\\", x,y,1)
        display.show()
        display.text("\\", x,y,0)
        await asyncio.sleep(1.5)
        display.text("|", x,y,1)
        display.show()
        display.text("|", x,y,0)
        await asyncio.sleep(1.5)
        display.text("/", x,y,1)
        display.show()
        display.text("/", x,y,0)
        await asyncio.sleep(1.5)
    
def servos_on():
    global steer_motor 
    steer_motor = machine.PWM(machine.Pin(13))
    steer_motor.freq(50)
    steer_motor.duty(75)

    global drive_motor
    drive_motor = machine.PWM(machine.Pin(12))
    drive_motor.freq(50)
    drive_motor.duty(75)

def servos_off():
    drive_motor.deinit()
    steer_motor.deinit()

def servo(device, input, inpmin, inpmax):
    def mapFromTo(x,a,b,c,d):
        y=(x-a)/(b-a)*(d-c)+c
        return y
    input = max(inpmin, min(inpmax,int(input)))
    try:
        device.duty(int(mapFromTo(input, inpmin, inpmax, 20, 130)))
    except:
        print("Servo not on")



fileversion = update()
servos_on()

app = Microdot()

@app.route('/', methods=['GET'])
async def index(request):
    return send_file('index.html')

@app.route('/joy.js', methods=['GET'])
async def index(request):
    return send_file('joy.js')

@app.route('/mem', methods=['GET'])
async def index(request):
    return str(gc.mem_alloc()) + " used, " +  str(gc.mem_free()) + " free"

@app.route('/shutdown', methods=['GET'])
async def shutdown(request):
    request.app.shutdown()
    return 'shutting down'

@app.route('/websocket')
@with_websocket
async def websocket(request, ws):
    while True:
        message = await ws.receive()
        print("ws: "+message)
        try:
            message = json.loads(message)
            if 'joy1x' in message.keys():
                servo(steer_motor, message['joy1x'], 75, 225)
            if 'joy2y' in message.keys():
                servo(drive_motor, message['joy2y'], 75, 225)
            if 'on' in message.keys():
                servos_on()
            if 'off' in message.keys():
                servos_off()
        except ValueError:
            print("malformed json")
        await ws.send("rcvd")





async def webserver():
    await app.start_server(debug=False,host='0.0.0.0', port=80)

async def main():
    await asyncio.gather(webserver(), do_display())

def start():
    asyncio.run(main())

start()
