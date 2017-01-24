from discord.ext import commands
import discord.utils as du
from cogs.utils import utils
import discord
import asyncio

def transpose_aliases(aliases):
    # mapping from each alias to their real role name
    # input is of form: {role: [aliases]}
    transposed = {}
    for role, roles in aliases.items():
        for alias in roles:
            transposed[alias] = role
    return transposed

class Roles:

    def __init__(self, bot):
        self.bot = bot
        # both must contain lower case only
        self.roles = self.bot.server_info['allowed_roles']
        self.aliases = transpose_aliases(self.bot.server_info['role_aliases'])

    @commands.command(pass_context=True,
                      brief='Set your tag to an available role',
                      ignore_extra=False)
    async def tag(self, ctx, role):
        # account for random capitalization in input
        role = role.lower()
        # resolve alias or use argument as is
        role = self.aliases.get(role, role)

        if role not in self.roles:
            raise commands.BadArgument()

        assigned = await self.modify_roles(ctx, role)
        await self.bot.reply('You are now tagged as: ' + assigned)
        
    async def on_command_error(self, error, ctx):
        if not utils.error_in_cog(ctx, self):
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.reply(ctx, 'I can\'t tag nothing. I mean.. I could. I just don\'t want to')
        elif isinstance(error, commands.TooManyArguments):
            await utils.reply(ctx, 'you can only have one tag. Don\'t be greedy')
        elif isinstance(error, commands.BadArgument):
            await utils.reply(ctx, 'you\'re just making up words now. ' + self.role_error())
        
    async def modify_roles(self, ctx, role):
        member = ctx.message.author
        server_roles = ctx.message.server.roles
        tags = {du.get(server_roles, name=r.title()) for r in self.roles}
        new_roles = list(set(member.roles) - tags)
        new_role = du.get(server_roles, name=role.title())
        new_roles.append(new_role)
        await self.bot.replace_roles(member, new_roles)
        return str(new_role)
        
        
    def role_error(self):
        #roles = map(lambda r: r.title(), self.roles)
        roles = [r.title() for r in self.roles]
        error = 'Allowed roles are: [ {} ]'.format(', '.join(roles))
        return error

def setup(bot):
    bot.add_cog(Roles(bot))
