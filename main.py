import discord
import asyncio
import logging
import json



discord.utils.setup_logging()
logger = logging.getLogger(__name__)

class Client(discord.Client):
    def __init__(self, channel_id, **kwargs):
        super().__init__(**kwargs)
        self.channel_id = channel_id

    async def on_ready(self):
        print(f"{self.user.name} is ready")

    async def setup_hook(self):
        self.loop.create_task(self.typing_loop())

    async def typing_loop(self):
        await self.wait_until_ready()
        channel = self.get_channel(self.channel_id)

        while not self.is_closed():
            async with channel.typing():
                await asyncio.sleep(1)

async def main():
    with open("config.json", "r") as file:
        data = json.load(file)

    tasks = []

    for token in data["tokens"]: 
        client = Client(channel_id=data["channel_id"])
    
        tasks.append(asyncio.create_task(client.start(token)))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
