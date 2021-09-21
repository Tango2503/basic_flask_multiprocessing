import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

cid = 'c637b844a8744a54b81cb491f84a74b2'
secret = 'a385f5d5f75a4a95885dc2da865bcbc2'
username = "uu5g7t2grcblz06h67w0rjfk1"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = True

def current_song():
    scope = 'user-read-currently-playing'
    token = util.prompt_for_user_token(username, scope, client_id = cid, client_secret = secret,
                                        redirect_uri = 'http://127.0.0.1:5000/')
    if token:
        sp = spotipy.Spotify(auth = token)
        current_song = sp.currently_playing()
        song_name = current_song['item']['name']
        artist_name = current_song['item']['artists'][0]['name']
        track_id = current_song['item']['id']
    else:
        print("No token")
    return song_name, artist_name, track_id

def get_features(track_id):
    features = sp.audio_features(track_id)[0]
    tempo = features['tempo']
    return tempo
    

song_name, artist_name, track_id = current_song()
tempo = get_features(track_id)




# track_id = '5MKInakULmoBNApeB2ZB3A' # No features, weird



#audio_analysis = sp.audio_analysis(track_id)

        
