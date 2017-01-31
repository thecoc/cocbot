from discord.ext import commands
from cogs.utils import utils
import discord.utils as du
import discord
import re

def combine_words(words):
    """Compiles list of words into a regex object
    that matches any of them. (whole words only)
    """
    regx = '|'.join(r"\b%s\b" % w for w in words)
    return re.compile(regx, flags=re.IGNORECASE)

class BadWords:

    def __init__(self, bot):
        self.bot = bot
        self.badwords_url = self.bot.config['urls']['badwords']
        self.badwords = utils.lines_from_url(self.badwords_url)
        self.re_badwords = combine_words(self.badwords)
        
    async def on_message(self, msg):
        
        if msg.author.bot:
            return
       
        words = self.re_badwords.findall(msg.content)
        
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

