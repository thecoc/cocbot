from discord.ext import commands
from discord.utils import find
from functools import partial
import discord

def transpose_aliases(aliases):
    d = {}
# d contains mapping from each alias to their 'base' role name
    for base, aliarr in aliases.items():
        for ali in aliarr:
            d[ali] = base
    return d

class Roles:

    def __init__(self, bot):
        self.bot = bot
        self.roles = self.bot.server_info['allowed_roles']
        self.aliases = transpose_aliases(self.bot.server_info['role_aliases'])
        self.mispellings = self.bot.server_info['mispellings'] #currently unused
    
    @commands.command(pass_context=True,
                      brief='Set your tag to an available role')
    async def tag(self, ctx, role):
        r = await self.modify_role(ctx, role, self.bot.add_roles)
        await self.bot.reply('You are now tagged as: ' + r)

    @commands.command(pass_context=True,
                      brief='Remove one of your tags')
    async def untag(self, ctx, role):
        r = await self.modify_role(ctx, role, self.bot.remove_roles)
        await self.bot.reply('You are no longer tagged as: ' + r)
    
    async def modify_role(self, ctx, role, fn):

        role = self.aliases.get(role, role) # expand alias if present, or itself
    
        if role not in self.roles: #among rolles allowed to (un)tag
            raise commands.BadArgument('Tag doesn\'t exist!')

        roles = ctx.message.server.roles
        member = ctx.message.author
        found = find(lambda r: str(r).lower() == role, roles)

        await fn(member, discord.Object(id=found.id))
        return str(found)
            
            
def setup(bot):
    bot.add_cog(Roles(bot))
