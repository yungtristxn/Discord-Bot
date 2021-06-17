import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# very private bot token o_o
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

# sets the command prefix for bot commands
bot = commands.Bot(command_prefix='-', intents=intents)

dir_path = os.path.dirname(os.path.realpath(__file__))

class Bot():
    # initializing bot variables
    def __init__(self, cog_list):
        self.bot = bot
        self.cog_list = cog_list
        self.control_channel = self.bot.get_channel(855090791009091584) # id of channel that error messages and co. will be send to

    # sets the activity and shows all connected servers on bot startup
    @bot.event
    async def on_ready(self=bot):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='World of Warships'))
        print(f'{bot.user} has connected to:')
        for guild in bot.guilds:
            print("Servername: " + str(guild.name) +
                  " |||| ServerID: " + str(guild.id))

    @bot.command(pass_context=True)
    
    async def cog(ctx,type=None,edit_cog=None,self=bot):
        if await self.bot.is_owner(ctx.author) != True:
            await ctx.send('This is a owner only command!')
            return
        if type == None:
            help_embed = discord.Embed(title='How to use:')
            help_embed.add_field(name='Use one of the following arguments:', value='-cog load/unload/reload')
            await ctx.send(embed=help_embed)
            return
        elif type == 'add':
            if edit_cog == None:
                await ctx.send('Please use the name of the new cog as the 2nd argument!')
                return
            cogs_file = open(fr'{dir_path}\cogs\cogs.txt', 'w')
            cog_l = ''
            for cog in self.cog_list:
                cog_l += f'{cog} '
            cog_l += f'{edit_cog}'
            cogs_file.write(cog_l)
            cogs_file.close()
            self.cog_list.append(edit_cog)
            await ctx.send(f'{edit_cog} successfully removed!')
        elif type == 'remove':
            if edit_cog == None:
                await ctx.send('Please use the name of the cog that will be removed as the 2nd argument!')
                return
            cogs_file = open(fr'{dir_path}\cogs\cogs.txt', 'w')
            print(edit_cog)
            self.cog_list.pop(self.cog_list.index(edit_cog))
            cog_l = ''
            for cog in self.cog_list:
                cog_l += f'{cog} '
            cog_l = cog_l[:-1]
            cogs_file.write(cog_l)
            cogs_file.close()
            await ctx.send(f'{edit_cog} successfully removed!')
            
        else:
            cog_embed = discord.Embed(title='Cogs:')
            x = 0
            for cog in self.cog_list:
                x += 1
                cog_embed.add_field(name=f'{x}',value=cog, inline=True)
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.message.channel
            if type != 'reload':
                await ctx.send(embed=cog_embed)
                await ctx.send(f'Which Cog would you like to {type}?')
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=10)
                except asyncio.TimeoutError:
                    await ctx.send('Please respond a little faster, command interrupted')
                    
            if type == 'load':
                try:
                    element = int(msg.content)-1
                    bot.load_extension(f'cogs.{self.cog_list[element]}')
                    await ctx.send(f'{self.cog_list[element]} succesfully loaded!')
                except:
                    await ctx.send("This didn't work! Cog couldn't be loaded or doesn't exist!")
            elif type == 'unload':
                try:
                    element = int(msg.content)-1
                    bot.unload_extension(f'cogs.{self.cog_list[element]}')
                    await ctx.send(f'{self.cog_list[element]} succesfully unloaded!')
                except:
                   await ctx.send("This didn't work! Cog couldn't be unloaded or doesn't exist!")
            elif type == 'reload':
                for cog in self.cog_list:
                    bot.reload_extension(f'cogs.{cog}')
                await ctx.send('All cogs succesfully reloaded!')
            
                
            


# initializes with file execution
if __name__ == '__main__':
    # setting up bot
    cogs_file = open(fr'{dir_path}\cogs\cogs.txt', 'r+')
    cogs = cogs_file.read().split(' ')
    print(cogs)
    cogs_file.close()
    cog_list = []
    try:
        for cog in cogs:
            cog_list.append(cog)
            bot.load_extension(f'cogs.{cog}')
    except commands.errors.ExtensionNotFound as e:
        print(e)
    Bot.__init__(bot, cog_list)
    # launches the bot
    bot.run(TOKEN)
