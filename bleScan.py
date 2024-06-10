import aioble
import time
import windowfunctions

async def ScanDevices():
    print('Begining scan')
    async with aioble.scan(duration_ms=0,interval_us=30000, window_us=30000, active=True) as scanner:
            async for result in scanner:
                if (result.name() == 'LPWBVFQI'):
                     print(result.rssi)


#enter bluetooth id here. 
TARGET_DEVICE_NAME = ''
RSSI_THRESHOLD = -95
# Weaker signal when closed as the signal needs to go through a window
RSSI_CLOSED_OUTSIDE_THRESHOLD = -95
RSSI_CLOSED_INSIDE_THRESHOLD = -75
# Stronger signal as window will be open 
RSSI_OPENED_THRESHOLD = -75
DURATION = 10
TRACKER_LOCATION = 'INSIDE'

async def monitor_signal_strength():
    print('start monitoring')
    start_time = None
    not_detected_time = None
    out_of_range_time = None
    devicedetected = False

    async with aioble.scan(duration_ms=0,interval_us=30000, window_us=30000, active=True) as scanner:
            async for result in scanner:
                 if (result.name() == TARGET_DEVICE_NAME):
                    rssi = result.rssi
                    #print(f"Device: {result.name()}, Signal strength (RSSI): {rssi} dBm")
                    
                    thresholdVal = RSSI_CLOSED_OUTSIDE_THRESHOLD 

                    if rssi >= thresholdVal and windowfunctions.window_state == 'closed':
                        devicedetected = True
                        out_of_range_time = None
                        not_detected_time = None
                        
                        if start_time is None:
                            # Start the timer if this is the first time RSSI is above the threshold
                            start_time = time.time()
                        else:
                            # Check if the duration has passed
                            if (time.time() - start_time) >= DURATION:
                                if windowfunctions.window_state == 'closed':
                                    print(f"Device has maintained the RSSI threshold for {DURATION} seconds.")
                                    await windowfunctions.runCommand('open', 15000)
                            
                    else:
                        # Reset the timer if the RSSI goes below the threshold
                        start_time = None
                        not_detected_time = None
                        
                        if (windowfunctions.window_state == 'open' and rssi <= RSSI_OPENED_THRESHOLD ):
                            if out_of_range_time == None:
                                out_of_range_time = time.time()

                            if (time.time() - out_of_range_time >= DURATION):
                                print(f'device is out of range threshold for more than {DURATION} seconds')
                                print('Issuing close command.')
                                await windowfunctions.runCommand('closeOverrideBeam', 15000)
                                out_of_range_time = None         

                 else:
                      # Device can no longer be found, wait for 20 seconds and issue close command if window is open
                      if devicedetected:
                        # only run if the device was detected

                        if not_detected_time is None:
                            not_detected_time = time.time()
                        
                        if windowfunctions.window_state == 'open':
                            #print(f"Not found for {time.time() - not_detected_time} seconds")

                            if (time.time() - not_detected_time) >= DURATION:
                                print("device not found for longer than 20 secs")
                                if windowfunctions.window_state == 'open':
                                    print(f"Device is out of range for more than {DURATION} seconds. Closing Window.")
                                    await windowfunctions.runCommand('closeOverrideBeam', 15000)
                                    devicedetected = False
                
                 #await asyncio.sleep(1)

