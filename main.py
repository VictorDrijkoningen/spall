import machine
import ssd1306
import time
import urequests as requests


with open(".env") as f:
        env = f.read().split(",")


def update():
    with open("VERSION") as file:
        spall_version = file.read()
        githubversion = requests.get(env[2]).text
        if spall_version != githubversion:
             with open('VERSION', 'w') as f:
                  f.write(githubversion)
                  
    return spall_version, githubversion



fileversion,githubversion = update()


i2c = machine.SoftI2C(sda=machine.Pin(22), scl=machine.Pin(21))
display = ssd1306.SSD1306_I2C(128,64, i2c)

display.text(fileversion.split("-")[0]+" / "+ str(githubversion), 0,0,1)
display.show()
time.sleep(5)
display.fill(0)
display.show()

