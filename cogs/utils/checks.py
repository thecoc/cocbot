from discord.ext import commands
import discord.utils

def is_owner_or_bot_admin():
    def predicate(ctx):
        owner = ctx.bot.config['owner']
        bot_admins = ctx.bot.config['bot admins']
        author_id = ctx.message.author.id
        return author_id in bot_admins or author_id == owner
    return commands.check(predicate)
    
def is_owner():
    def predicate(ctx):
        return ctx.message.author.id == ctx.bot.config['owner']
    return commands.check(predicate)
    
