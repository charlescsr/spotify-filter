import streamlit as st
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from langdetect import detect

# Get Spotify API credentials from streamlit secrets
client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]

# Spotify API authentication
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist_id(playlist_name):
    """
    Returns the playlist ID for a given playlist name.
    """
    playlist_id = None
    playlists = sp.user_playlists("spotify")
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                break
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return playlist_id


def main():
    st.title("Spotify Filter App")
    st.write("Welcome to the Spotify Filter App!")

    # Get Playlist Name from User
    playlist_name = st.text_input("Enter a Spotify Playlist Name")

    # Get Playlist ID from Spotify API
    playlist_id = get_playlist_id(playlist_name)

    # Get Playlist Tracks from Spotify API
    playlist_tracks = sp.playlist_tracks(playlist_id)

    # 

    
    
if __name__ == "__main__":
    main()
