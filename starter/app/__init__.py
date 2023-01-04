from flask import Flask, render_template, redirect
from .config import Config
from random import choice
from .tweets import tweets
from .form.form import TweetForm
from datetime import date

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    tweet = choice(tweets)
    return render_template("index.html", tweet=tweet)


@app.route('/feed')
def feed():
    return render_template("feed.html", feed=tweets)

@app.route('/new', methods=['GET', 'POST'])
def create_tweet():
    form = TweetForm()

    if form.validate_on_submit():
        new_tweet = {
            "id": len(tweets),
            "author": form.data['author'],
            "tweet": form.data['tweet'],
            "date": date.today(),
            "likes": 0
        }
        tweets.append(new_tweet)
        return redirect('/feed', 302)
    
    if form.errors:
        return form.errors

    return render_template("new_tweet.html", form=form)
