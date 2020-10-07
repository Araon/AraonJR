from textblob import TextBlob
from googletrans import Translator

def translate(text):
	trans = Translator()
	x = trans.translate(text)
	return x.text


def sentiment(text):
	analysis = TextBlob(translate(text))
	if analysis.sentiment.polarity > 0:
		return 1
	elif analysis.sentiment.polarity == 0:
		return 0
		return -1

