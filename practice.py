from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import urllib
import os
from googletrans import Translator

def imageSearch(result):
	site = 'https://en.wikipedia.org/wiki/' + result
	req = Request(site, headers={'User-Agent' : 'Mozilla/5.0'})

site = 'https://en.wikipedia.org/wiki/Chair'
req = Request(site, headers={'User-Agent' : 'Mozilla/5.0'})

	resp = urlopen(req)
	bs_obj = BeautifulSoup(resp.read(), 'html.parser')

	count = 0
	pics_lst = []

	for tag in bs_obj.findAll("img"):
		count+=1
		if(count < 4):
			target = tag.get('src')
			pics_lst.append(target)

	for i in pics_lst:
		print(i)

def main():
	trans = Translator()

	r = trans.translate('chaise')

	print(r)
main()
