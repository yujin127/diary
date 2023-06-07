from konlpy.tag import Mecab
from collections import Counter
from diary.models import Diary

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
import datetime

def keyword_list(author_id, date, n):
    try:
        diary = Diary.objects.filter(author_id=author_id, created_at=date).order_by('-created_at')[0]
    except (Diary.DoesNotExist, IndexError):
        diary = None
    if diary is None:
        diary = Diary.objects.filter(author_id=author_id).latest('created_at')

    diary = diary.content
    m=Mecab('C:/mecab/mecab-ko-dic')
    noun = m.nouns(diary)
    with open('C:/workspace/emotion_diary/stop_w.txt', encoding='utf-8') as f:
        list_file = f.readlines()
    for i in range(len(list_file)):
        list_file[i] = list_file[i].replace('\n', '')

    remove_stopwords = [x for x in noun if x not in list_file]
    count = Counter(remove_stopwords)
    noun_list = count.most_common(n)
    keyword = []
    for v in noun_list:
        keyword.append(v[0])

    return keyword


def make_wordcloud(author_id, date):
    try:
        diary = Diary.objects.filter(author_id=author_id, created_at=date).order_by('-created_at')[0]
    except (Diary.DoesNotExist, IndexError):
        diary = None
    if diary is None:
        diary = Diary.objects.filter(author_id=author_id).latest('created_at')

    diary = diary.content
    m=Mecab('C:/mecab/mecab-ko-dic')
    noun = m.nouns(diary)
    with open('C:/workspace/emotion_diary/stop_w.txt', encoding='utf-8') as f:
        list_file = f.readlines()
    for i in range(len(list_file)):
        list_file[i] = list_file[i].replace('\n', '')

    remove_stopwords = [x for x in noun if x not in list_file]
    count = Counter(remove_stopwords)
    img = Image.open('C:/workspace/emotion_diary/img.png')  # 경로 바꾸기
    imgArray = np.array(img)
    wordcloud = WordCloud(
        font_path='C:/workspace/emotion_diary/NanumBarunGothic.ttf',
        background_color='white',  # 배경색은 흰색으로
        colormap='Reds',  # 글씨색은 빨간색으로
        mask=imgArray,  # 워드클라우드 모양 설정
    ).generate_from_frequencies(count)  # count -> make_noun_list(diary)에서 생성한 딕셔너리
    # 사이즈 설정 및 출력
    plt.figure(figsize=(5, 5))
    plt.axis('off')

    today = datetime.datetime.now().date()
    file_name = f"wordcloud_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    wordcloud.to_file(image_path)

    return file_name

def cum_keyword_list(author_id, n):
    if Diary.objects.count() >= 7:
        diary_text = ''
        for i in range(7):
            diary = Diary.objects.filter(author_id=author_id).order_by('-created_at')[6 - i]
            diary_text += diary.content

    m=Mecab('C:/mecab/mecab-ko-dic')
    noun = m.nouns(diary_text)
    with open('C:/workspace/emotion_diary/stop_w.txt', encoding='utf-8') as f:
        list_file = f.readlines()
    for i in range(len(list_file)):
        list_file[i] = list_file[i].replace('\n', '')

    remove_stopwords = [x for x in noun if x not in list_file]
    count = Counter(remove_stopwords)
    noun_list = count.most_common(n)
    keyword = []
    for v in noun_list:
        keyword.append(v[0])

    return keyword

def cum_make_wordcloud(author_id):
    if Diary.objects.count() >= 7:
        diary_text = ''
        for i in range(7):
            diary = Diary.objects.filter(author_id=author_id).order_by('-created_at')[6 - i]
            diary_text += diary.content
    m=Mecab('C:/mecab/mecab-ko-dic')
    noun = m.nouns(diary_text)
    with open('C:/workspace/emotion_diary/stop_w.txt', encoding='utf-8') as f:
        list_file = f.readlines()
    for i in range(len(list_file)):
        list_file[i] = list_file[i].replace('\n', '')

    remove_stopwords = [x for x in noun if x not in list_file]
    count = Counter(remove_stopwords)
    img = Image.open('C:/workspace/emotion_diary/img.png')  # 경로 바꾸기
    imgArray = np.array(img)
    wordcloud = WordCloud(
        font_path='C:/workspace/emotion_diary/NanumBarunGothic.ttf',
        background_color='white',  # 배경색은 흰색으로
        colormap='Reds',  # 글씨색은 빨간색으로
        mask=imgArray,  # 워드클라우드 모양 설정
    ).generate_from_frequencies(count)  # count -> make_noun_list(diary)에서 생성한 딕셔너리
    # 사이즈 설정 및 출력
    plt.figure(figsize=(5, 5))
    plt.axis('off')

    today = datetime.datetime.now().date()
    file_name = f"cum_wordcloud_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    wordcloud.to_file(image_path)

    return file_name