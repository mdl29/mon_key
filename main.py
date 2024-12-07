from microdot import Microdot
from pyb import UART
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ssid ='SALLE_ADO'
password ='plcbAT2023'
wlan.connect(ssid, password)

app = Microdot()

def render(content):
    return '<meta charset="utf-8">{0}'.format(content), 200, {"Content-Type":"text/html"} 

@app.route('/')
async def index(request):
    return render('<h1>🪨KAYOOOUUU🪨</h1>')

@app.route('/api/kayou')
async def kayou(request):
    uart = UART(1, 9600)
    uart.write('kayou')
    return '', 200

port = 5000
print("Starting microdot on port {0}".format(port))
app.run(host="0.0.0.0", port=port)