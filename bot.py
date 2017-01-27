from discord.ext import commands
from cogs.utils import utils, checks
from cryptography.fernet import Fernet
import discord
import json
import os

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
            msg = 'wow, I didn\'t expect *that* to happen..'
            msg += 'But don\'t worry. I just bitched to my people about it '
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

def read_bytes(file):
    with open(file, 'rb') as f:
        return f.read()
        
def recreate_json(file):
    key = os.getenv('FERNET_KEY')
    cipher_text = read_bytes('config.encrypted')
    cipher_suite = Fernet(key.encode('utf-8'))
    plain_text = cipher_suite.decrypt(cipher_text)
    with open(file, 'w') as f:
        f.write(plain_text.decode('utf-8'))
        
if __name__ == '__main__':

    config_file = 'config.json'
    if not os.path.isfile(config_file):
        recreate_json(config_file)
    bot.config = load_json(config_file)
    token = bot.config['token']
    
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(
                extension, type(e).__name__, e))

    bot.run(token)
