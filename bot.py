from discord.ext import commands
from cogs.utils import utils
import discord
import json
import threading
import os

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

@bot.event
async def on_command_error(error, ctx):
    import traceback
    import sys
    msg = str(error) + '\n'
    msg += ("".join(traceback.format_exception(None, error, error.__traceback__)))
    print(msg, file=sys.stderr)

    if isinstance(error, commands.CommandOnCooldown):
        #error.retry_after => time left
        await utils.whisper(bot, ctx, str(error))
    elif isinstance(error, commands.BadArgument):
        await utils.reply(bot, ctx, str(error))
    elif isinstance(error, commands.errors.CommandNotFound):
        await utils.reply(bot, ctx, str(error))
    else:
        channel = discord.Object(id=bot_channel)
        await bot.send_message(channel, msg)
        await utils.reply(bot, ctx, str(error))

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

if __name__ == '__main__':

    bot.server_info = load_file('server.json')
    token = bot.server_info['credentials']['token']
    port = os.getenv('NODE_PORT', 3000)

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(
                extension, type(e).__name__, e))

    start(port, token)

