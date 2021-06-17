import discord
from urllib.error import HTTPError
from discord.ext import commands, tasks
import os
from discord.player import FFmpegPCMAudio
import youtube_dl as yt
import urllib
from PIL import Image
import asyncio
import sys
import urllib.request
import re

# declaring global path going up one directory
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def picConverter(url):
    # building the opener to download user avatar
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    filename = rf"{dir_path}\Media\image.jpg"
    try:
        urllib.request.urlretrieve(url, filename)
    except FileNotFoundError:
        os.makedirs(rf"{dir_path}\Media")
        urllib.request.urlretrieve(url, filename)
    return filename


def get_video_id(url):
    if 'youtube' in url:
        vID = url.split('watch?v=')[1]
    elif 'youtu.be' in url:
        vID = url.split('youtu.be/')[1]
    else:
        html = urllib.request.urlopen(
            f'https://www.youtube.com/results?search_query={url}')
        video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
        vID = video_ids[0]
        url = f'https://www.youtube.com/watch?v={vID}'
    return vID, url


def download(url):
    video_name, url = get_video_id(url)
    path = fr'{dir_path}\songs'
    downloaded_songs = os.listdir(path)
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': fr'{dir_path}\FFMPEG\ffmpeg.exe',
            'outtmpl': fr'{path}\{video_name}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]}
        if fr'{video_name}.mp3' in downloaded_songs:
            pass  # song already downloaded
        else:
            try:
                with yt.YoutubeDL(ydl_opts) as ydl:
                    ydl.download((url,))
            except Exception as e:  # Download failed
                type, value, traceback = sys.exc_info()
                errorlog = open('errorlog.txt', 'a+')
                errorlog.write(
                    f'Type: {type}\tValue: {value}\tTraceback: {traceback}\n')
                errorlog.close()
                print('Download failed, error has been logged')
    except:
        pass

    return fr'{path}\{video_name}.mp3'


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.vc = None
        self.skip = False
        self.playing = None
        try:
            path = fr'{dir_path}\songs'
            os.makedirs(path)
        except:  # path already exists
            pass

    @tasks.loop(seconds=5.0)
    async def loop_queue(self):
        if self.queue:
            self.vc.play(discord.FFmpegPCMAudio(executable=r'E:\Modules\FFMPEG\bin\FFMPEG.exe',
                                                source=self.queue[0]))
            self.playing = self.queue[0]
            print(self.playing)
            del self.queue[0]
            while self.vc.is_playing():
                await asyncio.sleep(0.1)
                if self.skip == True:
                    self.vc.stop()
                    self.skip = False
            if not self.queue:
                await self.vc.disconnect()
        else:
            self.loop_queue.stop()

    @commands.command()
    async def skip(self, ctx):
        self.skip = True
        await ctx.send('Song has been skipped!')

    @commands.command()
    async def stop(self, ctx):
        self.queue = []
        self.skip = True
        await ctx.send('Music has been stopped!')

    @commands.command()
    async def queue(self, ctx):
        ydl_opts = {
            'ignoreerrors': True
        }
        q_embed = discord.Embed(title='Queue:')
        if self.queue:
            with yt.YoutubeDL(ydl_opts) as ydl:
                x = 1
                for path in self.queue:
                    video_id = path.split('\songs')[1][1:12]
                    video_url = f'https://www.youtube.com/watch?v={video_id}'
                    data = ydl.extract_info(video_url, download=False)
                    video_name = data.get('title')
                    q_embed.add_field(
                        name=f'{x}.', value=video_name, inline=True)
                    x += 1
                await ctx.send(embed=q_embed)
        else:
            await ctx.send('Es sind keine Lieder in der Queue!')

    @commands.command()
    async def playing(self, ctx):
        ydl_opts = {
            'ignoreerrors': True
        }
        with yt.YoutubeDL(ydl_opts) as ydl:
            video_id = self.playing.split('\songs')[1][1:12]
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            data = ydl.extract_info(video_url, download=False)
            video_name = data.get('title')
            p_embed = discord.Embed(title='Playing:')
            p_embed.add_field(name='Current Song: ', value=video_name)
            await ctx.send(embed=p_embed)

    @commands.command(pass_context=True, name='play', aliases=['p'])
    async def play(self, ctx, *url):
        url = '+'.join(url)
        error = False
        channel = None
        try:
            path = download(url)
        except HTTPError as e:
            print('HTTPError has been logged')
            errorlog = open('errorlog.txt', 'a+')
            errorlog.write(f'Errorcode: {e.code}\tURLError: {e.reason}\n')
            errorlog.close()
            error = True

        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send('You have to be in a voice chat to play music!')
            return
        if error == False and channel != None:
            embed = discord.Embed(
                title='Wildus-Music-Bot', color=0x00ff00)
            embed.add_field(
                name='Your song has been added to queue!', value='Have patience please...', inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Video couldn't be downloaded, please try again in 5 seconds!")

        try:
            vc = await channel.connect()
        except:
            pass  # already in voice channel
        try:
            self.queue.append(path)
            try:
                self.vc = vc
                self.loop_queue.start()
            except:
                pass  # loop already running
        except Exception as e:
            try:
                await self.vc.disconnect()
            except UnboundLocalError:
                pass  # not in a voice channel


def setup(bot):
    bot.add_cog(MusicCog(bot))
