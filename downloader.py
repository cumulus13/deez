import requests
import os

BASE_URL = 'https://api.deezer.com'

def search_artist(artist_name):
    response = requests.get(f'{BASE_URL}/search/artist', params={'q': artist_name})
    response.raise_for_status()
    return response.json()['data'][0]

def get_artist_albums(artist_id):
    response = requests.get(f'{BASE_URL}/artist/{artist_id}/albums')
    response.raise_for_status()
    return response.json()['data']

def get_album_tracks(album_id):
    response = requests.get(f'{BASE_URL}/album/{album_id}/tracks')
    response.raise_for_status()
    return response.json()['data']

def download_track_preview(track_info):
    preview_url = track_info['preview']
    response = requests.get(preview_url, stream=True)
    response.raise_for_status()
    file_name = f"{track_info['title']} - {track_info['artist']['name']}.mp3"
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f'{file_name} downloaded successfully.')

def main():
    artist_name = input('Enter the artist name: ')
    artist_info = search_artist(artist_name)
    print(f"Found artist: {artist_info['name']}")

    albums = get_artist_albums(artist_info['id'])
    for i, album in enumerate(albums):
        print(f"{i+1}. {album['title']}")

    album_index = int(input('Select an album number: ')) - 1
    selected_album = albums[album_index]
    print(f"Selected album: {selected_album['title']}")

    tracks = get_album_tracks(selected_album['id'])
    for i, track in enumerate(tracks):
        print(f"{i+1}. {track['title']}")

    track_selection = input('Enter the track numbers to download (e.g., 1,2,3 or 1-3 or a for all): ')
    
    if track_selection.lower() == 'a':
        selected_tracks = range(1, len(tracks) + 1)
    else:
        selected_tracks = []
        ranges = track_selection.split(',')
        for item in ranges:
            if '-' in item:
                start, end = item.split('-')
                selected_tracks.extend(range(int(start), int(end) + 1))
            else:
                selected_tracks.append(int(item))

    for track_index in selected_tracks:
        track_info = tracks[track_index - 1]
        download_track_preview(track_info)

if __name__ == '__main__':
    main()
