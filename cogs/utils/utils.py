from discord.ext import commands
import discord.utils as du
import requests
import random
import discord
import traceback
import argparse
import json

async def reply(ctx, msg):
    channel = ctx.message.channel
    response = ctx.message.author.mention + ', ' + msg
    await ctx.bot.send_message(channel, response)

async def say(ctx, msg):
    await ctx.bot.send_message(ctx.message.channel, msg)

async def whisper(ctx, msg):
    await ctx.bot.send_message(ctx.message.author, msg)
    
def mention(ctx, msg):
    return ctx.message.author.mention + ', ' + msg
    
async def report_traceback(error, ctx):
    msg = ctx.message
    event = (str(msg.timestamp) + '\n' 
          + 'FROM: ' + msg.author.mention + '\n'
          + 'CHANNEL: ' + str(msg.channel) + '\n'
          + 'ORIGINAL MESSAGE: ' + msg.content + '\n')
    channels = ctx.message.server.channels
    log_channel = du.get(channels, name='bot-log')
    tb = traceback.format_exception(type(error), error, error.__traceback__)
    log_msg = event + '\n' + ''.join(tb)
    print(log_msg)
    await ctx.bot.send_message(log_channel, log_msg)
    
def lines_from_url(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.text.split('\r\n')
    
def random_line_from_source(source, fn):
    return random.choice(fn(source))
    
def load_json(file):
    with open(file) as f:
        return json.load(f)

def read_bytes(file):
    with open(file, 'rb') as f:
        return f.read()




    
    
