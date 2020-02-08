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

module_url = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\use" #@param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
model = hub.load(module_url)
def embed(input):
    if (model):
        return model(input)
    return False


def plot_similarity(labels, features, rotation):
    corr = np.inner(features, features)
    print(corr)
    sns.set(font_scale=1.2)
    g = sns.heatmap(
        corr,
        xticklabels=labels,
        yticklabels=labels,
        vmin=0,
        vmax=1,
        cmap="YlOrRd")
    g.set_xticklabels(labels, rotation=rotation)
    g.set_title("Semantic Textual Similarity")

def run_and_plot(messages_):
    message_embeddings_ = embed(messages_)
    plot_similarity(messages_, message_embeddings_, 90)

def runAndPlotPatterns(patterns,text):
    patternEmbed = embed(patterns)
    textEmbed = embed(text)

def comparePatternText(patterns,text):
    module_url = "C:\\Users\\trace\\projects\\python\\masters\\informationPull\\use" #@param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
    model = hub.load(module_url)
    print ("module %s loaded" % module_url)

    runAndPlotPatterns(patterns,text)
    


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

    run_and_plot(messages)
    plt.show()


if __name__== "__main__":
    main()
    #nltk.download()