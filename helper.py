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
		print('getting user dp')
	except OSError:
		user = Image.open('./user/user1.jpg')
		print("Fallback using default DP")# gets the defult dp
	img = Image.open('./user/Araonjr.png', 'r')# gets bot's dp
	background = Image.open('./Assets/slap/slap.jpg')# fetches the asset
	offset = (335,165)
	background.paste(img, offset)
	profile = user.resize((100,100))
	poffset = (125,180)
	background.paste(profile, poffset)
	background.save('slap.jpg')

