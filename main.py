# pylint: skip-file
import machine
import urequests as requests
import time
import uasyncio as asyncio
import gc

from microdot import Microdot, send_file

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
    while True:
        display.text("-", 15,15,5)
        display.show()
        display.fill(0)
        await asyncio.sleep(1.5)
        display.text("\\", 15,15,1)
        display.show()
        display.fill(0)
        await asyncio.sleep(1.5)
        display.text("|", 15,15,1)
        display.show()
        display.fill(0)
        await asyncio.sleep(1.5)
        display.text("/", 15,15,1)
        display.show()
        display.fill(0)
        await asyncio.sleep(1.5)
    


def servo(device, input, inpmin, inpmax):
    def mapFromTo(x,a,b,c,d):
        y=(x-a)/(b-a)*(d-c)+c
        return y
    input = max(inpmin, min(inpmax,int(input)))
    device.duty(int(mapFromTo(input, inpmin, inpmax, 20, 130)))


fileversion = update()

right_motor = machine.PWM(machine.Pin(13))
right_motor.freq(50)

i2c = machine.SoftI2C(sda=machine.Pin(22), scl=machine.Pin(21))
display = ssd1306.SSD1306_I2C(128,64, i2c)
display.text(fileversion.split("-")[0], 0,0,1)
display.show()







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

@app.route('/action', methods=['POST'])
async def action(request):
    if 'slider1' in request.json.keys():
        print(request.json['slider1'])
        servo(right_motor, request.json['slider1'], 0, 180)
    if 'joy1x' in request.json.keys():
        print(request.json['joy1x'])
        servo(right_motor, request.json['joy1x'], 50, 150)
    return "200"







async def webserver():
    await app.start_server(debug=False,host='0.0.0.0', port=80)

async def main():
    await asyncio.gather(webserver(), do_display())

def start():
    asyncio.run(main())




