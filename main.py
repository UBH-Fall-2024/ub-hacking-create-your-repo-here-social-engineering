# python3 -m venv venv
# New-Item requirements.txt
# source venv/bin/activate
# myvenv\scripts\activate.bat
# pip install -r .\requirements.txt OR

import os, json, random
from flask import Flask, request, redirect, session, url_for

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

client_id = '456a7e3b0864485aa14c091ec4bf8ca1'
client_secret = '47d4e57274df429cb8d25b5d3cd44a38'
redirect_uri = 'http://localhost:5000/callback'
scope = 'user-top-read' #can separate these with commas to add more fields

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True #for debugging purposes
) #authentication manager, how we authenticate. using authorization code in this ex

sp = Spotify(auth_manager=sp_oauth) #create spotify object

@app.route('/') #this just refers to the home page
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()): #if not logged in, get token to
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_top50'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_top50'))

#get user's playlist and print them out
@app.route('/get_top50')
def get_top50():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()): #if not logged in, get tohem to
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    songs = sp.current_user_top_tracks(time_range='Long_term', limit=50)
    #songs_html = '<br>'.join([item['name'] + ": " + item['artists'][0]['name'] + f'<img src={item['album']['images'][0]['url']} width=200 height=200>' for item in songs['items']]) #alt='{item['name']}'
    songs_html = ""

    randList = songs['items']
    random.shuffle(randList)
        
    for item in randList:
        
        song_name = item['name']
        artist_name = item['artists'][0]['name']
        album_image_url = item['album']['images'][0]['url']
        #songs_html += "<br>"
        song_html = f"<br> <img src={album_image_url} width=200 height=200> <br> {song_name}: {artist_name} "
        
        songs_html += "<br>"  # Add line break between songs
        songs_html += song_html
    
    return songs_html

@app.route('/get_top10')
def get_top10():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()): #if not logged in, get tohem to
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    songs = sp.current_user_top_tracks(time_range='Long_term', limit=10)
    #songs_html = '<br>'.join([item['name'] + ": " + item['artists'][0]['name'] + f'<img src={item['album']['images'][0]['url']} width=200 height=200>' for item in songs['items']]) #alt='{item['name']}'
    songs_html = ""
    
    randList = songs['items']
    random.shuffle(randList)
        
    for item in randList:
        
        song_name = item['name']
        artist_name = item['artists'][0]['name']
        album_image_url = item['album']['images'][0]['url']
        #songs_html += "<br>"
        song_html = f"<br> <img src={album_image_url} width=200 height=200> <br> {song_name}: {artist_name} "
        
        songs_html += "<br>"  # Add line break between songs
        songs_html += song_html
    
    return songs_html

#clear access token for logout
@app.route('/logout')
def logout():
    session.clear
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug = True)