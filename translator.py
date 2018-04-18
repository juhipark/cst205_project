from googletrans import Translator
import os


def translate( Ldest, Lsrc):

	translator = Translator()
		
	result1 = translator.translate("what does that mean ?", dest = Ldest, src = Lsrc)
	result2 = translator.translate("what does that mean ?", dest = Ldest)

	print(result1)
	print(result2)
	

translate('fr','en')