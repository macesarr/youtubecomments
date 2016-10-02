import psycopg2
import requests
import time

flag = 0
nextPageToken=""
#idVideo = "sRoc_mDweTA"
#idVideo = "RCUAe1nWvYc"
#idVideo = "6iGfbJhoH3U"
#idVideo = "XCmVahKQ_TM"
#idVideo = "B2aY0VfWjno"
#idVideo = "QDgwEhriRXU"
#idVideo = "HHkJEz_HdTg"
#idVideo = "jvAcyAJXqrs"
#idVideo = "xWsNEuFVLvM"
#idVideo = "8joXlwKMkrk"
idVideo = "TzvjRC6ftBI"

while True:

    db = psycopg2.connect("dbname=YOURDB user=YOURUSER")

    cursor = db.cursor()
    
    if flag == 1:
        url = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId='+ idVideo +'&key=YOURAPIKEY&maxResults=100'
    else:
        url = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId='+ idVideo +'&key=YOURAPIKEY&maxResults=100&pageToken=' + nextPageToken

    print(url)
        
    flag = 0
    resp = requests.get(url)
    data = resp.json()
    comments = data['items']
    nextPageToken = data['nextPageToken']
    
    for comment in comments:
        text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
        like = comment['snippet']['topLevelComment']['snippet']['likeCount']

        print('comment: ' + text)
        
        cursor.execute("INSERT INTO comments (text_display, like_count) VALUES ('" + text + "', " + format(like) + ")")
        db.commit()

    cursor.close()
    db.close()
    time.sleep(30)
    
