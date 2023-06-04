import os
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from math import pi
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

from analysis.stat_model.predict_func import predict, predict_main, make_df

def create_radar_chart(author_id):
    plt.switch_backend('AGG')
    emotion = predict_main(author_id)
    emotion_df = make_df(emotion)
    emotion_df = emotion_df.loc[:, emotion_df.ne(0).any()]

    plt.rc('font', family='Malgun Gothic')
    categories = emotion_df.columns
    # categories = list(emotion_df)[0:]
    values = emotion_df.mean().values.flatten().tolist()
    values += values[:1]
    angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
    angles += angles[:1]

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4),
                           subplot_kw=dict(polar=True))

    plt.xticks(angles[:-1], categories, color='black', size=11)
    ax.tick_params(axis='x', which='major', pad=15)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    ax.set_rlabel_position(0)
    plt.yticks([0, 1, 2, 3, 4, 5], ['0', '1', '2', '3', '4', '5'],
               color='grey', size=9)
    plt.ylim(0, 5)

    today = datetime.datetime.now().date()
    file_name = f"radar_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'skyblue', alpha=0.4)

    plt.savefig(image_path, dpi=200)

    return file_name

def create_pie_chart(author_id):
    emotion = predict_main(author_id)
    emotion_df = make_df(emotion)
    emotion_df = emotion_df.loc[:, emotion_df.ne(0).any()]
    data = emotion_df.iloc[0]
    x_label = emotion_df.columns
    plt.figure(figsize=(4, 4))
    plt.pie(data,
            labels=x_label,
            startangle=90,  # 축이 시작되는 각도 설정
            counterclock=True,  # True: 시계방향순 , False:반시계방향순
            # explode=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],  # 중심에서 벗어나는 정도 표시
            shadow=True,  # 그림자 표시 여부
            colors=['#C0DBEA', '#F9F9F9', '#65647C', '#85586F', '#BB6464', '#FDFDBD',
                    '#65647C', '#6096B4', '#FFB4B4', '#CE97B0', '#BBD6B8'],
            # colors=['gold','silver','whitesmoke','gray']
            wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 3}
            )  # width: 부채꼴 영역 너비,edgecolor: 테두리 색 , linewidth : 라인 두께
    plt.legend(loc=(0.85, 0.7))
    # plt.legend()

    today = datetime.datetime.now().date()
    file_name = f"pie_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    plt.savefig(image_path, dpi=200)

    return file_name