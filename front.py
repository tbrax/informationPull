from flask import Flask, jsonify, render_template, make_response, request, redirect, url_for, abort, jsonify, render_template

from splitText import SplitText
from getText import GetText
from textObject import TextObject
app = Flask(__name__)
tt = TextObject()

def getGraph(sentence):
    return tt.getGraph(sentence)

def findNeuralMatchesInArticle(resultType,resultLength):
    rt = resultType[0]
    rl = resultLength[0]
    results = tt.findNeuralMatches(rt,rl)
    return results

def findTreeMatchesInArticle():
    results = tt.findTreeMatches()
    return results

def savePattern(full,short,stype,articleName):
    if stype[0] == 'Neural':
        if len(short) > 0:
            tt.st.savePattern(full,short,articleName)
        tt.st.savePattern(full,full,articleName)

def checkArticle(name):
    return tt.getArticleSectionList(name)
    #article = gt.getArticle(name)
    #if article != False:
    #    if len(article) > 0:
    #        title = article[0]
    #        text = article[1]
    #        sentences = st.textToSentenceList(text)
    #        tt.saveSentences(title,sentences)
    #        return [title,sentences]
    #return False
    

def analyzeRegex(sentence):
    return tt.sentenceTokenDisplay(sentence)

def analyzeRegexList(sentenceList):
    return tt.sentenceTokenDisplayList(sentenceList)

def findPatternMatchesInArticle(articleName):
    #art = tt.gt.getArticle(articleName)
    matches = tt.findRegexMatches()
    return matches


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/ajaxneuralmatches')
def ajaxneuralmatches():
    a = request.args.getlist('valMatchGrammar', None)
    b = request.args.getlist('valMatchLength', None)
    results = findNeuralMatchesInArticle(a,b)
    return jsonify(result=results)

@app.route('/ajaxtreematches')
def ajaxtreematches():
    results = findTreeMatchesInArticle()
    return jsonify(result=results)

@app.route('/ajaxSavePattern')
def ajaxSavePattern():
    a = request.args.getlist('valFull', None)
    b = request.args.getlist('valShort', None)
    c = request.args.getlist('valSaveType', None)
    d = request.args.getlist('valArticleName', None)
    #a = request.args.getlist('valFullSentence', None)
    #b = request.args.getlist('valFullPOS', None)
    #c = request.args.getlist('valShortSentence', None)
    #d = request.args.getlist('valShortPOS', None)
    #c = 0
    savePattern(a,b,c,d)
    return jsonify(result=a)


@app.route('/ajaxReturnPatterns')
def ajaxReturnPatterns():
    a = request.args.get('valArticle', 0)
    return jsonify(result=findPatternMatchesInArticle(a))


@app.route('/ajaxIdentifySentence')
def ajaxIdentifySentence():
    a = request.args.get('valSentence', 0)
    #b = request.args.get('b', 0, type=int)
    return jsonify(result=checkArticle(a))

@app.route('/ajaxGetArticle')
def ajaxGetArticle():
    a = request.args.get('valArticle', 0)
    #b = request.args.get('b', 0, type=int)
    return jsonify(result=checkArticle(a))

@app.route('/ajaxGraph')
def ajaxGraph():
    a = request.args.get('valSentenceToAnalyze', 0)
    return jsonify(graph=getGraph(a))

@app.route('/ajaxAnalyzeRegex')
def ajaxAnalyzeRegex():
    a = request.args.get('valSentenceToAnalyze', 0)
    b = request.args.getlist('valSectionToAnalyze', None)
    return jsonify(result0=analyzeRegex(a),result1=analyzeRegexList(b),graph=0)

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