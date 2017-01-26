from discord.ext import commands
from cogs.utils import utils
import discord.utils as du
import discord

class BadWords:

    def __init__(self, bot):
        self.bot = bot
        self.badwords_url = self.bot.config['urls']['badwords']
        #self.mod_id = self.bot.config['channels']['moderators']
        self.badwords = utils.lines_from_url(self.badwords_url)
        
    async def on_message(self, msg):

        words = list(filter(lambda w: w in msg.content, self.badwords))

        if not words:
            return
        
        str = ', '.join(words)
        member = msg.author
        
        pm = 'Terms like [ %s ] are not allowed here' % str
        await self.bot.send_message(member, pm)
        
        to_mod = '%s used the following words: [ %s ]' % (member, str)
 
        #channel = discord.Object(id=self.mod_id)
        
        channels = message.server.channels
        channel = du.get(channels, name='moderators')
        await self.bot.send_message(channel, to_mod)


def setup(bot):
    bot.add_cog(BadWords(bot))

