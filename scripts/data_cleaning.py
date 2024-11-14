# scripts/data_cleaning.py

import polars as pl

def clean_data(input_path, output_path):
    """Clean the processed data by removing tracks with missing audio features."""
    df = pl.read_csv(input_path)
    
    # Identify essential audio features to retain
    essential_features = [
        'danceability', 'energy', 'key', 'loudness', 'mode',
        'speechiness', 'acousticness', 'instrumentalness',
        'liveness', 'valence', 'tempo'
    ]
    
    # Drop rows with nulls in essential features
    df_cleaned = df.drop_nulls(subset=essential_features)
    
    # Save the cleaned data
    df_cleaned.write_csv(output_path)
    print(f"Cleaned data saved to {output_path}. Number of tracks: {len(df_cleaned)}")

if __name__ == "__main__":
    input_csv = 'data/processed/data.csv'
    output_csv = 'data/processed/cleaned_data.csv'
    clean_data(input_csv, output_csv)
