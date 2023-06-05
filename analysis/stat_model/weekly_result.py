from diary.models import Diary
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os

def make_stacked_df(author_id):
    if Diary.objects.count() >= 7:
        df = []
        for i in range(7):
            diary = Diary.objects.filter(author_id=author_id).order_by('-created_at')[6-i]
            df.append(diary.emotion_data)
        return df
    else:
        df = []
        n = Diary.objects.count()
        for i in range(n):
            diary = Diary.objects.filter(author_id=author_id).order_by('-created_at')[n-1-i]
            df.append(diary.emotion_data)
        return df
