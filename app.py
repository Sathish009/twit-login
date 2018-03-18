#Flask==0.12.0
import requests
from flask import Flask, render_template, session, redirect, request, url_for, g
from twitter_utils import getRequestToken, getOauthVerifierUrl, getAccessToken
from user import User
from database import Database

app = Flask(__name__)
app.secret_key = '1234'
Database.initialise(database="learning",user="sathish",password="Password!23",host="localhost")

@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.loadFromDb(session['screen_name'])

@app.route("/")
def HomePage():
    #return "Hello World!!!"
    return render_template('home.html')

@app.route("/login/twitter")
def loginTwitter():
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    else:
        requestToken = getRequestToken()
        session['requestToken'] = requestToken
        return redirect(getOauthVerifierUrl(requestToken))

@app.route('/logout')
def logoutTwitter():
    session.clear()
    return redirect(url_for('HomePage'))

@app.route('/auth/twitter')
def authTwitter():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = getAccessToken(session['requestToken'], oauth_verifier)

    user = User.loadFromDb(access_token['screen_name'])
    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'],
                    access_token['oauth_token_secret'], None)
        user.saveToDb()

    session['screen_name'] = user.screen_name

    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    return render_template('profile.html', user=g.user)

@app.route('/search')
def search():
    query = request.args.get('q')
    tweets = g.user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query))

    tweet_texts = [{'tweet': tweet['text'], 'label': 'neutral'} for tweet in tweets['statuses']]

    for tweet in tweet_texts:
        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        json_response = r.json()
        label = json_response['label']
        tweet['label'] = label

    return render_template('search.html', content=tweet_texts)

#app.run(port=4995, debug=True)
app.run(port=4995)

