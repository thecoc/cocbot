from discord.ext import commands
from functools import wraps
import requests
import random
import discord
import traceback

async def reply(ctx, msg):
    channel = ctx.message.channel
    response = ctx.message.author.mention + ', ' + msg
    await ctx.bot.send_message(channel, response)

async def say(ctx, msg):
    await ctx.bot.send_message(ctx.message.channel, msg)

async def whisper(ctx, msg):
    await ctx.bot.send_message(ctx.message.author, msg)
    
def lines_from_url(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.text.split('\r\n')
    
def random_line_from_source(source, fn):
    return random.choice(fn(source))
    
def mention(ctx, msg):
    return ctx.message.author.mention + ', ' + msg
    
async def report_traceback(error, ctx):
    event = '{0.timestamp}\n{1}\n'.format(ctx.message, error)
    event += '{0.author.mention}: {0.content}\n'.format(ctx.message)
    channels = ctx.message.server.channels
    log_channel = du.get(channels, name='bot-log')
    tb = traceback.format_exception(type(error), error, error.__traceback__)
    log_msg = event + '\n```\n' + ''.join(tb) + '\n```'
    await ctx.bot.send_message(log_channel, log_msg) 
    
    
