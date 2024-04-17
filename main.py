import machine
import ssd1306
import time


def http_get(url):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

def update():
    with open("VERSION") as file:
        spall_version = file.read()
    print(spall_version, "...")

    return spall_version

fileversion = update()



i2c = machine.SoftI2C(sda=machine.Pin(22), scl=machine.Pin(21))
display = ssd1306.SSD1306_I2C(128,64, i2c)

display.text(fileversion.split("-")[0], 0,0,1)
display.show()
time.sleep(2)
display.fill(0)
display.show()

