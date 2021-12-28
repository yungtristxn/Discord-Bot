from discord.ext import commands
import discord
from PIL import Image
import urllib.request
import os
import platform

if platform.system() == 'Linux':
    system = 'Linux'
elif platform.system() == 'Windows':
    system = 'Windows'
else:
    quit()

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def picConverter(ctx):
    # building the opener to download user avatar
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    # downloading the image and converting it to png
    if system == 'Linux':
        filename = rf"{dir_path}/Media/{ctx.author.name}.png"
    elif system == 'Windows':
        filename = rf"{dir_path}\\Media\\{ctx.author.name}.png"
    attachment_url = str(ctx.message.attachments[0].url)
    im = urllib.request.urlretrieve(attachment_url, filename)
    im = Image.open(filename)
    return im, filename

class MemeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.meme_count = ["1","2","3"]
        self.meme_names = ["NiceGuy","AverageGuy","Trash"]
        self.meme_sizes = [(640,677),(645,586),(165,220)]
        self.meme_positions = [(0,0),(650,135),(55,80)]

    @commands.command(pass_context=True)
    async def meme(self,ctx,meme_nr=None):
        if meme_nr != None and meme_nr in self.meme_count or meme_nr in self.meme_names:
            if meme_nr in self.meme_count:
                meme_nr = int(meme_nr)
            elif meme_nr in self.meme_names:
                meme_nr = self.meme_names.index(meme_nr)+1
                print(meme_nr)
            image, filename = picConverter(ctx)
            if system == 'Linux':
                meme_template = Image.open(rf'{dir_path}/Media/Meme_Templates/MemeTP{meme_nr}.png')
            elif system == 'Windows':
                meme_template = Image.open(rf'{dir_path}\\Media\\Meme_Templates\\MemeTP{meme_nr}.png')
            template_size = self.meme_sizes[meme_nr-1]
            x,y = self.meme_positions[meme_nr-1]

            # scaling image to fit the template
            image = image.resize(template_size)

            # pasting the template onto the given image to create a really funny meme
            if system == 'Linux':
                final_path = rf'{dir_path}/Media/BakedMeme.png'
            elif system == 'Windows':
                final_path = rf'{dir_path}\\Media\\BakedMeme.png'
            if meme_nr == 1:
                image.paste(meme_template,(x,y),meme_template)
                image.save(final_path)
            else:
                meme_template.paste(image,(x,y),image)
                meme_template.save(final_path)
            
            await ctx.send(file=discord.File(final_path))
            os.remove(final_path)
            os.remove(filename)
            
        else:
            await ctx.send(f"Please try using a name or a number from following lists:\t{self.meme_names}\t{self.meme_count}")

    # Send avatar of mentioned user
    @commands.command()
    async def avatar(self, ctx, user = None):
        if user:
            try:
                user = await self.bot.fetch_user(user)
                await ctx.send(user.avatar_url)
            except:
                await ctx.send("Invalid User ID")
        else:
            await ctx.send(ctx.author.avatar_url)

def setup(bot):
    bot.add_cog(MemeCog(bot))
