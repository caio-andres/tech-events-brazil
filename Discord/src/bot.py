import os
import discord
import asyncio
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DB_JSON_URL = os.getenv("DB_JSON_URL")
NOTIFY_CHANNEL_ID = os.getenv("NOTIFY_CHANNEL_ID")


class MyClient(discord.Client):
    async def setup_hook(self):
        self.webhook_task = asyncio.create_task(self.start_webhook())

    async def on_ready(self):
        print(f"Logado como {self.user}")

    async def start_webhook(self):
        app = web.Application()
        app.add_routes([web.post("/notify_new_events", self.handle_new_events)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8000)
        await site.start()
        print("Webhook HTTP rodando na porta 8000...")

    async def handle_new_events(self, request):
        data = await request.json()
        eventos = data.get("novos_eventos", [])
        channel_id = int(data.get("channel_id", NOTIFY_CHANNEL_ID))
        channel = self.get_channel(channel_id)
        if not channel:
            print(f"Canal {channel_id} não encontrado!")
            return web.json_response({"error": "channel not found"}, status=404)

        if not eventos:
            await channel.send("Nenhum evento novo detectado hoje.")
        else:
            resposta = "**Novos eventos adicionados hoje:**\n"
            for e in eventos:
                nome = e.get("nome", "sem nome")
                url_evt = e.get("url", "")
                cidade = e.get("cidade", "")
                uf = e.get("uf", "")
                tipo = e.get("tipo", "")
                resposta += f"- [{nome}]({url_evt}) — {cidade}/{uf} | {tipo}\n"
            await channel.send(resposta)

        return web.json_response({"status": "ok"})


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
