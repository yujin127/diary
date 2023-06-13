import os
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from math import pi
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

from analysis.stat_model.predict_func import predict, predict_main, make_df, make_df2
from .weekly_result import make_stacked_df, make_good_bad_df

def create_radar_chart(author_id, date):

    emotion = predict_main(author_id, date)
    emotion_df = make_df(emotion)
    emotion_df = emotion_df.loc[:, emotion_df.ne(0).any()]
    emotion_df = pd.DataFrame(emotion_df.values, columns=emotion_df.columns)

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

    date_str = date.strftime("%Y-%m-%d")  # 예: "2023-06-03"
    file_name = f"radar_chart_{author_id}_{date_str}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    ax.plot(angles, values, linewidth=1, linestyle='solid', color='#9c89b8')
    ax.fill(angles, values, '#9c89b8', alpha=0.4)

    plt.savefig(image_path, dpi=200)

    return file_name, emotion_df

def create_pie_chart(author_id, date):
    # emotion = predict_main(author_id, date)
    # emotion_df = make_df(emotion)
    # emotion_df = emotion_df.loc[:, emotion_df.ne(0).any()]
    a, emotion_df = create_radar_chart(author_id, date)
    emotion_df = emotion_df
    data = emotion_df.iloc[0]
    x_label = emotion_df.columns

    plt.rc('font', family='Malgun Gothic')
    emotion_colors = {
        '분노': '#ff9aa2',
        '슬픔': '#a9def9',
        '공포': '#c7ceea',
        '놀람': '#ffdac1',
        '행복': '#e2f0cb',
        '기쁨': '#b5ead7'
    }

    colors = [emotion_colors[emotion] + '90' for emotion in x_label]

    # Set figure size and create pie chart
    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(data,
                                       labels=None,
                                       startangle=90,
                                       counterclock=True,
                                       shadow=False,
                                       colors=colors,
                                       wedgeprops={'width': 0.5, 'edgecolor': 'w', 'linewidth': 2},
                                       autopct='%1.1f%%',
                                       textprops={'fontsize': 12, 'color': '#333333'},
                                       )

    plt.title('Emotion Distribution', fontsize=20, fontweight='bold')
    # Remove legend
    plt.legend([], [], loc='best')

    # Remove text labels
    for text, autotext in zip(texts, autotexts):
        text.set_text('')
        autotext.set_text('')

    # Save chart as image
    today = datetime.datetime.now().date()
    file_name = f"pie_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)
    plt.savefig(image_path, dpi=200)

    return file_name

def create_bar_plot(author_id, date):
    # emotion = predict_main(author_id, date)
    # emotion_df = make_df(emotion)
    # emotion_df = emotion_df.loc[:, emotion_df.ne(0).any()]
    a, emotion_df = create_radar_chart(author_id, date)
    emotion_df = emotion_df
    data = emotion_df.iloc[0]
    x_label = emotion_df.columns
    emotion_colors = {
        '분노': '#ff9aa2',
        '슬픔': '#a9def9',
        '공포': '#c7ceea',
        '놀람': '#ffdac1',
        '행복': '#e2f0cb',
        '기쁨': '#b5ead7'
    }
    plt.rc('font', family='Malgun Gothic')
    total = sum(data)
    percentages = [val/total * 100 if val != 0 else 0 for val in data]

    plt.figure(figsize=(8, 6))
    ax = plt.gca()
    bars = ax.barh(x_label, percentages, color=[emotion_colors[emotion] for emotion in x_label], alpha=0.7)

    plt.xlim(0, 100)

    for i, value in enumerate(percentages):
        plt.text(value + 1, i, f"{value:.1f}%", va='center', fontsize=18, weight='bold')

    legend_labels = x_label
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=emotion_colors[emotion]) for emotion in x_label]
    plt.legend(legend_handles, legend_labels, loc='upper right')

    plt.yticks(fontsize=20, weight='bold')

    max_bar_height = 0.7
    for bar in bars:
        bar.set_height(max_bar_height)

    today = datetime.datetime.now().date()
    file_name = f"bar_plot_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)
    plt.savefig(image_path, dpi=200)

    return file_name

def create_bar_chart_per(author_id, date):
    emotion = predict_main(author_id, date)
    emotion_df = make_df2(emotion)
    emotion_df = emotion_df.loc[:, emotion_df.ne(0).any()]
    labels = emotion_df.columns

    colors = {'긍정': '#0079FF', '부정': '#BE0000'}
    color_list = [colors.get(label, '#CCCCCC') for label in labels]

    plt.rc('font', family='Malgun Gothic')
    ax = emotion_df.plot(kind='barh', stacked=True, figsize=(10, 3), alpha=0.7, color=color_list)

    legend_labels = ['긍정', '부정']
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in legend_labels]
    ax.legend(legend_handles, legend_labels, loc='upper right')

    for i, p in enumerate(ax.patches):
        left, bottom, width, height = p.get_bbox().bounds
        ax.annotate(f"{int(width)}%", xy=(left + width / 2, bottom + height / 2),
                    ha='center', va='center', fontsize=15)

    ax.axis('off')

    today = datetime.datetime.now().date()
    file_name = f"bar_chart_per_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    plt.savefig(image_path, dpi=300)

    return file_name
def create_bar_chart(author_id, date):
    # emotion = predict_main(author_id, date)
    # emotion_df = make_df(emotion)
    # emotion_df = emotion_df.loc[:, emotion_df.ne(0).any()]
    a, emotion_df = create_radar_chart(author_id, date)
    emotion_df = emotion_df
    data = emotion_df.iloc[0]
    x_label = emotion_df.columns
    colors = ['#8FBDD3', '#FAAB78', '#FFD966', '#D77FA1', '#B5F1CC', '#804674']

    plt.rc('font', family='Malgun Gothic')
    plt.figure(figsize=(8, 4))  # 막대 그래프의 크기 조정

    plt.bar(x_label, data, color=colors)  # 막대 그래프 생성

    plt.xlabel('Emotion')  # x축 레이블 설정
    plt.ylabel('Count')  # y축 레이블 설정
    plt.title('Emotion Count')  # 그래프 제목 설정

    plt.xticks(rotation=45)  # x축 레이블 회전 설정

    today = datetime.datetime.now().date()
    file_name = f"bar_chart_{author_id}_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    plt.savefig(image_path, dpi=200)

    return file_name