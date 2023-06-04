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

    test_eval = []

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
                    test_eval.append("슬픔이")
                elif np.argmax(logits) == 1:
                    test_eval.append("중립이")
                elif np.argmax(logits) == 2:
                    test_eval.append("불안이")
                elif np.argmax(logits) == 3:
                    test_eval.append("당황이")
                elif np.argmax(logits) == 4:
                    test_eval.append("분노가")
                elif np.argmax(logits) == 5:
                    test_eval.append("기쁨이")
                elif np.argmax(logits) == 6:
                    test_eval.append("혐오가")
                elif np.argmax(logits) == 7:
                    test_eval.append("상처가")
                elif np.argmax(logits) == 8:
                    test_eval.append("행복이")
                elif np.argmax(logits) == 9:
                    test_eval.append("놀람이")
                else:
                    test_eval.append("공포가")

            return test_eval

def predict_main(author_id):
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
        diary = \
            Diary.objects.filter(author_id=author_id, created_at=datetime.datetime.now().date()).order_by(
                '-created_at')[0]
    except (Diary.DoesNotExist, IndexError):
        diary = None
    if diary is None:
        diary = Diary.objects.filter(author_id=author_id).latest('created_at')


    sentences = diary.content
    d_l = sentences.split('.')

    total_emotion = []
    for i in range(len(d_l)):
        total_emotion.append(predict(d_l[i], model, tokenizer, vocab))

    diary.emotion_data = total_emotion
    diary.save()

    return total_emotion

def make_df(total_emotion):
    sad = total_emotion.count(['슬픔이'])
    neutral = total_emotion.count(['중립이'])
    insecure = total_emotion.count(['불안이'])
    embarrassing = total_emotion.count(['당황이'])
    angry = total_emotion.count(['분노가'])
    joy = total_emotion.count(['기쁨이'])
    hate = total_emotion.count(['혐오가'])
    hurt = total_emotion.count(['상처가'])
    happy = total_emotion.count(['행복이'])
    surprise = total_emotion.count(['놀람이'])
    fear = total_emotion.count(['공포가'])
    emotion_df = pd.DataFrame({'슬픔': sad, '중립':neutral, '불안': insecure,
                               '당황': embarrassing, '분노': angry, '기쁨':joy, '혐오':hate,
                               '상처':hurt, '행복': happy, '놀람':surprise, '공포':fear,}, index=[0])

    return emotion_df
