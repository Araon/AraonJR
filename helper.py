from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO
import requests

# meme_there = os.path.isfile("worthless.jpg")
# if meme_there:
# 	os.remove("worthless.jpg")



def worthless(name):
	name = name
	image = Image.open('./assets/worthless/meme.jpg')
	draw = ImageDraw.Draw(image)
	fontsize = 32
	font = ImageFont.truetype('./assets/worthless/Roboto-Bold.ttf', fontsize)
	(x, y) = (155, 100)
	msg = (f'{name}'+'\'s\nOpinion')
	message = msg
	color = 'rgb(0,0,0)'
	draw.text((x, y), message, fill=color, font=font)
	image.save(f'worthless.jpg')


def slap(url):
	responce = requests.get(url)
	try:
		user = Image.open(BytesIO(responce.content))
	except OSError:
		user = Image.open('./user/user1.jpg')
	img = Image.open('./user/Araonjr.png', 'r') # gets bot's dp
	background = Image.open('./Assets/slap/slap.jpg') # fetches the asset
	offset = (335,165)
	background.paste(img, offset)
	profile = user.resize((100,100))
	poffset = (125,180)
	background.paste(profile, poffset)
	background.save('slap.jpg')

def spank(url):
	responce = requests.get(url)
	try:
		user = Image.open(BytesIO(responce.content))
	except OSError:
		user = Image.open('./user/user1.jpg')
	img = Image.open('./Assets/profilepic/Araonjr.png')
	img = img.resize((190,240))
	background = Image.open('./Assets/spank/spank.jpg')
	offset = (745,45)
	background.paste(img, offset)
	profile = user.resize((240,240))
	poffset = (1200,340)
	background.paste(profile, poffset)
	background.save('spank.jpg')



#spank('https://cdn.discordapp.com/avatars/651715103313362944/d8b5f4ee9746238ef82dd5a7a10a575b.webp')