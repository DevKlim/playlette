import polars as pl
import torch
from sklearn.model_selection import train_test_split

df = pl.read_csv('data/processed/cleaned_data.csv')

# Select features and target
features = df.select(['danceability', 'energy', 'valence']).to_numpy()
# For simplicity, let's map valence to a grayscale value
targets = df.select(['valence']).to_numpy()

# Split data
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

# Save tensors
torch.save((X_train, y_train), 'data/processed/train_data.pt')
torch.save((X_test, y_test), 'data/processed/test_data.pt')
