from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from googletrans import Translator
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os
import ssl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)


pics_lst = ["http://leeford.in/wp-content/uploads/2017/09/image-not-found.jpg"]

class UsrLanguage(FlaskForm):
    user_language = StringField('Enter text...', validators=[DataRequired()])
    submit = SubmitField('Translate!')

def translate(user_input, Ldest, Lsrc):
    translator = Translator()
    result1 = translator.translate(user_input, dest=Ldest, src=Lsrc)
    return result1.text


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
        if (src[-3:] == 'png') or (src[-3:] == 'jpg'):
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
    if form.validate_on_submit():
        user_input = form.user_language.data
        print(user_input)

        #User choice of dropdown
        user_lang = 'fr'

        #Translate user_input
        translated_word = translate(user_input, 'en', user_lang)
        print(translated_word)

        #if(!check_stopword(translated_word)):
            #Update picture
        print(imageSearch(translated_word))
        #for src_url in imageSearch(translated_word):
         #   pics_lst[idex] = src_url
          #  print(pics_lst)
           # idex += 1

#       return redirect(url_for('home'))

    if translated_word == None:
        return render_template('home.html', pics=pics_lst, form=form, trans="English Translation...")
    else:
        return render_template('home.html', pics=pics_lst, form=form, trans=translated_word)
