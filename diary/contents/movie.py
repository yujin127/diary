import requests
from urllib.request import Request, urlopen
import bs4
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re
import pandas as pd
import random
import os

# 슬픔 (Sad)
url = 'https://www.vingle.net/posts/3951425'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
elements = soup.select('span[data-text="true"]')
text_list1 = [element.text.strip() for element in elements]
text_list1 = text_list1[:-1]
text_list1 = [re.sub(r'\(\d+\)', '', item) for item in text_list1][:10]
list1 = pd.DataFrame({'영화 제목': text_list1})[:10]
list1.index = list1.index + 1
image_tags = soup.select('img[data-role="brochure-thumbnail"]')
for i, img_tag in enumerate(image_tags[:10]):
    image_url = img_tag["src"]
    image_response = requests.get(image_url)
    image_data = image_response.content
    image_filename = f"sad_movie_image{i + 1}.jpg"
    image_path = os.path.join('C:/workspace/emotion_diary/analysis/static/image', image_filename)
    with open(image_path, 'wb') as f:
        f.write(image_data)

# 공포 (fear)
url2 = 'https://rayspace.tistory.com/588'
html2 = urlopen(url2)
soup2=BeautifulSoup(html2,'html.parser')
span_tags = soup2.find_all('span', style="font-size: 12pt; color: rgb(217, 65, 141);")
text_list2 = [span.get_text() for span in span_tags]
text_list2 = [re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣 ]+', '', text) for text in text_list2]
text_list2 = [text.strip() for text in text_list2 if text.strip() != ''][:10]
list2 = pd.DataFrame({'영화 제목':text_list2})[:10]
list2.index=list2.index+1
image_tags = soup2.find_all('img', filename=lambda value: value and '.jpg' in value)
image_count = 10  # 저장할 이미지 개수
start_index = 11
for i, img_tag in enumerate(image_tags[:image_count]):
    image_url = img_tag['src']
    image_response = requests.get(image_url)
    image_data = image_response.content
    image_filename = f"fear_movie_image{i+1}.jpg"
    image_path = os.path.join('C:/workspace/emotion_diary/analysis/static/image', image_filename)
    with open(image_path, 'wb') as f:
        f.write(image_data)

# 놀람 (surprise)
url3 = 'https://beige-chu.tistory.com/entry/%EB%84%B7%ED%94%8C%EB%A6%AD%EC%8A%A4-%EC%98%81%ED%99%94-%EC%B6%94%EC%B2%9C-BEST-10-%EC%BD%94%EB%AF%B8%EB%94%94-%EC%9E%91%ED%92%88'
html3 = urlopen(url3)
soup3=BeautifulSoup(html3,'html.parser')
p_tags = soup3.find_all('p', style='border-left: 4px solid; padding: 8px 12px;')
text_list3 = [p_tag.get_text() for p_tag in p_tags][:10]
list3 = pd.DataFrame({'영화 제목':text_list3})[:10]
list3.index=list3.index+1
img_tags = soup3.find_all('img', attrs={
    'data-origin-width': '1080',
    'data-origin-height': '799',
    'alt': True,
    'data-filename': True,
    'data-ke-mobilestyle': 'widthOrigin',
    'onerror': "this.onerror=null; this.src='//t1.daumcdn.net/tistory_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory_admin/static/images/no-image-v1.png';"
})
image_count = 10
start_index = 21
for i, img_tag in enumerate(img_tags[:image_count]):
    image_url = img_tag["src"]
    image_response = requests.get(image_url)
    image_data = image_response.content
    image_filename = f"surprise_movie_image{i+1}.jpg"
    image_path = os.path.join('C:/workspace/emotion_diary/analysis/static/image', image_filename)
    with open(image_path, 'wb') as f:
        f.write(image_data)

# # 분노 (angry)
url4= 'https://marryvery119.tistory.com/424'
html4 = urlopen(url4)
soup4=BeautifulSoup(html4,'html.parser')
text_list4 = [span.text for span in soup4.find_all('span', style=re.compile(r'font-family:\s*\'Noto Sans Light\';')) if re.match(r'\d+\.\s+\w+', span.text)]
text_list4 = [re.sub(r'^\d+\.\s*', '', text) for text in text_list4]
text_list4= [text.replace('\xa0', '') for text in text_list4][:10]
list4 = pd.DataFrame({'영화 제목':text_list4})[:10]
list4.index=list4.index+1
img_tags = soup4.find_all('img')
image_count = 10
start_index = 31
for i, img_tag in enumerate(img_tags):
    if i >= image_count:
        break
    image_url = img_tag['src']
    response = requests.get(image_url)
    image_data = response.content
    image_filename = f"angry_movie_image{i+1}.jpg"
    image_path = os.path.join('C:/workspace/emotion_diary/analysis/static/image', image_filename)
    with open(image_path, 'wb') as f:
        f.write(image_data)

# 기쁨 (joy)
url5='https://nara.tistory.com/4287'
html5 = urlopen(url5)
soup5=BeautifulSoup(html5,'html.parser')
span_tags = soup5.find_all('span')
text_list5 = []
for span in span_tags:
    text = span.get_text(strip=True)
    text_list5.append(text)
text_list5 = [text for text in text_list5 if text != '']
text_list5 = [text[text.find('<')+1:text.find('>')] if '<' in text and '>' in text else '' for text in text_list5]
text_list5=text_list5[:10]
list5 = pd.DataFrame({'영화 제목':text_list5})
list5.index=list5.index+1
image_tags = soup5.find_all('img')
image_count = 10  # 저장할 이미지 개수
for i, img_tag in enumerate(image_tags):
    if i >= image_count:
        break
    image_url = img_tag['src']
    response = requests.get(image_url)
    image_data = response.content
    image_filename = f"joy_movie_image{i + 1}.jpg"
    image_path = os.path.join('C:/workspace/emotion_diary/analysis/static/image', image_filename)
    with open(image_path, 'wb') as f:
        f.write(image_data)

# 행복 (happy)
url6 = 'https://luckysevens.tistory.com/619'
html6 = urlopen(url6)
soup6=BeautifulSoup(html6,'html.parser')
text_listt6 = []
span_tags = soup6.find_all('span')
for span_tag in span_tags:
    text = span_tag.get_text().strip()
    if text.startswith("제목"):
        title = text.split(":")
        if len(title) > 1:
            title_text = title[1].strip()
            text_listt6.append(title_text)
text_list6 = []
for text in text_listt6[:10]:
    if "장르" in text:
        genre = text.split("장르")[0].strip()
        text_list6.append(genre)
list6 = pd.DataFrame({'영화 제목':text_list6})
list6.index=list6.index+1
image_tags = soup6.find_all('img')  # img 태그 추출
for i, image_tag in enumerate(image_tags[3:13]):
    image_url = image_tag['src']  # 이미지 URL 추출
    response = requests.get(image_url)
    image_data = response.content
    image_filename = f"happy_movie_image{i + 1}.jpg"
    image_path = os.path.join('C:/workspace/emotion_diary/analysis/static/image', image_filename)
    with open(image_path, 'wb') as f:
        f.write(image_data)


