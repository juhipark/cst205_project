from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from PIL import Image
import urllib
import os
from googletrans import Translator

site = 'https://en.wikipedia.org/wiki/Chair'
req = Request(site, headers={'User-Agent' : 'Mozilla/5.0'})

resp = urlopen(req)
bs_obj = BeautifulSoup(resp.read(), 'html.parser')

count = 0

for tag in bs_obj.findAll("img"):
	count+=1
	if(count < 4):
		temp = tag.get('alt')
		target = tag.get('src')
		print(target)

"""
Save image list as pics_lst
"""
