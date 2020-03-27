import os
import json

resultFolder = 'C:\\Users\\trace\\projects\\python\\masters\\informationPull\\pdata\\results'


def main():
    
    nameListNeural = [
                            "Value",
                            "Pattern Grammar",
                            "Pattern Sentence",
                            "Article Grammar",
                            "Article Text",
                            "Compared"
                        ]
    endName = 'END:'
    articleResultList = []

    for filename in os.listdir(resultFolder):
        with open(resultFolder+'\\'+filename, "r", encoding="utf-8") as f:
            dictList = []
            tDict = {}
            for line in f:
                for name in nameListNeural:
                    tx = '{0}:'.format(name)
                    if (line.startswith(tx)):
                        reduced = line[len(tx)].strip()
                        tDict[name] = reduced
                if (line.startswith(endName)):
                    dictList.append(tDict)
                    tDict = {}
                
        articleResultList.append([filename.replace('.txt',''),dictList])
    

    for x in articleResultList:
        print(x[0])
        for y in x[1]:
            print(y)
            
        
        



if __name__== "__main__":
    main()