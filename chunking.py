import spacy
from spacy import displacy
class Chunking:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

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



    def compareTreeBool(self,sen0,sen1):
        'Compares two sentences to see if they have same tree'
        #parse0 = self.displacyService(sen0)
        #parse1 = self.displacyService(sen1)

        doc0 = self.nlp(sen0)
        doc1 = self.nlp(sen1)
        root0 = [token for token in doc0 if token.head == token][0]
        root1 = [token for token in doc1 if token.head == token][0]

        #same = self.compareTokenObj(root0,0)
        #print(root0.text)
        #parse1 = self.nlp(sen1).token
        result = self.compareTokenObj(root0,root1)
        #print(result)
        #self.compareTokenObj(root1)
        #print(list(root0.subtree))
        #    print(x.head)
        #    chs = x.children
        #    for y in chs:
        #        print(y.pos_)


        #wordsBool = self.tagsIdenticalBool(parse0['words'],parse1['words'])
        # = (parse0['arcs'] == parse1['arcs'])
        #return (wordsBool and arcsBool)
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
    sen0 = 'He is interested in learning natural language processing'
    
    sen1 = 'Men like cheese'
    sen2 = 'Girls like green plants'

    sen3 = "A blue lake is an area filled with water."
    sen4 = 'A desert is a area filled with course, fine sand.'

    result = ch.compareTree(sen1,sen4)
    print(result)


if __name__== "__main__":
    main()