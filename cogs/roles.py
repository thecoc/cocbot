from discord.ext import commands
import discord.utils as du
from functools import partial
import discord
import asyncio

def transpose_aliases(aliases):
    # mapping from each alias to their real role name
    # input is of form: {role: [aliases]}
    transposed = {}
    for role, aliases in aliases.items():
        for alias in aliases:
            transposed[alias] = role
    return transposed

class Roles:

    def __init__(self, bot):
        self.bot = bot
        # both must contain lower case only
        self.roles = self.bot.server_info['allowed_roles']
        self.aliases = transpose_aliases(self.bot.server_info['role_aliases'])

    @commands.command(pass_context=True,
                      brief='Set your tag to an available role')
    async def tag(self, ctx, role):
        # account for random capitalization in input
        role = role.lower()
        # resolve alias or use argument as is
        role = self.aliases.get(role, role)

        if role not in self.roles:
            raise commands.BadArgument(self.role_error())

        assigned = await self.modify_roles(ctx, role)
        await self.bot.reply('You are now tagged as: ' + assigned)

    async def modify_roles(self, ctx, role):
        member = ctx.message.author

        # title(): capitalize first letter of each word
        # to match actual roles
        found = du.get(ctx.message.server.roles, name=role.title())
        # currently active tags of the member, except `found` (if present)
        active = list(filter(lambda x: x and x != found,
            (du.get(member.roles, name=name.title())
                for name in self.roles)))

        print(member, ':', found, '<', *active)

        # remove active roles -> no more need for !untag
        await self.bot.remove_roles(member, *active)
        #didn't always delete:
        await asyncio.sleep(1)
        await self.bot.add_roles(member, found)
        return str(found)

    def role_error(self):
        roles = map(lambda r: r.title(), self.roles)
        error = 'Allowed roles are: [ {} ]'.format(', '.join(roles))
        return error

def setup(bot):
    bot.add_cog(Roles(bot))
