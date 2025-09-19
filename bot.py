import os
import discord
import asyncio
from discord.ext import commands
from flask import Flask, request, jsonify
import threading
from dotenv import load_dotenv

# تحميل القيم من ملف .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
SECRET = os.getenv("SECRET_KEY", "antar_2003")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

app = Flask(__name__)

@app.route('/create_invite', methods=['POST'])
def create_invite():
    data = request.get_json()
    if not data or data.get("secret") != SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)

    invite = None
    if channel:
        invite = asyncio.run_coroutine_threadsafe(
            channel.create_invite(max_uses=1, unique=True),
            bot.loop
        ).result()

    if invite:
        return jsonify({"invite_url": str(invite)})
    return jsonify({"error": "Failed to create invite"}), 500

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print("🚀 Flask running")

bot.run(TOKEN)
