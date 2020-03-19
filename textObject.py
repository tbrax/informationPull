
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
        self.st = SplitText(self)
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
        self.patterns = False
        self.load()
        

    def loadPatterns(self):
        self.patterns = self.st.getPatternObject()

    def load(self):
        'Load troublesome word file. "not" etc.'
        f=open(self.notFile, "r",encoding="utf8")
        ns = f.readlines()
        for x in ns:
            self.notList.append(x.strip())
        self.loadPatterns()
        

    def reset(self):
        self.sentences = []
        self.matchesCrafted = []
        self.matchesRegex = []
        self.matchesNeural = []
    #Pattern Sentence

    def returnPOSList(self,sentence):
        return self.ch.returnPOSList(sentence)

    def getGraph(self,sentence):
        #return self.ch.treeHTML(sentence)
        return self.ch.displacyService(sentence)

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
    def constructReducedSentence(self,index,articleSentence,fullSentence,shortSentence):
        indexList = index.split(" ")
        indexs = []
        for x in indexList:
            indexs.append(int(x))
        return self.ch.constructReducedSentence(indexs,articleSentence,fullSentence,shortSentence)

    def getColumn(self,lst,col):
        return [val[col] for val in lst]

    def getPatterns(self):
        return self.patterns

    def listCompareValue(self,l0,l1):
        return 0.0

    def findExactStructureMatches(self):
        text = self.getTextOnly(self.sentences)
        tks = self.sentenceTokenDisplayList(text)
        patterns = self.getPatterns()
        POSList = []
        matchList = []
        if not patterns:
            return False
        for x in patterns:
            POSList.append([x['ShortPOS'],x['ShortSentence']])
        for x in tks:
            xList = self.getColumn(x,1)
            for y in POSList:
                yList = y[0].split(' ')
                compareNum = self.listCompareValue(xList,yList)
                if (compareNum == 0.0):
                    textSen = ' '.join(self.getColumn(x,0))
                    savedSen = y[1]
                    resultDict = {
                                    'Article Sentence':textSen,
                                    'Pattern':savedSen,
                                    }
                    matchList.append(resultDict)
        return matchList
         
        

    def findTreeMatches(self):
        #return self.findExactStructureMatches()
        text = self.getTextOnly(self.sentences)
        patterns = self.getPatterns()
        matchList = []
        for x in text:
            for idy,y in enumerate(patterns):
                if 'ShortSentence' in y:
                    if self.ch.compareTree(x,y['ShortSentence']):
                        reducedSen = self.constructReducedSentence(y['ShortIndex'],x,y['FullSentence'],y['ShortSentence'])
                        resultDict = {
                                        'Article Sentence':x,
                                        'Short Sentence':y['ShortSentence'],
                                        'Reduced Article':reducedSen
                                        }
                        matchList.append(resultDict)
        return matchList

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
            patterns = self.getPatterns()
            fullSentence = []
            fullPOS = []
            shortSentence = []
            shortPOS = []

            for x in patterns:
                fullSentence.append(x['FullSentence'])
                fullPOS.append(x['FullPOS'])
                shortSentence.append(x['ShortSentence'])
                shortPOS.append(x['ShortPOS'])

            matchSentence = fullSentence
            matchPOS = fullPOS
            if (lengthType == "short"):
                matchSentence = shortSentence
                matchPOS = shortPOS
 
            getNeuText = False
            getNeuPOS = True
            getNeuDep = False
            getNeuHead = False
            results = {"Text":"F",
                        "POS":"F",
                        "Dependency":"F",
                        "Head":"F"
                        }
            if (getNeuText):
                results["Text"] = self.Neural.runAndPlotPatterns(matchSentence,text)
            if (getNeuPOS):
                results["POS"] = self.Neural.runAndPlotPatterns(matchPOS,grammarText)
            if (getNeuDep):
                results["Dep"] = self.Neural.runAndPlotPatterns(matchPOS,grammarText)
            if (getNeuHead):
                results["Head"] = self.Neural.runAndPlotPatterns(matchPOS,grammarText)

            matchList = []
            for idx, x in enumerate(results["POS"]):
                for idy, y in enumerate(x):
                    #Text = results[]
                    ps = results["POS"][idx][idy]
                    resultDict = {
                                    self.nameListNeural[0]:y,
                                    self.nameListNeural[1]:matchPOS[idy],
                                    self.nameListNeural[2]:matchSentence[idy],
                                    self.nameListNeural[3]:grammarText[idx],
                                    self.nameListNeural[4]:text[idx],
                                    self.nameListNeural[5]:resultType,
                                    "POS Value":ps
                                }
                  # matchList.append([ y,grammarPattern[idy],sentencesFull[idy],grammarText[idx],text[idx]])
                    matchList.append(resultDict)
            rt = self.convertListString(self.viewMatches(matchList))

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