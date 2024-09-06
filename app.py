from flask import Flask, request, jsonify
from pytube import YouTube
from youtubesearchpython import VideosSearch

app = Flask(__name__)

@app.route('/get_metadata', methods=['GET'])
def get_song_video_metadata():
    # Get the song name from query parameters
    song_name = request.args.get('song_name')
    
    if not song_name:
        return jsonify({"error": "Song name is required"}), 400
    
    # Search for the song on YouTube using youtube-search-python
    search = VideosSearch(song_name, limit=1)
    search_results = search.result()["result"]
    
    if not search_results:
        return jsonify({"error": "No videos found for the song."}), 404

    # Get the first search result
    video_id = search_results[0]['id']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Fetch metadata using pytube
    yt = YouTube(video_url)
    
    metadata = {
        "videoID": video_id,
        "title": yt.title,
        "views": yt.views,
        "length": yt.length,  # length in seconds
        "author": yt.author,
        "publish_date": yt.publish_date.strftime('%Y-%m-%d'),
        "description": yt.description,
        "keywords": yt.keywords,
        "thumbnail_url": yt.thumbnail_url,
    }

    return jsonify(metadata)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
