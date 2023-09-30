import streamlit as st
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from langdetect import detect

# Get lang map from JSON file
with open('lang_map.json', 'r') as f:
    lang_map = json.load(f)

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
    # Perform a Spotify API search for the playlist name
    results = sp.search(q=playlist_name, type='playlist')

    # Get the playlist ID from the search results
    playlist_id = results['playlists']['items'][0]['id']

    return playlist_id


def main():
    st.title("Spotify Filter App")
    st.write("Welcome to the Spotify Filter App!")

    # Use st.form to wait for user input
    with st.form(key='playlist_form'):
        # Get Playlist Name from User
        playlist_name = st.text_input("Enter a Spotify Playlist Name")
        submitted = st.form_submit_button('Submit')

    # Get Playlist ID from Spotify API if playlist name is entered
    playlist_id = None
    if submitted:
        playlist_id = get_playlist_id(playlist_name)

    # Display Playlist ID for the user
    if playlist_id:
        st.write("The playlist ID for this playlist is:")
        st.write(playlist_id)

        # Get Playlist Tracks from Spotify API
        playlist_tracks = sp.playlist_tracks(playlist_id)

        # Detect the language of each track in the playlist
        languages = []
        for track in playlist_tracks['items']:
            languages.append(detect(track['track']['name']))

        # Map each track to its language and display only the unique languages
        unique_languages = list(set(languages))
        
        # Map the unique languages to the actual language name
        language_names = []
        for language in unique_languages:
            language_names.append(lang_map[language])

        st.write("The playlist contains tracks in the following languages:")
        st.write(language_names)

    
    
if __name__ == "__main__":
    main()
