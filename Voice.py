import discord
from discord.ext import commands
from gtts import gTTS


class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Voice Cog is Ready")

    @commands.command(name="음성")
    async def play_tts(self, ctx, *args):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                embed = discord.Embed(title='오류 발생', description="음성 채널에 들어간 후 명령어를 사용 해 주세요!",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
                raise commands.CommandError("Author not connected to a voice channel.")

        text = ' '.join(args)
        tts = gTTS(text=text, lang='ko', slow=False)
        tts.save('voice.mp3')

        player = discord.FFmpegPCMAudio(source="[voice.mp3가 있는 위치]",
                                        options='-vn', executable="C:/ffmpeg/bin/ffmpeg")
        ctx.voice_client.play(player)

        embed = discord.Embed(title=f"{ctx.author.name}'s Say", description=text, color=discord.Color.orange())
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Voice(client))