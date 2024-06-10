from machine import Pin
import uasyncio

beam_monitor = None
current_task = None
state = 'closed'

def setRelays(relay1State, relay2State):
    # these are the pins on the gpio board
    gpioRelay1 = 0
    gpioRelay2 = 2
    relay1 = Pin(gpioRelay1,Pin.OUT)
    relay2 = Pin(gpioRelay2,Pin.OUT)

    if relay1State == True:
        relay1.high()
    else: 
        relay1.low()

    if relay2State == True:
        relay2.high()
    else: 
        relay2.low()

async def executeCommand(commandType, timeMs):
    print("runCommand called - ",commandType)
    global current_Task
    global state

    if commandType == 'open':
        print('opening')
        state = 'opening'
        setRelays(True, False)
        await uasyncio.sleep_ms(timeMs)
        setRelays(False, False)
        print('opened')
        state = 'open'
    elif commandType == 'close':
        print('closing')
        state = 'closing'
        setRelays(False, True)
        await uasyncio.sleep_ms(timeMs)
        setRelays(False, False)
        
        global beam_monitor
        if beam_monitor:
            beam_monitor.cancel()
        
        print('closed')
        state = 'closed'       
    elif commandType == 'cancel':
        setRelays(False, False)

        print('cancelled')
        state = 'cancelled'

async def monitorBeam(safteyOpen):
    beam = Pin(22, Pin.IN, Pin.PULL_UP)
    
    while True:
        if beam.value() == 1:
            print('beam ok')
        else:
            print('beam broken')

            if (safteyOpen == True):
                # Cancel any running function and reopen immediately
                await runCommand('cancel', None)
                await runCommand('open', 15000)
                break
        
        await uasyncio.sleep_ms(50)

async def runCommand(command, timeMs):
    global current_task
    global beam_monitor
    
    # cancel any current running tasks and send a cancel command to the relays 
    # as a safety precaution
    if (current_task):
        current_task.cancel()
        await executeCommand('cancel', None)

    if command == 'open': 
        current_task = uasyncio.create_task(executeCommand('open', timeMs))
    elif command == 'close':
        beam_monitor = uasyncio.create_task(monitorBeam(True))
        current_task = uasyncio.create_task(executeCommand('close', timeMs))
    elif command == 'closeOverrideBeam':
        current_task = uasyncio.create_task(executeCommand('close', timeMs))
    elif command == 'cancel':
        current_task = uasyncio.create_task(executeCommand('cancel', None)) 
