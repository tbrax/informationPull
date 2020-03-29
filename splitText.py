import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from timeit import default_timer as timer

import re

#import re

import neuralSentence

class SplitText:
    def __init__(self,tt):
        self.sentenceCount = 0
        self.patternFile = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\patterns.txt"
        self.patternSaveFile = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\patterns.txt"
        self.patternSaveFile2 = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\savedPatterns.txt"
        self.patternFolderNeural = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\patternNeural"
        self.patternFolderRegex = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\patternRegex"
        self.patterns = []
        self.nameListRegex = [
                                "Reduced Sentence",
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
        patternObj = []
        currDict = {}
        dictList = []
        for filename in os.listdir(self.patternFolderNeural):
            text = self.readFileLines(self.patternFolderNeural+'\\'+filename)
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
                elif (line.startswith('FS:')):
                    currDict['FullSentence'] = line[3:].strip()
                    #fullSen.append(line[2:].strip())
                elif (line.startswith('SS:')):
                    currDict['ShortSentence'] = line[3:].strip()
                elif (line.startswith('FP:')):
                    currDict['FullPOS'] = line[3:].strip()
                elif (line.startswith('SP:')):
                    currDict['ShortPOS'] = line[3:].strip()
                    #shortSen.append(line[2:].strip())
                elif (line.startswith('SI:')):
                    currDict['ShortIndex'] = line[3:].strip()
                elif (line.startswith('SR:')):
                    currDict['ShortRegex'] = line[3:].strip()
                    #indxSen.append(line[2:].strip())
                elif (line.startswith('END:')):
                    dictList.append(currDict)
                    currDict = {}
        return dictList

    def patternToSentence(self,pattern):
        words = []
        pos = []
        for x in pattern:
            words.append(x[0]+' ')
            pos.append(x[1]+' ')
        return [words,pos]



    def wordCommaSplit(self,words):
        if words == ',,,':
            x = [',',',']
        elif ',,' in words:
            x = [',']
            y = words[2:]
            for z in y.split(','):
                x.append(z)
        else:
            x = words.split(',')
        return x

    def namedFile(self,folder,articleName):
        f = open(folder+'\\'+articleName[0]+'.txt', "a",encoding="utf-8")
        return f

    def savePattern(self,fullList,shortList,articleName):
        indxString = ''
        fullRegex = ''
        shortRegex = ''
        fullSentence = ''
        shortSentence = ''
        shortPOSString = ''
        fullPOSString = ''
        for idx,i in enumerate(shortList):
            x = self.wordCommaSplit(i)
            #pString+="{1}|..|{0}|,,|".format(x[0],x[1])
            shortRegex += ".*?({0})".format(x[1])
            if (idx == len(shortList)-1):
                shortRegex += ".*?"
            shortPOSString += "{0} ".format(x[1])
            if x[2].isnumeric():
                indxString += "{0} ".format(x[2])
            shortSentence += "{0} ".format(x[0])
        for idx,i in enumerate(fullList):
            x = self.wordCommaSplit(i)
            #sString+="{1}|..|{0}|,,|".format(x[0],x[1])
            fullRegex += ".*?({0})".format(x[1])
            if (idx == len(fullList)-1):
                fullRegex += ".*?"
            fullPOSString += "{0} ".format(x[1])
            fullSentence += "{0} ".format(x[0])
    
        f = self.namedFile(self.patternFolderNeural,articleName)
        f.write("FS:{0}".format(fullSentence))
        f.write("\n")
        f.write("FP:{0}".format(fullPOSString))
        f.write("\n")
        f.write("FR:{0}".format(fullRegex))
        f.write("\n")
        f.write("SS:{0}".format(shortSentence))
        f.write("\n")
        f.write("SP:{0}".format(shortPOSString))
        f.write("\n")
        f.write("SR:{0}".format(shortRegex))
        f.write("\n")
        f.write("SI:{0}".format(indxString))
        f.write("\n")
        f.write("END:")
        f.write("\n")
        return 0
  
    def saveRegexPattern(self,fullList,shortList,articleName):
        fullSentence = ""
        shortSentence = ""
        pString = ""
        sString = ""
        for idx,value in enumerate(shortList):
            x = value.split(",")
            pString += ".*?({0})".format(x[1])
            shortSentence += "{0} ".format(x[0])
            if (idx == len(shortList)-1):
                pString += ".*?"
        for idx,value in enumerate(fullList):
            x = value.split(",")
            sString += ".*?({0})".format(x[1])
            fullSentence += "{0} ".format(x[0])
            if (idx == len(fullList)-1):
                sString += ".*?"

        f = self.namedFile(self.patternFolderRegex,articleName)
        f.write("SR:{0}".format(pString))
        f.write("\n")
        f.write("SS:{0}".format(shortSentence))
        f.write("\n")
        f.write("FR:{0}".format(sString))
        f.write("\n")
        f.write("FS:{0}".format(fullSentence))
        f.write("\n")
        f.write("END:")


    def loadRegexPatterns(self):
        'Load Regex Patterns from file'
        ps = []
        for filename in os.listdir(self.patternFolderNeural):
            with open(self.patternFolderRegex+'\\'+filename, "r", encoding="utf-8") as f:
                for line in f:
                    if (line.startswith('SR:')):
                        ps.append(line[2:].strip())
        return ps
  
    def getRegexPatterns(self):
        return False
        return self.loadRegexPatterns()

    def wordToToken(self,wordList):
        'Turn word list to POS tokens'
        return nltk.pos_tag(wordList)

    def listToToken(self, sentenceList):
        returnList = []
        for i in sentenceList:
            returnList.append(self.sentenceToToken(i))
        return returnList

    def sentenceToToken(self,sentence):
        'Turn sentence to list of POS tokens"The great big dog" becomes "(The,DT),(great,JJ),(Big,NNP),"(dog,NN)'
        #text = word_tokenize(sentence)
        #return self.wordToToken(text)
        return self.sentenceTokenDisplay(sentence)
 
    def sentenceTokenDisplay(self,sentence):
        'Turns a sentence to tokens, and returns list'
        tokenList = self.tt.returnPOSList(sentence)
        return tokenList

    def textToSentenceList(self,text):
        return sent_tokenize(text)

    #Turn sentence 
    def checkSentenceRegex(self,sentence,patternList):
        tks = self.sentenceToToken(sentence)
        result = self.checkListofWordsRegex(tks,sentence,patternList)
        return result

    def findInList(self,givenList, item):
        try:
            return givenList.index(item)
        except ValueError:
            return -1

    def checkAllPatterns(self,nltkTag, newSentence, sentenceLocationList,originalSentence,patternList):
        'Compare sentence against all patterns and pront if match'
        listOfMatches = []
        
        totalP = len(patternList)
        start = timer()
        
        
        for idx,pattern in enumerate(patternList):
            #print('{0} of {1}'.format(idx,totalP))
            result = self.checkPattern(pattern, nltkTag,newSentence, sentenceLocationList,originalSentence)
            end = timer()
            
            if (result):
                listOfMatches.append(result)
            if (end - start) > 0.1:
                break
        print('Finished patterns')
        if len(listOfMatches) == 0:
            listOfMatches.append(False)
        return listOfMatches

    def checkPattern(self,pattern, nltkTag, newSentence, sentenceLocationList,originalSentence):
        'Check a single sentence against a single pattern'
        #print(newSentence,pattern)
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

    def checkListofWordsRegex(self,tokenList,originalSentence,patternList):
        newSentence = ""
        sentenceLocationCount = 0
        sentenceLocationList = []
        
        for x in tokenList:
            characterAdd = x[1]+" "
            newSentence += characterAdd
            sentenceLocationList.append(sentenceLocationCount)
            sentenceLocationCount += len(characterAdd)

        patternMatches = self.checkAllPatterns(tokenList,newSentence, sentenceLocationList,originalSentence,patternList)
        return patternMatches
        #pront(result.group())
        #pront(result.group(1))
        #pront(result.span(1))


    def findRegexMatches(self,inputText):
        matchList = []
        print(inputText)
        #if (not inputText) or (inputText == ""):
        #    return False

        #sentences = sent_tokenize(inputText)
        #for x in sentences:
        #    matchList.append(self.checkSentenceRegex(x))
        #if (not matchList):
        #    return False
        return matchList

    def readFile(self,path):
        f=open(path, "r",encoding="utf8")
        text = f.read()
        return text
        