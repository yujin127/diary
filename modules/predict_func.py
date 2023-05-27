import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
import gluonnlp as nlp
from tqdm import tqdm, tqdm_notebook
import pandas as pd

from kobert_tokenizer import KoBERTTokenizer
from transformers import BertModel
from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

from modules.MyBert import BERTClassifier, BERTSentenceTransform, BERTDataset

# 파라미터 정립
max_len = 128
batch_size = 10
warmup_ratio = 0.1
num_epochs = 8
max_grad_norm = 1
log_interval = 200
learning_rate = 5e-5

# KoBERT의 tokenizer, model, vocabulary 불러오기
# bertmodel = BertModel.from_pretrained('skt/kobert-base-v1', return_dict=False)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 학습 모델 로드
def predict(predict_sentence, model):
    data = [predict_sentence, '0']
    dataset_another = [data]

    # 예측데이터 토큰화
    tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
    vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')
    another_test = BERTDataset(dataset_another, 0, 1, tokenizer, vocab, max_len, True, False)
    test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=5)

    model.eval()

    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)

        valid_length = valid_length
        label = label.long().to(device)

        out = model(token_ids, valid_length, segment_ids)

        test_eval_list = []
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
            else:
                test_eval.append("상처가")

        print(">> 입력하신 내용에서 " + test_eval[0] + " 느껴집니다.")

if __name__=="__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    PATH = '../stat_model/'
    model = torch.load(PATH + 'BestModel.pt', map_location=device)
    print(type(model))  # 전체 모델을 통째로 불러옴, 클래스 선언 필수
    model.load_state_dict(
        torch.load(PATH + 'BestModel_state_dict.pt', map_location=device))  # state_dict를 불러 온 후, 모델에 저장

    predict_sentence = "학교가기 싫다. 오늘 너무 행복하다."
    predict(predict_sentence, model)
