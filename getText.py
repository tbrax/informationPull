import wikipediaapi

import os
folderName = "articles"
loaded = ""
options = 0
class GetText:
    def __init__(self):
        self.loaded = "NONE"
        self.options = []
        self.wiki_wiki = wikipediaapi.Wikipedia('en')
        self.folder = "C:\\Users\\trace\\projects\\python\\masters\\informationpull\\articles"

    def readFile(self,path):
        f=open(path, "r",encoding="utf8")
        return f.read() 
    
    def getArticle(self,name):
        if self.loadWiki(name):
            
            path = "{0}/{1}.txt".format(self.folder,name)          
            return [name, self.readFile(path)]
        return False

    def splitSentencesToList(self,text):
        return text

    def loadWiki(self,fname):
        found = False
        for filename in os.listdir(self.folder):
            if filename == "{0}.txt".format(fname):
                print("Document already exists")
                found = True
                self.loaded = "LOADED"
                return True
        if (not found) and (not fname==""):
            print("Try to load article named {0}".format(fname))
            page_py = self.wiki_wiki.page(fname)
            if page_py.exists():
                encodedStr = page_py.text
                newName = "{0}\\{1}.txt".format(self.folder,fname)
                with open(newName, "w", encoding="utf-8") as f:
                    f.write(encodedStr)
                return True
        return False
                
            #with open("links\\"+fname + ".txt", "w", encoding="utf-8") as f:
            #    for x in wka.links:
            #        addS = str(x) + "|"
            #        f.write(addS)
            #with open("summary\\"+fname + ".txt", "w", encoding="utf-8") as f:
            #    f.write(wka.summary)



    def loadMultipleArticlesFromFile(self):
        path = "{0}\\{1}.txt".format("pdata","list")
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                self.loadWiki(line.strip())

