import socketpool
import wifi
from asyncio import create_task, gather, run, sleep as async_sleep
from adafruit_httpserver import Server, Request, Response, Websocket

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse

from layouts.keyboard_layout_win_fr import KeyboardLayout as LayoutFR
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as LayoutUS

kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

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
websocket: Websocket = None

@server.route("/")
def base(request: Request):
    return Response(request, "Hello World!")

@server.route("/api/trackpad", ['GET'])
def trackpad(request: Request):
    global websocket

    if websocket is not None:
        websocket.close()  # Close any existing connection

    websocket = Websocket(request)

    return websocket

async def handle_websocket_requests():
    while True:
        if websocket is not None:
            if (data := websocket.receive(fail_silently=True)) is not None:
                dX,dY = data.split(";")
                dX,dY = int(dX)*-1, int(dY)*-1
                mouse.move(dX,dY)

        await async_sleep(0)
        
async def handle_http_requests():
    while True:
        server.poll()

        await async_sleep(0)

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

server.start(str(wifi.radio.ipv4_address))

async def main():
    await gather(
        create_task(handle_http_requests()),
        create_task(handle_websocket_requests()),
    )


run(main())