from tqdm import tqdm
import matplotlib.pyplot as plt 
import multiprocessing
import editdistance
from numba import autojit
import re
import numpy as np
from scipy import spatial
import math
from Levenshtein import distance
from fasttext import FastVector





def read_weight_dictionary(file):
    f = open(file, 'r')
    dictionary = {}
    for line in f:
        m = re.search("([^ ]+) (.*)", line) # this is for tibetan
        #m = re.search("([^\t]+)\t(.*)", line) # this is for chinese
        if m:
            word = m.group(1)
            count = m.group(2)
            dictionary[word] = count
    return dictionary




def read_stopwords(file):
    f = open(file, 'r')
    dictionary = []
    for line in f:
        m = re.search("(.*)", line) # this is for tibetan
        #m = re.search("([^\t]+)\t(.*)", line) # this is for chinese
        if m:
            if not m[0] == "#":
                dictionary.append(m.group(1).strip())
    return dictionary

def load_data():
    global skt_dictionary,wdict_skt,skt_words,skt_stop
    print("Loading data")
    skt_dictionary = FastVector(vector_file='../data/skt_vectors.vec')
    wdict_skt = read_weight_dictionary("../data/word_count_skt.txt")
    skt_words = set(skt_dictionary.word2id.keys())
    skt_stop = read_stopwords("/home/basti/deeplearning/bilingual/skt2tib/data/skt_stop.txt")
load_data()


def get_sif_skt(word):
    a = 5e4 # this is the smoothing value
    if word in wdict_skt:
        freq = int(wdict_skt[word])
    else:
        freq = 1
    return a / (a + freq)



def skt_get_vectors_fast(sktwords):
    sktwords = sktwords.split()
    sktvectors = []
    for word in sktwords:
        if word in skt_words:
            sktvectors.append(skt_dictionary[word])
        else:
            sktvectors.append(skt_dictionary["ca"])
#    print(len(sktvectors))
    return sktvectors


                         
