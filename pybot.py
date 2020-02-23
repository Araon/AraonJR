from datetime import datetime
import discord
from discord.ext import commands
import random
from asset import responces_gali , kami_responces, choices
import asyncio


client = commands.Bot(command_prefix = ';')


@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.idle, activity=discord.Game('and doing her best'))
	print('AraonJR is running.')


@client.event
# async def on_member_join(member):
# 	print(f'{member} has joined a server on' f' {datetime.now().strftime("%c")}')
# 	jointime(member)
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)
        
@client.event
async def on_member_remove(member):
	print(f'{member} has left the server on' f' {datetime.now().strftime("%c")}')
	leavetime(member)



#COMMANDS

@client.command(aliases=['Ping','PING'])
async def ping(ctx):
	await ctx.send(f'Pongging you back at {round(client.latency * 100)}ms')
	print('ping function used on' f' {datetime.now().strftime("%d/%m/%Y, %H:%M")}')


@client.command(aliases=['YO'])
async def yo(ctx):
	await ctx.send('Yo mate\ni can do the following stuff\n1. ;ping for current ping\n2. ;date for current date and time\n3. ;owner\n4. ;gali for random gali\n5. ;Kami for custom kami command\n6. ;toss for coinflip\n7. ;invite to generate an Invite\n8. ;say(your text) for Text to speech\n9. ;poke@mention to poke somebody\n10. ;boop to make the bot send you a dm')


@client.command(aliases=['Date','DATE'])
async def date(ctx):
	await ctx.send('the current date is ' f' {datetime.now().strftime("%x")}')
	print('Date function used on' f' {datetime.now().strftime("%d/%m/%Y, %H:%M")}')


@client.command(aliases=['OWNER','Owner','Master','master'])
async def owner(ctx):
	await ctx.send('Custom Bot made by Araon#8553')
	print('Owner function used on' f' {datetime.now().strftime("%d/%m/%Y, %H:%M")}')


@client.command(aliases=['Gali','Khisti','khisti'])
async def gali(ctx):
	await ctx.send(random.choice(responces_gali))
	print('Gali function used on' f' {datetime.now().strftime("%d/%m/%Y, %H:%M")}')


@client.command(aliases=['Kami','KAMI'])
async def kami(ctx):
	await ctx.send(random.choice(kami_responces))
	print('Kami function used on' f' {datetime.now().strftime("%d/%m/%Y, %H:%M")}')

			
@client.command(aliases=['cls','Clear','Cls'])
async def clear(ctx, amount : int):
	await ctx.channel.purge(limit = amount)
	print('clear function used on' f' {datetime.now().strftime("%d/%m/%Y, %H:%M")}')


@client.command(aliases=['Toss','TOSS','coinflip','Coinflip','COINFLIP'])
async def toss(ctx):
        await ctx.send(random.choice(choices))
        print('Toss function used on' f' {datetime.now().strftime("%d/%m/%Y, %H:%M")}')


@client.command(aliases=['inv','Invite','INVITE'])
async def invite(ctx):
		await ctx.send(await ctx.message.channel.create_invite())
		print('Invite function used on' f' {datetime.now().strftime("%d/%m/%Y, %H:%M")}')


@client.event
async def on_command_error(ctx,error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Pls use correct command')


@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Pls specify how many messages to delete.')



# @client.command(aliases=['Say','say'])
# async def tts(ctx, *, message: str):
# 	await ctx.send(message, tts=True)
# 	#await ctx.send("Anindya ei function ta bondho korte boleche :'(\nNa korle bot kick kore debe")	      
# 	print('TTS function used')



'''@client.command()
async def shutdown(ctx, amount = 1):
	await ctx.channel.purge(limit = amount)
	await ctx.bot.logout()
	await ctx.send('AraonJR is shutting down')'''


@client.command()
async def boop(ctx):
	await ctx.author.send('boop!')

@client.command()
async def poke(ctx, user: discord.User):
    await user.send('poke')
    await ctx.channel.purge(limit = 1)


'''@client.command()
async def padoru(ctx):
	channel = client.get_channel(620502311063781396)
	print('padoru ran')

	await channel.send('Hashire sori yo')
	await channel.send('Kaze no you ni')
	await channel.send('Tsukimihara wo')
	await channel.send('Padoru Padoru')'''

@client.event
async def on_message(message):
    # Whenever a user other than bot says "stfu"
    if message.content == 'stfu':
        await message.channel.send('No u')
    await client.process_commands(message)








## SERIOUS COMMANDS, DON'T CHANGE



##KICK COMMAND
@client.command(aliases=['Lathi','LATHI'])
async def lathi(ctx, member : discord.Member, * , reason=None): 
	await member.kick(reason=reason)
	await ctx.send(f'{member.mention} ke lathi marlam just to flex')
	f = open('discord.txt','a')
	f.write('\n' + f'{member} kicked' f'{discord.member} on ' f' {datetime.now().strftime("%c")}')
	f.close()
##BAN COMMAND
@client.command(aliases=['Ban','BAN'])
async def ban(ctx, member : discord.Member, * , reason=None): 
	await member.ban(reason=reason)
	await ctx.send(f'Banned {member.mention}')
	f = open('discord.txt','a')
	f.write('\n' + f'{member} banned' f'{discord.member} on ' f' {datetime.now().strftime("%c")}')
	f.close()	

##UNBAN 
@client.command(aliases=['Unban','UNBAN'])
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		users = ban_entry.user
		if(user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guid.unban(user)
			await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
			f = open('discord.txt','a')
			f.write('\n' + f'{member} Unbanned' f' {datetime.now().strftime("%c")}')
			f.close()








def jointime(member):
	f = open('discord.txt','a')
	f.write('\n' + f'{member} has joined a server on' f' {datetime.now().strftime("%c")}')
	f.close()

def leavetime(member):
	f = open('discord.txt','a')
	f.write('\n' + f'{member} has left a server on' f' {datetime.now().strftime("%c")}')
	f.close()


client.run('NjUxNzE1MTAzMzEzMzYyOTQ0.XeldIA.r6NLPjHL15JPTKzj5d5tkZVuNuU')

