import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="", client_secret=""))


def main():
    uri_track = "spotify:track:29bXfCo3mQVzohwPJXohaU"
    playlist_id = "spotify:playlist:37i9dQZF1DWXnexX7CktaI"

    mother_track = feature_track(uri_track)
    new_playlist = analyze_playlist(mother_track, playlist_id)
    print(new_playlist)


def feature_track(uri_track):
    mother_track = sp.audio_features(uri_track)
    return mother_track[0]


def analyze_playlist(mother_track, playlist_id):
    playlist_features_list = ["track_name", "track_id", "preview_url", 'uri']

    playlist_df = pd.DataFrame(columns=playlist_features_list)

    playlist = sp.playlist(playlist_id)
    for track in playlist["tracks"]["items"]:
        playlist_features = {}
        playlist_features['track_name'] = track['track']['name']
        playlist_features['preview_url'] = track['track']['preview_url']
        playlist_features['track_id'] = track['track']['id']
        playlist_features['uri'] = track['track']['uri']

        track_features = feature_track(uri_track=playlist_features['uri'])

        similaridade = 0
        for feature in mother_track.keys():
            if track_features[feature] == mother_track[feature]:
                similaridade += 1

        if similaridade > 2:
            track_df = pd.DataFrame(playlist_features, index=[0])
            playlist_df = playlist_df.append(track_df)


    return playlist_df


if __name__ == '__main__':
    main()
