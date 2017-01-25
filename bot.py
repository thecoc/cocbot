from discord.ext import commands
from cogs.utils import utils
import discord.utils as du
import discord
import json
import threading
import os
import sys

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
    
@bot.command()
async def logout():
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
