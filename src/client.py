#!/usr/bin/env python3
import simplejson as json
import asyncio
import websockets
import urllib.request

delay = 60  # change as desired
_id = 0  # change as desired


async def client():
    uri = "ws://localhost:8080"  # change as needed
    while True:
        async with websockets.connect(uri) as websocket:
            payload = {
                "id": _id,
                "ip": urllib.request.urlopen("https://ident.me").read().decode("utf-8")
            }
            await websocket.send(json.dumps(payload))
            ret = await websocket.recv()
            if ret != "200 OK":
                print(f"New ID: {ret}")
        await asyncio.sleep(delay)


asyncio.get_event_loop().run_until_complete(client())
