from discord.ext import commands
import discord
from PIL import Image
import urllib.request
import os

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def picConverter(ctx):
    # building the opener to download user avatar
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    # downloading the image and converting it to png
    filename = rf"{dir_path}\Media\{ctx.author.name}.webp"
    new_filename = rf"{dir_path}\Media\{ctx.author.name}.png"
    attachment_url = str(ctx.message.attachments[0].url)
    im = urllib.request.urlretrieve(attachment_url, filename)
    im = Image.open(filename)
    im.save(new_filename, format="png")
    im = Image.open(new_filename).convert("RGBA")
    os.remove(filename)
    os.remove(new_filename)
    return im


class MemeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # meme maker N.1
    @commands.command(pass_context=True)
    async def NiceGuy(self, ctx):
        im1 = picConverter(ctx)
        im2 = Image.open(rf'{dir_path}\Media\Meme_Templates\MemeTP1.png')

        # scaling the second image to fit the first image
        image_size = im2.size
        im1 = im1.resize(image_size)

        # pasting the template onto the given image to create a really funny meme
        im1.paste(im2, (0, 0), im2)
        finalpath = rf'{dir_path}\Media\BakedMeme.png'

        # saving and sending the merged image
        im1.save(finalpath)
        await ctx.send(file=discord.File(finalpath))
        os.remove(finalpath)

    # Meme N.2
    @commands.command(pass_context=True)
    async def AverageGuy(self, ctx):
        im1 = picConverter(ctx)
        im2 = Image.open(
            rf'{dir_path}\Media\Meme_Templates\MemeTP2.png').convert("RGBA")

        im1 = im1.resize((635, 586))
        im2.paste(im1, (650, 135), im1)

        finalpath = rf'{dir_path}\Media\BakedMeme2.png'

        # saving and sending the merged image
        im2.save(finalpath)
        await ctx.send(file=discord.File(finalpath))
        os.remove(finalpath)

    # Meme N.3
    @commands.command(pass_context=True)
    async def Trash(self, ctx):
        im1 = picConverter(ctx)
        im2 = Image.open(
            rf'{dir_path}\Media\Meme_Templates\MemeTP3.jpg').convert("RGBA")

        # resizing given image to fit to meme tp
        im1 = im1.resize((165, 220))
        im2.paste(im1, (55, 80), im1)
        finalpath = rf'{dir_path}\Media\BakedMeme3.png'

        # saving and sending the merged image
        im2.save(finalpath)
        await ctx.send(file=discord.File(finalpath))
        os.remove(finalpath)

    # Send avatar of mentioned user
    @commands.command()
    async def avatar(ctx, user: discord.User = None):
        if user != None:
            await ctx.send(user.avatar_url)
        else:
            await ctx.send(ctx.author.avatar_url)


def setup(bot):
    bot.add_cog(MemeCog(bot))
