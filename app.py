from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/mdata', methods=['GET'])
def get_song_metadata():
    # Get the song name from the query parameter
    song_name = request.args.get('q')

    if not song_name:
        return jsonify({"error": "Please provide a song name."}), 400

    # Construct YouTube search URL
    search_url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first video in the search results
    video = soup.find('a', {'href': lambda x: x and x.startswith('/watch')})

    if not video:
        return jsonify({"error": "No video found."}), 404

    # Extract video details
    video_url = f"https://www.youtube.com{video['href']}"
    video_id = video['href'].split('v=')[-1]
    video_title = video.get('title')
    video_thumbnail = f"https://img.youtube.com/vi/{video_id}/0.jpg"

    # Retrieve video page for additional metadata
    video_page_response = requests.get(video_url)
    video_page_soup = BeautifulSoup(video_page_response.text, 'html.parser')
    
    # Extract metadata (keywords, description, etc.)
    meta_tags = video_page_soup.find_all('meta')
    keywords = []
    description = ""

    for meta in meta_tags:
        if meta.get('name') == 'keywords':
            keywords = meta.get('content').split(',')
        if meta.get('name') == 'description':
            description = meta.get('content')

    # Return metadata as JSON
    video_metadata = {
        "video_url": video_url,
        "video_id": video_id,
        "video_title": video_title,
        "video_thumbnail": video_thumbnail,
        "video_keywords": keywords,
        "video_description": description
    }

    return jsonify(video_metadata)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
