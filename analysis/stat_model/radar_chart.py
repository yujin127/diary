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


def create_radar_chart():
    plt.switch_backend('AGG')
    emotion = predict_main()
    emotion_df = make_df(emotion)
    plt.rc('font', family='Malgun Gothic')
    # categories = list(emotion_df)[0:]
    categories = ['슬픔', '중립', '불안', '당황', '분노', '기쁨', '혐오', '상처','행복','놀람','공포']
    values = emotion_df.mean().values.flatten().tolist()
    values += values[:1]
    angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
    angles += angles[:1]

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 3.7),
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
    file_name = f"radar_chart_{today}.jpg"
    image_path = os.path.join('analysis/static/image', file_name)

    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'skyblue', alpha=0.4)

    plt.savefig(image_path)

    return image_path