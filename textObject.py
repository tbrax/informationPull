
from neuralSentence import NeuralClass
from splitText import SplitText
from getText import GetText
from chunking import Chunking

import numpy as np

class TextObject:
    def __init__(self):
        self.sentences = []
        self.matchesCrafted = []
        self.matchesRegex = []
        self.matchesNeural = []
        self.title = ""
        self.textLoaded = False
        self.Neural = False
        self.st = SplitText()
        self.gt = GetText()
        self.ch = Chunking()
        self.nameListNeural = [
                                "Value",
                                "Pattern Grammar",
                                "Pattern Sentence",
                                "Article Grammar",
                                "Article Text",
                                "Compared"
                            ]
        self.notFile = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\notlist.txt"
        self.notList = []
        self.load()

    def load(self):
        'Load troublesome word file. "not" etc.'
        f=open(self.notFile, "r",encoding="utf8")
        ns = f.readlines()
        for x in ns:
            self.notList.append(x.strip())

    def reset(self):
        self.sentences = []
        self.matchesCrafted = []
        self.matchesRegex = []
        self.matchesNeural = []
    #Pattern Sentence

    def sentenceTokenDisplay(self,sentence):
        return self.st.sentenceTokenDisplay(sentence)

    def sentenceTokenDisplayList(self,sentenceList):
        ls = []
        for x in sentenceList:
            ls.append(self.st.sentenceTokenDisplay(x))
        return ls

    def getArticle(self,name):
        'Given an article title, return list of sentences from article'
        article = self.gt.getArticle(name)
        if article != False:
            if len(article) > 0:
                title = article[0]
                text = article[1]
                sentences = self.st.textToSentenceList(text)
                self.saveSentences(title,sentences)
                return [title,sentences]
        return False

    def splitSentencesInSectionList(self,articleSections):
        for x in articleSections:
            tx = x["Text"]
            sentences = self.st.textToSentenceList(tx)
            txList = []
            for y in sentences:
                txList.append(y)
            x["Text"] = txList
        return articleSections

    def getArticleSectionList(self,name):
        articleSections = self.gt.getArticleSectionList(name)
        if articleSections != False:
            if len(articleSections) > 0:
                title = articleSections[0]
                textDict = articleSections[1]
                sentences = self.splitSentencesInSectionList(textDict)
                #sentences = textDict
                self.saveSentences(title,sentences)
                return [title,sentences]
        return False

    def isTroubleSome(self,sentence):
        checkSentence = sentence.lower()
        for x in self.notList:
            if x in checkSentence:
                return True 
        return False

    def removeTroublesomeSentencesRegex(self,matchList,nameToCheck):
        for x in matchList:
            if (len(x) > 0) and (x[0] != False):
                for y in x:
                    if self.isTroubleSome(y[nameToCheck]):
                        x.remove(y)
        return matchList

    def removeTroublesomeSentencesNeural(self,matchList,nameToCheck):
        'Given a list of dicts, removes entries where any word in "nameToCheck" matches ban list'
        for x in matchList:
            if self.isTroubleSome(x[nameToCheck]):
                matchList.remove(x)
        return matchList


    def findRegexMatches(self,inputText):
        rt = self.st.findRegexMatches(inputText)
        #print(rt[0])
        return self.removeTroublesomeSentencesRegex(rt,self.st.nameListRegex[3])


    def findNeuralMatchesText(self):
        return 0
    def findNeuralMatchesPOS(self):
        return 0

    def getTextOnly(self,textDict):
        textList = []
        for x in textDict:
            for y in x['Text']:
                textList.append(y)
        return textList

    def textToPOSTokens(self,text):
        return 0

    def findNeuralMatches(self,resultType,lengthType):
        if self.textLoaded:
            if not self.Neural:
                self.Neural = NeuralClass()
                self.Neural.loadModel()
            #text = testText
            text = self.getTextOnly(self.sentences)

            #A list of sentences
            grammarTextList = self.st.listToToken(text)           
            grammarText = []


            #Turns [('word0','POS0'),('word1','POS1')] to 'POS0 POS1'
            for senList in grammarTextList:
                sentence = ""
                for word in senList:
                    sentence +=  word[1]+" "
                grammarText.append(sentence)


            #Load patterns
            #[0] Reduced
            #[1] Full
            #[2] Dependency
            #[3] Head
            patterns = self.st.getPatternObject()

            sentencesFull = []
            grammarPattern = []

            matchList = patterns[1]
            if (lengthType == "short"):
                matchList = patterns[0]

            for senList in matchList:
                sentenceP = ""
                sentenceS = ""
                for word in senList:
                    sentenceP +=  word[0]+" " #POS
                    sentenceS +=  word[1]+" " # Actual word
                grammarPattern.append(sentenceP)
                sentencesFull.append(sentenceS)
 
            getNeuText = True
            getNeuPOS = True
            getNeuDep = False
            getNeuHead = False
            results = {"Text":"F",
                        "POS":"F",
                        "Dependency":"F",
                        "Head":"F"
                        }
            if (getNeuText):
                results["Text"] = self.Neural.runAndPlotPatterns(sentencesFull,text)
            if (getNeuPOS):
                results["POS"] = self.Neural.runAndPlotPatterns(grammarPattern,grammarText)
            if (getNeuDep):
                results["Dep"] = self.Neural.runAndPlotPatterns(grammarPattern,grammarText)
            if (getNeuHead):
                results["Head"] = self.Neural.runAndPlotPatterns(grammarPattern,grammarText)

            matchList = []
            for idx, x in enumerate(results["Text"]):
                for idy, y in enumerate(x):
                    #Text = results[]
                    ps = results["POS"][idx][idy]
                    resultDict = {
                                    self.nameListNeural[0]:y,
                                    self.nameListNeural[1]:grammarPattern[idy],
                                    self.nameListNeural[2]:sentencesFull[idy],
                                    self.nameListNeural[3]:grammarText[idx],
                                    self.nameListNeural[4]:text[idx],
                                    self.nameListNeural[5]:resultType,
                                    "POS Value":ps
                                }
                  # matchList.append([ y,grammarPattern[idy],sentencesFull[idy],grammarText[idx],text[idx]])
                    matchList.append(resultDict)
            rt = self.convertListString(self.viewMatches(matchList))
            #print(rt[0])
            return self.removeTroublesomeSentencesNeural(rt,self.nameListNeural[4])

    def convertListString(self,data):
        for x in data:
            for key, value in x.items():
                x[key]=str(value)
            #x[self.nameListNeural[0]] = str(x[self.nameListNeural[0]])
        return data

    def viewMatches(self,neuralMatchList):
        'Sorts so higher values are first'
        #columnIndex = 0
        #sortedArr = neuralMatchList
        #sortedArr.sort(key=lambda x: x[columnIndex],reverse=True)
        sortedArr = sorted(neuralMatchList, key = lambda i: i[self.nameListNeural[0]],reverse=True) 
        return sortedArr
        
    def saveSentences(self,title,sentences):
        self.textLoaded = True
        self.title = title
        self.sentences = sentences
       
def main():
    return True

if __name__== "__main__":
    main()