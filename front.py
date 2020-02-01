from flask import Flask, render_template, make_response, request, redirect, url_for, abort, jsonify, render_template

from splitText import SplitText
from getText import GetText
app = Flask(__name__)
gt = GetText()
st = SplitText()
def checkArticle(name):
    #print(gt.getArticle(name))
    return gt.getArticle(name)

def analyzeRegex(sentence):
    #print(gt.getArticle(name))
    return st.sentenceTokenDisplay(sentence)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/ajaxIdentifySentence')
def ajaxIdentifySentence():
    a = request.args.get('valArticle', 0)
    #b = request.args.get('b', 0, type=int)
    return jsonify(result=checkArticle(a))

@app.route('/ajaxGetArticle')
def ajaxGetArticle():
    a = request.args.get('valArticle', 0)
    #b = request.args.get('b', 0, type=int)
    return jsonify(result=checkArticle(a))

@app.route('/ajaxAnalyzeRegex')
def ajaxAnalyzeRegex():
    a = request.args.get('valSentenceToAnalyze', 0)
    print(a)
    return jsonify(result=analyzeRegex(a))

@app.route("/", methods = ['GET'])
def mainpage():
    if request.method == 'GET':
        return render_template('hello.html')

@app.route("/getArticle", methods = ['POST'])
def getArticle():
    if request.method == 'POST':
        articleValue = request.form['searchName']
        foundSentences = checkArticle(articleValue)
        resp = make_response(render_template('hello.html',foundSentences=foundSentences))
        return resp

@app.route("/saveRegex", methods = ['POST'])
def saveRegex():
    if request.method == 'POST':
        articleValue = request.form['putNameHere']
        foundSentences = checkArticle(articleValue)
        resp = make_response(render_template('hello.html',foundSentences=foundSentences))     
        return resp

@app.route("/loadRegex", methods = ['POST'])
def loadRegex():
    if request.method == 'POST':
        articleValue = request.form['putNameHere']
        foundSentences = checkArticle(articleValue)
        resp = make_response(render_template('hello.html',foundSentences=foundSentences))     
        return resp

if __name__ == "__main__":

    app.run()