from discord.ext import commands
from cogs.utils import utils
import discord.utils as du
import discord
import json
import threading
import os
import sys

import crypto

import logging
logging.basicConfig(level=logging.INFO)

extensions = [ 'cogs.games',
               'cogs.media',
               'cogs.roles',
               'cogs.badwords' ]

prefix = [ '!' ]
bot = commands.Bot(command_prefix=prefix, pm_help=True)

@bot.event
async def on_ready():
    print('Logged in as:')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('------')

@bot.command()
async def logout():
    if os.getenv('IGNORELOGOUT', False):
        return

    print('logout requested: shutting down...')
    await bot.logout()

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        msg = 'How dare you ask me for that. I\'m not that kind of bot!'
        msg = utils.mention(ctx, msg)
        channel = ctx.message.channel
    else:
        try:
            response = ctx.cog.prepare_error(error, ctx)
            msg = response['msg']
            channel = response.get('channel', ctx.message.channel)
        #except (NameError, TypeError, ValueError, AttributeError):
        except Exception:
            msg = 'Well.. something went wrong. '
            msg += 'Just so we\'re clear, it wasn\'t my fault. '
            msg += '[ ' + str(error.original) + ' ]'
            msg = utils.mention(ctx, msg)
            channel = ctx.message.channel

            await utils.report_traceback(error, ctx)

    await bot.send_message(channel, msg)

@bot.event
async def on_message(msg):
    if msg.author.bot:
       return
    await bot.process_commands(msg)

def load_json(file):
    with open(file) as f:
        return json.load(f)

def assert_settings(cryptokey):
    if not os.path.isfile('config.json'):
        if os.path.isfile('config.json.aes'):
            crypto.file_decrypt(cryptokey, 'config.json')
        else:
            raise Exception('missing: config.json')

def select_token(config):
    name = os.getenv('TOKEN_NAME', 'dbg')
    token = config['token'][name]

    if not token:
        raise Exception('TOKEN_NAME(%s) not found in config.' % name)

    return token

def main():

    cryptokey = os.getenv('CRYPTOKEY', '').encode('utf-8')

    # handle differnt modes and cmd args
    if len(sys.argv) == 3:
        if sys.argv[1] == 'enc':
            crypto.file_encrypt(cryptokey, sys.argv[2])
            return
        if sys.argv[1] == 'dec':
            crypto.file_decrypt(cryptokey, sys.argv[2])
            return

    assert_settings(cryptokey)

    bot.config = load_json('config.json')

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(
                extension, type(e).__name__, e))

    bot.run(select_token(bot.config))

if __name__ == '__main__':
    main()
