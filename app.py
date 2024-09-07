# YouTube Trending Music Metadata Fetcher

from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/trending', methods=['GET'])
def fetch_trending_videos():
    url = "https://m.youtube.com/feed/trending?bp=4gINGgt5dG1hX2NoYXJ0cw%3D%3D"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    videos = []
    for video in soup.find_all('div', class_='yt-lockup-content'):
        title = video.find('a', class_='yt-uix-tile-link').text
        thumbnail = video.find('img')['src']
        description = video.find('div', class_='yt-lockup-description').text if video.find('div', class_='yt-lockup-description') else ''
        views = video.find('div', class_='yt-lockup-meta-info').find_all('li')[0].text if video.find('div', class_='yt-lockup-meta-info') else ''
        likes = video.find('div', class_='yt-lockup-meta-info').find_all('li')[1].text if len(video.find('div', class_='yt-lockup-meta-info').find_all('li')) > 1 else ''

        videos.append({
            'title': title,
            'thumbnail': thumbnail,
            'description': description,
            'views': views,
            'likes': likes
        })

    return jsonify(videos)

if __name__ == '__main__':
    app.run(port=8000)
    
