from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

SUBREDDIT_URL = "https://reddit.com/r/worldnews"

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")


def get_headlines():
    """
    retrieve headlines from a subreddit on the Reddit API as a json
    :return: headlines as a string
    """
    # log into reddit account
    user_pass_dict = { 'user': '',  # put in your username here
                       'passwd': '',    # put in your password here
                       'api_type': 'json' }
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'Building basic Alexa Skill'})
    sess.post('https://www.reddit.com/api/login', data=user_pass_dict)
    # sleep since this might take a second or two
    time.sleep(1)
    url = SUBREDDIT_URL + "/.json?limit=5"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    return '... '.join([title for title in titles])


def test_get_headlines():
    """
    Method to test code that gets headlines from the reddit api
    :return:
    """
    titles = get_headlines()
    print(titles)


@app.route("/")
def homepage():
    return "Hello World!"


@ask.launch
def start_skill():
    welcome_message = "Would you like to hear the latest news updates?"
    return question(welcome_message)


@ask.intent("YesIntent")
def read_headlines():
    headlines = get_headlines()
    headlines_msg = "Here's what's happening around the world. {}".format(headlines)
    return statement(headlines_msg)


@ask.intent("NoIntent")
def no_headlines():
    bye_text = "I'll just.... go."
    return statement(bye_text)


if __name__ == '__main__':
    app.run(debug=True)
