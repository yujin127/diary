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
    colors = ['#C2DEDC', '#FAAB78', '#FFD966', '#F7C8E0', '#DFFFD8', '#804674']
    for i, emotion in enumerate(emotions):
        plt.plot(df.index, df[emotion], label=emotion, color=colors[i], marker='o')
    plt.xticks(rotation=45)
    plt.legend()

    today = datetime.datetime.now().date()
    file_name = f"weekly_line_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    plt.savefig(image_path, dpi=300)

    return file_name

def cum_weekly_line_chart(author_id):
    df = make_stacked_df_fin(author_id)
    emotions = df.columns.tolist()
    plt.figure(figsize=(10, 6))
    plt.rc('font', family='Malgun Gothic')
    cumulative_data = df.cumsum()
    colors = ['#8FBDD3', '#FAAB78', '#FFD966', '#D77FA1', '#B5F1CC', '#804674']
    for i, emotion in enumerate(emotions):
        plt.plot(df.index, cumulative_data[emotion], color=colors[i], label=emotion, marker='o')
    plt.xticks(rotation=45)
    plt.xlabel('날짜')
    plt.ylabel('감정')
    plt.title('주간 감정 데이터 누적 선그래프')
    plt.legend()

    today = datetime.datetime.now().date()
    file_name = f"cum_weekly_line_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    plt.savefig(image_path, dpi=300)

    return file_name

def weekly_bar_chart(author_id):
    df = make_stacked_df_fin_per(author_id)
    emotions = df.columns
    dates = df.index
    num_emotions = len(emotions)
    colors = ['#8FBDD3', '#FAAB78', '#FFD966', '#D77FA1', '#B5F1CC', '#804674']
    fig, ax = plt.subplots(figsize=(10, 6))  # 세로 비율을 크게 조정
    bar_width = 0.8

    # 각 감정에 대한 막대 그래프 생성
    bottom = np.zeros(len(dates))  # 이전 감정의 누적 합을 저장하기 위한 변수
    for i in range(num_emotions):
        emotion = emotions[i]
        data = df[emotion].values

        ax.bar(dates, data, bar_width, bottom=bottom, label=emotion, color=colors[i])

        bottom += data  # 이전 감정의 누적 합 업데이트

    ax.set_xlabel('날짜')
    ax.set_ylabel('백분율(%)')
    ax.set_title('주간 감정 데이터 누적 막대 그래프')
    ax.legend()

    # x 축 레이블 회전
    plt.xticks(rotation=45)

    plt.tight_layout()

    today = datetime.datetime.now().date()
    file_name = f"weekly_bar_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    plt.savefig(image_path, dpi=300)

    return file_name

