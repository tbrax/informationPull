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
    articleResultListNeural = []
    for filename in os.listdir(resultFolder):
        if ('-neural' in filename):
            name = filename.replace('-neural.txt','')
            resultDictList = loadResultDict(name+'-neural.txt',nameListNeural,resultFolder)
            try:
                patternDictList = loadResultDict(name+'.txt',nameListPattern,patternFolder)
                articleResultListNeural.append([name,resultDictList,patternDictList])
            except:
                print('Could not load {0}'.format(name+'.txt'))


                


    
    #p = tt.getPatterns()
    #for x in p:
    #    print(x)

    for x in articleResultListNeural:
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
            matchResultList.append([x[0],result['Article Text'], result['Value'], match])

        neuralThere = []
        neuralNot = []
        for y in matchResultList:
            if y[3]:
                neuralThere.append(float(y[2]))
            else:
                neuralNot.append(float(y[2]))
        print('Article name: ',y[0])
        print('Average of located sentences',averageOfList(neuralThere))
        print('Average of Other sentences',averageOfList(neuralNot))
        #print('Total Average',averageOfList(neuralThere+neuralNot))

            

            
        
        



if __name__== "__main__":
    main()