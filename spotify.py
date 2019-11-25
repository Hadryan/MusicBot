import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import random 


class spotify():
    def __init__(self):
        self.credentials = self.get_credentials()
        self.sp = spotipy.Spotify(client_credentials_manager=self.credentials)
    
    # this places our credentials in the client manager for spotify
    def get_credentials(self):
        creds = SpotifyClientCredentials(client_id = '89ba12dbb318412baa7c3f1c642d17d9', client_secret='47689f35aa354d0dbe06d1b89323561d')
        return creds
 
    # this allows us to pick an indidvidual song from the list of songs retuned from spotipy search
    # expects a song/artist
    # returns song
    def get_song(self, input):
        result = self.sp.search(input)
        return result['tracks']['items'][0]

    # expects a song 
    def get_songid(self, song):
        return song['id']

    def get_artistid(self, song):
        return song['artists'][0]['id']

    #expects a list of genres
    def get_genre_tracks(self, genres):
        result = [] #{}
        for genre in genres:
            #result[genre] = []
           
           # normalizes string to allow for proper search
            # then reverts it back to original state
            genre.replace(' ', '+')
            tracklist = self.sp.search('genre:' + genre, 25)
            genre.replace('+', ' ')

            songs = tracklist['tracks']['items']
            for elem in songs:
                if(elem['name'].lower() in genre or elem['name'].lower() in 'song'):
                    continue
                else:
                    result.append((elem['name'], self.get_features(elem['id'])))#result[genre].append(( elem['name'], self.get_features(elem['id'])))
        return result 
   
   #expects song id, uri, urlid
    def get_features(self, input):
        result = self.sp.audio_features(input)
        return result[0]

    #expects artist id, uri, urlid
    def get_artist(self, input):
        return self.sp.artist(input)
        

    #expects artist id, uri, urlid
    def get_genres(self, input):
        result = self.sp.artist(input)
        return result['genres']

    def get_popularity(self, song):
        return song['popularity']



# this should be used as a struct to group the values we need from a given song
# in addition to allowing AI to search songs on its own  

class Song(spotify):
    def __init__(self, input=''):
        super().__init__()
        self.set_attributes(input)

    # attributes for Song this allows us to create an instance of Song
    # with and without input to allow AI to search for songs if needded
    def set_attributes(self, input):
        if(input != ''):
            self.track = self.get_song(input)
            self.track_id = self.get_songid(self.track)
            self.name = self.track['name']
            self.artist_id = self.get_artistid(self.track)
            self.artist = self.get_artist(self.artist_id)
            self.popularity = self.get_popularity(self.track)
            self.features = self.get_features(self.track_id)
            self.related_songs = self.get_related_songs()
        else:
            self.track = None
            self.track_id = None
            self.name = None
            self.artist_id = None
            self.artist = None
            self.popularity = None
            self.features = None
            self.related_songs = []

    def get_related_songs(self):
        genres = self.get_genres(self.artist_id)
        songs =  self.get_genre_tracks(genres)
        random.shuffle(songs)
        return songs

