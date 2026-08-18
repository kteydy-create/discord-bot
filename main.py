import os
import asyncio
import threading
from flask import Flask
import discord
from discord.ext import commands
import yt_dlp
import imageio_ffmpeg

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

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

@bot.event
async def on_ready():
    print(f'บอท {bot.user} พร้อมใช้งานแล้ว!')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
            await ctx.send(f'เข้าห้อง {channel.name} เรียบร้อยแล้ว!')
        else:
            await ctx.voice_client.move_to(channel)
    else:
        await ctx.send('คุณต้องเข้าห้องเสียงก่อนพิมพ์คำสั่งนะครับ')

@bot.command()
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        await ctx.send('คุณต้องเข้าห้องเสียงก่อนสั่งเล่นเพลงนะครับ!')
        return

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()

    async with ctx.typing():
        if not (search.startswith('http://') or search.startswith('https://')):
            search_query = f"ytsearch:{search}"
        else:
            search_query = search

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(search_query, download=False))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url']
        title = data.get('title', 'เพลง')

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        ffmpeg_executable = imageio_ffmpeg.get_ffmpeg_exe()

        source = discord.FFmpegPCMAudio(filename, executable=ffmpeg_executable, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)

        await ctx.send(f'🎵 กำลังเล่น: **{title}**')

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('หยุดเล่นเพลงแล้วครับ')
    else:
        await ctx.send('ไม่ได้กำลังเล่นเพลงอยู่ครับ')

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
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

@bot.event
async def on_ready():
    print(f'บอท {bot.user} พร้อมใช้งานแล้ว!')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
            await ctx.send(f'เข้าห้อง {channel.name} เรียบร้อยแล้ว!')
        else:
            await ctx.voice_client.move_to(channel)
    else:
        await ctx.send('คุณต้องเข้าห้องเสียงก่อนพิมพ์คำสั่งนะครับ')

@bot.command()
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        await ctx.send('คุณต้องเข้าห้องเสียงก่อนสั่งเล่นเพลงนะครับ!')
        return

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()

    async with ctx.typing():
        if not (search.startswith('http://') or search.startswith('https://')):
            search_query = f"ytsearch:{search}"
        else:
            search_query = search

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(search_query, download=False))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url']
        title = data.get('title', 'เพลง')

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        # ดึง Path ของ FFmpeg executable จาก imageio-ffmpeg
        ffmpeg_executable = imageio_ffmpeg.get_ffmpeg_exe()

        source = discord.FFmpegPCMAudio(filename, executable=ffmpeg_executable, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)

        await ctx.send(f'🎵 กำลังเล่น: **{title}**')

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('หยุดเล่นเพลงแล้วครับ')
    else:
        await ctx.send('ไม่ได้กำลังเล่นเพลงอยู่ครับ')

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
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

@bot.event
async def on_ready():
    print(f'บอท {bot.user} พร้อมใช้งานแล้ว!')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
            await ctx.send(f'เข้าห้อง {channel.name} เรียบร้อยแล้ว!')
        else:
            await ctx.voice_client.move_to(channel)
    else:
        await ctx.send('คุณต้องเข้าห้องเสียงก่อนพิมพ์คำสั่งนะครับ')

@bot.command()
async def play(ctx, *, search: str):
    if not ctx.author.voice:
        await ctx.send('คุณต้องเข้าห้องเสียงก่อนสั่งเล่นเพลงนะครับ!')
        return

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()

    async with ctx.typing():
        # ถ้าไม่ใช่ลิงก์ ให้ค้นหาจากชื่อเพลงบน YouTube
        if not (search.startswith('http://') or search.startswith('https://')):
            search_query = f"ytsearch:{search}"
        else:
            search_query = search

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(search_query, download=False))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url']
        title = data.get('title', 'เพลง')

        # ถ้าบอทกำลังเล่นเพลงอยู่ให้หยุดก่อนเล่นเพลงใหม่
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        source = discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)

        await ctx.send(f'🎵 กำลังเล่น: **{title}**')

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('หยุดเล่นเพลงแล้วครับ')
    else:
        await ctx.send('ไม่ได้กำลังเล่นเพลงอยู่ครับ')

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
