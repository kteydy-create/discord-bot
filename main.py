import os
import threading
from flask import Flask
import discord
from discord.ext import commands

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'บอท {bot.user} พร้อมใช้งานแล้ว!')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'เข้าห้อง {channel.name} เรียบร้อยแล้ว!')
    else:
        await ctx.send('คุณต้องเข้าห้องเสียงก่อนพิมพ์คำสั่งนะครับ')

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('ออกจากห้องเสียงเรียบร้อย!')
    else:
        await ctx.send('บอทไม่ได้อยู่ในห้องเสียงครับ')

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot.run(os.getenv('TOKEN'))
        
