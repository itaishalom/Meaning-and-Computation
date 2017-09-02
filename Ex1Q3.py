from nltk import pos_tag, word_tokenize
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords

from nltk.stem.porter import *

first_arr = ["club began play home games","park home play four games","cardinals started play home games",
             "september 1893 play home games","home games play stadio olimpico"];

second_arr = ["dancing queen play guitar keyboards","last song play acoustic guitar","s guitar play often characterized",
              "acoustic guitar play either unplugged","guitar style play"];


def remove_stop_words(input_line):
    if word not in input_line:
        return
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(input_line)
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

    newLine = "";
    for word_res in res:
        newLine += word_res+" ";

    for fromQ1Sentence in first_arr:
        if fromQ1Sentence in newLine:
            print("========")
            temp = line.split()
            tempNewLine = "";
            for word_temp in temp:
                tempNewLine += word_temp + " ";
            print(tempNewLine)

    for fromQ1Sentence in second_arr:
        if fromQ1Sentence in newLine:
            print("========")
            temp = line.split()
            tempNewLine = "";
            for word_temp in temp:
                tempNewLine += word_temp + " ";
            print(tempNewLine)

    return res;



import os
cwd = os.getcwd()
path = nltk.data.find(cwd+'\\corpus_ex1.txt');
#path = nltk.data.find(cwd+'\\temp.txt');
word = 'play';
seedA = 'home';
seedB = 'guitar'
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
    noStopWords = remove_stop_words(line)
