from lib.microdot import Microdot
import controllerFunctions

app = Microdot()

@app.route('/open')
async def openFull(request):
    await controllerFunctions.runCommand('open',15000)
    return 'Opening fully'

@app.route('/open/<int:timeMs>')
async def open(request, timeMs):    
    if timeMs is None:
        timeMs = 15000
    
    await controllerFunctions.runCommand('open',timeMs)
    return 'Opening'

@app.route('/close')
async def closeFull(request):
    await controllerFunctions.runCommand('close', 15000)
    return 'Closing fully'

@app.route('/close/<int:timeMs>')
async def close(request, timeMs):
    await controllerFunctions.runCommand('close',timeMs)
    return 'Closing'

@app.route('/cancel')
async def cancel(request):
    await controllerFunctions.runCommand('cancel', None)    
    return 'Cancelled'

@app.route('/closeOverrideBeam')
async def closeOverrideBeam(request):
    await controllerFunctions.runCommand('closeOverrideBeam', 15000)
    return 'Closing. Ignoring the beam sensor'

@app.route('/status')
async def status(request):
    return 'Status is - ' + controllerFunctions.state

async def runMicrodotServer():
    print("running microdot server")
    try:
        app.run(port=80)
    except:
        app.shutdown()