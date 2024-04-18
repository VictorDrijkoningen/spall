# pylint: skip-file
import machine
import urequests as requests
import time
import uasyncio as asyncio


from microdot import Microdot

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
        display.text("-", 15,15,2)
        display.show()
        display.fill(0)
        await asyncio.sleep(0.5)
        display.text("\\", 15,15,1)
        display.show()
        display.fill(0)
        await asyncio.sleep(0.5)
        display.text("|", 15,15,1)
        display.show()
        display.fill(0)
        await asyncio.sleep(0.5)
        display.text("/", 15,15,1)
        display.show()
        display.fill(0)
        await asyncio.sleep(0.1)
        time.sleep(0.4)
    


def servo():
    right_motor = machine.PWM(machine.Pin(13))
    right_motor.freq(50)
    right_motor.duty(300)
    time.sleep(0.05)
    right_motor.deinit()


fileversion = update()


i2c = machine.SoftI2C(sda=machine.Pin(22), scl=machine.Pin(21))
display = ssd1306.SSD1306_I2C(128,64, i2c)
display.text(fileversion.split("-")[0], 0,0,1)
display.show()







app = Microdot()

@app.route('/')
async def index(request):
    servo()
    return 'Hello, world!'

async def webserver():
    await app.start_server(debug=True,host='0.0.0.0', port=80)

async def main():
    await asyncio.gather(webserver(), do_display())

asyncio.run(main())

servo()
































# def web_page():
#     with open("index.html") as f:
#         html = f.read()
#     return html


# async def webserver():
#     try:
#         webserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         webserver.bind(('0.0.0.0', 80))
#         webserver.listen(5)
#         webserver.setblocking(False)
#         webserver.settimeout(1)
#         print("setup server")

#         while True:
#             try:
#                 conn, addr = webserver.accept()
#                 print('Got a connection from %s' % str(addr))
#                 request = conn.recv(1024)
#                 request = str(request)
#                 print('Content = %s' % request)

#                 try:
#                     response = web_page()
#                     conn.sendall(response)
#                     conn.close()
#                 except:
#                     print("send exception")
                
#             except:
#                  pass
#             await asyncio.sleep(0.5)
#             do_display()
            

#     except Exception as e:
#         print(e)
#     webserver.close()

# async def handle_client(reader, writer):
#     try:
#         request = (await reader.read(255)).decode('utf8')
#         response = web_page().encode('utf8')
#         writer.write(header())
#         writer.write(response)
#         await writer.drain()
#     except Exception as e:
#         print(e)
#     finally:
#         writer.close()

# async def run_server():
#     server = await asyncio.start_server(handle_client, '0.0.0.0', 80)
#     async with server:
#         print("started server")
#         await server.wait_closed()


# async def main():
#      await asyncio.gather(do_display(), run_server())

# def start():
#     asyncio.run(main())