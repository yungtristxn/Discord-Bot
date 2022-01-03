from discord.ext import commands
import discord
import requests
from dateutil import parser

def getPlayerinfo(playername):
    response = requests.get(f"https://gameinfo.albiononline.com/api/gameinfo/search?q={playername}")
    try:
        id = response.json()["players"][0]["Id"]
    except:
        return "error"
    response = requests.get(f"https://gameinfo.albiononline.com/api/gameinfo/players/{id}")
    if response.status_code == 404:
        return "error"
    else:
        return response

class AlbionCog(commands.Cog):

    @commands.command()
    async def kb(self,ctx):
        response = getPlayerinfo(ctx.message.content[4:])
        if response != 'error':
            data = response.json()
            embed=discord.Embed(title=f"PvP Stats", description=f"**IGN:** {data['Name']}", color=0xf50f0f)
            embed.add_field(name="Stats", value=f"**Guild:** {data['GuildName']}\n **Alliance:** {data['AllianceName']}\n**Kill Fame:** {data['KillFame']:,}\n**Death Fame:** {data['DeathFame']:,}\n**Ratio:** {data['FameRatio']}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Player not found!")

    @commands.command()
    async def stats(self,ctx):
        response = getPlayerinfo(ctx.message.content[7:])

        if response != 'error':
            data = response.json()
            stats = data['LifetimeStatistics']
            pve = stats['PvE']
            gathering = stats['Gathering']
            crafting = stats['Crafting']
            
            embed = discord.Embed(title="Stats", description=f"**IGN:** {data['Name']}", color=0x1db9fc, timestamp=parser.parse(stats['Timestamp']))
            embed.add_field(name='Player Info', value=f"**Name:** {data['Name']}\n**Guild:** {data['GuildName']}\n**Alliance:** {data['AllianceName']}\n", inline=True)
            embed.add_field(name='PvE Fame',value=f"**Fame by killing mobs:** {pve['Total']:,}\n**Royal Zone:** {pve['Royal']:,}\n**Outlands:** {pve['Outlands']:,}\n**Avalon**: {pve['Avalon']:,}\n**Hellgate:** {pve['Hellgate']:,}\n**Corrupted Dungeon:** {pve['CorruptedDungeon']:,}", inline=True)
            embed.add_field(name='\u200b', value='\u200b', inline=True)
            embed.add_field(name='Gathering',value=f"**Total Gathering Fame:** {gathering['All']['Total']:,}\n**Fiber Fame:** {gathering['Fiber']['Total']:,}\n**Hide Fame:** {gathering['Hide']['Total']:,}\n**Ore Fame:** {gathering['Ore']['Total']:,}\n**Wood Fame:** {gathering['Wood']['Total']:,}", inline=True)
            embed.add_field(name='Other',value=f"**Total Crafting Fame:** {crafting['Total']:,}\n**Total Fishing Fame:** {stats['FishingFame']:,}\n**Total Farming Fame:** {stats['FarmingFame']:,}", inline=True)
            embed.add_field(name='\u200b', value='\u200b', inline=True)
            embed.set_footer(text='Data from:')
            await ctx.send(embed=embed)
        else: 
            await ctx.send('Player not found!')

def setup(bot):
    bot.add_cog(AlbionCog(bot))