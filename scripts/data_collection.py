# scripts/data_collection.py

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import polars as pl

# Load credentials from environment variables
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Spotify CLIENT_ID and CLIENT_SECRET must be set in environment variables.")

# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def fetch_playlist_tracks(playlist_id):
    """Fetch all tracks from a Spotify playlist."""
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        for item in results['items']:
            track = item['track']
            if track:
                tracks.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artists': ', '.join(artist['name'] for artist in track['artists']),
                    'uri': track['uri']
                })
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return pl.DataFrame(tracks)

def fetch_audio_features(track_ids):
    """Fetch audio features for a list of track IDs."""
    features_list = []
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        features = sp.audio_features(batch)
        # Filter out None responses
        features = [feat for feat in features if feat]
        features_list.extend(features)
    return pl.DataFrame(features_list)

if __name__ == "__main__":
    playlist_id = '37i9dQZF1DXcBWIGoYBM5M'
    df_tracks = fetch_playlist_tracks(playlist_id)
    df_tracks.write_csv('data/raw/tracks.csv')
    print(f"Fetched {len(df_tracks)} tracks from playlist {playlist_id}.")
    track_ids = df_tracks['id'].to_list()
    df_features = fetch_audio_features(track_ids)
    df = df_tracks.join(df_features, left_on='id', right_on='id', how='left')
    df.write_csv('data/processed/data.csv')
    print(f"Fetched audio features for {len(df_features)} tracks.")