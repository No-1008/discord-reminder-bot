import os
import discord
from discord.ext import commands
import asyncio
from flask import Flask
from threading import Thread

# --- Flask (keep alive for UptimeRobot) ---
app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Discord Bot settings ---
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ ログイン完了: {bot.user}")

@bot.command()
async def remind(ctx, time: int, *, message: str):
    """
    !remind <分> <メッセージ>
    指定した分数後にリマインドを送信します。
    例: !remind 10 会議の時間です
    """
    await ctx.send(f"⏰ {time}分後にリマインドします: {message}")
    await asyncio.sleep(time * 60)
    await ctx.send(f"🔔 リマインド: {message}")

# --- Run everything ---
keep_alive()
bot.run(TOKEN)
