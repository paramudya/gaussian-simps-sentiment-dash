import pandas as pd

import tweepy
import pytz

import mysql.connector
import datetime

import twint
import nest_asyncio

from collections import Counter

def delete_predicted():
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM predicted_tweets")
    mydb.commit()

def insert(id,link,user,time,tweet,sent,topic):
    mycursor = mydb.cursor()

    sql = "INSERT INTO predicted_tweets (id,username,time,tweet,topic,sentiment) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (id,link,user,time,tweet,sent,topic) #ganti
    try:
        mycursor.execute(sql, val)
    except:
        print('duplicate on predicted?')
    mydb.commit()

def scrape():
    c = twint.Config()
    c.Search = '@bni OR @bnicustomercare'
    c.Since = waktu_str
    c.Limit = 800
    c.Pandas = True
    # Run
    # nest_asyncio.apply()
    search=twint.run.Search(c)

    tweets_loaded=twint.storage.panda.Tweets_df[['id','link','date','tweet','username']] 
    tweets_loaded = tweets_loaded.rename(columns={'date': 'time'})
    
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

def load():
    mycursor = mydb.cursor()

    sql = f"SELECT * FROM new_tweets WHERE time>='{waktu_str}'"

    mycursor.execute(sql)
    results = mycursor.fetchall()
    return pd.DataFrame(results,columns=['id','link','username','time','tweet'])

def load_bytopic(topic_to_query):
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM predicted_tweets WHERE topic='{topic_to_query}';"
    mycursor.execute(sql)

    results = pd.DataFrame(mycursor.fetchall(),columns=['id',' link','username','time','tweet','topic','sentiment'])
    sents=list(results.loc[:,'sentiment'])
    count=dict(sorted(Counter(sents).items(), key=lambda item: item[1],reverse=True))

    return {"table":results,"labels": list(count.keys()),"values": list(count.values())}
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="new_tweets"
)

skrg = datetime.datetime.now()
waktu_kebelakang = skrg - datetime.timedelta(days = 1)
waktu_str=str(waktu_kebelakang.replace(microsecond=0))
# consumer_key = "TT4Bj6NmvWdTjhFYGKmcSFp1j"
# consumer_secret = "ukqMH4TbVcJ5xU0zLpygW697VJjfHO7fE76j3EWmqn6lxrbleF"
# access_token = "371720101-Ebi0IZ7J7QbWgvoMfmWIpH7oahvdy6bKrRsg2i0O"
# access_token_secret = "xp9qrIrpCQXgqHIw2sA3YzSyy36xNTCROzknRD732gPmI"

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)