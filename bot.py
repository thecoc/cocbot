from discord.ext import commands
from cogs.utils import utils, checks, crypto
import discord.utils as du
import discord
import os
import sys

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

@checks.is_owner_or_bot_admin()
@bot.command(hidden=True)
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

    token_name=None
    if len(sys.argv) == 2:
        token_name = sys.argv[1]

    token = select_token(bot.config, token_name)

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(
                extension, type(e).__name__, e))

    bot.run(token)

