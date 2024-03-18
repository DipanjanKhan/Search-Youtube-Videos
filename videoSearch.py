from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv('.env')
api_key = os.getenv('API_KEY')

def findChannelId(channelName):
    youtube = build('youtube', 'v3', developerKey = api_key)
    request = youtube.search().list(
        part = 'snippet',
        q = channelName,
        type = 'channel',
        maxResults = 1
    )
    response = request.execute()
    for i in response['items']:
        channel_id = i['id']['channelId']
        if channel_id:
            return channel_id
    return 'Not found'

def findLatestVideos(channel_id):
    youtube = build('youtube', 'v3', developerKey = api_key)
    request = youtube.search().list(
        part = 'snippet',
        channelId = channel_id,
        order = 'date',
        type = 'video',
        maxResults = 5,
    )
    response = request.execute()
    return response['items']
        
