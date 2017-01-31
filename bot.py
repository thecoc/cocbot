from discord.ext import commands
from cogs.utils import utils, crypto
import discord.utils as du
import discord
import os
import sys
import random

import logging
logging.basicConfig(level=logging.INFO)

extensions = [ 'cogs.games',
               'cogs.media',
               'cogs.roles',
               'cogs.badwords',
               'cogs.admin' ]

prefix = [ '!' ]
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print('Logged in as:')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('------')
    

@bot.event
async def on_command_error(error, ctx):
    etype = type(error).__name__
    handler = ctx.command.name if ctx.command else 'global'
    is_template = bot.errors[handler].get('is_template', False)
    
    unknown_error = bot.errors['global']['unknown']
    error_choices = bot.errors[handler].get(etype, unknown_error)
    
    msg = random.choice(error_choices) 
    
    # no clue what happened, so report the traceback
    if msg in unknown_error:
        await utils.report_traceback(error, ctx)
    else:
        # extra processing from cog if needed
        if is_template:
            msg = ctx.cog.error(error, ctx, msg)
            
    msg = utils.mention(ctx, msg)
    await bot.send_message(ctx.message.channel, msg)

    
@bot.event
async def on_message(msg):
    if msg.author.bot:
       return
    await bot.process_commands(msg)


def select_token(config, token_name=None):
    name = token_name or os.getenv('TOKEN_NAME', 'dbg')
    token = config['token'][name]

    if not token:
        raise Exception('TOKEN_NAME(%s) not found in config.' % name)

    return token

    
def load_config(config_file):
    if not os.path.isfile(config_file):
        key = os.getenv('CRYPTOKEY', '').encode('utf-8')
        crypto.file_decrypt(key, config_file)
    return utils.load_json(config_file)


if __name__ == '__main__':

    bot.config = load_config('config.json')
    bot.errors = bot.config['errors']
    
    token_name=None
    if len(sys.argv) == 2:
        token_name = sys.argv[1]
        bot.command_prefix = '?'

    token = select_token(bot.config, token_name)

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(
                extension, type(e).__name__, e))

    bot.run(token)

