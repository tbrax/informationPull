
from neuralSentence import NeuralClass
from splitText import SplitText
from getText import GetText


class TextObject:
    def __init__(self):
        self.sentences = []
        self.matchesCrafted = []
        self.matchesRegex = []
        self.matchesNeural = []
        self.title = ""
        self.textLoaded = False
        self.Neural = False
        self.st = SplitText()

    def reset(self):
        self.sentences = []
        self.matchesCrafted = []
        self.matchesRegex = []
        self.matchesNeural = []

    def findNeuralMatches(self):
        if self.textLoaded:
            #if not self.Neural:
            #    self.Neural = NeuralClass()
            #    self.Neural.loadModel()
            testText = ["Dog is big",
                    "Cat is small",
                    "Mice are white"
                    ]

            text = testText
            #text = self.sentences

            grammarTextList = self.st.listToToken(text)
            grammarText = []
            for senList in grammarTextList:
                sentence = ""
                for word in senList:
                    sentence +=  word[0]+" "
                grammarText.append(sentence)
            
            

            patterns = self.st.getPatternObject()
            patternShort = patterns[0]
            patternFull = patterns[1]
            grammarPattern = []
            for senList in patternFull:
                sentence = ""
                for word in senList:
                    sentence +=  word[1]+" "
                grammarPattern.append(sentence)

            print(grammarText)
            print(grammarPattern)
            #print(patterns)
            
            #self.Neural.runAndPlotPatterns(patterns,text)


    def saveSentences(self,title,sentences):
        self.textLoaded = True
        self.title = title
        self.sentences = sentences
       


def main():
    tt = TextObject()
    
    tt.textLoaded = True
    tt.findNeuralMatches()


if __name__== "__main__":
    main()