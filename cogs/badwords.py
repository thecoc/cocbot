from discord.ext import commands
from cogs.utils import utils
import discord.utils as du
import discord

class BadWords:

    def __init__(self, bot):
        self.bot = bot
        self.badwords_url = self.bot.config['urls']['badwords']
        self.badwords = utils.lines_from_url(self.badwords_url)
        
    async def on_message(self, msg):
        
        if msg.author.bot:
            return
       
        words = [w for w in self.badwords if w in msg.content]
        
        if not words:
            return
        
        str = ', '.join(words)
        member = msg.author
        
        pm = 'Terms like [ %s ] are not allowed here' % str
        await self.bot.send_message(member, pm)
        
        to_mod = '%s used the following words: [ %s ]' % (member, str)
        
        channels = msg.server.channels
        channel = du.get(channels, name='moderators')
        await self.bot.send_message(channel, to_mod)


def setup(bot):
    bot.add_cog(BadWords(bot))

