# Micropython. Easy Start)
# 
#
#### Blink onboard LED
# led_pin 5
print("Hello World!")

import machine
import time


led_pin = machine.Pin(5, machine.Pin.OUT)           # create Pin on GPIO5, config as OUT

led_pin.off()
time.sleep(1)
led_pin.on()
time.sleep(0.5)


# led_pin.value(True)
# led_pin.value()


"""
led_pin.off()
time.sleep(0.2)
led_pin.on()
time.sleep(0.8)

led_pin.off()
time.sleep(0.3)
led_pin.on()
time.sleep(0.7)


def led_invert(led_pin):
    if led_pin.value():
        led_pin.off()
    else:
        led_pin.on()

def led_blink(led_pin):
    led_invert(led_pin)
    time.sleep_ms(500)
    led_invert(led_pin)


for i in range(3):
    led_blink(led_pin)
    time.sleep(0.5)
"""

led_pin.on()                                    # turn off led












#'#'#'
#####################################################################################################


"help()"
"help('modules')"

# ESP32 Temperature, Hall sensor

import esp32

global esp32_tc
global esp32_hs

esp32_temp_f = esp32.raw_temperature()               # read Temperature from esp32

def t2c(Temp):
    return (Temp-32)*(5/9)                           # Temperature to `C

esp32_tc = t2c(esp32_temp_f)
print("esp32_Temp: ", esp32_tc, '`C')                ## print Temperature

esp32_hs = esp32.hall_sensor()                       # read Hall_Sensor from esp32
print("esp32_Hall_sensor: ", esp32_hs)               ## print Hall_Sensor 
print()












#######################################################################################################
# Network
# socket

import network
import socket
import ubinascii

wlan = network.WLAN(network.STA_IF)                            # create station interface
wlan.active(True)                                              # activate the interface
time.sleep(1)
#ap_list = wlan.scan()                                         # scan for access points
#for ap in ap_list:
#    print(ap)                                                 ## print APs

SSID = '<SSID>'                 # SSID
PASS = '<PASSWORD>'             # PASS
wlan.connect(SSID, PASS)        # connect to SSID with PASS
time.sleep(1)

## Process connection (check, attempts, timeout, new(SSID, PASS))
while True:
    if wlan.isconnected():
        break
    print('.', end='')
    time.sleep(1)

# print network config
print()
print("wlan.isconnected(): {}".format(wlan.isconnected()));      # check if the station is connected to an AP
print()
client_id = ubinascii.hexlify(machine.unique_id())
print("client_id: {}".format(client_id))
print("Connected to: {}".format(SSID))
print("config('mac'): {}".format(ubinascii.hexlify(wlan.config('mac'))))
print("ifconfig(): {}".format(wlan.ifconfig()))
print()














###################################################################################################

##### Socket (SW)
###
def socket_show():
    addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)
    addr = addr_info[0][-1]
    s = socket.socket()
    s.connect(addr)
    
    while True:
        data = s.recv(500)
        print(str(data, 'utf8'), end='')


#socket_show()














########################################################################################

##### RTC + NTP
#
print()
rtc = machine.RTC()             # Init RTC
print(rtc.datetime())
try:
    import ntptime
    ntptime.settime()
except:
    print("NTP time FAILED")
print(rtc.datetime())

status = "{0}-{1}-{2} {4}:{5}:{6}  _: {3}  _: {7}".format(*rtc.datetime())
print(status)
print()











#####################################################################################

#### GET request
#
def http_get(url):
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


##############################################################################################

#### ThingSpeak Config
#
API_KEY = '<API_WRITE_KEY>'        # ThingSpeak Channel API_WRITE_KEY
# esp32_tc, esp32_hs, status (DataTime)
# https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&status={}

url = "https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&status={}".format(API_KEY, esp32_tc, esp32_hs, status)
http_get(url)                      # Publish data














#
