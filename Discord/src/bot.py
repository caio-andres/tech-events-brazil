from configs import *
import discord


class MyClient(discord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("$hello bro"):
            await message.channel.send("sup!")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token=TOKEN)
