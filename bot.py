from discord.ext import commands
from cogs.utils import utils, checks, crypto
import discord
import os
import sys

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
 
@checks.is_owner_or_bot_admin() 
@bot.command()
async def zlogout():
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
            msg = ('wow, I didn\'t expect *that* to happen..'
                + 'But don\'t worry. I just bitched to my people about it '
                + '[ ' + str(error.original) + ' ]')
            msg = utils.mention(ctx, msg)
            channel = ctx.message.channel
            await utils.report_traceback(error, ctx)
    await bot.send_message(channel, msg)
        
@bot.event
async def on_message(msg):
    if msg.author.bot:
       return
    await bot.process_commands(msg)
        
if __name__ == '__main__':

    config_file = 'config.json'
    if not os.path.isfile(config_file):
        key = os.getenv('CRYPTOKEY', '').encode('utf-8')
        crypto.file_decrypt(key, config_file)
    bot.config = utils.load_json(config_file)
    
    if any('debug' in arg.lower() for arg in sys.argv):
        try:
            # maa env var on his machine
            token = os.getenv('TOKEN_NAME')
        except Exception:
            # my token in config.json
            token = bot.config['debug']
    else:
        token = bot.config['token']  
    
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(
                extension, type(e).__name__, e))

    bot.run(token)
