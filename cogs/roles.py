from discord.ext import commands
import discord.utils as du
from cogs.utils import utils
import discord
import asyncio

def transpose_aliases(role_aliases):
    # mapping from each alias to their real role name
    # input is of form: {role: [aliases]}
    transposed = {}
    for role, aliases in role_aliases.items():
        for alias in aliases:
            transposed[alias] = role
    return transposed

   
class Roles:

    def __init__(self, bot):
        self.bot = bot
        # both must contain lower case only
        self.roles = self.bot.config['allowed_roles']
        self.aliases = transpose_aliases(self.bot.config['role_aliases'])
    
    
    async def on_ready(self):
         self.bot.commands['tag'].description = self.tag_info()
     

    @commands.command(pass_context=True,
                      brief='Set your tag to an available role',
                      help='These colour-coded tags help to identify yourself and your interests in our chat server. Please note: you may only have one tag at a time',
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


    async def modify_roles(self, ctx, role):
        member = ctx.message.author
        server_roles = ctx.message.server.roles
        
        # get every role member has minus tags
        tags = [du.get(server_roles, name=r.title()) for r in self.roles]
        new_roles = list(set(member.roles) - set(tags))

        # put new role in the list
        new_role = du.get(server_roles, name=role.title())
        new_roles.append(new_role)
        
        await self.bot.replace_roles(member, *new_roles)
        return str(new_role)
 
 
    def tag_info(self):
        roles = [r.title() for r in self.roles]
        info = 'Allowed roles are: [ {} ]'.format(', '.join(roles))
        return info

        
    def error(self, error, ctx, msg):
        info = self.tag_info()
        return '{0}. {1}'.format(msg, info)

        
def setup(bot):
    bot.add_cog(Roles(bot))
