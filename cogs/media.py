from discord.ext import commands
from cogs.utils import tumblr
import random

# TODO: multiple cooldowns + error messages
DEFAULT_COOLDOWN = 60

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
        await self.bot.reply(self.photo_set(tag=self.tag))

    @commands.command(
        brief='Request a random image post from our Tumblr page')
    @commands.cooldown(1, DEFAULT_COOLDOWN)
    async def tumblr(self):
        await self.bot.reply(self.random_post(tag=self.tag))
        
    def photo_set(self, **params):
        post = self.random_photo(**params)['posts'][0]
        urls = map(lambda p: p['original_size']['url'], post['photos'])
        return '\n'.join(urls)
           
    def random_photo(self, **params):
        total_photos = self.client.total_photos(**params)
        index = random.randrange(total_photos)
        return self.client.photos(limit=1, offset=index, **params)

    def random_post(self, **params):
        post = self.random_photo(**params)['posts'][0]
        return post['short_url']
        
                       
def setup(bot):
    bot.add_cog(Media(bot))





