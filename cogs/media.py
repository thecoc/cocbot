from discord.ext import commands
from cogs.utils import tumblr, utils
import random

# TODO: multiple cooldowns + error messages
DEFAULT_COOLDOWN = 5

class Media:

    def __init__(self, bot):
        self.bot = bot
        self.key = self.bot.server_info['tumblr']['key']
        self.blogname = self.bot.server_info['tumblr']['blogname']
        self.tag = self.bot.server_info['tumblr']['default_tag']
        self.client = tumblr.Client(self.key, blogname=self.blogname)
        
    @commands.command(
        brief='Request a random image from our Tumblr page')
    @commands.cooldown(1, DEFAULT_COOLDOWN)
    async def poster(self):
        post = self.random_post(tag=self.tag)
        response = post['summary'] + '\ntumblr post @ ' 
        response += '<' + post['short_url'] + '>\n'
        response += self.photo_set(post)
        await self.bot.reply(response)
    
    async def on_command_error(self, error, ctx):
        if not utils.error_in_cog(ctx, self):
            return
        if isinstance(error, commands.CommandOnCooldown):
            #error.retry_after => time left
            response = self.cooldown_error(error.retry_after)
            await utils.whisper(ctx, response)  
        elif isinstance(error, commands.CommandInvokeError):
            response = 'Well.. something went wrong. '
            response += 'Just so we\'re clear, it wasn\'t my fault. '
            response += '[ ' + str(error.original) + ' ]'
            await utils.reply(ctx, response)
        
    def photo_set(self, post):
        urls = [p['original_size']['url'] for p in post['photos']]
        return '\n'.join(urls)
           
    def random_photo(self, **params):
        try:
            total_photos = self.client.total_photos(**params)
            index = random.randrange(total_photos)
            return self.client.photos(limit=1, offset=index, **params)
        except Exception as e:
            raise commands.CommandInvokeError(e)       

    def random_post(self, **params):
        return self.random_photo(**params)['posts'][0]
    
    def cooldown_error(self, retry_after):
        error = 'Dude, you\'re interrupting my Netflix! '
        error += 'I\'ll get to your command in: '
        error += '{:.2f}s'.format(retry_after)
        return error
        
                       
def setup(bot):
    bot.add_cog(Media(bot))





