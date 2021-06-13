import discord
from discord.ext import commands
import asyncio
import datetime
from discord.ext.commands import errors, Bot
import requests
import subprocess
import os
from PIL import Image
import urllib.request
import random
import numpy as np
from dotenv import load_dotenv

# very private bot token o_o
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

# sets the command prefix for bot commands
bot = commands.Bot(command_prefix='-', intents=intents)


def picConverter(ctx):
    # building the opener to download user avatar
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    # downloading the image and converting it to png
    filename = rf"E:\Code\Media\{ctx.author.name}.webp"
    new_filename = rf"E:\Code\Media\{ctx.author.name}.png"
    attachment_url = str(ctx.message.attachments[0].url)
    im = urllib.request.urlretrieve(attachment_url, filename)
    im = Image.open(filename)
    im.save(new_filename, format="png")
    im = Image.open(new_filename).convert("RGBA")
    os.remove(filename)
    os.remove(new_filename)
    return im


def listTo2dArray(list):
    n = 0
    visual = '```'
    for x in list:
        n += 1
        if n == 1:
            visual += f'{x} '
        elif n == 3:
            visual += f'| {x}\n'
            n = 0
        else:
            visual += f'| {x} '

    visual += '```'
    embed = discord.Embed(title='Wildus-Game-Bot',
                          color=0x00ff00, timestamp=datetime.datetime.utcnow())
    embed.add_field(name='**Tic-Tac-Toe**', value=f'{visual}')
    return embed


class Bot():
    # initializing bot variables
    def __init__(self):
        self.bot = bot
        self.bot_channel_ids = [563024724612087829,
                                746945705142124596,
                                826223294243012659,
                                746945705142124596,
                                852236803079798784]
        self.deleted_messages_channel_id = 832018754874769448

    # sets the activity and shows all connected servers on bot startup
    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Tristan beim scheißen zu'))
        print(f'{bot.user} has connected to:')
        for guild in bot.guilds:
            print("Servername: " + str(guild.name) +
                  " |||| ServerID: " + str(guild.id))

    # Function that is called on every message
    @bot.event
    async def on_message(message, self=bot):
        # checking if message is a command and if true, checking if it is sent into one of the given botchannels, if not the message is deleted and logged in deleted_messages_channel
        if message.content.startswith('-') and message.channel.id not in self.bot_channel_ids:
            backupchannel = bot.get_channel(self.deleted_messages_channel_id)
            # creating the embed message that contains the deleted command, the author and the server it was sent on
            deletedMessage = discord.Embed(
                title='Overwatch', color=0x00ff00, timestamp=datetime.datetime.utcnow())
            deletedMessage.add_field(
                name='Deleted command:', value=message.content, inline=False)
            deletedMessage.add_field(
                name='Author:', value=message.author, inline=False)
            deletedMessage.add_field(
                name='Channel:', value=message.channel, inline=False)
            deletedMessage.add_field(
                name='Server:', value=message.guild.name, inline=False)
            deletedMessage.add_field(
                name='Server-ID:', value=message.guild.id, inline=False)
            await backupchannel.send(embed=deletedMessage)
            await message.delete()
            response = await message.channel.send('Please use Wildus-Bot in bot channels only!! :)')
            await asyncio.sleep(3)
            await response.delete()
        else:
            await bot.process_commands(message)

    # sends the current daytime
    @bot.command(pass_context=True)
    async def time(ctx):
        time = str(datetime.datetime.now())[:19]
        await ctx.send(time)

    # get guild icon
    @bot.command()
    async def geticon(ctx):
        try:
            guild = ctx.author.guild
            await ctx.send(guild.icon_url)
        except discord.errors.HTTPException:
            await ctx.send('This server has no icon!')

    # Shutdown the bot, owner only
    @bot.command(pass_context=True)
    async def shutdown(ctx):
        is_owner = await bot.is_owner(ctx.author)
        if is_owner == False:
            await ctx.send("You don't have the permissions to use this command!")
        else:
            await ctx.send(f'Wildus Bot shutting down...')
            await bot.logout()

    # leave server the bot is on, owner only
    @bot.command(pass_context=True)
    async def leave_server(ctx):
        is_owner = await bot.is_owner(ctx.author)
        if is_owner == False:
            await ctx.send("You don't have the permissions to use this command!")
        else:
            await ctx.guild.leave()

    # delete all/given number of messages in chat
    @bot.command(pass_context=True)
    async def purge(ctx, arg=None, self=bot):
        if ctx.author.guild_permissions.administrator:
            if arg:
                limit = int(arg)
            else:
                limit = None
            channel = bot.get_channel(self.deleted_messages_channel_id)
            deletedMessage = discord.Embed(
                title='Channel Purger', color=0x00ff00, timestamp=datetime.datetime.now())
            deletedMessage.add_field(
                name='Used by:', value=ctx.message.author, inline=False)
            deletedMessage.add_field(
                name='In Channel:', value=ctx.message.channel, inline=False)
            deletedMessage.add_field(
                name='Server:', value=ctx.message.guild.name, inline=False)
            deletedMessage.add_field(
                name='Server-ID:', value=ctx.message.guild.id, inline=False)
            await channel.send(embed=deletedMessage)
            deleted = await ctx.channel.purge(limit=limit)
            response = await ctx.channel.send(f"Successfully deleted {len(deleted)} messages!")
            await asyncio.sleep(3)
            await response.delete()
        else:
            await ctx.send('Du besitzt nicht die nötigen Rechte um das zu tun!')

    # meme maker N.1
    @bot.command(pass_context=True)
    async def NiceGuy(ctx, self=bot):
        im1 = picConverter(ctx)
        im2 = Image.open('E:\Code\Media\MemeTP1.png')

        # scaling the second image to fit the first image
        image_size = im2.size
        im1 = im1.resize(image_size)

        # pasting the template onto the given image to create a really funny meme
        im1.paste(im2, (0, 0), im2)
        finalpath = r'E:\Code\Media\BakedMeme.png'

        # saving and sending the merged image
        im1.save(finalpath)
        await ctx.send(file=discord.File(finalpath))
        os.remove(finalpath)

    # Meme N.2
    @bot.command(pass_context=True)
    async def AverageGuy(ctx, self=bot):
        im1 = picConverter(ctx)
        im2 = Image.open('E:\Code\Media\MemeTP2.png').convert("RGBA")

        im1 = im1.resize((635, 586))
        im2.paste(im1, (650, 135), im1)

        finalpath = r'E:\Code\Media\BakedMeme2.png'

        # saving and sending the merged image
        im2.save(finalpath)
        await ctx.send(file=discord.File(finalpath))
        os.remove(finalpath)

    # Meme N.3
    @bot.command(pass_context=True)
    async def Trash(ctx, self=bot):
        im1 = picConverter(ctx)
        im2 = Image.open('E:\Code\Media\MemeTP3.jpg').convert("RGBA")

        # resizing given image to fit to meme tp
        im1 = im1.resize((165, 220))
        im2.paste(im1, (55, 80), im1)
        finalpath = r'E:\Code\Media\BakedMeme3.png'

        # saving and sending the merged image
        im2.save(finalpath)
        await ctx.send(file=discord.File(finalpath))
        os.remove(finalpath)

    # Send avatar of mentioned user
    @bot.command()
    async def avatar(ctx, user: discord.User = None):
        if user != None:
            await ctx.send(user.avatar_url)
        else:
            await ctx.send(ctx.author.avatar_url)

    # logs activity in voice channels
    @bot.event
    async def on_voice_state_update(member, before, after):
        send = False
        logchannel = bot.get_channel(832019802264305694)
        try:
            if before.channel == after.channel:
                pass
            elif before.channel == None and after.channel != None:
                description = f'**{member.mention} has joined {after.channel}**'
                send = True
            elif before.channel != None and after.channel == None:
                description = f'**{member.mention} has left {before.channel}**'
                send = True
            elif before.channel != None and after.channel != None:
                description = f'**{member.mention} went from {before.channel} to {after.channel}'
                send = True
            else:
                pass
            if send == True:
                log = discord.Embed(description=description,
                                    color=0x00ff00, timestamp=datetime.datetime.utcnow())
                log.set_author(name=member, icon_url=member.avatar_url)
                log.set_footer(text=str(member.guild.name))
                await logchannel.send(embed=log)
                send = False
        except AttributeError:
            pass

    @bot.command()
    async def mlist(ctx):
        mlist = discord.Embed(description="**Memberlist**",
                              color=0x00ff00, timestamp=datetime.datetime.utcnow())
        mlist.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        mlist.set_footer(text=str(ctx.author.guild.name))

        for member in ctx.guild.members:
            mlist.add_field(
                name=f'**{member.name}**', value=f'Joined Server: ```{str(member.joined_at)[:19]}```Joined Discord: ```{member.created_at}```', inline=True)

        await ctx.send(embed=mlist)

    @bot.command()
    async def ttt(ctx, user: discord.User = None):
        winner = None
        # all possible fields that can be chosen to place either an X or an O
        availabe_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        number_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        channel = ctx.message.channel  # channel the game is going to be played in
        user1 = ctx.message.author.id   # user that started the game
        user2 = user.id     # tagged user
        userlist = [user1, user2]

        # chooses a random user of the 2 that begins the round
        first_user = random.choice(userlist)

        ttt_array = await ctx.send(embed=listTo2dArray(number_list))
        startmsg = await ctx.send(f"{bot.get_user(first_user).mention} beginnt mit X!")
        current_user = first_user

        if first_user == user1:
            userlist = [first_user, user2]
        else:
            userlist = [first_user, user1]
        x = 9
        y = 0
        while y < x:
            def check(m):
                return m.channel == channel and m.author.id == current_user
            try:
                msg = await bot.wait_for('message', check=check, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send(f"Deine Zeit ist ausgelaufen {bot.get_user(current_user).mention}!")
                break
            await msg.delete()
            if msg.content in availabe_numbers:
                if msg.content in number_list:
                    if userlist.index(current_user) == 0:
                        number_list[number_list.index(msg.content)] = "X"
                    else:
                        number_list[number_list.index(msg.content)] = "0"

                    await ttt_array.edit(embed=listTo2dArray(number_list))
                    y += 1
                    availabe_numbers.remove(msg.content)

                def checkRows(array):
                    for row in array:
                        if len(set(row)) == 1:
                            if row[0] == "X":
                                winner = userlist[0]
                            else:
                                winner = userlist[1]

                            return winner
                        else:
                            pass

                def checkDiagonals(array):
                    symbol = None
                    if len(set([array[i][i] for i in range(len(array))])) == 1:
                        symbol = array[0][0]
                    if len(set([array[i][len(array)-i-1] for i in range(len(array))])) == 1:
                        symbol = array[0][len(array)-1]
                    if symbol:
                        if symbol == "X":
                            winner = userlist[0]
                            return winner
                        elif symbol == "0":
                            winner = userlist[1]
                            return winner
                    else:
                        pass

                mdnumber_array = np.reshape(number_list, (-1, 3))
                # checking if a winner exists, if winner is found ends the game and announces winner
                winCon1 = checkRows(mdnumber_array)
                winCon2 = checkDiagonals(mdnumber_array)
                if winCon1:
                    winner = winCon1
                elif winCon2:
                    winner = winCon2
                if winner:
                    await startmsg.delete()
                    await ctx.send(f"{bot.get_user(winner).mention} hat gewonnen!")
                    break
                # changing the user whose turn it is
                if userlist.index(current_user) == 0:
                    current_user = userlist[1]
                else:
                    current_user = userlist[0]
                await startmsg.edit(content=f"{bot.get_user(current_user).mention} ist dran!")

            else:
                error = await ctx.send(f"Die Stelle {msg.content} ist bereits besetzt!")
                await asyncio.sleep(2)
                await error.delete()
        else:
            error = await ctx.send(f"Die Stelle {msg.content} gibt es nicht!")
            await asyncio.sleep(2)
            await error.delete()

        if not winner:
            await ctx.send("Das Spiel ist vorbei und keiner hat gewonnen!")


# initializes with file execution
if __name__ == '__main__':
    # setting up bot
    Bot.__init__(bot)

    # launches the bot
    bot.run(TOKEN)
