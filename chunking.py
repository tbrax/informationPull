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

    def compareTreeBool(self,sen0,sen1):
        'Compares two sentences to see if they have same tree'
        parse0 = self.displacyService(sen0)
        parse1 = self.displacyService(sen1)      
        wordsBool = self.tagsIdenticalBool(parse0['words'],parse1['words'])
        arcsBool = (parse0['arcs'] == parse1['arcs'])
        return (wordsBool and arcsBool)
        #return False

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
    sen1 = "Hello There"
    sen2 = 'Men like cheese'
    sen3 = 'Girls like plants'
    print(ch.compareTree(sen2,sen3))


if __name__== "__main__":
    main()