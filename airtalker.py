import time
import board, busio
import adafruit_mprls
import array
from morseMaps import codes

i2c = busio.I2C(board.SCL, board.SDA)
mpr = adafruit_mprls.MPRLS(i2c)

BASELINE = 0
THRESH_LOW    = 10 # delta in hPa
THRESH_HIGH   = 10 # delta in hPa
DEBOUNCE = 0.005

DIT = 0
DAH = 1
IDLE = 2

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

def sendCode(pendingChar, numShifts):
    #lookup pendingChar in the right table - we need 7 tables
    #one for each length of numShifts
    if (pendingChar in codes[numShifts]):
        print(codes[numShifts][pendingChar], end='')
    else:
        print(".", end='')
    return None #do this later


baseline, sip_threshold , puff_threshold = pressure_sensor_init()

#must be configurable - how long to wait on idle before sending the code
acceptDelay = .50

#We keey the code we're building here in binary shifted bits
pendingChar = 0

#How many shifts we've done (means how many dits or dahs tracked so far (0-7)
numShifts = 0

#When we last had a shift from DIT/DAH/IDLE - needed to know when to send code
lastTransitionAt = 0

#State of the sensor
lastState = IDLE

lastPressure = baseline

avgPressure = RollingAverage(10)
avgDiff = RollingAverage(10)

while True:
    # driver checks conversion ready status, so OK do run this as fast as needed
    pressure = mpr.pressure
    #probably don't need this but I don't trust my Python scoping rules
    newState = lastState

    #We might want to optimize this to only call monotonic() when needed
    readAt = time.monotonic()
    
    # PUFF = dit
    if pressure > puff_threshold:
        newState = DIT
    # SIP = dah
    elif pressure < sip_threshold:
        newState = DAH
    else:
        newState = IDLE
        
    relPressure = (pressure - baseline)
    pressChange = (pressure - lastPressure)
    avgPressure.addValue(relPressure)
    avgDiff.addValue(pressChange)
    #print((relPressure, pressChange))#, avgPressure.average(), avgDiff.average()))
    lastPressure = pressure
    time.sleep(.05)
    #Something changed - we'll update the char on release (until told otherwise)
    if (newState != lastState):
        lastTransitionAt = readAt
        if (newState == IDLE):
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