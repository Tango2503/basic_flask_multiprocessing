from flask import Flask, render_template
from spotify_api import current_song, get_features
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    song_name, artist_name, track_id = current_song()
    tempo = get_features(track_id)
    bps = tempo/60
    bps = 1/bps
    
    return render_template('current_song_playing.html', song_title = song_name, artist = artist_name, bpm = tempo, bps = bps)

if __name__ == '__main__':
    app.run()