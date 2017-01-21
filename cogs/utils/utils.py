import requests
import random
import discord

async def reply(bot, ctx, msg):
    channel = ctx.message.channel
    response = ctx.message.author.mention + ', ' + msg
    await bot.send_message(channel, response)

async def say(bot, ctx, msg):
    await bot.send_message(ctx.message.channel, msg)

async def whisper(bot, ctx, msg):
    await bot.send_message(ctx.message.author, msg)
    
def lines_from_url(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.text.split('\r\n')
    
def random_line_from_source(source, fn):
    return random.choice(fn(source))
    
