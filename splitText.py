import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import neuralSentence

class SplitText:
    def __init__(self,tt):
        self.sentenceCount = 0
        self.patternFile = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\patterns.txt"
        self.patternSaveFile = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\patterns.txt"
        self.patternSaveFile2 = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\savedPatterns.txt"
        self.patterns = []
        self.nameListRegex = [
                                "Matching Text",
                                "Regex Matched",
                                "Article Tokens",
                                "Article Sentence"
                            ]
        self.tt = tt

    def getNeuralPatterns(self):
        return 0

    def readFileLines(self,path):
        f=open(path, "r",encoding="utf8")
        return f.readlines()

    def getPatternObject(self):
        text = self.readFileLines(self.patternSaveFile2)
        patternObj = []
        fullObj = []
        depObj = []
        headObj = []
        fullSen = []
        shortSen = []
        for line in text:
            if (line.startswith('P:')):
                reduced = line[2:].strip()
                rSep = reduced.split("|,,|")
                wordArr = []
                for item in rSep:
                    if item is not "":
                        iSep = item.split("|..|")
                        wordArr.append(iSep)
                if len(wordArr) > 0:
                    patternObj.append(wordArr)
            elif (line.startswith('S:')):
                full = line[2:].strip()
                fSep = full.split("|,,|")
                wordArr = []
                for item in fSep:
                    if item is not "":
                        iSep = item.split("|..|")
                        wordArr.append(iSep)
                if len(wordArr) > 0:
                    fullObj.append(wordArr)
            elif (line.startswith('D:')):
                full = line[2:].strip()
                fSep = full.split("|,,|")
                wordArr = []
                for item in fSep:
                    if item is not "":
                        iSep = item.split("|..|")
                        wordArr.append(iSep)
                if len(wordArr) > 0:
                    depObj.append(wordArr)
            elif (line.startswith('H:')):
                full = line[2:].strip()
                fSep = full.split("|,,|")
                wordArr = []
                for item in fSep:
                    if item is not "":
                        iSep = item.split("|..|")
                        wordArr.append(iSep)
                if len(wordArr) > 0:
                    headObj.append(wordArr)
            elif (line.startswith('O:')):
                fullSen.append(line[2:].strip())
            elif (line.startswith('H:')):
                shortSen.append(line[2:].strip())

        return [patternObj,fullObj,depObj,headObj,fullSen,shortSen]

    def patternToSentence(self,pattern):
        words = []
        pos = []
        for x in pattern:
            words.append(x[0]+' ')
            pos.append(x[1]+' ')
        return [words,pos]


    def saveRegexPattern(self,fullList,shortList):
        pString = ""
        sString = ""
        for idx,value in enumerate(shortList):
            x = value.split(",")
            #pString += ".*"
            pString += ".*?({0})".format(x[1])
            if (idx == len(shortList)-1):
                pString += ".*?"
        for idx,value in enumerate(fullList):
            x = value.split(",")
            #sString += " "
            sString += ".*?({0})".format(x[1])
            if (idx == len(fullList)-1):
                sString += ".*?"

        f = open(self.patternSaveFile, "a",encoding="utf-8")
        f.write("P:{0}".format(pString))
        f.write("\n")
        f.write("F:{0}".format(sString))
        f.write("\n")

    def wordCommaSplit(self,words):
        if words == ',,,':
            x = [',',',']
        else:
            x = words.split(",")
        return x

    def savePattern(self,fullList,shortList):
        pString = ""
        sString = ""
        sen = ""
        senShort = ""
        for i in shortList:
            x = self.wordCommaSplit(i)
            pString+="{1}|..|{0}|,,|".format(x[0],x[1])
            senShort += "{0} ".format(x[0])
        for i in fullList:
            x = self.wordCommaSplit(i)
            sString+="{1}|..|{0}|,,|".format(x[0],x[1])
            sen += "{0} ".format(x[0])
    
        f = open(self.patternSaveFile2, "a",encoding="utf-8")
        #f.write("P:{0}".format(pString))
        #f.write("\n")
        #f.write("S:{0}".format(sString))
        #f.write("\n")
        f.write("F:{0}".format(sen))
        f.write("\n")
        f.write("S:{0}".format(senShort))
        f.write("\n")
        return 0


    
    def loadRegexPatterns(self):
        'Load Regex Patterns from file'
        ps = []
        with open(self.patternFile, "r", encoding="utf-8") as f:
            for line in f:
                if (line.startswith('P:')):
                    ps.append(line[2:].strip())
        return ps
  
    def getRegexPatterns(self):
        return self.loadRegexPatterns()

    #Turn word list to POS tokens

    def wordToToken(self,wordList):
        return nltk.pos_tag(wordList)

    def listToToken(self, sentenceList):
        returnList = []
        for i in sentenceList:
            returnList.append(self.sentenceToToken(i))
        return returnList

    def sentenceToToken(self,sentence):
        'Turn sentence to list of POS tokens"The great big dog" becomes "(The,DT),(great,JJ),(Big,NNP),"(dog,NN)'
        #Seperates sentence into list of words
        text = word_tokenize(sentence)
        return self.wordToToken(text)
        #return nltk.pos_tag(sentence)
 
    def sentenceTokenDisplay(self,sentence):
        'Turns a sentence to tokens, and returns list'
        #tokenList = self.sentenceToToken(sentence)
        tokenList = self.tt.returnPOSList(sentence)
        #result = [i[1] for i in tokenList]
        return tokenList

    def textToSentenceList(self,text):
        return sent_tokenize(text)

    #Turn sentence 
    def checkSentenceRegex(self,sentence):
        result = self.checkListofWordsRegex(self.sentenceToToken(sentence),sentence)
        return result
        #text = word_tokenize(sentence)
        #self.checkWord(nltk.pos_tag(text))

    def findInList(self,givenList, item):
        try:
            return givenList.index(item)
        except ValueError:
            return -1

    #Compare sentence against all patterns and pront if match
    def checkAllPatterns(self,nltkTag, newSentence, sentenceLocationList,originalSentence):
        listOfMatches = []
        for pattern in self.getRegexPatterns():
            result = self.checkPattern(pattern, nltkTag,newSentence, sentenceLocationList,originalSentence)
            if (result):
                listOfMatches.append(result)
        if len(listOfMatches) == 0:
            listOfMatches.append(False)
        return listOfMatches

    #Check a single sentence against a single pattern
    def checkPattern(self,pattern, nltkTag, newSentence, sentenceLocationList,originalSentence):
        result = re.match(pattern, newSentence)      
        if result is None:
            self.sentenceCount += 1
            return False
        else:

            showStr = ""
            for counter, value in enumerate(result.groups()):
                
                gp = counter+1
                #pront(result.span(gp))
                #pront(nltkTag)
                #wordNum = self.findInList(posList, result.span(gp)[0])
                wordNum = self.findInList(sentenceLocationList, result.span(gp)[0])
                showStr += nltkTag[wordNum][0] + " "
            resultDict = {  
                            self.nameListRegex[0]:showStr,
                            self.nameListRegex[1]:pattern,
                            self.nameListRegex[2]:newSentence,
                            self.nameListRegex[3]:originalSentence
                            }
            #return {showStr,pattern,newSentence,originalSentence}
            return resultDict
        return False

    def checkListofWordsRegex(self,tokenList,originalSentence):
        newSentence = ""
        sentenceLocationCount = 0
        sentenceLocationList = []
        for x in tokenList:
            characterAdd = x[1]+" "
            newSentence += characterAdd
            sentenceLocationList.append(sentenceLocationCount)
            sentenceLocationCount += len(characterAdd)

        patternMatches = self.checkAllPatterns(tokenList,newSentence, sentenceLocationList,originalSentence)
        return patternMatches
        #pront(result.group())
        #pront(result.group(1))
        #pront(result.span(1))


    def findRegexMatches(self,inputText):
        matchList = []
        if (not inputText) or (inputText == ""):
            return False

        sentences = sent_tokenize(inputText)
        for x in sentences:
            matchList.append(self.checkSentenceRegex(x))
        if (not matchList):
            return False
        return matchList

    def readFile(self,path):
        f=open(path, "r",encoding="utf8")
        text = f.read()
        return text
        