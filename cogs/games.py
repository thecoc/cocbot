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
        
    @commands.command(name = '8ball', 
                      pass_context=True, 
                      brief='Ask the 8-ball.. if you dare!')
    async def _8ball(self, ctx, *, question):
        await self.bot.reply(random_line(self.eightball_url))
        
    @commands.command(pass_context=True,
                      brief='Request a random conversation starter')
    async def topic(self, ctx):
        await self.bot.reply(random_line(self.topics_url)) 
     
    def prepare_error(self, error, ctx):
        if isinstance(error, commands.MissingRequiredArgument):
            msg = 'I\'m drawing a blank. Oh.. that\'s probably because you didn\'t give me anything to work with'
            return {'msg':utils.mention(ctx, msg)}
        
def setup(bot):
    bot.add_cog(Games(bot))
