from discord.ext import commands
from cogs.utils import utils
from functools import partial

random_line = partial(utils.random_line_from_source, 
                      fn=utils.lines_from_url)

class Games:

    def __init__(self, bot):
        self.bot = bot
        self.eightball_url = self.bot.config['urls']['8ball']
        self.topics_url = self.bot.config['urls']['topics']
        
        
    @commands.command(name = '8ball', 
                      pass_context=True, 
                      brief='Ask the 8-ball.. if you dare!',
                      description='The 8-ball knows all! Usually. Please be sure to include a question or it won\'t be happy')
    async def _8ball(self, ctx, *, question):
        await self.bot.reply(random_line(self.eightball_url))

        
    @commands.command(pass_context=True,
                      brief='Request a random conversation starter',
                      help='I present the room with a random question for all to answer, so I can peer into your souls and steal your secrets. The questions aren\'t mine, but your secrets will be')
    async def topic(self, ctx):
        await self.bot.say(random_line(self.topics_url)) 

        
def setup(bot):
    bot.add_cog(Games(bot))
