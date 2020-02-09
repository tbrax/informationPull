
from neuralSentence import NeuralClass
from splitText import SplitText
from getText import GetText

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

    def reset(self):
        self.sentences = []
        self.matchesCrafted = []
        self.matchesRegex = []
        self.matchesNeural = []

    def findNeuralMatches(self,resultType,lengthType):
        if self.textLoaded:
            if not self.Neural:
                self.Neural = NeuralClass()
                self.Neural.loadModel()
            #text = testText
            text = self.sentences
            grammarTextList = self.st.listToToken(text)
            grammarText = []
            for senList in grammarTextList:
                sentence = ""
                for word in senList:
                    sentence +=  word[1]+" "
                grammarText.append(sentence)
            
            

            patterns = self.st.getPatternObject()
            patternShort = patterns[0]
            patternFull = patterns[1]

            sentencesFull = []
            grammarPattern = []
            if (lengthType == "short"):
                for senList in patternShort:
                    sentenceP = ""
                    sentenceS = ""
                    for word in senList:
                        sentenceP +=  word[0]+" " #POS
                        sentenceS +=  word[1]+" " # Actual word
                    grammarPattern.append(sentenceP)
                    sentencesFull.append(sentenceS)
            else:
                for senList in patternFull:
                    sentenceP = ""
                    sentenceS = ""
                    for word in senList:
                        sentenceP +=  word[0]+" " #POS
                        sentenceS +=  word[1]+" " # Actual word
                    grammarPattern.append(sentenceP)
                    sentencesFull.append(sentenceS)
            
            if (resultType == "text"):
                results = self.Neural.runAndPlotPatterns(sentencesFull,text)
            else:
                results = self.Neural.runAndPlotPatterns(grammarPattern,grammarText)

            matchList = []
            for idx, x in enumerate(results):
                for idy, y in enumerate(x):

                    resultDict = {
                                    "Value":y,
                                    "Pattern Grammar":grammarPattern[idy],
                                    "Pattern Sentence":sentencesFull[idy],
                                    "Article Grammar":grammarText[idx],
                                    "Article Text":text[idx],
                                    "Compared":resultType
                                }
                  # matchList.append([ y,grammarPattern[idy],sentencesFull[idy],grammarText[idx],text[idx]])
                    matchList.append(resultDict)
                    
            return self.convertListString(self.viewMatches(matchList))

    def convertListString(self,data):
        for x in data:
            x["Value"] = str(x["Value"])
        return data

    def viewMatches(self,neuralMatchList):
        #columnIndex = 0
        #sortedArr = neuralMatchList
        #sortedArr.sort(key=lambda x: x[columnIndex],reverse=True)
        sortedArr = sorted(neuralMatchList, key = lambda i: i['Value'],reverse=True) 
        return sortedArr
        
    def saveSentences(self,title,sentences):
        self.textLoaded = True
        self.title = title
        self.sentences = sentences
       


def main():
    return True


if __name__== "__main__":
    main()