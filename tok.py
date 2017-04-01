from nltk import pos_tag, word_tokenize
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
from operator import itemgetter
from nltk.stem.porter import *

def remove_stop_words(line):

    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(line)
    stemmer = PorterStemmer()
    singles = [stemmer.stem(plural) for plural in word_tokens]

    filtered_sentence = []
    #singales?
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    new = ' '.join(filtered_sentence)
    tokenizer = RegexpTokenizer(r'\w+')
    res = tokenizer.tokenize(new)
    return res;


def cut_window (line ):
   "This prints a passed string into this function"
   split = line
   index = split.index(word);
   window = "";
   if index-2 >= 0:
    window = split[index - 2];

    if index-1 >= 0:
        window += " "+split[index - 1];

    window += " "+split[index];

    if index+1 < len(split):
        window += " "+split[index + 1];

   if index + 2 < len(split):
       window += " " + split[index + 2];

   return window

import os
cwd = os.getcwd()
path = nltk.data.find(cwd+'\\corpus_ex1.txt');
raw = open(path, 'rU').read();
raw = raw.replace('<s>','');
raw = raw.replace('</s>','');
lines = sent_tokenize(raw);
word = 'light';
seedA = 'reflect';
seedB = 'weight'
senseA = [];
senseB = [];
allOccurences = [];
for line in lines:
    split = line.split();
    for words in split:

      if word == words:

        try:
            noStopWords = remove_stop_words(line)
            window = cut_window(noStopWords);
        except ValueError:
                print ("ERROR ! ! ! ")
                print (line);
                print (noStopWords);
        allOccurences += window.split();
        if seedA in window:

                senseA += [window];

        elif seedB in window:

                senseB += [window];


print (senseA)
print (senseB)

arr = (Counter(allOccurences))
print(arr)
arr = list(arr.items());

arr.sort(key = itemgetter(1), reverse=True)
i = 0;
for key, value in arr:
    if (word in key) or (seedA in key) or  (seedB in key) or (key == 's'):
        continue;
    i = i + 1;
    print(key + " " + str(value))
    if i == 5:
        break;