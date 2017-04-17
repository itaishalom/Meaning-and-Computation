from nltk import pos_tag, word_tokenize
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
from operator import itemgetter
from nltk.stem.porter import *
from math import log10


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
#path = nltk.data.find(cwd+'\\temp.txt');
word = 'play';
seedA = 'recreation';
seedB = 'sound'
raw = open(path, 'rU').read();
raw = raw.replace('<s>','');
raw = raw.replace('</s>','');

raw = raw.lower();
raw = raw.replace(word+'s',word);
raw = raw.replace(word+'ed',word);
raw = raw.replace(word+'ing',word);

#raw = raw.replace(word+'-years',word+' years');
raw = raw.replace(seedA+'s',seedA);
#raw = raw.replace(seedA+'al',seedA);
raw = raw.replace(seedB+'s',seedB);
raw = raw.replace(seedB+'al',seedB);
#raw = raw.replace('weighed',seedB);
lines = sent_tokenize(raw);

word_counter = 0;

senseA = [];
senseB = [];
allOccurences = [];
for line in lines:
    split = line.split();
    for words in split:
      word_counter = word_counter+1;
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


print ("There are " + str(len(senseA)) + " sentences with the seed " + seedA);
print ("There are " + str(len(senseB)) + " sentences with the seed " + seedB);

arr = (Counter(allOccurences))

arr = list(arr.items());

arr.sort(key=itemgetter(1), reverse=True)
i = 0;
for key, value in arr:
    if (word in key) or (seedA in key) or (seedB in key) or (key == 's') or (key == 'two') or (key == 'one')or (key == 'also') or (key == 'may')or (key == 'would')  :
        continue;
    i = i + 1;



    keyInSenseA = 0;
    keyInSenseB = 0;

    for sentence in senseA:
        temp = sentence.split().count(key)
        #if temp>0:
           # print(sentence)
        keyInSenseA += temp

    for sentence in senseB:
        keyInSenseB += sentence.split().count(key)


    print(key + " " + str(value))
    print("The word " + key + " with the seed " + seedA + " occurs: " + str(keyInSenseA));
    print("The word " + key + " with the seed " + seedB + " occurs: " + str(keyInSenseB));

    if i == 15:
        break;
print("number of words: "+str(word_counter))
