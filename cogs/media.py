from discord.ext import commands
from cogs.utils import tumblr, utils
import random

DEFAULT_COOLDOWN = 60

class Media:

    def __init__(self, bot):
        self.bot = bot
        self.key = self.bot.config['tumblr']['key']
        self.blogname = self.bot.config['tumblr']['blogname']
        self.tag = self.bot.config['tumblr']['default_tag']
        self.client = tumblr.Client(self.key, blogname=self.blogname)    

        
    async def on_ready(self):
        msg = ('A random image taken from: http://' + self.blogname
            + '. You may only request an image every '
            + str(DEFAULT_COOLDOWN) + 's')        
        self.bot.commands['poster'].description = msg
 
 
    @commands.command(
        brief='Request a random image from our Tumblr page',
        help='In addition to the tumblr image, you\'ll also receive its post url in case you want to visit the page, reblog, etc.')
    @commands.cooldown(1, DEFAULT_COOLDOWN, type=commands.BucketType.user)
    async def poster(self):
        post = self.random_post(tag=self.tag)
        msg = (post['summary'] + '\ntumblr post @ ' 
            + '<' + post['short_url'] + '>\n'
            + self.photo_set(post))
        await self.bot.reply(msg)

            
    def photo_set(self, post):
        urls = [p['original_size']['url'] for p in post['photos']]
        return '\n'.join(urls)

        
    def random_photo(self, **params):
        total_photos = self.client.total_photos(**params)
        index = random.randrange(total_photos)
        return self.client.photos(limit=1, offset=index, **params)      

        
    def random_post(self, **params):
        return self.random_photo(**params)['posts'][0]

        
    def error(self, error, ctx, msg):
        #error.retry_after => time left
        fmt = '{:.0f}'.format(error.retry_after)
        error = msg.format(remaining=fmt)
        return error


def setup(bot):
    bot.add_cog(Media(bot))





