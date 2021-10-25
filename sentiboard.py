
import pandas as pd
pd.options.mode.chained_assignment = None 
import torch
from transformers import BertTokenizer,BertForSequenceClassification,TextClassificationPipeline
import time

from sql import load

from collections import Counter

torch.cuda.is_available = lambda : False #important
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#load model
model_path="bert_multiclass-10_21-4_18"
model_multiclass = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', 
                                          do_lower_case=True)
pipe = TextClassificationPipeline(model=model_multiclass, tokenizer=tokenizer)
labels_saved={0: 'mesin dan pelayanan cabang', 1: '-', 2: 'tapcash', 3: 'rekening', 4: 'layanan digital', 5: 'reputasi', 6: 'fraud', 7: 'campaign'}

def labels_name(label_numbers):
    labels=[]
    for label_dict in (label_numbers):
        labels.append(labels_saved[int(label_dict['label'][-1])])
    return labels

def predict_pertweet(tweet):
    start_time = time.time()
    predicted_label=labels_name(pipe(tweet))
    duration = (time.time() - start_time)
    return {"pred": predicted_label[0],"dur": duration}

def predict_fromdb():
    tweets_loaded=load()
    tweets=list(tweets_loaded.loc[:,'tweet'])

    start_time = time.time()
    predicted_labels=[]
    for tweet in tweets:
        predicted_label=labels_name(pipe(tweet))
        predicted_labels.append(predicted_label[0])
    duration = (time.time() - start_time)

    return {"tweets": tweets,"pred": predicted_labels,"dur": duration}

def predict_fromdb_chart():
    tweets_loaded=load()
    tweets=list(tweets_loaded.loc[:,'tweet'])

    start_time = time.time()
    predicted_labels=[]
    for tweet in tweets:
        predicted_label=labels_name(pipe(tweet))
        predicted_labels.append(predicted_label[0])
    duration = (time.time() - start_time)

    return Counter(predicted_labels)
# if __name__ == '__main__':
#     pass