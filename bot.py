import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
# very private bot token q-_-p
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

# sets the command prefix for bot commands
bot = commands.Bot(command_prefix='-', intents=intents)

dir_path = os.path.dirname(os.path.realpath(__file__))

class Bot():
    # initializing bot variables
    def __init__(self):
        self.bot = bot
        self.control_channel = self.bot.get_channel(855090791009091584) # id of channel that error messages and logs will be send to

    # sets the activity and shows all connected servers on bot startup
    @bot.event
    async def on_ready(self=bot):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='World of Warships'))
        print(f'{bot.user} has connected to:')
        for guild in bot.guilds:
            print("Servername: " + str(guild.name) +
                  " |||| ServerID: " + str(guild.id))

    @bot.command(pass_context=True)
    async def cog(ctx,type=None, self=bot):
        if await self.bot.is_owner(ctx.author) != True:
            await ctx.send('This is a owner only command!')
            return
        if type == None:
            help_embed = discord.Embed(title='How to use:')
            help_embed.add_field(name='Use one of the following arguments:', value='-cog reload')
            await ctx.send(embed=help_embed)
        elif type == 'reload':
            for cog in self.cog_list:
                bot.reload_extension(f'cogs.{cog}')
            await ctx.send('All cogs succesfully reloaded!')

# initializes with file execution
if __name__ == '__main__':
    # setting up bot
    cogs_file = open(fr'{dir_path}\cogs\cogs.txt', 'r+')
    cogs = cogs_file.read().split(',')
    cogs_file.close()
    try:
        for cog in cogs:
            bot.load_extension(f'cogs.{cog}')
    except commands.errors.ExtensionNotFound as e:
        pass
    Bot.__init__(bot)
    # launches the bot
    bot.run(TOKEN)