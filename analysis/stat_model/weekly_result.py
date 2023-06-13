from diary.models import Diary
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
from .predict_func import make_df


def make_stacked_df(author_id):
    if Diary.objects.count() >= 7:
        data = []
        index = []
        for i in range(7):
            diary = Diary.objects.filter(author_id=author_id).order_by('-created_at')[6-i]
            data.append(diary.emotion_data)
            index.append(diary.created_at)
        df = pd.DataFrame(data, columns=['data'], index=index)
        return df
    else:
        data = []
        index = []
        n = Diary.objects.count()
        for i in range(n):
            diary = Diary.objects.filter(author_id=author_id).order_by('-created_at')[n-1-i]
            data.append(diary.emotion_data)
            index.append(diary.created_at)
        df = pd.DataFrame(data, columns=['data'], index=index)
        return df

def make_stacked_df_fin(author_id):
    if Diary.objects.count() >= 7:
        emotions = ['슬픔', '분노', '기쁨', '행복', '놀람', '공포']
        index = []
        data = []
        for i in range(7):
            diary = Diary.objects.filter(author_id=author_id).order_by('-created_at')[6 - i]
            emotions_count = [diary.emotion_data.count(emotion) for emotion in emotions]
            total_count = sum(emotions_count)
            emotions_percent = [count / total_count * 100 for count in emotions_count]
            index.append(diary.created_at)
            data.append(emotions_percent)
        df = pd.DataFrame(data, columns=emotions, index=index)

        return df

def make_good_bad_df(author_id):
    if Diary.objects.count() >= 7:
        data = []
        for i in range(7):
            good = 0
            bad = 0

            diary = Diary.objects.filter(author_id=author_id).order_by('-created_at')[6 - i]
            date = diary.created_at
            emotion_list = diary.emotion_data

            for emotion in emotion_list:
                if emotion in ['기쁨', '행복']:
                    good += 1
                else:
                    bad += 1
            data.append([date, good, bad])
        df = pd.DataFrame(data, columns=['date', 'Good', 'Bad'])
        df.set_index(keys='date')
        return df

def make_stacked_df_fin_per(author_id):
    if Diary.objects.count() >= 7:
        emotions = ['슬픔', '분노', '기쁨', '행복', '놀람', '공포']
        index = []
        data = []
        for i in range(7):
            diary = Diary.objects.filter(author_id=author_id).order_by('-created_at')[6 - i]
            emotions_count = [diary.emotion_data.count(emotion) for emotion in emotions]
            total_count = sum(emotions_count)
            emotions_percent = [count / total_count * 100 for count in emotions_count]
            index.append(diary.created_at)
            data.append(emotions_percent)
        df = pd.DataFrame(data, columns=emotions, index=index)
        return df