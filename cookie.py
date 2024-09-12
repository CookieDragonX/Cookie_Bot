import discord
from discord.ext import commands, tasks
import youtube_dl
from random import choice
import cv2
import os
from PIL import GifImagePlugin
from mutagen.mp3 import MP3
client=commands.Bot(command_prefix='>')

game_status=["with my awesome father","Minecraft","Undertale","The Binding Of Isaac","**kill me please I am being held hostage**","Celeste","Hades","Skyrim","The Witcher 3","Slay The Spire","Paladins",
             "Fuck League Of Legends","TeamFight Tactics","Stardew Valley","Wizard Of Legend","Pokemon Emerald"]

@tasks.loop(seconds=120)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(game_status)))
    
@client.event
async def on_ready():
    change_status.start()
    print('Hello I have been born')
@client.command(name='hi', help='This is a way to say hi')
async def hi(ctx):
    if str(ctx.author)=='CookieDragonX#9854':
        await ctx.send('Hello father <3')
    elif str(ctx.author)=='strawberrymilk#2357' :
        await ctx.send("Hello mother <3")
    else :
        await ctx.send("You're not my real dad :(")
    
youtube_dl.utils.bug_reports_message = lambda: ''

def loadFromFolder(folder):
    stuff = []
    for filename in os.listdir(folder):
        stuff.append(os.path.join(folder,filename))
    return stuff

hugs=loadFromFolder(r"D:\Python stuffs\Cookie\hugs")
niceshit=["You are doing great!","You are more than enough!","Looking great!","Much love <3", "You are loved!!!","You're doing awesome!","Nice ass"]
@client.command(name='hug', help='Gib hog')
async def hug(ctx):
    await ctx.send(choice(niceshit))
    await ctx.send(file=discord.File(choice(hugs)))

foods=loadFromFolder(r'D:\Python stuffs\Cookie\food')

@client.command(name='food', help='yum')
async def food(ctx):
    await ctx.send(file=discord.File(choice(foods)))

drinks=loadFromFolder(r'D:\Python stuffs\Cookie\\drinks')
@client.command(name='cheers', help='cheers')
async def cheers(ctx,arg):
    await ctx.send(f'Hey {arg}! Have a drink on {ctx.author.display_name}!!!')
    await ctx.send(file=discord.File(choice(drinks)))

noises=["***Whooosh***","mlem","*blep*","**blop**","****slorp****"]
@client.command(name='sound',help='this make sounds yes')
async def sound(ctx):
    await ctx.send(choice(noises))


@client.command(name='flip',help='flip a coin')
async def flip(ctx):
    x=choice([1,0])
    if x==1 :
        await ctx.send("***It's heads!***")
    else :
        await ctx.send("***It's tails!***")

wins=["Ez","I WIN HAHAHAH","You kinda suck at this","Damn I'm awesome","lmao noob","HUZZAH","Do they not teach rock paper scissors in **human** school?"]

losses=["fuckin rigged","A temporary setback","fuck","sad","God shits in my dinner once again"]

draw=["We're equally matched","I see you're a man of culture yourself","I can do this all day"]

@client.command(name='rps',help='Play rock paper scissors with me! Type "rock" "paper" or "scissors"')
async def rps(ctx,arg):
    if(arg=="pula") :
        await ctx.send("----->scissors!!!")
        await ctx.send("I guess you know what happens now")
    else :
        if(arg!='rock' and arg!='paper' and arg!='scissors') :
            await ctx.send('Try typing "rock" "paper" or "scissors" am dumb :(')
        else :
            rps=choice(["rock","paper","scissors"])
            await ctx.send("----->"+rps+"!!!")
            if arg=="rock" :
                if rps=="scissors" :
                    await ctx.send(choice(losses))
                elif rps=="rock" :
                    await ctx.send(choice(draw))
                else :
                    await ctx.send(choice(wins))
            elif arg=="scissors" :
                if rps=="scissors" :
                    await ctx.send(choice(draw))
                elif rps=="rock" :
                    await ctx.send(choice(wins))
                else :
                    await ctx.send(choice(losses))
            else :
                if rps=="scissors" :
                    await ctx.send(choice(wins))
                elif rps=="rock" :
                    await ctx.send(choice(losses))
                else :
                    await ctx.send(choice(draw))
        
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '192.168.0.104' 
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
@client.command(name='play', help='This command plays music')
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Now playing:** {}'.format(player.title))

@client.command(name='stop', help='This command stops the music and makes the bot leave the voice channel')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()


beer=['beer','bere','piva','cerveza','beeer','beeeer','beere','beeere',"BERE",'Bere','Beer','BEER',"BEEER",'BEEEER','PIVA','Piva','Cerveza','CERVETA','BEEERE']
@client.event
async def on_message(message):
    for i in beer:
        if i in message.content:
            await message.channel.send("*Did someone say the magic word?*")
            await message.channel.send(file=discord.File(r"D:\Python stuffs\Cookie\drinks\beer.jpg"))
            return
    await client.process_commands(message)

balkanSongs=loadFromFolder(r"D:\Python stuffs\Cookie\balkan")
@client.command(name='balkan', help="No escape from balkan")
async def balkan(ctx):
    if (ctx.author.voice):
        channel=ctx.message.author.voice.channel
        voice=await channel.connect()
        source=discord.FFmpegPCMAudio(choice(balkanSongs))
        player=voice.play(source)
        audio=MP3(source)
        await ctx.send(">stop")

    else :
        await ctx.send("I'll want you with me if I play music :D")

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Ce faci coaie {member.mention}!')
client.run('OTE0NTEwMzE1OTk4Mjk4MTE0.YaOGGg.tdwV6WEaw1aweftHL9lMSp0tf80')
