
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

    def findNeuralMatches(self,resultType):
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
            for senList in patternFull:
                sentenceP = ""
                sentenceS = ""
                for word in senList:
                    sentenceP +=  word[0]+" " #POS
                    sentenceS +=  word[1]+" " # Actual word
                grammarPattern.append(sentenceP)
                sentencesFull.append(sentenceS)
            
            if (resultType ==0):
                results = self.Neural.runAndPlotPatterns(grammarPattern,grammarText)
            elif (resultType ==1):
                results = self.Neural.runAndPlotPatterns(sentencesFull,text)
            matchList = []
            for idx, x in enumerate(results):
                for idy, y in enumerate(x):
                    matchList.append([  y,
                                        grammarPattern[idy],
                                        sentencesFull[idy],
                                        grammarText[idx],
                                        text[idx]
                                        
                                        ])
                    
            return self.convertListString(self.viewMatches(matchList))

    def convertListString(self,data):
        for x in data:
            x[0] = str(x[0])
        return data

    def viewMatches(self,neuralMatchList):
        columnIndex = 0
        sortedArr = neuralMatchList
        sortedArr.sort(key=lambda x: x[columnIndex],reverse=True)
        return sortedArr
        
    def saveSentences(self,title,sentences):
        self.textLoaded = True
        self.title = title
        self.sentences = sentences
       


def main():
    tt = TextObject()
    
    tt.textLoaded = True
    tt.findNeuralMatches()


if __name__== "__main__":
    main()