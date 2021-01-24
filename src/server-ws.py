#!/usr/bin/env python3
import sys
import simplejson as json
import websockets
import asyncio


def loading_json(file: str) -> dict:
    with open(file) as f:
        return json.load(f)


def writing_json(file: str, state: dict):
    with open(file, "w") as f:
        json.dump(state, f)


# FIXME: Duplicated code, find some way to not do this
_args = sys.argv
_cnf = {"location": _args[2]}
_f_map = {
    "json": [loading_json, writing_json]
}
_cnf["load"] = _f_map[_args[1]][0]
_cnf["write"] = _f_map[_args[1]][1]
_j_file = _cnf["load"](_cnf["location"])


async def server(websocket, path):
    args = sys.argv
    cnf = {"location": args[2]}
    f_map = {
        "json": [loading_json, writing_json]
    }
    cnf["load"] = f_map[args[1]][0]
    cnf["write"] = f_map[args[1]][1]
    j_file = cnf["load"](cnf["location"])
    async for message in websocket:
        req = json.loads(message)
        if 0 <= req["id"] < len(j_file["ips"]):
            j_file["ips"][req["id"]] = req["ip"]
        else:
            j_file["ips"].append(req["ip"])
            await websocket.send(str(len(j_file["ips"])-1))
        cnf["write"](cnf["location"], j_file)
        await websocket.send("200 OK")


# noinspection PyTypeChecker
serve = websockets.serve(server, _j_file["bind"], _j_file["port"])
asyncio.get_event_loop().run_until_complete(serve)
asyncio.get_event_loop().run_forever()
