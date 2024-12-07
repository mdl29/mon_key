import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ssid ='SALLE_ADO'
password ='plcbAT2023'
wlan.connect(ssid, password)

from microdot import Microdot

app = Microdot()

@app.route('/')
async def index(request):
    return 'kayooouuu'

app.run(host="0.0.0.0", port=5000)