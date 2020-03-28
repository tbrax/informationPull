import os
import json
from splitText import SplitText
from textObject import TextObject

resultFolder = 'C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\results'
patternFolder = 'C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\patternNeural'
tt = TextObject()
nameListNeural = [
                        'Value',
                        'Pattern Grammar',
                        'Pattern Sentence',
                        'Article Grammar',
                        'Article Sentence',
                        'Compared'
                    ]
nameListTree = [    
                    'Article Sentence',
                    'Short Sentence',
                    'Reduced Sentence'
                    ]
nameListRegex = [
                    'Article Sentence',
                    'Reduced Sentence',
                    'Regex Matched'
                    ]
    
endName = 'END:'

nameListPattern = [
                        'FS',
                        'SS',
                        'FR',
                        'SR',
                        'SI'
                    ]



def averageOfList(lst): 
    return sum(lst) / len(lst) 

def loadResultDict(filename,nameList,folder):
    with open(folder+'\\'+filename, "r", encoding="utf-8") as f:
        dictList = []
        tDict = {}
        for line in f:
            for name in nameList:
                tx = '{0}:'.format(name)
                if (line.startswith(tx)):
                    reduced = line[len(tx):].strip()
                    tDict[name] = reduced
            if (line.startswith(endName)):
                dictList.append(tDict)
                tDict = {}   
        return dictList
    return False


def loadFileType(typeName,nameList):
    articleResultList = []
    for filename in os.listdir(resultFolder):    
        if (typeName in filename):
            name = filename.replace(typeName+'.txt','')
            resultDictList = loadResultDict(name+typeName+'.txt',nameList,resultFolder)
            try:
                patternDictList = loadResultDict(name+'.txt',nameListPattern,patternFolder)
                articleResultList.append([name,resultDictList,patternDictList])
            except:
                print('Could not load {0}'.format(name+'.txt'))
    return articleResultList




def displayNeuralResults(art,resultList):
     for x in resultList:
        if x[0] == art:
            matchResultList = []
            for result in x[1]:
                match = False
                for hand in x[2]:
                    sen0 = result['Article Sentence'].replace(' ','')
                    sen1 = hand['FS'].replace(' ','')
                    if (sen0 == sen1):
                        match = hand
                #r0 = result.get('Article Sentence',False)
                #r1 = result.get('Value',False)
                matchResultList.append([x[0], result, match])

            thereList = []
            notList = []
            for y in matchResultList:
                if y[2]:
                    thereList.append(float(y[1]['Value']))
                else:
                    notList.append(float(y[1]['Value']))

            print('Neural results for: ',y[0])
            print('Average of located sentences',averageOfList(thereList))
            print('Average of Other sentences',averageOfList(notList))
            #print('Total Average',averageOfList(neuralThere+neuralNot))

def displayTreeResults(art,resultList):
    for x in resultList:
        if x[0] == art:
            matchResultList = []
            matchHandList = []
            #######
            for result in x[1]:
                match = False
                for hand in x[2]:
                    sen0 = result['Article Sentence'].replace(' ','')
                    sen1 = hand['SS'].replace(' ','')
                    if (sen0 == sen1):
                        match = hand               

                matchResultList.append([x[0], result, match])

            for hand in x[2]:
                match = False
                for result in x[1]:
                    sen0 = result['Article Sentence'].replace(' ','')
                    sen1 = hand['SS'].replace(' ','')
                    if (sen0 == sen1):
                        match = result

                matchHandList.append([x[0], match, hand])

            matchedHand = []
            extraHand = []
            matchedResult = []
            extraResult = []

            for y in matchHandList:
                if y[1]:
                    matchedHand.append(y)
                else:
                    extraHand.append(y)

            for y in matchResultList:
                if y[2]:
                    matchedResult.append(y)
                else:
                    extraResult.append(y)
            
            print('Tree results for: ',y[0])
            print('Total Hand Picked Values', len(matchHandList))
            print('Matched: ',len(matchedHand))
            print('Hand Missed: ', len(extraHand))
            
            extraNoDuplicates = []
            for y in extraResult:
                sen = y[1]['Article Sentence']
                if sen not in extraNoDuplicates:
                    extraNoDuplicates.append(sen)

            print('Result Extra: ',len(extraNoDuplicates))
            for y in extraNoDuplicates:
                print('"{0}"'.format(y))
            
def displayRegexResults(art,resultList):
    
    for x in resultList:

        if x[0] == art:
            matchResultList = []
            matchHandList = []
            #######
            for result in x[1]:
                match = False
                if len(result) > 0:
                    for hand in x[2]:
                        sen0 = result['Article Sentence'].replace(' ','')

                        sen1 = hand['SS'].replace(' ','')
                        if (sen0 == sen1):
                            match = hand               

                matchResultList.append([x[0], result, match])

            for hand in x[2]:
                match = False
                for result in x[1]:
                    if len(result) > 0:
                        sen0 = result['Article Sentence'].replace(' ','')
                        sen1 = hand['SS'].replace(' ','')
                        if (sen0 == sen1):
                            match = result

                matchHandList.append([x[0], match, hand])

            matchedHand = []
            extraHand = []
            matchedResult = []
            extraResult = []

            for y in matchHandList:
                if y[1]:
                    matchedHand.append(y)
                else:
                    extraHand.append(y)

            for y in matchResultList:
                if y[2]:
                    matchedResult.append(y)
                else:
                    extraResult.append(y)
            
            print('Regex results for: ',y[0])
            print('Total Hand Picked Values', len(matchHandList))
            print('Matched: ',len(matchedHand))
            print('Hand Missed: ', len(extraHand))
            
            extraNoDuplicates = []
            for y in extraResult:
                if len(y[1]) > 0:
                    sen = y[1]['Article Sentence']
                    if sen not in extraNoDuplicates:
                        extraNoDuplicates.append(sen)

            print('Result Extra: ',len(extraNoDuplicates))
            for y in extraNoDuplicates:
                #False
                print('"{0}"'.format(y))


def main(): 
    #displayNeuralResults('cat',loadFileType('-neural',nameListNeural))
    #displayTreeResults('cat',loadFileType('-tree',nameListTree))
    displayRegexResults('cat',loadFileType('-regex',nameListRegex))


   

        

            

            
        
        



if __name__== "__main__":
    main()