import os
import json
from splitText import SplitText
from textObject import TextObject

resultFolder = 'C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\results'
patternFolder = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\patternNeural"
tt = TextObject()
nameListNeural = [
                        "Value",
                        "Pattern Grammar",
                        "Pattern Sentence",
                        "Article Grammar",
                        "Article Text",
                        "Compared"
                    ]
endName = 'END:'

nameListPattern = [
                        "FS",
                        "SS",
                        "FR",
                        "SR",
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


def main(): 
    articleResultList = []
    for filename in os.listdir(resultFolder):
        name = filename.replace('.txt','')
        resultDictList = loadResultDict(name+'.txt',nameListNeural,resultFolder)
        try:
            patternDictList = loadResultDict(name+'.txt',nameListPattern,patternFolder)
            articleResultList.append([name,resultDictList,patternDictList])
        except:
            print('Please add pattern file back to folder')

    
    #p = tt.getPatterns()
    #for x in p:
    #    print(x)

    for x in articleResultList:
        #print(x[0])
        #for y in x[2]:
        #    print(y)

        matchResultList = []

        for result in x[1]:
            match = False
            for hand in x[2]:
                sen0 = result['Article Text'].replace(' ','')
                sen1 = hand['FS'].replace(' ','')
                if (sen0 == sen1):
                    match = hand
            matchResultList.append([result['Article Text'], result['Value'], match])

        neuralThere = []
        neuralNot = []
        for y in matchResultList:
            if y[2]:
                neuralThere.append(float(y[1]))
            else:
                neuralNot.append(float(y[1]))
        print('Average of located sentences',averageOfList(neuralThere))
        print('Average of Other sentences',averageOfList(neuralNot))

            

            
        
        



if __name__== "__main__":
    main()