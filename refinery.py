import os
import re
import requests
import subprocess
import json
import time

# Configuration
API_KEY = 'your_tmdb_api_key'
DIRECTORY = '/path/to/your/media/files'
REQUEST_LIMIT = 50  # Maximum requests per second
REQUEST_INTERVAL = 1  # Time window in seconds

# Track API requests
api_requests = 0
last_request_time = time.time()

def authenticate_tmdb():
    """ Authenticate to TMDB API and return session object """
    session = requests.Session()
    session.params = {'api_key': API_KEY}
    return session

def rate_limit():
    """ Enforce TMDB API rate limit """
    global api_requests, last_request_time
    current_time = time.time()
    elapsed_time = current_time - last_request_time

    if elapsed_time < REQUEST_INTERVAL:
        if api_requests >= REQUEST_LIMIT:
            time.sleep(REQUEST_INTERVAL - elapsed_time)
            api_requests = 0
            last_request_time = time.time()
    else:
        api_requests = 0
        last_request_time = current_time

    api_requests += 1

def fetch_media_info(session, title, media_type, season=None, episode=None):
    """ Fetch media information from TMDB based on title and type (movie or tv) """
    rate_limit()
    if media_type == 'tv':
        response = session.get(f"https://api.themoviedb.org/3/search/tv?query={title}")
        data = response.json()
        if data['results']:
            show_id = data['results'][0]['id']
            if season and episode:
                rate_limit()
                episode_info = session.get(f"https://api.themoviedb.org/3/tv/{show_id}/season/{season}/episode/{episode}").json()
                return episode_info
            return data['results'][0]
    elif media_type == 'movie':
        response = session.get(f"https://api.themoviedb.org/3/search/movie?query={title}")
        data = response.json()
        if data['results']:
            return data['results'][0]
    return None

def get_user_confirmation(directory_name):
    """ Prompt user to confirm or provide a new title """
    response = input(f"Could not determine the title from the filename. Use directory name '{directory_name}' as the title? (Y/n) ")
    if response.lower() == 'n':
        title = input("Please enter the correct title: ")
        return title.strip()
    return directory_name.strip()

def parse_media_info_from_filename(filename):
    """ Parse resolution, video codec, and audio codec from filename """
    pattern = re.compile(r"(?P<resolution>720p|1080p|4K|2160p)\.(?P<video_codec>x264|x265|H\.264|H\.265)\.(?P<audio_codec>FLAC|AAC|EAC3|AC3|DTS)")
    match = pattern.search(filename)
    return match.groupdict() if match else {}

def get_media_details(file_path, media_info):
    """ Use ffprobe to extract media information from a file only if not already parsed from filename """
    if not media_info:
        cmd = ['ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', file_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        details = json.loads(result.stdout)
        
        video_streams = [stream for stream in details['streams'] if stream['codec_type'] == 'video']
        audio_streams = [stream for stream in details['streams'] if stream['codec_type'] == 'audio']
        
        if video_streams:
            media_info['video_codec'] = video_streams[0]['codec_name']
        if audio_streams:
            media_info['audio_codec'] = audio_streams[0]['codec_name']
        
    return media_info

def rename_files(session):
    """ Analyze files in the directory and rename them based on TMDB info and parsed/analyzed media details """
    tv_pattern = re.compile(r"(?i)(.*?)[\.\s-]*[Ss](\d+)[Ee](\d+)")
    for root, dirs, files in os.walk(DIRECTORY):
        directory_name = os.path.basename(root)
        for filename in files:
            filepath = os.path.join(root, filename)
            match = tv_pattern.search(filename)
            if match:
                title = match.group(1).strip().replace('.', ' ')
                season = match.group(2)
                episode = match.group(3)
                if not title:
                    title = get_user_confirmation(directory_name)
                info = fetch_media_info(session, title, 'tv', season, episode)
                if info:
                    parsed_info = parse_media_info_from_filename(filename)
                    media_details = get_media_details(filepath, parsed_info)
                    file_extension = os.path.splitext(filepath)[1]  # Get the file extension dynamically
                    new_name = f"{info['name']}_{info['air_date'][:4]}_tmdb-{info['id']}_S{season}E{episode}_{media_details.get('resolution', '')}_{media_details.get('video_codec', '')}_{media_details.get('audio_codec', '')}{file_extension}"
                    old_path = filepath
                    new_path = os.path.join(root, new_name)
                    os.rename(old_path, new_path)
                    print(f"Renamed '{filename}' to '{new_name}'")
            else:
                title = get_user_confirmation(directory_name)
                info = fetch_media_info(session, title, 'movie')
                if info:
                    parsed_info = parse_media_info_from_filename(filename)
                    media_details = get_media_details(filepath, parsed_info)
                    file_extension = os.path.splitext(filepath)[1]  # Get the file extension dynamically
                    new_name = f"{info['title']}_{info['release_date'][:4]}_tmdb-{info['id']}_{media_details.get('resolution', '')}_{media_details.get('video_codec', '')}_{media_details.get('audio_codec', '')}{file_extension}"
                    old_path = filepath
                    new_path = os.path.join(root, new_name)
                    os.rename(old_path, new_path)
                    print(f"Renamed '{filename}' to '{new_name}'")

def main():
    session = authenticate_tmdb()
    rename_files(session)

if __name__ == "__main__":
    main()
