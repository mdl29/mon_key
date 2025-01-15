import socketpool
import wifi
from adafruit_httpserver import Server, Request, Response

import usb_hid
from adafruit_hid.keyboard import Keyboard

from layouts.keyboard_layout_win_fr import KeyboardLayout as LayoutFR
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as LayoutUS

kbd = Keyboard(usb_hid.devices)
layouts = {
    "fr": LayoutFR(kbd),
    "us": LayoutUS(kbd)
}
layout = layouts["fr"]

ssid =''
password =''
print(f"Connecting to {ssid}...")
wifi.radio.connect(ssid, password)
print(f"Connected to {ssid}")

pool = socketpool.SocketPool(wifi.radio)

server = Server(pool, "/static", debug=True)

@server.route("/")
def base(request: Request):
    return Response(request, "Hello World!")

@server.route("/api/write", ['POST', 'GET'])
def typing(request: Request):
    if request.method == 'GET':
        layout.write("MDL")
    elif request.method == 'POST':
        data = request.json()
        lyt = layouts.get(data.get("layout", "fr").lower(), None)
        if lyt == None:
            return Response(request, f"invalid layout '{data.get('layout')}'")
        if "message" in data.keys():
            lyt.write(data["message"])
        else:
            return Response(request, "'message' not found")
    
    return Response(request, "done")

server.serve_forever(str(wifi.radio.ipv4_address))