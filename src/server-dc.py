# noinspection PyPackageRequirements
import discord
import simplejson as json
import asyncio

delay = 30


class Client(discord.Client):
    def __init__(self):
        super().__init__()
        # todo: add different db support
        self.cnf = json.load(open("server.json"))

    async def on_ready(self):
        print(f"Logged on as {self.user}")
        ch = self.get_channel(self.cnf["channel"])
        while True:
            tmp = json.load(open("server.json"))
            if tmp["ips"] != self.cnf["ips"]:
                await ch.send(str(tmp["ips"]))
                self.cnf = tmp
            await asyncio.sleep(delay)

    async def on_message(self, message):
        if message.content == "!ips":
            await message.channel.send(str(self.cnf["ips"]))


client = Client()
client.run(json.load(open("server.json"))["token"])
