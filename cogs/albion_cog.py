from discord.ext import commands
import discord
import requests
from dateutil import parser


def getPlayerId(playername):
    response = requests.get(
        f"https://gameinfo.albiononline.com/api/gameinfo/search?q={playername}",
        verify=False,
        timeout=15
    )
    try:
        id = response.json()["players"][0]["Id"]
        return id
    except:
        return "error"


def getPlayerInfo(playername):
    id = getPlayerId(playername)
    if id == "error":
        return "error"
    else:
        response = requests.get(
            f"https://gameinfo.albiononline.com/api/gameinfo/players/{id}",
            verify=False,
            timeout=15
        )
        if response.status_code == 404:
            return "error"
        else:
            return response


class AlbionCog(commands.Cog):
    @commands.command()
    async def get_id(self, ctx):
        response = getPlayerInfo(ctx.message.content[8:])
        if response != "error":
            data = response.json()
            await ctx.send(
                f"**PlayerId:** {data['Id']}\n**GuildId:** {data['GuildId']}\n**AllianceId:** {data['AllianceId']}"
            )
        else:
            await ctx.send("Player not found!")

    @commands.command()
    async def recent(self, ctx):
        playerId = getPlayerId(ctx.message.content[8:])
        if playerId != "error":
            killdata = requests.get(
                f"https://gameinfo.albiononline.com/api/gameinfo/players/{playerId}/kills",
                verify=False,
                timeout=15
            ).json()
            deathdata = requests.get(
                f"https://gameinfo.albiononline.com/api/gameinfo/players/{playerId}/deaths",
                verify=False,
                timeout=15
            ).json()

            recent_killfame = 0
            recent_deathfame = 0
            total_victimDeathfame = 0

            for killfame in killdata:
                recent_killfame += killfame["Killer"]["KillFame"]
                total_victimDeathfame += killfame["TotalVictimKillFame"]
            for deathfame in deathdata:
                recent_deathfame += deathfame["Victim"]["DeathFame"]

            embed = discord.Embed(
                title=f"Recent K/D ratio of {killfame['Killer']['Name']}",
                description=f"Kill/Fame ratio of last 10 kills/deaths",
                color=0xF50F0F,
            )
            embed.add_field(name="Recent gained killfame",
                            value=f"{recent_killfame:,}")
            embed.add_field(
                name="Total victim killfame", value=f"{total_victimDeathfame:,}"
            )
            embed.add_field(name="Recent deathfame",
                            value=f"{recent_deathfame:,}")
            embed.add_field(
                name="Actual K/D ratio",
                value=f"{round((recent_killfame/recent_deathfame),2)}",
            )
            embed.add_field(
                name="Total K/D ratio",
                value=f"{round((total_victimDeathfame/recent_deathfame),2)}",
            )
            embed.add_field(name="\u200b", value="\u200b")
            await ctx.send(embed=embed)

        else:
            await ctx.send("Player not found!")

    @commands.command()
    async def recentG(self, ctx):
        pInput = ctx.message.content[9:]
        response = requests.get(
            f"https://gameinfo.albiononline.com/api/gameinfo/search?q={pInput}",
            verify=False,
            timeout=15
        )
        if response.status_code != 404:
            data = response.json()

            try:
                guildName = data['guilds'][0]['Name']
                guildId = data['guilds'][0]['Id']
            except IndexError:
                try:
                    guildName = data['players'][0]['GuildName']
                    guildId = data['players'][0]['GuildId']
                except IndexError:
                    await ctx.send('Guild/Player was not found!')
                    return

            event_response = requests.get(
                f"https://gameinfo.albiononline.com/api/gameinfo/events?limit=9&offset=0&guildId={guildId}",
                verify=False,
                timeout=15)
            if event_response.status_code != 404:
                data = event_response.json()

                embed = discord.Embed(
                    name='Recent Guildkills',
                    description=f'Shows 9 latest kills of {guildName}',
                    color=0xF50F0F
                )
                i = 0
                for kill in data:
                    i += 1
                    embed.add_field(
                        name=f'Kill{i}\n',
                        value=f"```Killer: {kill['Killer']['Name']}\nKillerIP: {int(kill['Killer']['AverageItemPower'])}\nVictim: {kill['Victim']['Name']}\nVictimIP: {int(kill['Victim']['AverageItemPower'])}\nKill Fame: {kill['TotalVictimKillFame']}```"
                    )
                await ctx.send(embed=embed)
            else:
                await ctx.send("Couldn't get recent kill data, please try again!")

        else:
            await ctx.send('Player/Guild not found!')

    @commands.command()
    async def kb(self, ctx):
        response = getPlayerInfo(ctx.message.content[4:])
        if response != "error":
            data = response.json()
            embed = discord.Embed(
                title=f"PvP Stats",
                description=f"**IGN:** {data['Name']}",
                color=0xF50F0F,
            )
            embed.add_field(
                name="Stats",
                value=f"**Guild:** {data['GuildName']}\n **Alliance:** {data['AllianceName']}\n**Kill Fame:** {data['KillFame']:,}\n**Death Fame:** {data['DeathFame']:,}\n**Ratio:** {data['FameRatio']}",
                inline=False,
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Player not found!")

    @commands.command()
    async def stats(self, ctx):
        response = getPlayerInfo(ctx.message.content[7:])

        if response != "error":
            data = response.json()
            stats = data["LifetimeStatistics"]
            pve = stats["PvE"]
            gathering = stats["Gathering"]
            crafting = stats["Crafting"]

            embed = discord.Embed(
                title="Stats",
                description=f"**IGN:** {data['Name']}",
                color=0x1DB9FC,
                timestamp=parser.parse(stats["Timestamp"]),
            )
            embed.add_field(
                name="Player Info",
                value=f"**Name:** {data['Name']}\n**Guild:** {data['GuildName']}\n**Alliance:** {data['AllianceName']}\n",
                inline=True,
            )
            embed.add_field(
                name="PvE Fame",
                value=f"**Fame by killing mobs:** {pve['Total']:,}\n**Royal Zone:** {pve['Royal']:,}\n**Outlands:** {pve['Outlands']:,}\n**Avalon**: {pve['Avalon']:,}\n**Hellgate:** {pve['Hellgate']:,}\n**Corrupted Dungeon:** {pve['CorruptedDungeon']:,}",
                inline=True,
            )
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(
                name="Gathering",
                value=f"**Total Gathering Fame:** {gathering['All']['Total']:,}\n**Fiber Fame:** {gathering['Fiber']['Total']:,}\n**Hide Fame:** {gathering['Hide']['Total']:,}\n**Ore Fame:** {gathering['Ore']['Total']:,}\n**Wood Fame:** {gathering['Wood']['Total']:,}",
                inline=True,
            )
            embed.add_field(
                name="Other",
                value=f"**Total Crafting Fame:** {crafting['Total']:,}\n**Total Fishing Fame:** {stats['FishingFame']:,}\n**Total Farming Fame:** {stats['FarmingFame']:,}",
                inline=True,
            )
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.set_footer(text="Data from:")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Player not found!")


def setup(bot):
    bot.add_cog(AlbionCog(bot))
