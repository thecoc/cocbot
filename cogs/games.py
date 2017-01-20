from discord.ext import commands
from cogs.utils import utils
from functools import partial

random_line = partial(utils.random_line_from_source, 
                      fn=utils.lines_from_url)

class Games:

    def __init__(self, bot):
        self.bot = bot
        self.eightball_url = self.bot.server_info['urls']['8ball']
        self.topics_url = self.bot.server_info['urls']['topics']
        
    @commands.command(pass_context=True, 
                      aliases=['8ball'],
                      brief='Ask the 8-ball.. if you dare!')
    async def eightball(self, ctx):
        await self.bot.reply(random_line(self.eightball_url))
        
    @commands.command(pass_context=True,
                      brief='Request a random conversation starter')
    async def topic(self, ctx):
        await self.bot.reply(random_line(self.topics_url))
        
        
def setup(bot):
    bot.add_cog(Games(bot))