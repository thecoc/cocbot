from discord.ext import commands
from cogs.utils import utils
from functools import partial

DEFAULT_COOLDOWN = 10

random_line = partial(utils.random_line_from_source, 
                      fn=utils.lines_from_url)

class Games:

    def __init__(self, bot):
        self.bot = bot
        self.eightball_url = self.bot.config['urls']['8ball']
        self.topics_url = self.bot.config['urls']['topics']]
        
        
    async def on_ready(self):
        msg = 'To give everyone a chance to respond, you may only request a new topic yourself once every ' + str(DEFAULT_COOLDOWN) + 's'      
        self.bot.commands['topic'].description = msg
   
   
    @commands.command(name = '8ball', 
                      pass_context=True, 
                      brief='Ask the 8-ball.. if you dare!',
                      description='The 8-ball knows all! Usually. Please be sure to include a question or it won\'t be happy')
    async def _8ball(self, ctx, *, question):
        await self.bot.reply(random_line(self.eightball_url))
        
    @commands.command(pass_context=True,
                      brief='Request a random conversation starter',
                      help='I present the room with a random question for all to answer, so I can peer into your souls and steal your secrets. The questions aren\'t mine, but your secrets will be')
    @commands.cooldown(1, DEFAULT_COOLDOWN, type=commands.BucketType.user)
    async def topic(self, ctx):
        await self.bot.say(random_line(self.topics_url)) 
        
        
    def error(self, error, ctx, msg):
        #error.retry_after => time left
        fmt = '{:.0f}'.format(error.retry_after)
        #user = '{0.mention}'.format(ctx.message.author)
        #error = msg.format(member=user, remaining=fmt)
        error = msg.format(remaining=fmt)
        return error
        
def setup(bot):
    bot.add_cog(Games(bot))
