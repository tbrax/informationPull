import re
import spacy
import pytextrank
import nltk
from spacy import displacy
from joblib import Parallel, delayed
class Chunking:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.debug = False
        self.oklist = ['ADJ','PUNCT','CCONJ','NOUN']
        self.posList = [
                        ['NOUN','PROPN'],
                        ]
        self.tt = False
    def addTT(self,tt):
        self.tt = tt
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

    def reduceGuess(self,sentence):
        docFull = self.nlp(sentence)
        rootFull = [token for token in docFull if token.head == token][0]

        for tok in list(docFull):
            print(tok)
        return False

    def importantReturnToken(self,tok):
        returnList = []
        tkList = ['ADJ','PUNCT']
        for x in tok.subtree:
            if (x is tok):
                returnList.append(x)
            elif (x.pos_ not in tkList):
                returnList += self.importantReturnToken(x)
        return returnList

    def findTokenObj(self,find,tok0,tok1,parent):
        if find == tok0: 
            return self.importantReturnToken(tok1)

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


    def constructReducedSentence(self,index,articleSentence,fullSentence,shortSentence):
        indexList = index.split(" ")
        indexs = []
        for x in indexList:
            try:
                indexs.append(int(x))
            except:
                print(index,articleSentence,fullSentence,shortSentence)
        return self.constructReducedSentenceOnce(indexs,articleSentence,fullSentence,shortSentence)

    def constructReducedSentenceOnce(self,indexList,articleSentence,fullSentence,shortSentence):
        'Takes a full sentence and turns it into a reduced one'
        docArticle = articleSentence
        docShort = shortSentence
        docFull = self.nlp(fullSentence)

        rootArticle = [token for token in docArticle if token.head == token][0]
        rootShort = [token for token in docShort if token.head == token][0]
        rootFull = [token for token in docFull if token.head == token][0]

        tokensInFull = []
        tokensInArticle = []
        returnSentence = ''
        #pront(docShort,indexList,fullSentence)
        for x in indexList:
            try:
                tokensInFull.append(docFull[x])
            except:
                #pront(docFull.__len__())
                True
        for x in tokensInFull:
            find = self.findTokenObj(x,rootFull,rootArticle,rootArticle)
            tokensInArticle.append(find)
        #pront(tokensInArticle)
        returnSentenceList = []
        for x in tokensInArticle:
            if x:
                for y in x:
                    if y not in returnSentenceList:
                        returnSentenceList.append(y) 
        for x in returnSentenceList:
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
        for x in self.posList:
            if pos0 in x and pos1 in x:
                return True
        return False

    def posAcceptExcess(self,tok0):
        self.pront('Is {0}, {1} ok to drop?'.format(tok0,tok0.pos_))
        if tok0.pos_ not in self.oklist:
            return False
        return True

    def pront(self,*msg):
        if self.debug:
            print(msg)

    def importantToken(self,tok):
        trivList = ['ADJ','PUNCT','CCONJ']
        if tok.pos_ not in trivList:
            return True
        return False

    def compareTokens(self,tokList0,tokList1):
        if (len(tokList0) is 0) and (len(tokList1)is 0):
            return True
        if len(tokList0) is not len(tokList1):
           self.pront('Not same size',tokList0,tokList1)
           return False
        for idx,x in enumerate(tokList0):
            if not self.posMatch(tokList0[idx].pos_,tokList1[idx].pos_):
                self.pront('POS mismatch',tokList0[idx].pos_,tokList1[idx].pos_)
                return False

        treel0 = []
        treer0 = []
        treel1 = []
        treer1 = []
        for x in tokList0:
            lefts = x.lefts
            rights = x.rights
            for l0 in lefts:
                if self.importantToken(l0):
                    treel0.append(l0)
            for r0 in rights:
                if self.importantToken(r0):
                    treer0.append(r0)
        for x in tokList1:
            lefts = x.lefts
            rights = x.rights
            for l1 in lefts:
                if self.importantToken(l1):
                    treel1.append(l1)
            for r1 in rights:
                if self.importantToken(r1):
                    treer1.append(r1)
        #print(treel0,treer0)
        #print(treel1,treer1)
        if not self.compareTokens(treel0,treel1):
            return False
        if not self.compareTokens(treer0,treer1):
            return False
        return True


    def compareTokenObj(self,tok0,tok1):
        matchTotal = self.posMatch(tok0.pos_,tok1.pos_)      
        if not matchTotal:
            self.pront('Fail', tok0, tok0.pos_, tok1, tok1.pos_)
        else:
            self.pront('Pass', tok0, tok0.pos_, tok1, tok1.pos_)
            self.pront(list(tok0.lefts),list(tok1.lefts))
            self.pront(list(tok0.rights),list(tok1.rights))
        if not matchTotal:
            return False
        '''
        l0 = list(tok0.lefts)
        l1 = list(tok1.lefts)
        if len(l0) > 0 and len(l1) > 0:
            new0 = " ".join(str(x) for x in l0)
            new1 = " ".join(str(x) for x in l1)
            if not self.compareTreeBool(new0,new1):
                return False

        l0 = list(tok0.rights)
        l1 = list(tok1.rights)
        if len(l0) > 0 and len(l1) > 0:
            if not self.compareTreeBool(" ".join(str(x) for x in l0)," ".join(str(x) for x in l1)):
                return False

        '''

        l0 = list(tok0.lefts)
        l1 = list(tok1.lefts)
        
        if len(l0) > len(l1):
            for idx0,x0 in enumerate(l0[len(l1):]):
                #print(x0)
                if not self.posAcceptExcess(x0):
                    #matchTotal = False
                    return False
        elif len(l1) > len(l0):
            for idx0,x0 in enumerate(l1[len(l0):]):
                if not self.posAcceptExcess(x0):
                    #matchTotal = False
                    return False

        if len(l0) > len(l1):
            for idx0,x0 in enumerate(l0[len(l1):]):
                if not self.posAcceptExcess(x0):
                    #matchTotal = False
                    return False

        elif len(l1) > len(l0):
            for idx0,x0 in enumerate(l1[len(l0):]):
                if not self.posAcceptExcess(x0):
                    #matchTotal = False
                    return False
        
        if matchTotal:
            for idx0,x0 in enumerate(tok0.lefts):
                for idx1,x1 in enumerate(tok1.lefts):
                    if idx0 == idx1:
                        if self.compareTokenObj(x0,x1) is False:
                            #matchTotal = False
                            return False
        if matchTotal:
            for idx0,x0 in enumerate(tok0.rights):
                for idx1,x1 in enumerate(tok1.rights):
                    if idx0 == idx1:
                        if self.compareTokenObj(x0,x1) is False:
                            #matchTotal = False     
                            return False
        
        return True

    def compareToken(self,a,b):
        return a.pos_ == b.pos_


    def compareSubTree(self,depth,a,b):
        if (depth > 5):
            return False
        bothLimitLeft = (a == a.left_edge and b == b.left_edge)
        bothLimitRight = (a == a.right_edge and b == b.right_edge)
        #pront(a,a.left_edge,a.right_edge,b,b.left_edge,b.right_edge)
        if ((a is None and b is None)):
            return True 
        if a is not None and b is not None: 
            dataSame = (a.pos_ == b.pos_)
            left = self.compareSubTree(depth+1,a.left_edge,b.left_edge)
            right = self.compareSubTree(depth+1,a.right_edge,b.right_edge)

            ret = (dataSame and left and right)
            return ret

        return False

    def compareTreeBool(self,sen0,sen1):
        'Compares two sentences to see if they have same tree'
        doc0 = self.nlp(sen0)
        doc1 = self.nlp(sen1)
        root0 = [token for token in doc0 if token.head == token][0]
        root1 = [token for token in doc1 if token.head == token][0]
        if self.debug:
            self.pront('Check', sen0,sen1)
        result = self.compareTokenObj(root0,root1)
        #result = self.compareTokens([root0],[root1])
        #result = self.compareSubTree(0,root0,root1)
        #self.serve(sen0)
        return result

    def exactMatch(self,sen0,sen1):
        return self.exactMatchDoc(self.nlp(sen0),self.nlp(sen1))

    def exactMatchDoc(self,doc0,doc1):

        posList0 = []
        posList1 = []

        for token in doc0:
            posList0.append(token.pos_)
        for token in doc1:
            posList1.append(token.pos_)

        return posList0 == posList1

    def compareTree(self,sen0,sen1):
        'Compares two sentences to see if they have same tree'
        return self.compareTreeBool(sen0,sen1)
    

    def compareTreeSingle(self,doc0,doc1):
        root0 = [token for token in doc0 if token.head == token][0]
        root1 = [token for token in doc1 if token.head == token][0]
        return self.compareTokenObj(root0,root1)

    def compareRegexAll(self,articleList,patternList):
        #print('Check Regexes')
        articleDocs = []
        matchList = []

        regexList = []
        for x in patternList:
            if 'ShortRegex' in x:
                if x['ShortRegex'] not in regexList:
                    regexList.append(x['ShortRegex'])


        print('Num of sentences: ',len(articleList))
        print('Num of patterns: ',len(regexList))
        print('Total Checks: ',len(articleList)*len(regexList))
        matchList = []
        for idx,sentence in enumerate(articleList):
            #print(idx)
            #print(sentence)
            matchList.append(self.tt.st.checkSentenceRegex(sentence,regexList))
        #result = re.match(pattern, newSentence) 

        return matchList

    def compareTreeAll(self,articleList,PatternList):
        articleDocs = []
        matchList = []
        for x in articleList:
            articleDocs.append(self.nlp(x))

        for y in PatternList:
            doc0 = self.nlp(y['ShortSentence'])
            for idx,x in enumerate(articleList):
                if self.compareTreeSingle(doc0,articleDocs[idx]):
                    resultDict = {
                                        'Article Sentence':x,
                                        'Pattern Sentence':y['ShortSentence'],
                                        } 
                    match = self.exactMatchDoc(doc0,articleDocs[idx])
                    if match:
                            resultDict['Exact'] = 'Exact'
                    if (y['FullSentence'] is not y['ShortSentence']):
                            reducedSen = self.constructReducedSentence(y['ShortIndex'],articleDocs[idx],y['FullSentence'],doc0)
                            resultDict['Reduced Sentence'] = reducedSen  

                    matchList.append(resultDict)
        return matchList

def main():
    #nltk.download()
    ch = Chunking()
    #conference_text = ('He is interested in learning natural language processing')
    #conference_doc = ch.processText(conference_text)
    #for chunk in conference_doc.noun_chunks:
    #    pront (chunk)   
    #for token in conference_doc:
        #pront(token)
    #    pront (token.text, token.tag_, token.head.text, token.dep_) 
    #pront(displacy.render(conference_doc, style='dep'))
    sens = [
            'He is interested in learning natural language processing',
            'Big hairy men like cheese',
            'Girls like green plants',
            'A lake is an area',
            "A blue lake is an area filled with water.",
            'A desert is a place filled with course, fine sand.',
            'A taco is a traditional Mexican food consisting of a small hand-sized tortilla.',
            'A taco is a tasty, traditional Mexican food',
            'A banana is an Australian fruit',
            'displaCy uses CSS and JavaScript to show you how computers understand language',
            'The cat has no unique anatomical feature that is clearly responsible for the sound.',
            'The cat ( Felis catus ) is a small carnivorous mammal .',
            "The cat has no unique anatomical feature that is clearly responsible for the sound.",
            'A man is a human',
    ]
    #print(ch.compareTree(sens[4],sens[7]))
    #print(ch.exactMatch(ch.nlp(sens[3]),ch.nlp(sens[13])))
    #ch.reduceGuess(sens[1])
    #print(result)
    index = [0,2,3,4,5]
    #print(ch.constructReducedSentence(index,sens[5],sens[4],sens[3]))


if __name__== "__main__":
    main()