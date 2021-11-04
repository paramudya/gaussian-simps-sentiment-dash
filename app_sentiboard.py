from sentiboard import *
from sql import *

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def home():
    # Crawl and Predict
    if request.method == 'POST':
        results = crawl_predict()
        count = predict_counts()
        topics = topic_list()

        return render_template("home_charts.html", count=count, topic_list=topics,topic_labels=results['topic_labels'],topic_values=results['topic_values'], sentiment_labels=results['sentiment_labels'],sentiment_values=results['sentiment_values'])
    else: # GET
        count = predict_counts()
        topics = []
        
        if(count > 0): # Ada Predicted
            topics = topic_list()
            results = predict_chart_result()
            return render_template("home_charts.html", count=count, topic_list=topics,topic_labels=results['topic_labels'],topic_values=results['topic_values'], sentiment_labels=results['sentiment_labels'],sentiment_values=results['sentiment_values'])
        else:
            return render_template("home.html", count=count, topic_list=topics)    


@app.route('/topik/<topik>', methods=['GET', 'POST'])
def getTopik(topik):
    topic_name = topik

    res=load_bytopic(topic_name) 
    return render_template("topik.html",topik=topic_name,result_table=[res['table'].to_html(classes='data', header="true")], titles=res['table'].columns.values,
    labels=res['labels'],values=res['values'])


@app.route('/secondpredict', methods=['GET', 'POST'])
def getPredict():
    # Cuma buat ngetes pake model lain, compare dengan model indobert
    result = second_predict()
    return "DONE"

if __name__ == "__main__":
    app.run(debug=True)