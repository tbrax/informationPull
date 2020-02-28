import spacy
from spacy import displacy
class Chunking:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def processText(self,text):
        'Returns a spacy text object'
        return self.nlp(text)

    def treeHTML(self,text):
        'Takes a sentence. Returns a string of HTML that displays a picture of the nlp graph'
        return displacy.render(self.processText(text), style='dep')

def main():
    ch = Chunking()
    conference_text = ('He is interested in learning natural language processing')
    conference_doc = ch.processText(conference_text)
    #for chunk in conference_doc.noun_chunks:
    #    print (chunk)   
    for token in conference_doc:
        #print(token)
        print (token.text, token.tag_, token.head.text, token.dep_) 
    print(displacy.render(conference_doc, style='dep'))

if __name__== "__main__":
    main()