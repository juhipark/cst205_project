from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from googletrans import Translator

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

def imageSearch():


@app.route('/', methods=['GET', 'POST'])
def home():
    form = UsrLanguage()
    if form.validate_on_submit():
        user_input = form.user_language.data
        print(user_input)    
        
        #User choice of dropdown
        user_lang = 'fr'

        #Translate user_input
        print(translate(user_input, 'en', user_lang))

        #Update picture        
        pics_lst[0] = "chair1"
        pics_lst[1] = "chair2"
        
        return redirect(url_for('home'))

    return render_template('home.html', pics=pics_lst, form=form)
