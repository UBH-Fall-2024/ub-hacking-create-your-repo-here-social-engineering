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

client_id = 'c989d8c539aa4057ba2754ff23fc7223'
client_secret = '1191724783924d189e55d5b2203f0089'
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


CorrectList = []

#Basically Does the same thing as get_top50 excpet turns it into a list rather than a string for html.
#This List should stay in the backend and only be pushed to the frontend through the check_answer function
@app.route('/generate_Correct_List')
def generate_Correct_List():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()): #if not logged in, get tohem to
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    songs = sp.current_user_top_tracks(time_range='Long_term', limit=50)

    CorrectList =([item['name'] for item in songs['items']])
    return



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
    songs_html = ""
    
    randList = songs['items']
    random.shuffle(randList)
        
    for item in randList:
        
        song_name = item['name']
        artist_name = item['artists'][0]['name']
        album_image_url = item['album']['images'][0]['url']
        song_html = f"<br> <img src={album_image_url} width=200 height=200> <br> {song_name}: {artist_name} "
        
        songs_html += "<br>"  # Add line break between songs
        songs_html += song_html
    
    return songs_html

@app.route('/get_topX')
def get_topX(songCount, length):
    if not sp_oauth.validate_token(cache_handler.get_cached_token()): #if not logged in, get tohem to
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    songs = sp.current_user_top_tracks(time_range= length, limit=songCount)
    songs_html = ""
    
    randList = songs['items']
    random.shuffle(randList)
        
    for item in randList:
        
        song_name = item['name']
        artist_name = item['artists'][0]['name']
        album_image_url = item['album']['images'][0]['url']
        song_html = f"<br> <img src={album_image_url} width=200 height=200> <br> {song_name}: {artist_name} "
        
        songs_html += "<br>"  # Add line break between songs
        songs_html += song_html
    
    return songs_html



#Compares the list returned from the website against the correct ordering. Returned List must be a LIST OF SONG NAMES
#Correct list is generated by running generate_Correct_List()
@app.route('/check_answer')
def check_answer(list):
    correct = 0
    total = 0
    percent = 0     
    topX = []       #Correct List for number of songs they want to include

    #Iterates Through Returned List and compares to CorrectList
    for i in list:
        if (list[i] == CorrectList[i]):
            correct+=1
            total+=1
        else:
            total+=1
        topX[i]=CorrectList[i]

    percent = (correct/total) *100


    retVal = [topX, correct, total, percent]
    return retVal


#clear access token for logout
@app.route('/logout')
def logout():
    session.clear
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug = True)
