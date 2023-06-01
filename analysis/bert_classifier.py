import torch
from torch import nn
import torch.nn.functional as F

class BERTClassifier(nn.Module):
    def __init__(self, bert, hidden_size=768, num_classes=8, dr_rate=None, params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate
        self.classifier = nn.Linear(hidden_size, num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)

    def forward(self, token_ids, valid_length, segment_ids):
        _, pooler = self.bert(
            input_ids=token_ids,
            token_type_ids=segment_ids.long(),
            attention_mask=valid_length.float().to(token_ids.device)
        )
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)
