import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import neuralSentence

class SplitText:
    def __init__(self):
        self.sentenceCount = 0
        self.patternFile = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\patterns.txt"
        self.patternSaveFile = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\patterns.txt"
        self.patternSaveFile2 = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\savedPatterns.txt"
        self.patterns = []
        self.loadPatterns()

    def getNeuralPatterns(self):
        return 0

    def readFileLines(self,path):
        f=open(path, "r",encoding="utf8")
        return f.readlines()

    def getPatternObject(self):
        text = self.readFileLines(self.patternSaveFile2)
        patternObj = []
        fullObj = []
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
        return [patternObj,fullObj]

    
    def savePattern(self,patternList,fullSentenceList):
        #print(patternList)
        #(fullSentenceList)
        pString = ""
        sString = ""
        for i in patternList:
            x = i.split(",")
            pString+="{1}|..|{0}|..|{2}|,,|".format(x[0],x[1],x[2])
        for i in fullSentenceList:
            x = i.split(",")
            sString+="{1}|..|{0}|,,|".format(x[0],x[1])

        f = open(self.patternSaveFile2, "a",encoding="utf-8")
        f.write("P:{0}".format(pString))
        f.write("\n")
        f.write("S:{0}".format(sString))
        f.write("\n")
        return 0


    #Load Regex Patterns from file
    def loadPatterns(self):
        with open(self.patternFile, "r", encoding="utf-8") as f:
            for line in f:
                if (line.startswith('P:')):
                    self.patterns.append(line[2:].strip())

    #Turn word list to POS tokens

    def wordToToken(self,wordList):
        return nltk.pos_tag(wordList)

    def listToToken(self, sentenceList):
        returnList = []
        for i in sentenceList:
            returnList.append(self.sentenceToToken(i))
        return returnList

        

    #Turn sentence to list of POS tokens
    # 'The great big dog' becomes
    # (The,DT),(great,JJ),(Big,NNP),(dog,NN)
    def sentenceToToken(self,sentence):
        #Seperates sentence into list of words
        text = word_tokenize(sentence)
        return self.wordToToken(text)
        #return nltk.pos_tag(sentence)

    #Turns a sentence to tokens, and returns list
    def sentenceTokenDisplay(self,sentence):
        tokenList = self.sentenceToToken(sentence)
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
    #Compare sentence against all patterns and print if match
    def checkAllPatterns(self,nltkTag, newSentence, sentenceLocationList,originalSentence):
        listOfMatches = []
        for pattern in self.patterns:
            result = self.checkPattern(pattern, nltkTag,newSentence, sentenceLocationList,originalSentence)
            if (result):
                listOfMatches.append(result)
        if len(listOfMatches) == 0:
            listOfMatches.append(False)
        return listOfMatches

    #Check a single sentence against a single pattern
    def checkPattern(self,pattern, nltkTag, newSentence, sentenceLocationList,originalSentence):

        result = re.match(pattern, newSentence)
        #print(result)
        #print(result.groups())
        if result is None:
            self.sentenceCount += 1
            return False
        else:
            showStr = ""
            for counter, value in enumerate(result.groups()):
                gp = counter+1
                wordNum = self.findInList(sentenceLocationList, result.span(gp)[0])
                showStr += nltkTag[wordNum][0] + " "
            resultDict = {  
                            "Matching":showStr,
                            "Regex Matched":pattern,
                            "Full Tokens":newSentence,
                            "Full Matching":originalSentence
                            }
            #return {showStr,pattern,newSentence,originalSentence}
            return resultDict
        return False

    def checkListofWordsRegex(self,tokenList,originalSentence):
        #print(nltkTag)
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
        #print(result.group())
        #print(result.group(1))
        #print(result.span(1))

    def matchToStatement(self,result, nltkTag):
        #print(result.group())
        print("Result is")
        print(result)

    def findRegexMatches(self,inputText):
        matchList = []
        if (not inputText) or (inputText == ""):
            return False

        sentences = sent_tokenize(inputText)
        for x in sentences:
            matchList.append(self.checkSentenceRegex(x))
        #print(matchList)
        if (not matchList):
            return False
        return matchList


    def readFile(self,path):
        f=open(path, "r",encoding="utf8")
        text = f.read()
        return text
        



def main():
    sc = SplitText()
    name = "bird"
    folder = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\articles"
    path = "{0}/{1}.txt".format(folder,name)
    sc.findRegexMatches(sc.readFile(path))
    

        


if __name__== "__main__":
    main()
    #nltk.download()