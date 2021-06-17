import discord
from discord.ext import commands
import asyncio
import datetime


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forbidden_channel_ids = [853372174319222795]
        self.deleted_messages_channel_id = 832018754874769448

    # # Function that is called on every message
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     # checking if message is a command and if true, checking if it is sent into one of the given botchannels, if not the message is deleted and logged in deleted_messages_channel
    #     if message.content.startswith('-') and message.channel.id in self.forbidden_channel_ids:
    #         backupchannel = self.bot.get_channel(
    #             self.deleted_messages_channel_id)
    #         # creating the embed message that contains the deleted command, the author and the server it was sent on
    #         deletedMessage = discord.Embed(
    #             title='Overwatch', color=0x00ff00)
    #         deletedMessage.add_field(
    #             name='Deleted command:', value=message.content, inline=False)
    #         deletedMessage.add_field(
    #             name='Author:', value=message.author, inline=False)
    #         deletedMessage.add_field(
    #             name='Channel:', value=message.channel, inline=False)
    #         deletedMessage.add_field(
    #             name='Server:', value=message.guild.name, inline=False)
    #         deletedMessage.add_field(
    #             name='Server-ID:', value=message.guild.id, inline=False)
    #         await backupchannel.send(embed=deletedMessage)
    #         await message.delete()
    #         response = await message.channel.send('Using me in this channel is forbidden!')
    #         await asyncio.sleep(3)
    #         await response.delete()
    #     elif message.author.id != 788874938139672610: #not bot himself
    #         await self.bot.process_commands(message)
    #     else:
    #         pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        send = False
        logchannel = self.bot.get_channel(832019802264305694)
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

        # delete all/given number of messages in chat
    @commands.command(pass_context=True)
    async def purge(self, ctx, arg=None):
        if ctx.message.channel.permissions_for(ctx.message.guild.get_member(ctx.message.author.id)).administrator == True or await self.bot.is_owner(ctx.author) == True:
            if arg:
                limit = int(arg)
            else:
                limit = None
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
            deleted = await ctx.channel.purge(limit=limit)
            response = await ctx.channel.send(f"Successfully deleted {len(deleted)} messages!")
            await asyncio.sleep(3)
            await response.delete()
        else:
            await ctx.send('Du besitzt nicht die nötigen Rechte um das zu tun!')

    # sends the current daytime
    @commands.command(pass_context=True)
    async def time(self, ctx):
        time = str(datetime.datetime.now())[:19]
        await ctx.send(time)

    # get guild icon
    @commands.command()
    async def geticon(self, ctx):
        try:
            guild = ctx.author.guild
            await ctx.send(guild.icon_url)
        except discord.errors.HTTPException:
            await ctx.send('This server has no icon!')
            
    @commands.command()
    async def mlist(self, ctx):
        mlist = discord.Embed(description="**Memberlist**",
                              color=0x00ff00, timestamp=datetime.datetime.utcnow())
        mlist.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        mlist.set_footer(text=str(ctx.author.guild.name))

        for member in ctx.guild.members:
            mlist.add_field(
                name=f'**{member.name}**', value=f'Joined Server: ```{str(member.joined_at)[:19]}```Joined Discord: ```{member.created_at}```', inline=True)

        await ctx.send(embed=mlist)

    @commands.command()
    async def isAdmin(self, ctx, member: discord.Member = None):
        if member:
            member = member
        else:
            member = ctx.message.guild.get_member(ctx.message.author.id)

        has_permission = ctx.message.channel.permissions_for(
            member).administrator
        await ctx.send(f'Admin status: {has_permission}')
        
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
