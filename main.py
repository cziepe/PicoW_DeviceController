from wlan import connectToWLAN
from microdotFunctions import runMicrodotServer
from bleScan import monitor_signal_strength
import asyncio
import time

async def setupStartup():
    print("starting up services")
    taskWebServer = asyncio.create_task(runMicrodotServer())
    scanbluetooth = asyncio.create_task(monitor_signal_strength())
   
    await asyncio.gather(taskWebServer, scanbluetooth)
    #await asyncio.gather(scanbluetooth)

print('starting')

connected = connectToWLAN()
print ("connected is ", connected)

if (connected == True):
    asyncio.run(setupStartup())
    print("not connected")