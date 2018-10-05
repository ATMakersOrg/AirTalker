import time
import board, busio
import adafruit_mprls

i2c = busio.I2C(board.SCL, board.SDA)
mpr = adafruit_mprls.MPRLS(i2c)

THRESH_LOW    = 10 # delta in hPa
THRESH_HIGH   = 10 # delta in hPa
DEBOUNCE = 0.005

DIT = 0
DAH = 1
IDLE = 2


def pressure_sensor_init(count=10, delay=0.1):
    reading = 0
    for _ in range(count):
        reading += mpr.pressure
        time.sleep(delay)
    reading /= count
    return reading - THRESH_LOW, reading + THRESH_HIGH

def sendCode(pendingChar, numShifts):
    #lookup pendingChar in the right table - we need 7 tables
    #one for each length of numShifts
    print(bin(pendingChar))
    return None #do this later


sip_threshold , puff_threshold = pressure_sensor_init()

#must be configurable - how long to wait on idle before sending the code
acceptDelay = .200

#We keey the code we're building here in binary shifted bits
pendingChar = 0

#How many shifts we've done (means how many dits or dahs tracked so far (0-7)
numShifts = 0

#When we last had a shift from DIT/DAH/IDLE - needed to know when to send code
lastTransitionAt = 0

#State of the sensor
lastState = IDLE


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
    if pressure < sip_threshold:
        newState = DAH

    #Something changed - we'll update the char on release (until told otherwise)
    if (newState != lastState):
        lastTransitionAt = readAt
        if (newState == IDLE):
            #shift in a 0 for DIT and 1 for DAH
            pendingChar = (pendingChar << lastState) | lastState
            numShifts = numShifts + 1
        else:
            lastState = newState
    #Here, nothing has changed... but we need to know whether to process the code
    elif(lastState == IDLE and numShifts > 0 and (readAt - lastTransitionAt) > acceptDelay):
        sendCode(pendingChar, numShifts)
        pendingChar = 0
        numShifts = 0

