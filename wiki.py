import time
import wikipedia

def sendWiki(text):
    try:
        sh = wikipedia.summary(text, sentences = 3)
        pgContent = sh
    except:
        pgContent = 'Search term is too broad, be more specific '
        
    return pgContent

