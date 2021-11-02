
import pandas as pd
pd.options.mode.chained_assignment = None 
import torch
from transformers import BertTokenizer,BertForSequenceClassification,TextClassificationPipeline
import time

from sql import *
import twint

from collections import Counter

torch.cuda.is_available = lambda : False #important
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#multiclass TOPIC model
topic_model_path="bert_multiclass-10_21-4_18"
topic_model = BertForSequenceClassification.from_pretrained(topic_model_path)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', 
                                          do_lower_case=True)
pipe_topic = TextClassificationPipeline(model=topic_model, tokenizer=tokenizer)
topic_labels_saved={0: 'mesin dan pelayanan cabang', 1: '-', 2: 'tapcash', 3: 'rekening', 4: 'layanan digital', 5: 'reputasi', 6: 'fraud', 7: 'campaign'}

#SENTIMENT model
sentiment_model_path="bert_sentiment-10_26-16_11_81percent"
sentiment_model = BertForSequenceClassification.from_pretrained(sentiment_model_path)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', 
                                          do_lower_case=True)
pipe_sentiment = TextClassificationPipeline(model=sentiment_model, tokenizer=tokenizer)
sentiment_labels_saved={0: 'negatif',1: 'netral',2: 'positif'}

def labels_name(label_numbers,saved_labels):
    labels=[]
    for label_dict in (label_numbers):
        labels.append(saved_labels[int(label_dict['label'][-1])])
    return labels

def predict():
    start_time = time.time()
    scrape()
    tweets_loaded=load() #load from scraped tweets
    tweets=list(tweets_loaded.loc[:,'tweet'])
    delete_predicted()

    predicted_topics,predicted_sentiments=[],[]
    for i,row in tweets_loaded.iterrows():
        predicted_topic=labels_name(pipe_topic(row['tweet']),topic_labels_saved)
        predicted_topics.append(predicted_topic[0])
        predicted_sentiment=labels_name(pipe_sentiment(row['tweet']),sentiment_labels_saved)
        predicted_sentiments.append(predicted_sentiment[0])
        insert(row['id'],row['link'],row['username'],row['time'],row['tweet'],predicted_sentiment[0],predicted_topic[0])

    duration = (time.time() - start_time)
    count_topic=dict(sorted(Counter(predicted_topics).items(), key=lambda item: item[1],reverse=True))
    count_sentiment=dict(sorted(Counter(predicted_sentiments).items(), key=lambda item: item[1],reverse=True))

    return {"topic_labels": list(count_topic.keys()),"topic_values": list(count_topic.values()),
    "sentiment_labels": list(count_sentiment.keys()),"sentiment_values": list(count_sentiment.values()),
    "duration": duration}


def predict_pertweet(tweet):
    start_time = time.time()
    predicted_label=labels_name(pipe_topic(tweet))
    duration = (time.time() - start_time)
    return {"pred": predicted_label[0],"dur": duration}

# def predict_fromdb(label_selected):
#     start_time = time.time()

#     tweets_loaded=load()
#     tweets=list(tweets_loaded.loc[:,'tweet'])

#     predicted_labels=[]
#     for tweet in tweets:
#         predicted_label=labels_name(pipe_topic(tweet),topic_labels_saved)
#         predicted_labels.append(predicted_label[0])
#     duration = (time.time() - start_time)
#     df_predicted=pd.DataFrame({"tweets": tweets,"pred": predicted_labels})
#     return df_predicted[df_predicted.pred==label_selected],duration

def load_fromdb_bytopic(label_selected):
    return load_bytopic(label_selected)    


# if __name__ == '__main__':
#     pass