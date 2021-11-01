import pandas as pd

import tweepy
import pytz

import mysql.connector
import datetime

from collections import Counter

def insert(user,time,tweet):
    mycursor = mydb.cursor()

    sql = "INSERT INTO new_tweets (username,time,tweet) VALUES (%s, %s, %s)"

    val = (user,time,tweet) #ganti

    mycursor.execute(sql, val)

    mydb.commit()

def scrape(delta_day):
    skrg = datetime.datetime.now()
    waktu_kebelakang = skrg - datetime.timedelta(days = delta_day)
    waktu_kebelakang_tz=pytz.UTC.localize(waktu_kebelakang) 

    search = tweepy.Cursor(api.search_tweets, q='@bni OR @bnicustomercare -filter:retweets',
                           result_type='recent',lang="id",tweet_mode='extended').items(100)
    for tweet in search: #ati2 di waktu bsii masi salah
        created = tweet.created_at

        if created > waktu_kebelakang_tz:
            text = tweet.full_text.replace("\n", "")
            user = tweet.user.screen_name

            insert(user,created,text)
        
def load():
    mycursor = mydb.cursor()

    sql = "SELECT * FROM new_tweets"

    mycursor.execute(sql)
    results = mycursor.fetchall()
    return pd.DataFrame(results,columns=['id','username','time','tweet'])

def load_bytopic(topic_to_query):
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM predicted_tweets WHERE topic='{topic_to_query}';"
    mycursor.execute(sql)

    results = pd.DataFrame(mycursor.fetchall(),columns=['id','username','time','tweet','topic','sentiment'])
    sents=list(results.loc[:,'sentiment'])
    count=dict(sorted(Counter(sents).items(), key=lambda item: item[1],reverse=True))

    return {"table":results,"labels": list(count.keys()),"values": list(count.values())}
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="new_tweets"
)

consumer_key = "TT4Bj6NmvWdTjhFYGKmcSFp1j"
consumer_secret = "ukqMH4TbVcJ5xU0zLpygW697VJjfHO7fE76j3EWmqn6lxrbleF"
access_token = "371720101-Ebi0IZ7J7QbWgvoMfmWIpH7oahvdy6bKrRsg2i0O"
access_token_secret = "xp9qrIrpCQXgqHIw2sA3YzSyy36xNTCROzknRD732gPmI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)