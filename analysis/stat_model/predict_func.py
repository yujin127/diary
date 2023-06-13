import torch
from transformers import BertModel
from torch.utils.data import Dataset
import gluonnlp as nlp
import numpy as np
import pandas as pd

from kobert_tokenizer import KoBERTTokenizer
from analysis.stat_model.MyBert import BERTDataset, BERTClassifier
from diary.models import Diary
import datetime

# 파라미터 정립
max_len = 128
batch_size = 10
warmup_ratio = 0.1
num_epochs = 8
max_grad_norm = 1
log_interval = 200
learning_rate = 5e-5

# 예측 함수 정의
def predict(predict_sentence, model, tokenizer, vocab):
    data = [predict_sentence, '0']
    dataset_another = [data]

    another_test = BERTDataset(dataset_another, 0, 1, tokenizer, vocab, max_len, True, False)
    test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=0)

    model.eval()

    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
        token_ids = token_ids.long()
        segment_ids = segment_ids.long()

        valid_length = valid_length
        label = label.long()

        with torch.no_grad():
            out = model(token_ids, valid_length, segment_ids)

            test_eval = []
            for i in out:
                logits = i
                logits = logits.detach().cpu().numpy()

                if np.argmax(logits) == 0:
                    test_eval.append("슬픔")
                elif np.argmax(logits) == 1:
                    test_eval.append("중립")
                elif np.argmax(logits) == 2:
                    test_eval.append("불안")
                elif np.argmax(logits) == 3:
                    test_eval.append("당황")
                elif np.argmax(logits) == 4:
                    test_eval.append("분노")
                elif np.argmax(logits) == 5:
                    test_eval.append("기쁨")
                elif np.argmax(logits) == 6:
                    test_eval.append("혐오")
                elif np.argmax(logits) == 7:
                    test_eval.append("상처")
                elif np.argmax(logits) == 8:
                    test_eval.append("행복")
                elif np.argmax(logits) == 9:
                    test_eval.append("놀람")
                else:
                    test_eval.append("공포")

            return test_eval

def predict_main(author_id, date):
    PATH = 'analysis/stat_model/'

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
    vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')

    # BertClassifier 오류 발생 해결 방안
    # bertmodel = BertModel.from_pretrained("bert-base-multilingual-cased")
    bertmodel = BertModel.from_pretrained("skt/kobert-base-v1")
    model = BERTClassifier(bert=bertmodel, dr_rate=0.5).to(device)

    # model = torch.load(PATH + 'BestModel.pt', map_location=device)
    model.load_state_dict(torch.load(PATH + 'model_state_dict_final.pt', map_location=device))
    model.to(device)
    model.eval()

    try:
        diary = Diary.objects.filter(author_id=author_id, created_at=date).order_by('-created_at')[0]
    except (Diary.DoesNotExist, IndexError):
        diary = None
    if diary is None:
        diary = Diary.objects.filter(author_id=author_id).latest('created_at')


    sentences = diary.content
    d_l = sentences.split('.')

    total_emotion = []
    for i in range(len(d_l)-1):
        # total_emotion.append(predict(d_l[i], model, tokenizer, vocab))
        emotions = predict(d_l[i], model, tokenizer, vocab)
        total_emotion.extend(emotions)

    if '불안' in total_emotion:
        index1 = total_emotion.index('불안')
        total_emotion[index1] = '슬픔'
    elif '당황' in total_emotion:
        index2 = total_emotion.index('당황')
        total_emotion[index2] = '슬픔'
    elif '상처' in total_emotion:
        index3 = total_emotion.index('상처')
        total_emotion[index3] = '슬픔'
    elif '혐오' in total_emotion:
        index4 = total_emotion.index('혐오')
        total_emotion[index4] = '분노'
    else:
        total_emotion = total_emotion
    diary.emotion_data = total_emotion
    diary.save()

    return total_emotion


def make_df(total_emotion):
    sad = total_emotion.count('슬픔') + total_emotion.count('불안') + total_emotion.count('당황') + total_emotion.count('상처')
    angry = total_emotion.count('분노') + total_emotion.count('혐오')
    joy = total_emotion.count('기쁨')
    happy = total_emotion.count('행복')
    surprise = total_emotion.count('놀람')
    fear = total_emotion.count('공포')
    emotion_df = pd.DataFrame({'슬픔': sad, '분노': angry, '기쁨':joy,
                               '행복': happy, '놀람':surprise, '공포':fear,}, index=[0])
    # colors = ['#C0DBEA', '#F9F9F9', '#65647C', '#85586F', '#BB6464', '#FDFDBD',
    #           '#65647C', '#6096B4', '#FFB4B4', '#CE97B0', '#BBD6B8']
    # emotion_df.loc[1] = colors

    return emotion_df


def make_df2(total_emotion):
    bad = total_emotion.count('슬픔') + total_emotion.count('불안') + total_emotion.count('분노') + \
          total_emotion.count('혐오') + total_emotion.count('상처') + total_emotion.count('당황') + \
          total_emotion.count('공포') + total_emotion.count('놀람')
    good = total_emotion.count('기쁨') + total_emotion.count('행복')
    total_counts = good + bad

    if total_counts == 0:
        good_percent = good / (total_counts + 1) * 100
        bad_percent = bad / (total_counts + 1) * 100
    else:
        good_percent = good / total_counts * 100
        bad_percent = bad / total_counts * 100

    emotion_df = pd.DataFrame({'긍정': good_percent, '부정': bad_percent}, index=[0])

    return emotion_df

def count_emotion(total_emotion):
    def count_emotion(total_emotion):
        if total_emotion is None:
            return None
    sad = total_emotion.count('슬픔') + total_emotion.count('불안') + total_emotion.count('당황') + total_emotion.count('상처')
    angry = total_emotion.count('분노') + total_emotion.count('혐오')
    joy = total_emotion.count('기쁨')
    happy = total_emotion.count('행복')
    surprise = total_emotion.count('놀람')
    fear = total_emotion.count('공포')

    result = {
        '슬픔': sad,
        '분노': angry,
        '기쁨': joy,
        '행복': happy,
        '놀람': surprise,
        '공포': fear
    }

    return result
