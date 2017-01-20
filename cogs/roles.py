from discord.ext import commands
from discord.utils import find
from functools import partial
import discord

class Roles:

    def __init__(self, bot):
        self.bot = bot
        self.roles = self.bot.server_info['allowed_roles']
        self.aliases = self.bot.server_info['role_aliases']
        self.mispellings = self.bot.server_info['mispellings']
    
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
    
        if role not in self.roles and role not in self.aliases:
            raise commands.BadArgument('Tag doesn\'t exist!')

        roles = ctx.message.server.roles
        member = ctx.message.author
        found = find(lambda r: str(r).lower() == role, roles)
        # TODO: check for valid aliases
        await fn(member, discord.Object(id=found.id))
        return str(found)
            
            
def setup(bot):
    bot.add_cog(Roles(bot))
