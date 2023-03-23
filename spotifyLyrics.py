import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import requests
import lyricsgenius as lg
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QPlainTextEdit
import sys
import re
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


# ####    SPOTIFY INFO    ###

# scope = 'user-read-currently-playing'

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# result = sp.current_user_playing_track()
# songName = result['item']['name']
# songArtist = result['item']['artists'][0]['name']

# ### GENIUS LYRICS STUFF ###

# genius = lg.Genius('1ULpWkSwH6TGpL1QPsO6VT5dqSYgyRtlaGNjuMyokMJZMACfhBJLPw6wia3NeHw8')

# song = genius.search_song(songName, songArtist)
# print(song.lyrics)

class spotifyLyrics(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.qbtn = QPushButton('Update lyrics', self)
        self.qbtn.clicked.connect(self.updateLyrics)
        self.qbtn.resize(self.qbtn.sizeHint())
        self.qbtn.move(100, 50)

        self.lyricLabel = QPlainTextEdit(self)
        self.lyricLabel.move(50, 100)
        self.lyricLabel.resize(600, 700)

        self.setGeometry(300, 200, 700, 900)
        self.show()

    def updateLyrics(self):

        ### SPOTIFY STUFF ###
        scope = 'user-read-currently-playing'

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                                                       client_secret=os.getenv(
                                                           'CLIENT_SECRET'),
                                                       redirect_uri=os.getenv(
                                                           'REDIRECT_URI'),
                                                       scope=scope))

        result = sp.current_user_playing_track()
        if (result == None):
            self.lyricLabel.setPlainText("No song currently playing.")
            return

        songName = result['item']['name']
        songName = re.sub(r" ?\([^)]+\)", "", songName)
        songArtist = result['item']['artists'][0]['name']

        ### GENIUS LYRICS STUFF ###

        genius = lg.Genius(
            '1ULpWkSwH6TGpL1QPsO6VT5dqSYgyRtlaGNjuMyokMJZMACfhBJLPw6wia3NeHw8')

        song = genius.search_song(songName, songArtist)
        self.lyricLabel.setPlainText(song.lyrics)


def main():

    app = QApplication(sys.argv)
    ex = spotifyLyrics()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
