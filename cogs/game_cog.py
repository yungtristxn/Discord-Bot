from discord.ext import commands
import asyncio
import discord
import random
import numpy as np


def listTo2dArray(list, user_x, user_0):
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
                          color=0x00ff00)
    embed.add_field(name='**Tic-Tac-Toe**', value=f'{visual}')
    embed.set_footer(text=f'{user_x}=X\n{user_0}=0')
    return embed


class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ttt(self, ctx, user: discord.User = None):
        winner = None
        # all possible fields that can be chosen to place either an X or an O
        availabe_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        number_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        channel = ctx.message.channel  # channel the game is going to be played in
        user1 = ctx.message.author.id   # user that started the game
        user2 = user.id     # tagged user

        # chooses a random beginner
        current_user = random.choice([user1, user2])

        # assinging unique names to both players
        user_x = current_user
        if user_x == user1:
            user_0 = user2
        else:
            user_0 = user1

        # sending messages to give the players all needed info, these will be updated during the game
        ttt_array = await ctx.send(embed=listTo2dArray(number_list, self.bot.get_user(user_x).name, self.bot.get_user(user_0).name))
        startmsg = await ctx.send(f"{self.bot.get_user(current_user).mention} begins X!")

        x = 9
        y = 0
        while y < x:
            def check(m):
                return m.channel == channel and m.author.id == current_user
            try:
                ready_message = await ctx.send('Ready for input:')
                msg = await self.bot.wait_for('message', check=check, timeout=20)
                await ready_message.delete()
            except asyncio.TimeoutError:
                await ctx.send(f"Your time's up! {self.bot.get_user(current_user).mention}!")
                break
            await msg.delete()
            if msg.content in availabe_numbers:
                if msg.content in number_list:
                    availabe_numbers.remove(msg.content)
                    if current_user == user_x:
                        number_list[number_list.index(msg.content)] = "X"
                    else:
                        number_list[number_list.index(msg.content)] = "0"

                    await ttt_array.edit(embed=listTo2dArray(number_list, self.bot.get_user(user_x).name, self.bot.get_user(user_0).name))
                    y += 1

                # functions for check winner from https://stackoverflow.com/a/39923218
                def checkBoard(array):
                    # Rows
                    for r in range(array):
                        yield [(r, c) for c in range(array)]
                    # Columns
                    for c in range(array):
                        yield [(r, c) for r in range(array)]
                    # Diagonal top left to bottom right
                    yield [(i, i) for i in range(array)]
                    # Diagonal top right to bottom left
                    yield [(i, array - 1 - i) for i in range(array)]

                def is_winner(board, decorator):
                    b_len = len(board)
                    for indexes in checkBoard(b_len):
                        if all(board[r][c] == decorator for r, c in indexes):
                            return True
                    return False

                mdnumber_array = np.reshape(number_list, (-1, 3))
                if is_winner(mdnumber_array, "X") == True:
                    winner = user_x
                elif is_winner(mdnumber_array, "0") == True:
                    winner = user_0
                if winner:
                    await startmsg.delete()
                    await ctx.send(f"{self.bot.get_user(winner).mention} won!")
                    break

                # changing the user whose turn it is
                if current_user == user_0:
                    current_user = user_x
                else:
                    current_user = user_0
                await startmsg.edit(content=f"It's {self.bot.get_user(current_user).mention} turn!")
            else:
                error = await ctx.send(f"The field {msg.content} is already occupied!")
                await asyncio.sleep(2)
                await error.delete()
        else:
            error = await ctx.send(f"The field {msg.content} doesn't exist!")
            await asyncio.sleep(2)
            await error.delete()

        if not winner:
            await ctx.send("The game is over and nobody won!")


def setup(bot):
    bot.add_cog(GameCog(bot))
