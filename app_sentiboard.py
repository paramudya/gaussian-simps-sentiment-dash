from sentiboard import predict_pertweet,predict_fromdb,predict_fromdb_chart

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def input():
    return render_template("input.html")

@app.route("/result", methods=['POST','GET'])
def isi_tweet():
    data_input = (request.form)
    tweet=data_input.get("tweet_input") #name pada input

    # label=sentipredict(tweet_preprocessed) #bagian predict sentiment
    res = predict_pertweet(tweet)
    label = res['pred']
    dur = res['dur']
    return render_template("result.html",input=tweet,result=label,duration=dur)

@app.route("/result_fromdb", methods=['POST','GET'])
def list_tweet():
    res_list=predict_fromdb()
    labels = res_list['pred']
    dur = res_list['dur']
    tweets = res_list['tweets']
    tweets_labels=dict(zip(tweets,labels))
    return render_template("result_fromdb.html",result=tweets_labels,duration=dur)

@app.route("/result_fromdb_chart", methods=['POST','GET'])
def chart():
    res_list=predict_fromdb_chart()
    return render_template("result_fromdb_chart.html",result=res_list)

if __name__ == "__main__":
    app.run(debug=True)