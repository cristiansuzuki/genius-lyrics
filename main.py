import os
import dotenv
from dotenv import load_dotenv
import spotipy
import lyricsgenius as lg
import json
import time

dotenv.load_dotenv(dotenv.find_dotenv())

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
GENIUS_ACCESS_TOKEN = os.getenv('GENIUS_ACCESS_TOKEN')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

#variavel utilizada pelo spotify
scope = 'user-read-currently-playing'

oauth_object = spotipy.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                    client_secret=SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=SPOTIPY_REDIRECT_URI,
                                    scope=scope)

token_dict = oauth_object.get_access_token()
token = token_dict['access_token']

# Objeto do spotify criado !
spotify_object = spotipy.Spotify(auth=token)

# Objeto do genius criado
genius = lg.Genius(GENIUS_ACCESS_TOKEN)

# Pega a musica que está tocando atualmente
current = spotify_object.currently_playing()

# Função para continuar a rodar o script
while True:
    current = spotify_object.currently_playing()
    status = current['currently_playing_type']
    
    if status == 'track':
        artist_name = current['item']['album']['artists'][0]['name']
        song_title = current['item']['name']
        
        length = current['item']['duration_ms']
        progress = current['progress_ms']
        duracao = int(length/1000)
        
        song = genius.search_song(title=song_title, artist=artist_name)
        lyrics = song.lyrics
        print(lyrics)
        
        time.sleep(duracao)
    # Verifica se é um anuncio tocando
    elif status == 'ad':
        time.sleep(30)
        
