from konlpy.tag import Mecab
from collections import Counter
from diary.models import Diary

def keyword_list(author_id, date, n):
    try:
        diary = Diary.objects.filter(author_id=author_id, created_at=date).order_by('-created_at')[0]
    except (Diary.DoesNotExist, IndexError):
        diary = None
    if diary is None:
        diary = Diary.objects.filter(author_id=author_id).latest('created_at')

    m = Mecab('C:/mecab/mecab-ko-dic')
    noun = m.nouns(diary)
    with open('C:/workspace/emotion_diary/stop_w.txt', encoding='utf-8') as f:
        list_file = f.readlines()
    for i in range(len(list_file)):
        list_file[i] = list_file[i].replace('\n', '')
    stopwords = list_file
    remove_stopwords = [x for x in noun if x not in list_file]
    count = Counter(remove_stopwords)
    noun_list = count.most_common(n)
    keyword = []
    for v in noun_list:
        keyword.append(v)
    return keyword
