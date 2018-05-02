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

pics_lst = ["test1", "test2"]

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

    count = 1
    new_pics_lst = []
    #getting at least three images
    for tag in bs_obj.findAll("img"):
        count += 1
        if(count < 5):
            target = tag.get('src')
            new_pics_lst.append(target)
    
    #check if all of these new_pics_lst 
    #are valid image links

    return new_pics_lst


@app.route('/', methods=['GET', 'POST'])
def home():
    form = UsrLanguage()
    if form.validate_on_submit():
        user_input = form.user_language.data
        print(user_input)

        #User choice of dropdown
        user_lang = 'fr'

        #Translate user_input

        translated_word = translate(user_input, 'en', user_lang)
        print(translated_word)

        #Update picture
        print(imageSearch(translated_word))
        pics_lst[0] = "chair1"
        pics_lst[1] = "chair2"

        return redirect(url_for('home'))

    return render_template('home.html', pics=pics_lst, form=form)
