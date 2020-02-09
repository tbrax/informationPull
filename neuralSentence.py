import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
from absl import logging

class NeuralClass:
    def __init__(self):
        self.module_url = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\use" #@param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
        self.model = False

    def loadModel(self):
        self.model = hub.load(self.module_url)

    def embed(self,input):
        if (not self.model):
            self.loadModel()
        if (self.model):
            return self.model(input)
        return False

    def runAndPlotPatterns(self,patterns,text):
        patternEmbed = self.embed(patterns)
        textEmbed = self.embed(text)
        cross = np.inner(textEmbed, patternEmbed)
        #print(cross)
        #self.plot_similarity(text,patterns, textEmbed,patternEmbed, cross)
        #plt.show()
        return cross

    def plot_similarity(self, labels0,labels1, features0,features1, corr):
        #corr = np.inner(features0, features1)
        #print(corr)
        sns.set(font_scale=1.2)
        g = sns.heatmap(
            corr,
            xticklabels=labels1,
            yticklabels=labels0,
            vmin=0,
            vmax=1,
            cmap="YlOrRd")
        g.set_xticklabels(labels1, rotation=90)
        g.set_yticklabels(labels0, rotation=0)
        g.set_title("Semantic Textual Similarity")

#def run_and_plot(messages_):
#   message_embeddings_ = embed(messages_)
#   plot_similarity(messages_, message_embeddings_, 90)



#def comparePatternText(patterns,text):
#    module_url = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\use" #@param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
#    model = hub.load(module_url)
#    print ("module %s loaded" % module_url)

#    runAndPlotPatterns(patterns,text)
    


def main():
    messages = [
    # Smartphones
    "I like my phone",
    "My phone is not good.",
    "Your cellphone looks great.",

    # Weather
    "Will it snow tomorrow?",
    "Recently a lot of hurricanes have hit the US",
    "Global warming is real",

    # Food and health
    "An apple a day, keeps the doctors away",
    "Eating strawberries is healthy",
    "Is paleo better than keto?",

    # Asking about age
    "How old are you?",
    "what is your age?",
    ]

    #run_and_plot(messages)
    plt.show()


if __name__== "__main__":
    main()
    #nltk.download()