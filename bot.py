from discord.ext import commands
from cogs.utils import utils
import discord
import json

bot_channel='234066444449480704'

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
    if isinstance(error, commands.CommandOnCooldown):
        #error.retry_after => time left
        await utils.whisper(bot, ctx, error)
    elif isinstance(error, commands.BadArgument):
        await utils.reply(bot, ctx, error)
    else:
        channel = discord.Object(id=bot_channel)
        await bot.send_message(channel, error)
            
@bot.event
async def on_message(msg):
    if msg.author.bot:
       return
    await bot.process_commands(msg)

def load_file(file):
    with open(file) as f:
        return json.load(f)
        
if __name__ == '__main__':
    
    bot.server_info = load_file('server.json')
    token = bot.server_info['credentials']['token']
    
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(
                extension, type(e).__name__, e))
            
    bot.run(token)