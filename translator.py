from googletrans import Translator
import os


def translate(Ldest, Lsrc):

	translator = Translator()
		
	result1 = translator.translate("yes", dest = Ldest, src = Lsrc)

	print(result1)
	

translate('fr','en')
