class TextObject:
    def __init__(self):
        self.sentences = []
        self.matchesCrafted = []
        self.matchesRegex = []
        self.matchesNeural = []
        self.title = ""

    def reset(self):
        self.sentences = []
        self.matchesCrafted = []
        self.matchesRegex = []
        self.matchesNeural = []

    def findNeuralMatches(self):
        return 0

    def saveSentences(self,title,sentences):
        self.title = title
        self.sentences = sentences
       
        return 0