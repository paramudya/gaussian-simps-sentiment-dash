from sentiboard import *
from sql import *
# from IPython.display import HTML

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def input():
    return render_template("home.html")
    
@app.route("/main", methods=['POST','GET'])
def chart():
    results=predict() 

    return render_template("main.html",topic_labels=results['topic_labels'],topic_values=results['topic_values'],
    sentiment_labels=results['sentiment_labels'],sentiment_values=results['sentiment_values'])

@app.route("/tapcash", methods=['POST','GET'])
def list_tapcash():
    res=load_bytopic('tapcash') 
    return render_template("tapcash.html",result_table=[res['table'].to_html(classes='data', header="true")], titles=res['table'].columns.values,
    labels=res['labels'],values=res['values'])

@app.route("/rekening", methods=['POST','GET'])
def list_rekening():
    res=load_bytopic('rekening') #label_seleced here is tapcash, but gonna be changed for every label later
    # return render_template("rekening.html",result_table=[res.to_html(classes='data', header="true")], titles=res.columns.values)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)