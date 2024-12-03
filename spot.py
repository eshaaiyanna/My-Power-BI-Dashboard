import requests
import pandas as pd

# Function to get Spotify access token
def get_spotify_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_data = auth_response.json()
    return auth_data['access_token']

# Function to search for a track and get its ID
def search_track(track_name, artist_name, token):
    query = f"{track_name} artist:{artist_name}"
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    response = requests.get(url, headers={
        'Authorization': f'Bearer {token}'
    })
    json_data = response.json()
    try:
        first_result = json_data['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except (KeyError, IndexError):
        return None

# Function to get track details (like album cover image URL)
def get_track_details(track_id, token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = requests.get(url, headers={
        'Authorization': f'Bearer {token}'
    })
    json_data = response.json()
    # Get the first album cover image URL
    image_url = json_data['album']['images'][0]['url']
    return image_url

# Your Spotify API Credentials
client_id = 'baa522ed729a4f0c8e9ed8f02716ebed'
client_secret = '4ddbd736bd414992933fa637dfdd1a50'

# Get Access Token
access_token = get_spotify_token(client_id, client_secret)

# Read your existing Spotify CSV file (replace with the actual file path)
df_spotify = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')

# Check if 'image_url' column exists, otherwise create it
if 'image_url' not in df_spotify.columns:
    df_spotify['image_url'] = None

# Loop through each row to get track details and add the album cover URL to the DataFrame
for i, row in df_spotify.iterrows():
    track_name = row['track_name']  # Adjust the column name as per your CSV
    artist_name = row['artist(s)_name']  # Adjust the column name as per your CSV
    track_id = search_track(track_name, artist_name, access_token)
    
    if track_id:
        image_url = get_track_details(track_id, access_token)
        # Update the image_url column with the fetched URL
        df_spotify.loc[i, 'image_url'] = image_url

# Save the updated DataFrame to a new CSV file (replace with your desired output file name)
df_spotify.to_csv('updated_spotify_data.csv', index=False)

print("Album cover URLs have been added and the updated file has been saved.")
