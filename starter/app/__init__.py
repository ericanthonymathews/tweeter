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
    def sort_by_date(item):
        date_info = item['date'].split("/")
        year = int(date_info[2])
        month = int(date_info[0])
        day = int(date_info[1])
        return date(year, month, day)
    sorted_feed = sorted(tweets, key=lambda x: sort_by_date(x))
    return render_template("feed.html", feed=sorted_feed)


@app.route('/new', methods=['GET', 'POST'])
def create_tweet():
    form = TweetForm()

    if form.validate_on_submit():
        new_tweet = {
            "id": len(tweets),
            "author": form.data['author'],
            "tweet": form.data['tweet'],
            "date": date.today().strftime("%-m/%-d/%y"),
            "likes": 0
        }
        tweets.append(new_tweet)
        return redirect('/feed', 302)

    if form.errors:
        return form.errors

    return render_template("new_tweet.html", form=form)


# @app.route("/like")
# def add_like():
