import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from langdetect import detect

# Dictionary mapping language codes to language names
lang_map = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'ny': 'Chichewa',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'iw': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'rw': 'Kinyarwanda',
    'ko': 'Korean',
    'ku': 'Kurdish (Kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'or': 'Odia (Oriya)',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots Gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'tt': 'Tatar',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'tk': 'Turkmen',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'ug': 'Uyghur',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu'
}

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
