"""
Course: CST205: Multimedia Design & Progmng
Title: Picture Dictionary 
Project Description: Team17 Collaborated to create multi-language dictionary 
					  that displays three randomized images 

GitHub Link: https://github.com/juhipark/cst205_project.git

#In case flickr API exceed limit, below are new set of API Auth. Key
public = 'f3ddaa6e238bdb2cbba67f415f94f8ea' 
secret = '2ca9067a250f47d2'

#Contribution:
Juhi Park: I created image display in carousel format with three default image values.
                        I worked on the formatting of the webpage and grouped each of the widgets within a well and applied colors.
                        I also coded for linking up the WTF to get user words as well as making sure that the application
                        can find the updated source url for the images.

Clement Davin: I worked on creating 2 dropdowns which allows the user to 
				choose the source(what language the word is in)of the language 
				and the destination(what language it will be translated to).
				I was also responsible for working on the code for the translation using
				googletrans API.

Cesar Aldrete: I worked on webscraping the images from Wikipedia using beautiful soup.
				Webscraping was not working how we wanted. We decided to use an Image API(Flickr).
				I was responsible for providing the code for the FickrAPI as well. Along side with 
				Clement we were able to get the translation code with googletrans API to work.



"""

from flask import Flask, render_template, url_for, redirect, request,current_app, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from googletrans import Translator
from my_text import stop_words
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from flickrapi import FlickrAPI
import os
import ssl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)

#Grabs the source language and destination language
#for the word translation
class UsrLanguage(FlaskForm):
	user_language = StringField('Enter text...', validators=[DataRequired()])
	#Language source
	from_select = SelectField(u"", [DataRequired()],choices=[("en","English"),("fr", "French"),("de","German"), 
							("ga","Irish"),("it","Italian"),("'ja","Japanese"),("ko", "Korean"),("pt","Portuguese"),
							("ru","Russian"),("es", "Spanish"),("tr","Turkish")],
							description=u"Translate from",render_kw= None)	
	#Language destination
	to_select = SelectField(u"", [DataRequired()],choices=[("en","English"),("fr", "French"),("de","German"), 
							("ga","Irish"),("it","Italian"),("'ja","Japanese"),("ko", "Korean"),("pt","Portuguese"),
							("ru","Russian"),("es", "Spanish"),("tr","Turkish")],
							description=u"Choose Translated Language",render_kw= None)
   
	submit = SubmitField('Translate!')

#translates the word that the user inputs
#Googletrans API Documntation: http://py-googletrans.readthedocs.io/en/documentation/
def translate(user_input, Ldest, Lsrc):
	translator = Translator()
	result1 = translator.translate(user_input, dest=Ldest, src=Lsrc)
	return result1.text

#returns T||F if the translated word is a stop word. No image will display if T
def check_stopword(translate_word):
	for e in stop_words:
		if translate_word == e:
			return True
	return False

#Flickr API image searh
#returns a list of images with tags that match the translated wordi
#FlickrAPI Documentation: https://www.flickr.com/services/api/flickr.photos.search.html
def imageSearch2(result):
	public = '9c6109575396742440a08a2c2565448d'
	secret = 'e72741e04719dbf8'

	flickr = FlickrAPI(public, secret, format='parsed-json')
	im = 'url_c'	
	search = flickr.photos.search(tags=result, per_page=200, extras=im)
	images = search['photos']
	
	new_pics_lst = []

	for i in range(len(images['photo'])):
		if im in images['photo'][i]:
			new_pics_lst.append(images['photo'][i][im])
	return new_pics_lst
"""
#CURRENTLY NOT IN USE
#Wikipedia image webscraping search
#Grabs the html image 'src' from wikipedia searchi
#Partial code grabbed from iLearn BS4 sample
def imageSearch(result):
    ctx = ssl._create_unverified_context()
    site = 'https://en.wikipedia.org/wiki/' + result
    req = Request(site, headers={'User-Agent' : 'Mozilla/5.0'})

    resp = urlopen(req, context=ctx)
    bs_obj = BeautifulSoup(resp.read(), 'html.parser')

    new_pics_lst = []
    #getting at least three images
    for tag in bs_obj.findAll("img"):
        target = tag.get('src')
        new_pics_lst.append(target)

    #check if all of these new_pics_lst are valid image links
    index = 0
    for src in new_pics_lst:
        #check if extension is either png / jpg
        if(src[-3:] == 'jpg'):
            #don't do anything
            print(new_pics_lst[index])
        else:
            #erase that src b/c it is not valid
            del new_pics_lst[index]
        index += 1

    return new_pics_lst
"""

@app.route('/', methods=['GET', 'POST'])
def home():
	translated_word=None
	form = UsrLanguage()

    #default pics_lst each with images not found
	pics_lst = ["https://renderman.pixar.com/assets/camaleon_cms/image-not-found-4a963b95bf081c3ea02923dceaeb3f8085e1a654fc54840aac61a57a60903fef.png",
				"https://renderman.pixar.com/assets/camaleon_cms/image-not-found-4a963b95bf081c3ea02923dceaeb3f8085e1a654fc54840aac61a57a60903fef.png",
				"https://renderman.pixar.com/assets/camaleon_cms/image-not-found-4a963b95bf081c3ea02923dceaeb3f8085e1a654fc54840aac61a57a60903fef.png"]

	if request.method == 'POST':
		user_input = form.user_language.data
		print(user_input)
		
		from_lang = request.form.get('from_select')
		to_lang = request.form.get('to_select')

        #Translate user_input to find english image of it
		translated_word = translate(user_input, 'en', from_lang)
		# Then translate in the language asked
		translated_word_print = translate(user_input, to_lang, from_lang)
		
		print(translated_word)
		if(not check_stopword(translated_word)):
                        #Update picture
			searched_src = (imageSearch2(translated_word))
                        #check when searched_src
			if(len(searched_src) >= 3):
				for c in range(0,3):
					pics_lst[c] = searched_src[c]
			elif(len(searched_src) == 2):
				pics_lst[0] = searched_src[0]
				pics_lst[1] = searched_src[1]
			elif(len(searched_src) == 1):
				pics_lst[0] = searched_src[0]        
        #return redirect(url_for('home'))

	if translated_word == None:
		return render_template('home.html', pics=pics_lst, form=form, trans="Translated word here...")
	else:
		return render_template('home.html', pics=pics_lst, form=form, trans=translated_word_print)

if __name__ == "__main__":
    app.run(debug=True)
