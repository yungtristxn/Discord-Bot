import discord
from discord.ext import commands
import asyncio
import datetime

class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleted_messages_channel_id = 832018754874769448
        self.limit = None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        send = False
        logchannel = self.bot.get_channel(832019802264305694)
        try:
            if before.channel == after.channel:
                description = f'**{member.mention} has started/stopped their stream!**'
                send = True
            elif before.channel == None and after.channel != None:
                description = f'**{member.mention} has joined {after.channel}**'
                send = True
            elif before.channel != None and after.channel == None:
                description = f'**{member.mention} has left {before.channel}**'
                send = True
            elif before.channel != None and after.channel != None:
                description = f'**{member.mention} went from {before.channel} to {after.channel}**'
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

    # delete all/given number of messages in chat
    @commands.command(pass_context=True)
    async def purge(self, ctx, arg=None):
        if ctx.message.channel.permissions_for(ctx.message.guild.get_member(ctx.message.author.id)).administrator == True or await self.bot.is_owner(ctx.author) == True:
            if arg and (arg == 'all' or arg =='a'):
                def check(m):
                    return m
                try:
                    await ctx.send('Are you sure you want to delete every message in this channel? (y/n)')
                    msg = await self.bot.wait_for('message', check=check, timeout=20)
                    if msg.content == "yes" or msg.content == "y":
                        self.limit = None
                    elif msg.content == "no" or msg.content == "n":
                        self.limit = 0
                    else:
                        self.limit = 0
                        await ctx.send("That didn't work... please try again")
                except asyncio.TimeoutError:
                    await ctx.send(f"You didn't answer in time, deletion canceled")
            else:
                try:
                    self.limit = int(arg)
                except:
                    await ctx.send("That didn't work! Please try using '-purge number'/'-purge all'")
                    self.limit = 0
            
            if self.limit != 0:
                channel = self.bot.get_channel(self.deleted_messages_channel_id)
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
                deleted = await ctx.channel.purge(limit=self.limit)
                response = await ctx.channel.send(f"Successfully deleted {len(deleted)} messages!")
                await asyncio.sleep(3)
                await response.delete()
        else:
            await ctx.send("You don't have the permissions to use this command!")

    # get guild icon
    @commands.command()
    async def geticon(self, ctx):
        try:
            guild = ctx.author.guild
            await ctx.send(guild.icon_url)
        except discord.errors.HTTPException:
            await ctx.send('This server has no icon!')

    # Shutdown the bot, owner only
    @commands.command(pass_context=True)
    async def shutdown(self, ctx):
        is_owner = await self.bot.is_owner(ctx.author)
        if is_owner == False:
            await ctx.send("You don't have the permissions to use this command!")
        else:
            await ctx.send(f'Wildus Bot shutting down...')
            await self.bot.logout()

    # leave server the bot is on, owner only
    @commands.command(pass_context=True)
    async def leave_server(self, ctx):
        is_owner = await self.bot.is_owner(ctx.author)
        if is_owner == False:
            await ctx.send("You don't have the permissions to use this command!")
        else:
            await ctx.guild.leave()

def setup(bot):
    bot.add_cog(MainCog(bot))
