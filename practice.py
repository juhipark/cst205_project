from my_text import stop_words

def check_stopword(translate_word):
	for e in stop_words:
		if translate_word == e:
			return True
	return False

def main():
	word = 'chair'
	print(check_stopword(word))
main()
