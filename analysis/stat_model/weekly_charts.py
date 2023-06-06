import os
import datetime
import matplotlib.pyplot as plt
import pandas as pd

from .weekly_result import make_stacked_df_fin

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
    plt.legend()

    today = datetime.datetime.now().date()
    file_name = f"weekly_line_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    plt.savefig(image_path, dpi=300)

    return file_name

def weekly_bar_chart(author_id):
    plt.figure(figsize=(10, 6))
    df = make_stacked_df_fin(author_id)
    emotions = df.columns.tolist()
    plt.rc('font', family='Malgun Gothic')
    cumulative_data = df.cumsum()
    for emotion in emotions:
        plt.bar(df.index, cumulative_data[emotion], label=emotion)
    plt.xticks(rotation=45)
    plt.legend()

    today = datetime.datetime.now().date()
    file_name = f"weekly_bar_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    plt.savefig(image_path, dpi=300)

    return file_name


