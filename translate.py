from googletrans import Translator
trans = Translator()
text = input()
x = trans.translate(text)

print(x.text)