import pandas as pd

import tweepy
import pytz

import mysql.connector
import datetime

import twint
import nest_asyncio

from collections import Counter

def predict_counts(): # Done
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM predicted_tweets")
    # mydb.commit()
    (count,) = mycursor.fetchone()

    # mycursor.close()

    return count

def topic_list(): # Done
    mycursor = mydb.cursor()
    mycursor.execute("SELECT DISTINCT topic FROM predicted_tweets")
    # mydb.commit()
    #(count,) = mycursor.fetchone()
    # results = mycursor.fetchall()
    results = [topik[0] for topik in mycursor.fetchall()] # To list

    mycursor.close()

    return results

def predict_chart_result(): # Done
    mycursor = mydb.cursor()
    mycursor.execute("SELECT topic, sentiment FROM predicted_tweets")

    topik = []
    sentiment = []
    for (t, s) in mycursor.fetchall():
        topik.append(t)
        sentiment.append(s)

    count_topic=dict(sorted(Counter(topik).items(), key=lambda item: item[1],reverse=True))
    count_sentiment=dict(sorted(Counter(sentiment).items(), key=lambda item: item[1],reverse=True))

    return {"topic_labels": list(count_topic.keys()),"topic_values": list(count_topic.values()),
    "sentiment_labels": list(count_sentiment.keys()),"sentiment_values": list(count_sentiment.values())}

def delete_predicted(): # Done
    mycursor = mydb.cursor()
    mycursor.execute("TRUNCATE TABLE predicted_tweets")
    mydb.commit()

def insert(id,time,tweet,username,link,retweets,jam,likes,topic,sent):
    mycursor = mydb.cursor()

    sql = "INSERT INTO predicted_tweets (id,time,tweet,username,link,retweets,jam,likes,topic,sentiment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (id,time,tweet,username,link,retweets,likes,jam,topic,sent)

    try:
        mycursor.execute(sql, val)
    except:
        print('Failed to insert. Check the column')
    # mycursor.execute(sql, val)
    mydb.commit()

def update(id, topic2, sent2):
    mycursor = mydb.cursor()

    sql = "UPDATE predicted_tweets SET topic2 = '"+topic2+"', sentiment2 = '"+sent2+"' WHERE id = "+id
    mycursor.execute(sql)


def scrape(): # Done
    c = twint.Config()
    c.Search = '@bni OR @bnicustomercare'
    c.Since = waktu_str
    c.Limit = 800
    c.Pandas = True
    # Run
    # nest_asyncio.apply()
    search=twint.run.Search(c)

    tweets_loaded=twint.storage.panda.Tweets_df[['id','link','date','tweet','username','nlikes','nretweets']] 
    tweets_loaded = tweets_loaded.rename(columns={'date': 'time', 'nlikes': 'likes', 'nretweets': 'retweets'})

    # Remove Duplicated & BNI Tweets
    tweets_loaded.drop_duplicates(keep='first', inplace=True)
    tweets_loaded = tweets_loaded[tweets_loaded['username'] != 'BNICustomerCare']
    tweets_loaded = tweets_loaded[tweets_loaded['username'] != 'BNI']
    tweets_loaded.reset_index(drop=True, inplace=True)
    tweets_loaded

    
    cursor = mydb.cursor()
    cols = "`,`".join([str(i) for i in tweets_loaded.columns.tolist()])
    for i,row in tweets_loaded.iterrows():
        print(row['id'])
        sql = "INSERT INTO `new_tweets` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
        try:
            cursor.execute(sql, tuple(row))
        except:
            print('duplicate')
        mydb.commit()

def load(): # Done
    mycursor = mydb.cursor()

    sql = f"SELECT * FROM new_tweets WHERE time>='{waktu_str}'"

    mycursor.execute(sql)
    results = mycursor.fetchall()

    return pd.DataFrame(results,columns=['id','time','tweet','username','link','retweets','likes'])

def load_predicted(): # Done
    mycursor = mydb.cursor()

    sql = f"SELECT * FROM predicted_tweets"

    mycursor.execute(sql)
    results = mycursor.fetchall()

    return pd.DataFrame(results,columns=['id','time','tweet','username','link','retweets','likes','jam','topic','topic2','sentiment','sentiment2'])

def load_bytopic(topic_to_query): # Done
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM predicted_tweets WHERE topic='{topic_to_query}';"
    mycursor.execute(sql)

    results = pd.DataFrame(mycursor.fetchall(),columns=['id','time','tweet','username','link','retweets','likes','jam','topic','topic2','sentiment','sentiment2'])
    sents=list(results.loc[:,'sentiment'])
    count=dict(sorted(Counter(sents).items(), key=lambda item: item[1],reverse=True))

    return {"table":results,"labels": list(count.keys()),"values": list(count.values())}

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  database="new_tweets",
  autocommit=True,
  password="root", # Tambah
  port="8889" # Tambah
)


skrg = datetime.datetime.now()
waktu_kebelakang = skrg - datetime.timedelta(days = 1)
waktu_str=str(waktu_kebelakang.replace(microsecond=0))