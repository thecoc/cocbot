from discord.ext import commands
from cogs.utils import tumblr, utils
import random

# TODO: multiple cooldowns + error messages
DEFAULT_COOLDOWN = 5

class Media:

    def __init__(self, bot):
        self.bot = bot
        self.key = self.bot.config['tumblr']['key']
        self.blogname = self.bot.config['tumblr']['blogname']
        self.tag = self.bot.config['tumblr']['default_tag']
        self.client = tumblr.Client(self.key, blogname=self.blogname)
    

    @commands.command(
        brief='Request a random image from our Tumblr page')
    @commands.cooldown(1, DEFAULT_COOLDOWN)
    async def poster(self):
        post = self.random_post(tag=self.tag)
        msg = post['summary'] + '\ntumblr post @ ' 
        msg += '<' + post['short_url'] + '>\n'
        msg += self.photo_set(post)
        await self.bot.reply(msg)

    def prepare_error(self, error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            #error.retry_after => time left
            msg = self.cooldown_error(error.retry_after)
            return {'msg':utils.mention(ctx, msg)}
            
    def photo_set(self, post):
        urls = [p['original_size']['url'] for p in post['photos']]
        return '\n'.join(urls)
           
    def random_photo(self, **params):
        total_photos = self.client.total_photos(**params)
        index = random.randrange(total_photos)
        return self.client.photos(limit=1, offset=index, **params)      

    def random_post(self, **params):
        return self.random_photo(**params)['posts'][0]
    
    def cooldown_error(self, retry_after):
        error = 'Dude, you\'re interrupting my Netflix! '
        error += 'I\'ll get to whatever you asked for in: '
        error += '{:.2f}s'.format(retry_after)
        return error
        
                       
def setup(bot):
    bot.add_cog(Media(bot))





