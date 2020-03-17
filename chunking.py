import spacy
from spacy import displacy
class Chunking:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.debug = False

    def processText(self,text):
        'Returns a spacy text object'
        return self.nlp(text)

    def displacyService(self,text):
        'Returns a graph object'
        doc = self.nlp(text)
        return displacy.parse_deps(doc)

    def treeHTML(self,text):
        'Takes a sentence. Returns a string of HTML that displays a picture of the nlp graph'
        return displacy.render(self.processText(text), style='dep')

    def findTokenObj(self,find,tok0,tok1,parent):
        if find == tok0:
            return tok1

        for idx0,x0 in enumerate(tok0.lefts):
            for idx1,x1 in enumerate(tok1.lefts):
                if idx0 == idx1:
                    left = self.findTokenObj(find,x0,x1,tok0)
                    if left is not False:
                        return left
        for idx0,x0 in enumerate(tok0.rights):
            for idx1,x1 in enumerate(tok1.rights):
                if idx0 == idx1:
                    right = self.findTokenObj(find,x0,x1,tok0)
                    if right is not False:
                        return right
        return False


    def constructReducedSentence(self,indexList,articleSentence,fullSentence,shortSentence):
        'Takes a full sentence and turns it into a reduced one'
        docArticle = self.nlp(articleSentence)
        docShort = self.nlp(shortSentence)
        docFull = self.nlp(fullSentence)

        rootArticle = [token for token in docArticle if token.head == token][0]
        rootShort = [token for token in docShort if token.head == token][0]
        rootFull = [token for token in docFull if token.head == token][0]

        tokensInFull = []
        tokensInArticle = []
        returnSentence = ''
        for x in indexList:
            tokensInFull.append(docFull[x])
        for x in tokensInFull:
            find = self.findTokenObj(x,rootFull,rootArticle,rootArticle)
            tokensInArticle.append(find)
        print(list(tokensInArticle))
        
        for x in tokensInArticle:
            if x:
                returnSentence += (x.text+' ')
        return returnSentence

    def returnPOSList(self,sentence):
        ls = []
        doc = self.nlp(sentence)
        for x in doc:
            ls.append([x.text,x.pos_])
        return ls

    def tagsIdenticalBool(self,wordList0,wordList1):
        if len(wordList0) is not len(wordList1):
            return False
        for idx, x in enumerate(wordList0):
            if wordList0[idx]['tag'] is not wordList1[idx]['tag']:
                return False
        return True

    def posMatch(self,pos0,pos1):
        if (pos0 == pos1):
            return True
        return False

    def compareTokenObj(self,tok0,tok1):
        matchTotal = self.posMatch(tok0.pos_,tok1.pos_)
        if self.debug == True:
            if not matchTotal:
                print("Failed")
            print(tok0, tok0.pos_, tok1, tok1.pos_)
            print(list(tok0.lefts),list(tok1.lefts))
            print(list(tok0.rights),list(tok1.rights))

        for idx0,x0 in enumerate(tok0.lefts):
            for idx1,x1 in enumerate(tok1.lefts):
                if idx0 == idx1:
                    if self.compareTokenObj(x0,x1) is False:
                        matchTotal = False

        for idx0,x0 in enumerate(tok0.rights):
            for idx1,x1 in enumerate(tok1.rights):
                if idx0 == idx1:
                    if self.compareTokenObj(x0,x1) is False:
                        matchTotal = False     
        return matchTotal

    def compareToken(self,a,b):
        return a.pos_ == b.pos_


    def compareSubTree(self,depth,a,b):
        if (depth > 5):
            return False
        bothLimitLeft = (a == a.left_edge and b == b.left_edge)
        bothLimitRight = (a == a.right_edge and b == b.right_edge)
        #print(a,a.left_edge,a.right_edge,b,b.left_edge,b.right_edge)
        if ((a is None and b is None)):
            return True 
        if a is not None and b is not None: 
            dataSame = (a.pos_ == b.pos_)
            #print("Left")
            left = self.compareSubTree(depth+1,a.left_edge,b.left_edge)
            #print("Right")
            right = self.compareSubTree(depth+1,a.right_edge,b.right_edge)

            ret = (dataSame and left and right)
            print("Compare", ret)
            return ret

        return False

    def compareTreeBool(self,sen0,sen1):
        'Compares two sentences to see if they have same tree'
        doc0 = self.nlp(sen0)
        doc1 = self.nlp(sen1)
        root0 = [token for token in doc0 if token.head == token][0]
        root1 = [token for token in doc1 if token.head == token][0]
        result = self.compareTokenObj(root0,root1)
        #result = self.compareSubTree(0,root0,root1)
        #self.serve(sen0)
        return result

    def compareTree(self,sen0,sen1):
        'Compares two sentences to see if they have same tree'
        return self.compareTreeBool(sen0,sen1)

def main():
    ch = Chunking()
    #conference_text = ('He is interested in learning natural language processing')
    #conference_doc = ch.processText(conference_text)
    #for chunk in conference_doc.noun_chunks:
    #    print (chunk)   
    #for token in conference_doc:
        #print(token)
    #    print (token.text, token.tag_, token.head.text, token.dep_) 
    #print(displacy.render(conference_doc, style='dep'))
    sens = [
            'He is interested in learning natural language processing',
            'Men like cheese',
            'Girls like green plants',
            'A lake is an area',
            "A blue lake is an area filled with water.",
            'A desert is a place filled with course, fine sand.',
            'A taco is a traditional Mexican food consisting of a small hand-sized tortilla.',
            'A taco is a blue and gold traditional Mexican food',
            'A banana is an Australian fruit consisting of a yellow, stinky peel',
            'displaCy uses CSS and JavaScript to show you how computers understand language',

    ]
    #result = ch.compareTree(sens[4],sens[7])
    #print(result)

    index = [0,2,3,4,5]
    print(ch.constructReducedSentence(index,sens[5],sens[4],sens[3]))


if __name__== "__main__":
    main()