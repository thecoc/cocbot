from discord.ext import commands
from cogs.utils import utils
import discord.utils as du
import discord
import json
import threading
import os
import sys
import traceback

import crypto

# bot_channel='234066444449480704'
bot_channel='271117684395999243' # test.bot-log

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
 
async def report_traceback(error, ctx):
    channels = ctx.message.server.channels
    log_channel = du.get(channels, name='bot-log')
    log_msg = str(error) + '\n' + traceback.format_exc()
    await ctx.bot.send_message(log_channel, log_msg) 
    
@bot.event
async def on_command_error(error, ctx):
    # BUG: when prepare_error exists and doesn't handle error
    # empty msg
    if hasattr(ctx.cog, 'prepare_error'):
        response = ctx.cog.prepare_error(error, ctx)
        msg = response['msg']
        channel = response.get('channel', ctx.message.channel)
    elif isinstance(error, commands.CommandNotFound):
        msg = 'How dare you ask me for that. I\'m not that kind of bot!'
        msg = utils.mention(ctx, msg)
        channel = ctx.message.channel
    else:
        msg = 'Well.. something went wrong. '
        msg += 'Just so we\'re clear, it wasn\'t my fault. '
        msg += '[ ' + str(error.original) + ' ]'
        channel = ctx.message.channel
        
        channels = ctx.message.server.channels
        bot_channel = du.get(channels, name='bot-log')
        bot_msg = str(error) + '\n' + traceback.format_exc()
        await bot.send_msesage(bot_channel, bot_msg)
    
    await bot.send_message(channel, msg)
        
@bot.event
async def on_message(msg):
    if msg.author.bot:
       return
    await bot.process_commands(msg)

def load_file(file):
    with open(file) as f:
        return json.load(f)

def start(port, token):
    import web.server as ws

    if not os.getenv('WEBSERVER', False):
        # don't run as/with web server: bot only
        bot.run(token)
        return

    server_runner = threading.Thread(target=lambda: ws.run(port=port))
    server_runner.start()
    bot.run(token)
#     server_runner.join() - don't wait for server to stop if bot closes

def assert_settings(cryptokey):
    if not os.path.isfile('server.json'):
        if os.path.isfile('server.json.aes'):
            crypto.file_decrypt(cryptokey, 'server.json')
        else:
            raise Exception('missing: server.json')

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

    bot.server_info = load_file('server.json')
    token = bot.server_info['credentials']['token']
    port = os.getenv('PORT', 3000)

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(
                extension, type(e).__name__, e))

    token = 'MjczMTU1NTg2ODEwNTc2ODk2.C2fbfQ.2iIcxe7W1z1fh4Vl04kQNdooR1Q'
    #start(int(port), token)
    bot.run(token)

if __name__ == '__main__':
    main()
