#################################
#
#  Adafruit Feather M4 Express
#  https://www.adafruit.com/product/3857
#  Adafruit MPRLS Ported Pressure Sensor Breakout
#  https://www.adafruit.com/product/3965
#
#################################

import time
import board, busio
import adafruit_mprls
import array

from morseMaps import groups

#Modified this to support boards with Neopixels (like the Feathers) or Dotstars (like the Trinket/ItsyBitsy)
#Don't mess with the next few lines
if hasattr(board, 'NEOPIXEL'):
    import neopixel
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.05, auto_write=False)
elif hasattr(board, 'APA102_SCK'):
    import adafruit_bus_device
    import adafruit_dotstar
    pixels = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.9)

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

#################################
#Constants for Jim to Edit Easily
#################################

#These two are how hard you have to sip (LOW) or puff (HIGH) in Pascals
THRESH_LOW    = 5 # delta in hPa
THRESH_HIGH   = 5 # delta in hPa

#This adds a delay between sip & puffs in case it is bouncing
#Keep this low unless you are seeing false triggers
DEBOUNCE = 0.001

#how long to wait on idle before sending the code
acceptDelay = .25

#how many times to measure before we average
#INCREASE this to smooth things out and remove bounciness
#DECREATE this if you are missing sips/puffs
POINTS_TO_AVERAGE = 8

#Modifier keys - these will modify the next key sent
#Eventually hold/release will be implemented as well
modifier_keys = [Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.LEFT_SHIFT, Keycode.LEFT_GUI, Keycode.RIGHT_CONTROL, Keycode.RIGHT_ALT, Keycode.RIGHT_SHIFT, Keycode.RIGHT_GUI]
active_modifiers = []

#Mouse Speeds
mouse_normal=4
mouse_slow=1
mouse_fast=8
#start in normal speed
currentSpeed=mouse_normal
#This is convert CP movement to what Jim's used to on the Adapt2U
mouseSpeedFactor = 3
# Mouse Repeat Delay (milliseconds between movments when repeating - lower is faster)
mouseRepeatDelay=100

#we have two groups (0 and 1) - we start in group 0
#changeGroup() ("group 1" in the config) can switch between them
codes = groups[0]


i2c = busio.I2C(board.SCL, board.SDA)
mpr = adafruit_mprls.MPRLS(i2c)

pixels[0] = (0,0,0)
pixels.show()

time.sleep(1)
pixels[0] = (255,0,255)
pixels.show()
############################################
####Nothing else to tweak - feel free to recode it if you want :-)
############################################
keyboard = Keyboard()
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

mouse = Mouse()

groupColors = {}
groupColors[0] = (0,255,0)
groupColors[1] = (255,255,0)
groupColors[2] = (255,0,255)

BASELINE = 0

# a DIT is a DOT, a DAH is a DASH
DIT = 0
DAH = 1
IDLE = 2

colors = {}
colors[DIT] = (255,0,0)
colors[DAH] = (0,0,255)
colors[IDLE] = groupColors[0]


class RollingAverage:
    def __init__(self, size):
        self.size=size
        self.buffer = array.array('d')
        for i in range(size):
            self.buffer.append(0.0)
        self.pos = 0
    def addValue(self,val):
        self.buffer[self.pos] = val
        self.pos = (self.pos + 1) % self.size
    def average(self):
        return (sum(self.buffer) / self.size)

def pressure_sensor_init(count=10, delay=0.1):
    reading = 0
    for _ in range(count):
        reading += mpr.pressure
        time.sleep(delay)
    reading /= count
    return reading, reading - THRESH_LOW, reading + THRESH_HIGH

def sendString(s):
    for letter in s:
        keys = keyboard_layout.keycodes(letter)
        for mod in active_modifiers:
            keyboard.press(mod)
        for k in keys:
            keyboard.press(k)
        keyboard.release_all()
    active_modifiers.clear() #will need to obey hold/release later

def changeGroup(groupString):
    global codes
    (cmd, groupNum) = groupString.split()
    codes = groups[int(groupNum)]
    colors[IDLE] = groupColors[int(groupNum)]

lastMouseMove = (0,0,0)
def moveMouse(moveString):
    global lastMouseMove
    (cmd, x, y, wheel) = moveString.split()
    x=int(x)*currentSpeed*mouseSpeedFactor
    y=int(y)*currentSpeed*mouseSpeedFactor
    wheel=int(wheel)*currentSpeed*mouseSpeedFactor
    mouse.move(x, y, wheel)
    lastMouseMove=(x,y,wheel)
    print(lastMouseMove)


def mouseClick(clickString):
    (cmd, button, countString) = clickString.split()
    buttonList = []
    if (button.lower() == "left"):
        buttonNum = Mouse.LEFT_BUTTON
    elif (button.lower() == "right"):
        buttonNum = Mouse.RIGHT_BUTTON
    elif (button.lower() == "middle"):
        buttonNum = Mouse.MIDDLE_BUTTON
    count = int(countString)
    while(count > 0):
        mouse.click(buttonNum)
        count = count - 1

nextRptTime = 0
mouseRepeating = False
def mouseRepeat():
    global nextRptTime
    global mouseRepeating
    #if the last move was not a move, don't repeat it
    if (lastMouseMove[0] == 0 and lastMouseMove[1] == 0 and lastMouseMove[2] == 0):
        stopMouseRepeat()
        return
    startTime = time.monotonic()
    if (startTime > nextRptTime):
        nextRptTime = startTime + (mouseRepeatDelay/1000)
        mouse.move(lastMouseMove[0], lastMouseMove[1], lastMouseMove[2])

def startMouseRepeat():
    global lastMouseMove
    global nextRptTime
    global mouseRepeating
    #if the last move was not a move, don't repeat it
    if (lastMouseMove[0] == 0 and lastMouseMove[1] == 0 and lastMouseMove[2] == 0):
        stopMouseRepeat()
        return
    mouseRepeating=True
    nextRptTime = 0 #always repeat once
    mouseRepeat()

def stopMouseRepeat():
    global lastMouseMove
    global nextRptTime
    global mouseRepeating
    lastMouseMove=(0,0,0)
    nextRptTime = 0
    mouseRepeating = False


def sendCode(pendingChar, numShifts):
    global currentSpeed
    #lookup pendingChar in the right table - we need 7 tables
    #one for each length of numShifts
    if (numShifts <= len(codes)):
        if (pendingChar in codes[numShifts]):
            result = codes[numShifts][pendingChar]
            print(result, end='')
            if isinstance(result, str):  # If it's a string...
                if result.startswith("mmove"):
                    moveMouse(result)
                elif result.startswith("mrepeat"):
                    if (mouseRepeating):
                        stopMouseRepeat()
                        return
                    else:
                        startMouseRepeat()
                elif result.startswith("mslow"):
                    if (currentSpeed == mouse_slow):
                        currentSpeed = mouse_normal
                    else:
                        currentSpeed = mouse_slow
                elif result.startswith("mfast"):
                    if (currentSpeed == mouse_fast):
                        currentSpeed = mouse_normal
                    else:
                        currentSpeed = mouse_fast
                elif result.startswith("mclick"):
                    mouseClick(result)
                elif result.startswith("group"):
                    changeGroup(result)
                else:
                    sendString(result) #will send active_modifiers if set
            elif (type(result) == tuple):
                keyboard.press(*result)
                keyboard.release_all()
            else:  # If it's not a string...its a keycode
            #Before we press it, we need to see if it's a modifier
                if (result in modifier_keys):
                    print("Modifier Pressed: ", result)
                    if (not (result in active_modifiers)):
                        active_modifiers.append(result)
                else:
                    keyboard.press(result)  # "Press"...
                    keyboard.release_all()  # ..."Release"
        else:
            print(".", end='')
    else:
        print("X", end='')
    return None #do this later


baseline, sip_threshold , puff_threshold = pressure_sensor_init()


#We keey the code we're building here in binary shifted bits
pendingChar = 0

#How many shifts we've done (means how many dits or dahs tracked so far (0-7)
numShifts = 0
maxShifts = 8
#When we last had a shift from DIT/DAH/IDLE - needed to know when to send code
lastTransitionAt = 0

#State of the sensor
lastState = IDLE

lastPressure = baseline

avgPressure = RollingAverage(POINTS_TO_AVERAGE)
avgDiff = RollingAverage(POINTS_TO_AVERAGE)

while True:
    # driver checks conversion ready status, so OK do run this as fast as needed
    pressure = mpr.pressure
    #probably don't need this but I don't trust my Python scoping rules
    newState = lastState

    #We might want to optimize this to only call monotonic() when needed
    readAt = time.monotonic()

    # PUFF = DIT
    if pressure > puff_threshold:
        newState = DAH
    # SIP = DAH
    elif pressure < sip_threshold:
        newState = DIT
    else:
        newState = IDLE

    relPressure = (pressure - baseline)
    pressChange = (pressure - lastPressure)
    avgPressure.addValue(relPressure)
    avgDiff.addValue(pressChange)
#    print((relPressure, pressChange))#, avgPressure.average(), avgDiff.average()))
    lastPressure = pressure
#   time.sleep(.01)
    #Something changed - we'll update the char on release (until told otherwise)
    if (newState != lastState):
        lastTransitionAt = readAt
        if (mouseRepeating):
            stopMouseRepeat()
            newState = IDLE
            time.sleep(.25)
        elif (newState == IDLE):
            #shift in a 0 for DIT and 1 for DAH
            pendingChar = (pendingChar << 1) | lastState
            numShifts = numShifts + 1
        lastState = newState
#        print("New State: {}".format(newState))
    #Here, nothing has changed... but we need to know whether to process the code
    elif(lastState == IDLE and numShifts > 0 and (readAt - lastTransitionAt) > acceptDelay):
        sendCode(pendingChar, numShifts)
        pendingChar = 0
        numShifts = 0
        lastTransitionAt = readAt
    #Here we're not doing anything unless we need to send a repeat code
    else:
        if (mouseRepeating):
            mouseRepeat()
#    print(lastState)
    pixels[0] = colors[lastState]
    pixels.show()