import os
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from .weekly_result import make_stacked_df_fin, make_stacked_df_fin_per


def weekly_line_chart(author_id):
    df = make_stacked_df_fin(author_id)
    emotions = df.columns.tolist()
    plt.figure(figsize=(10, 6))
    plt.rc('font', family='Malgun Gothic')
    x_label = df.columns
    emotion_colors = {
        '분노': '#ff9aa2',
        '슬픔': '#a9def9',
        '공포': '#c7ceea',
        '놀람': '#ffdac1',
        '행복': '#e2f0cb',
        '기쁨': '#b5ead7'
    }
    line_styles = ['-', '--', ':', '-.', 'dashed']

    for i, emotion in enumerate(emotions):
        line_style = line_styles[i % len(line_styles)]
        plt.plot(df.index, df[emotion], label=emotion, color=emotion_colors[emotion], linestyle=line_style, linewidth=5)

    plt.xticks(df.index, [date.strftime("%m-%d") for date in df.index])
    plt.xlabel('주간 날짜')
    plt.ylabel('백분율(%)')
    plt.legend()
    plt.tight_layout()

    today = datetime.datetime.now().date()
    file_name = f"weekly_line_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    plt.savefig(image_path, dpi=300)

    return file_name

def weekly_bar_chart(author_id):
    df = make_stacked_df_fin_per(author_id)
    plt.rc('font', family='Malgun Gothic')
    emotions = df.columns
    dates = df.index
    num_dates = len(dates)
    num_emotions = len(emotions)
    x_label = df.columns
    emotion_colors = {
        '분노': '#ff9aa2',
        '슬픔': '#a9def9',
        '공포': '#c7ceea',
        '놀람': '#ffdac1',
        '행복': '#e2f0cb',
        '기쁨': '#b5ead7'
    }
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.8

    # 각 날짜에 대한 100% 누적 막대 그래프 생성
    bottom = np.zeros(num_dates)  # 이전 날짜의 누적 합을 저장하기 위한 변수
    for i in range(num_emotions):
        emotion = emotions[i]
        data = df[emotion].values / 100  # 감정 데이터를 백분율로 변환하여 사용

        ax.bar(dates, data, bar_width, bottom=bottom, label=emotion, color=emotion_colors[emotion])

        bottom += data  # 이전 날짜의 누적 합 업데이트

    ax.set_xlabel('날짜')
    ax.set_ylabel('백분율(%)')
    ax.legend()

    plt.xticks(df.index, [date.strftime("%m-%d") for date in df.index])
    plt.tight_layout()

    today = datetime.datetime.now().date()
    file_name = f"weekly_bar_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    plt.savefig(image_path, dpi=300)

    return file_name