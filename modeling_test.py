import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from diary.models import Diary

df = []
for i in range(7):
    diary = Diary.objects.filter(author_id=1).order_by('-created_at')[6-i]
    df.append(diary.emotion_data)

print(df)