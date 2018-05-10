from flask import Flask, render_template, url_for, redirect, request,current_app, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from googletrans import Translator
from my_text import stop_words
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os
import ssl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)

class UsrLanguage(FlaskForm):
    user_language = StringField('Enter text...', validators=[DataRequired()])
    single_select = SelectField(u"", [DataRequired()],choices=[("fr", "French"), ("es", "Spanish"), ("ko", "Korean")],description=u"Choose Language",render_kw= None)	
    submit = SubmitField('Translate!')


def translate(user_input, Ldest, Lsrc):
    translator = Translator()
    result1 = translator.translate(user_input, dest=Ldest, src=Lsrc)
    return result1.text

def check_stopword(translate_word):
	for e in stop_words:
		if translate_word == e:
			return True
	return False

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


@app.route('/', methods=['GET', 'POST'])
def home():
    translated_word=None
    form = UsrLanguage()
    #default pics_lst each with images not found
    pics_lst = ["https://renderman.pixar.com/assets/camaleon_cms/image-not-found-4a963b95bf081c3ea02923dceaeb3f8085e1a654fc54840aac61a57a60903fef.png", "https://renderman.pixar.com/assets/camaleon_cms/image-not-found-4a963b95bf081c3ea02923dceaeb3f8085e1a654fc54840aac61a57a60903fef.png", "https://renderman.pixar.com/assets/camaleon_cms/image-not-found-4a963b95bf081c3ea02923dceaeb3f8085e1a654fc54840aac61a57a60903fef.png"]

    if request.method == 'POST':
        user_input = form.user_language.data
        print(user_input)
		
		
        lang = request.form.get('single_select')
        print(lang)

        #Translate user_input
        translated_word = translate(user_input, 'en', lang)
        print(translated_word)
        #pics_lst.clear()
        if(not check_stopword(translated_word)):
            #Update picture
            searched_src = (imageSearch(translated_word))
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
        return render_template('home.html', pics=pics_lst, form=form, trans="English Translation...")
    else:
        return render_template('home.html', pics=pics_lst, form=form, trans=translated_word)
		
if __name__ == "__main__":
    app.run(debug=True)		
		
