from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")


def get_headlines():
    """
    retrieve headlines from a subreddit on the Reddit API as a json
    :return: ??!?
    """
    pass


@app.route("/")
def homepage():
    return "Hello World!"


@ask.launch
def start_skill():
    welcome_message = "Would you like some news updates?"
    return question(welcome_message)


@ask.intent("YesIntent")
def read_headlines():
    headlines = get_headlines()
    headlines_msg = 'Here\'s what\'s happening around the world. {}'.format(headlines)
    return statement(headlines_msg)


@ask.intent("NoIntent")
def no_headlines():
    bye_text = "I'll just.... go."
    return statement(bye_text)


if __name__ == '__main__':
    app.run(debug=True)
