from selenium import webdriver
from urllib.request import Request, urlopen
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import random
import os
from analysis.stat_model.predict_func import make_df, predict_main
from diary.models import Diary
from collections import Counter
import urllib.parse

def music_recommend(author_id, date):
    try:
        diary = Diary.objects.filter(author_id=author_id, created_at=date).order_by('-created_at')[0]
    except (Diary.DoesNotExist, IndexError):
        diary = None
    if diary is None:
        diary = Diary.objects.filter(author_id=author_id).latest('created_at')
    emotion_data = diary.emotion_data
    emotion_data = eval(emotion_data)
    emotion_frequency = Counter(emotion_data)
    max_frequency = max(emotion_frequency.values())
    most_frequent_emotions = [emotion for emotion, count in emotion_frequency.items() if count == max_frequency]
    emotion = random.choice(most_frequent_emotions)
    if emotion == "기쁨":
        url = "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=478102836"
    elif emotion == "슬픔":
        url = "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=522118665"
    elif emotion == "분노":
        url = "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=477792358"
    elif emotion == "놀람":
        url = "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=436119495"
    elif emotion == "공포":
        url = "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=444696172"
    elif emotion == "행복":
        url = "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=490579862"
    else:
        url = "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=490579862"

    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=header).text

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')

    articles = soup.select("#frm > div > table > tbody tr .image_typeAll")
    random_index = random.randint(0, min(len(articles), 50) - 1)
    selected_article = articles[random_index]
    title = soup.select('div.ellipsis.rank01 > span > a')[random_index].text
    artist = soup.select('div.ellipsis.rank02 > span')[random_index].text

    thumbnail = selected_article.select_one('div > a > img')['src']
    image_response = requests.get(thumbnail)
    image_data = image_response.content
    image_filename = f"music_{title}_{artist}.jpg"
    image_path = os.path.join('C:/workspace/emotion_diary/analysis/static/image', image_filename)
    with open(image_path, 'wb') as f:
        f.write(image_data)

    song_info = title, artist
    if song_info:
        # 앨범 정보로 연결되는 링크 출력
        search_query = title + ' ' + artist + ' 앨범 정보'
        search_query = urllib.parse.quote(search_query)
        url = f"https://www.google.com/search?q={search_query}"
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        res = requests.get(url, headers=header).text
        soup = BeautifulSoup(res, 'html.parser')
        link_element = soup.find('div', {'class': 'yuRUbf'}).a
        if link_element:
            album_link = link_element['href']
        else:
            album_link = None

    return image_filename, title, artist, album_link


