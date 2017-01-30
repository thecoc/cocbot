from discord.ext import commands
from cogs.utils import utils, checks
import os

class Admin:

    def __init__(self, bot):
        self.bot = bot
        

    @checks.is_owner_or_bot_admin()
    @commands.command(hidden=True, description='Don\'t even think about it')
    async def quit(self):
        if os.getenv('IGNORELOGOUT', False):
            return

        print('logout requested: shutting down...')
        await self.bot.logout() 

        
def setup(bot):
    bot.add_cog(Admin(bot))