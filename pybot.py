'''
TODO: 
1.Implement cogs or something similar to cogs 
2.Add sentiment analyzer






'''
# Imports

from datetime import datetime
import discord
from discord.ext import commands
from discord.utils import find
import random
from asset import responces_gali, kami_responces, choices, responces_headpat, responces_bot
import asyncio
from discord.utils import get
import os
import youtube_dl
import shutil
from os import system
import logging
from dotenv import load_dotenv
from helper import worthless, slap, spank
from sentimentAnalyzer import sentiment
load_dotenv()

'''
nodemon --exec "Python" ./pybot.py
'''

PREFIX = ';'
client = commands.Bot(command_prefix = PREFIX)
ownerid = 322346259371393054

#Basic Startup procedures

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.idle, activity=discord.Game('and doing her best'))
	print('AraonJR is running.')
	starttime = datetime.now()
	print(starttime)
	f = open('botlog.txt','a')
	f.write('\n' + f'Bot Online from' f' {datetime.now().strftime("%c")}')
	f.close()	


@client.event
async def on_member_join(member):
	guild = member.guild
	if guild.system_channel is not None:
		to_send = 'Hey {0.mention} nice to meet you, Welcome to {1.name}!.'.format(member, guild)
		await guild.system_channel.send(to_send)
		
@client.event
async def on_member_remove(member):
	print(f'{member} has left the server on' f' {datetime.now().strftime("%c")}')
	leavetime(member)

def is_it_me(ctx):
	return ctx.author.id == ownerid

@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hey it\'s me, AraonJR {} sure looks cozy!'.format(guild.name))

'''

COMMANDS

'''



@client.command(aliases=['Ping','PING'])
async def ping(ctx):
	await ctx.send(f'Pongging you back at {round(client.latency * 100)}ms')


@client.command(aliases=['YO'])
async def yo(ctx):
	embed = discord.Embed(
		title = 'Commands',
		description = 'The following Commands can be performed with `;` as prefix',
		colour = discord.Colour.blue()
	)
	embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/651715103313362944/d8b5f4ee9746238ef82dd5a7a10a575b.webp')
	embed.add_field(name='`ping`', value='Ping of the bot',inline=True)
	embed.add_field(name='`gali`', value='Get bestowed with a random gali',inline=True)
	embed.add_field(name='`inv`', value='Generate an Invite to this Server',inline=True)
	embed.add_field(name='`poke`', value='Use this command as ;poke@mention to poke someone',inline=True)
	embed.add_field(name='`worth`', value='Use as ;worth @mention',inline=True)
	embed.add_field(name='`kami`', value='kami',inline=True)
	embed.add_field(name='`gibslap`', value='use as ;slap @mention',inline=True)
	embed.add_field(name='`toss`', value='do a coin flip',inline=True)
	embed.add_field(name='`gibspank`', value='use as ;gibspank @mention',inline=True)
	embed.add_field(name='`owner`', value='Notify the owner of this Bot',inline=True)
	embed.set_footer(text='Have a nice day!😄')
	await ctx.send(embed = embed)

@client.command(aliases=['Date','DATE'])
async def date(ctx):
	await ctx.send('Today\'s date is ' f' {datetime.now().strftime("%x")}')



@client.command(aliases=['OWNER','Owner','Master','master'])
async def owner(ctx):
	await ctx.send('I receive headpats from <@322346259371393054>')
	# print('Owner function used on' f' {datetime.now().strftime("%d/%m/%Y, %H:%M")}')


@client.command(aliases=['Gali','Khisti','khisti'])
async def gali(ctx):
	await ctx.send(random.choice(responces_gali))



@client.command(aliases=['Kami','KAMI'])
async def kami(ctx):
	await ctx.send(random.choice(kami_responces))


			
@client.command(aliases=['cls','Clear','Cls'])
async def clear(ctx, amount : int):
	await ctx.channel.purge(limit = amount)



@client.command(aliases=['Toss','TOSS','coinflip','Coinflip','COINFLIP'])
async def toss(ctx):
		await ctx.send(random.choice(choices))



@client.command(aliases=['inv','Invite','INVITE'])
async def invite(ctx):
		await ctx.send(await ctx.message.channel.create_invite())
 



@client.command()
async def boop(ctx):
	await ctx.author.send('boop!😸')
	await ctx.channel.purge(limit = 1)

@client.command(aliases=['pk'])
async def poke(ctx, user: discord.User):
	await user.send(f'{ctx.message.author} poked you')
	await ctx.channel.purge(limit = 1)


@client.command(pass_context=True)
async def worth(ctx, usr: str):
		worthless(usr)
		await ctx.send(file=discord.File('worthless.jpg'))

@client.command()
async def gibslap(ctx, *,  avamember : discord.Member=None):
    #userAvatarUrl = avamember.avatar_url
    slap(avamember.avatar_url)
    await ctx.send(file=discord.File('slap.jpg'))

@client.command()
async def gibspank(ctx, *,  avamember : discord.Member=None):
    #userAvatarUrl = avamember.avatar_url
    spank(avamember.avatar_url)
    await ctx.send(file=discord.File('spank.jpg'))

@client.command(aliases=['sentiment'])
async def senti(ctx):
	lastmessageID = ctx.channel.last_message_id
	msg = await ctx.fetch_message(lastmessageID)
	print(msg.content) 
	lastmsg = sentiment(msg.content)
	print(lastmsg) 
	if lastmsg == 1:
		await ctx.send_reaction("👍")
	if lastmsg == 0:
		await ctx.send_reaction("👌")
	else:
		await ctx.send_reaction("👎")


@client.command(aliases=['pl'])
async def poll(ctx,*,msg,avamember : discord.Member=None):
	channel = ctx.channel
	aut = ctx.author
	try:
		op1, op2 = msg.split("or")
		txt = f"React with ✅ for `{op1}` or ❎ for  `{op2}`"
	except: 
		await channel.send("Correct Syntax: [choice1] or [choice2]")
		return
	embed = discord.Embed(title=f"Poll by `{aut}`", description = txt, colour = discord.Colour.red())
	message_ = await channel.send(embed=embed)
	await message_.add_reaction("✅")
	await message_.add_reaction("❎")
	await ctx.message.delete()


'''
	This command does not work for some reasons, gets stuck at "getting user dp"
	update it dosent "get stuck", it makes the meme but fails to send it for some reason
	UPDATE: nevermind, the problem was not with the code it was me, extension should have been .jpg 
	and i've been using .png 
'''

#New stuff


'''
@client.command()
async def uptime(ctx):
	today = datetime.now().strftime("%x")
	uptime = (today - starttime)
	print(uptime)
	print("beep boop this part ran")
	await ctx.send(f'AraonJR is up for {uptime}')



@client.command()
async def padoru(ctx):
	channel = client.get_channel(620502311063781396)
	print('padoru ran')

	await channel.send('Hashire sori yo')
	await channel.send('Kaze no you ni')
	await channel.send('Tsukimihara wo')
	await channel.send('Padoru Padoru')
'''




# This part gives her Charecter

@client.command()
@commands.check(is_it_me)
async def say(ctx, *,msg):
	await ctx.message.delete()
	await ctx.send("{}".format(msg))


@client.event
async def on_message(message):
	if message.content == 'stfu':
		await message.channel.send('No u')
	elif message.content == 'bot':
		await message.channel.send(random.choice(responces_bot))
	elif message.content == 'headpat':
		await  message.channel.send(random.choice(responces_headpat))
	await client.process_commands(message)



'''
Error Handler

'''

@client.event
async def on_command_error(ctx,error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Please use correct command, You can use the `;yo` command for help')


@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Please specify how many messages to delete.')


## SERIOUS COMMANDS, DON'T CHANGE



##KICK COMMAND
@client.command(aliases=['Lathi','LATHI'])
@commands.check(is_it_me)
async def lathi(ctx, member : discord.Member, * , reason=None): 
	await member.kick(reason=reason)
	await ctx.send(f'kicked {member.mention} just to flex')
	f = open('botlog.txt','a')
	f.write('\n' + f'{member} kicked' f'{discord.member} on ' f' {datetime.now().strftime("%c")}')
	f.close()


##BAN COMMAND
@client.command(aliases=['Ban','BAN'])
@commands.check(is_it_me)
async def ban(ctx, member : discord.Member, * , reason=None): 
	await member.ban(reason=reason)
	await ctx.send(f'Banned {member.mention}💢')
	f = open('botlog.txt','a')
	f.write('\n' + f'{member} banned' f'{discord.member} on ' f' {datetime.now().strftime("%c")}')
	f.close()	


##UNBAN 
@client.command(aliases=['Unban','UNBAN'])
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user
		if(user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guid.unban(user)
			await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
			f = open('botlog.txt','a')
			f.write('\n' + f'{member} Unbanned' f' {datetime.now().strftime("%c")}')
			f.close()



#music part

@client.command(pass_context = True, aliases = ['j','joi'])
async def join(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice is not None:
		return await voice.move_to(channel)

	voice = await channel.connect()
	f = open('botlog.txt','a')
	f.write('\n' + f"Connected to {channel}" f' {datetime.now().strftime("%c")}')
	f.close()

	await ctx.send(f"Vibing with the guys in {channel} 🤙")

	await asyncio.sleep(1)

	voice.play(discord.FFmpegPCMAudio('./voices/greets/voice'+f'{random.randint(0,13)}.mp3'), after=lambda e: print("Greetings error: %s' % e") if e else None)
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.09



@client.command(pass_context=True, aliases=['l','lea'])
async def leave(ctx):

	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_connected():
		await voice.disconnect()
		await ctx.channel.purge(limit = 1)
		await client.change_presence(status=discord.Status.idle, activity=discord.Game("and doing her best"))
		await ctx.send(f"Bye {channel} 🙋")
		f = open('botlog.txt','a')
		f.write('\n' + f"Left the {channel} channel \n" f' {datetime.now().strftime("%c")}')
		f.close()
	else:
		await ctx.send("I don't think i'm in any voice channel")
		f = open('botlog.txt','a')
		f.write('\n' + f"Bot was told to leave voice channel, but was not in one from {channel} channel\n" f' {datetime.now().strftime("%c")}')
		f.close()


last_play = None


@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, *url: str):

	global last_play
	await join(ctx)
	await ctx.send(f":mag: `Searching:{url}`")

	def check_queue():
		Queue_infile = os.path.isdir("./Queue")
		if Queue_infile is True:
			DIR = os.path.abspath(os.path.realpath("Queue"))
			length = len(os.listdir(DIR))
			still_q = length - 1
			try:
				first_file = os.listdir(DIR)[0]
			except:
				print("No more queued song(s)\n")
				queues.clear()
				return
			main_location = os.path.dirname(os.path.realpath(__file__))
			song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
			if length != 0:
				print("Song done, playing next queued\n")
				print(f"Songs still in queue: {still_q}")
				song_there = os.path.isfile("song.mp3")
				if song_there:
					os.remove("song.mp3")
				shutil.move(song_path, main_location)
				for file in os.listdir("./"):
					if file.endswith(".mp3"):
						os.rename(file, 'song.mp3')


				voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
				voice.source = discord.PCMVolumeTransformer(voice.source)
				voice.source.volume = 0.20

			else:
				queues.clear()
				return

		else:
			queues.clear()
			print("No songs were queued before the ending of the last song\n")



	song_there = os.path.isfile("song.mp3")
	try:
		if song_there:
			os.remove("song.mp3")
			queues.clear()
			print("Removed old song file")
	except PermissionError:
		print("Trying to delete song file, but it's being played")
		await ctx.send("ERROR: Music playing")
		return


	Queue_infile = os.path.isdir("./Queue")
	try:
		Queue_folder = "./Queue"
		if Queue_infile is True:
			print("Removed old Queue Folder")
			shutil.rmtree(Queue_folder)
	except:
		print("No old Queue folder")

	voice = get(client.voice_clients, guild=ctx.guild)

	ydl_opts = {
		'format': 'bestaudio/best',
		'quiet': False,
		'outtmpl': "./song.mp3",
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	song_search = " ".join(url)
	songsource = song_search.split(sep='/')
	print(songsource)

	if 'open.spotify.com' in [songsource]:
		try:
			print("Downloading using Spotify")
			q_path = os.path.abspath(os.path.realpath("Queue"))
			system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + song_search)
			await ctx.send(f":musical_note: `Just Singing for you guys`")
			
		except:
			await ctx.send("Invaid Spotify URL")
	else:
		try:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				print("Downloading audio now\n")
				ydl.download([f"ytsearch1:{song_search}"])
				await ctx.send(f":musical_note: `Playing:{song_search}`")
		except:
			await ctx.send("Invaid URL,Use 'Songname Artistname' format")

	

	await client.change_presence(status=discord.Status.idle, activity=discord.Game('and singing'))
	voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.20


#timer based leaving 
	obj = object()
	last_play = id(obj)
	await asyncio.sleep(600)
	if last_play == id(obj):
		await leave(ctx)


@client.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_playing():
		print("Music paused")
		voice.pause()
		await ctx.send("Music Paused 🔈")
	else:
		print("Music not playing failed pause")
		await ctx.send("What should i pause?, there is nothing")


@client.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_paused():
		print("Resumed music")
		voice.resume()
		await ctx.send("Music resumed 🔊")
	else:
		print("Music is not paused")
		await ctx.send("Are you dense?")



@client.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):

	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_playing():
		print("Music stopped")
		voice.stop()
		await ctx.send("Music Stopped ⭕️")
	else:
		print("No music playing failed to stop")
		await ctx.send("Stop my ass")



queues = {}

@client.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, *url: str):
	Queue_infile = os.path.isdir("./Queue")
	if Queue_infile is False:
		os.mkdir("Queue")
	DIR = os.path.abspath(os.path.realpath("Queue"))
	q_num = len(os.listdir(DIR))
	q_num += 1
	add_queue = True
	while add_queue:
		if q_num in queues:
			q_num += 1
		else:
			add_queue = False
			queues[q_num] = q_num

	queue_path = os.path.abspath(os.path.realpath("Queue") + f"/song{q_num}.%(ext)s")

	ydl_opts = {
		'format': 'bestaudio/best',
		'quiet': True,
		'outtmpl': queue_path,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	song_search = " ".join(url)
	songsource = song_search.split(sep='/')
	print(songsource)

	if 'open.spotify.com' in [songsource]:
		try:
			print("Downloading using Spotify")
			q_path = os.path.abspath(os.path.realpath("Queue"))
			system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + song_search)
			print("This is a Spotify link")
			await ctx.send(f":musical_note: `Singing for you guys`")
		except:
			await ctx.send("Invaid Spotify URL")
	else:
		try:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				print("Downloading audio now\n")
				ydl.download([f"ytsearch1:{song_search}"])
				await ctx.send(f":musical_note: `Playing:{song_search}`")
		except:
			await ctx.send("Invaid URL,Use 'SongName ArtistName' format")


	await ctx.send("Adding song " + str(q_num) + " to the queue")

	print("Song added to queue\n")


@client.command(pass_context=True, aliases=['n', 'nex'])
async def next(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_playing():
		print("Playing Next Song")
		voice.stop()
		await ctx.send("Aye aye! onto the next song")
	else:
		print("No music playing")
		await ctx.send("What next? there is nothing to play")


@client.command(pass_context=True, aliases=['v', 'vol'])
async def volume(ctx, volume: int):

	if ctx.voice_client is None:
		return await ctx.send("Not connected to voice channel")
	f = open('botlog.txt','a')
	f.write('\n' + f'volume changed to {volume/100}' f' {datetime.now().strftime("%c")}')
	f.close()

	ctx.voice_client.source.volume = volume / 100
	await ctx.send(f"Changed volume to {volume}%")






#logging

def jointime(member):
	f = open('botlog.txt','a')
	f.write('\n' + f'{member} has joined a server on' f' {datetime.now().strftime("%c")}')
	f.close()

def leavetime(member):
	f = open('botlog.txt','a')
	f.write('\n' + f'{member} has left a server on' f' {datetime.now().strftime("%c")}')
	f.close()


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discordsystem.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)




client.run(os.getenv('BOT_TOKEN'))







