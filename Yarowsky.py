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
    # singales?
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    new = ' '.join(filtered_sentence)
    tokenizer = RegexpTokenizer(r'\w+')
    res = tokenizer.tokenize(new)
    return res;


def cut_window(line):
    "This prints a passed string into this function"
    split = line
    index = split.index(word);
    window = "";
    if index - 2 >= 0:
        window = split[index - 2];

        if index - 1 >= 0:
            window += " " + split[index - 1];

        window += " " + split[index];

        if index + 1 < len(split):
            window += " " + split[index + 1];

    if index + 2 < len(split):
        window += " " + split[index + 2];

    return window


def runOnSeeds(seedA, seedB, seedC):
    from sentence import sentence
    senseA = []
    senseB = []
    senseC = []
    allOccurences = []
    for line in lines:
        if line.startswith("<text id="):
            header = line
            headerSplit = header.split("wikipedia:")
            header = headerSplit[1]
            headerSplit = header.split(">")
            header = headerSplit[0]
            header = header.replace("\"", "");
            print(header)
            continue
        split = line.split()
        for words in split:
            if word == words:

                try:
                    noStopWords = remove_stop_words(line)
                    window = cut_window(noStopWords)
                except ValueError:
                    print("ERROR ! ! ! ")
                    print(line)
                    print(noStopWords)
                allOccurences += window.split()
                new_sentence = None
                if seedA in window:
                    senseA += [window]
                    new_sentence = sentence(window, seedA)


                elif seedB in window:
                    senseB += [window]
                    new_sentence = sentence(window, seedB)

                elif seedC in window:
                    senseC += [window]
                    new_sentence = sentence(window, seedC  )

                if(new_sentence is not None):
                    if header not in my_dict:
                        my_dict[header] = new_sentence
                    else:
                        wordList = [my_dict[header]]
                        wordList.append(new_sentence)
                        my_dict[header] = wordList


    print("There are " + str(len(senseA)) + " sentences with the seed " + seedA)
    print("There are " + str(len(senseB)) + " sentences with the seed " + seedB)
    print("There are " + str(len(senseC)) + " sentences with the seed " + seedC)
    arr = (Counter(allOccurences))

    arr = list(arr.items())

    arr.sort(key=itemgetter(1), reverse=True)
    i = 0
    MaxSenseA = 0
    MaxSenseB = 0
    MaxSenseC = 0

    MaxWordSenseA = seedA
    MaxWordSenseB = seedB
    MaxWordSenseC = seedC
    for key, value in arr:
        if (word in key) or (seedA in key) or (seedC in key) or (seedB in key) or (key == 's') or (
                    key == 'two') or (
                    key == 'one') or (
                    key == 'also') or (key == 'may') or (key == 'would') or (key == 'first') or (key == 'often') or (
                    key == 'many'):
            continue

        sentences_A = []
        sentences_B = []
        sentences_C = []

        keyInSenseA = 0
        keyInSenseB = 0
        keyInSenseC = 0

        #  print("~~~~~~~sense A sentences:~~~~~~~~~~")
        for sentence in senseA:
            temp = sentence.split().count(key)
            if temp > 0:
                if sentence in sentences_A:
                    continue
                sentences_A += [sentence]
                #      print(sentence)
            keyInSenseA += temp

            #  print("~~~~~~~sense B sentences:~~~~~~~~~~")
        for sentence in senseB:
            temp = sentence.split().count(key)
            if temp > 0:
                if sentence in sentences_B:
                    continue
                sentences_B += [sentence]
                #       print(sentence)
            keyInSenseB += temp

        # print("~~~~~~~sense C sentences:~~~~~~~~~~")
        for sentence in senseC:
            temp = sentence.split().count(key)
            if temp > 0:
                if sentence in sentences_C:
                    continue
                sentences_C += [sentence]
                #     print(sentence)
            keyInSenseC += temp

        if keyInSenseB == 0 and keyInSenseA == 0 and keyInSenseC == 0:
            # print("--------------------------------------------------------------------------------")
            continue
            #      elif keyInSenseB == 0:
            # print("==============")
            #          print("Collocation_i Log(SenseA/SenseB) = +infinity")
            #      elif keyInSenseA == 0:
            # print("==============")
            #          print("Collocation_i Log(SenseA/SenseB) = -infinity")
            #    else:
        # print("==============")
        #        print("Collocation_i Log(SenseA/SenseB) = " + str(log10(keyInSenseA / keyInSenseB)))
        i = i + 1

        if keyInSenseA == max(keyInSenseA, keyInSenseB, keyInSenseC):
            dividor = max(1, keyInSenseB + keyInSenseC)
            grade = log10(keyInSenseA / dividor)
            if (grade > MaxSenseA):
                MaxSenseA = grade
                MaxWordSenseA = key

        elif keyInSenseB == max(keyInSenseA, keyInSenseB, keyInSenseC):
            dividor = max(1, keyInSenseA + keyInSenseC)
            grade = log10(keyInSenseB / dividor)
            if (grade > MaxSenseB):
                MaxSenseB = grade
                MaxWordSenseB = key

        elif keyInSenseC == max(keyInSenseA, keyInSenseB, keyInSenseC):
            dividor = max(1, keyInSenseA + keyInSenseB)
            grade = log10(keyInSenseC / dividor)
            if (grade > MaxSenseC):
                MaxSenseC = grade
                MaxWordSenseC = key

        print(key + " " + str(value))
        print("The word " + key + " with the seed " + seedA + " occurs: " + str(keyInSenseA))
        print("The word " + key + " with the seed " + seedB + " occurs: " + str(keyInSenseB))
        print("The word " + key + " with the seed " + seedC + " occurs: " + str(keyInSenseC))
        print("--------------------------------------------------------------------------------")
        if i == 15:
            return (MaxWordSenseA, MaxWordSenseB, MaxWordSenseC)


import os

cwd = os.getcwd()
path = nltk.data.find(cwd + '\\coprs\\corpus_ex1.txt');
# path = nltk.data.find(cwd+'\\temp.txt');
word = 'play'
seedA = 'game'
seedB = 'role'
seedC = 'music'
raw = open(path, 'rU', encoding="utf8").read();
raw = raw.replace('<s>', '');
raw = raw.replace('</s>', '');

raw = raw.lower();
raw = raw.replace(word + 's', word);
raw = raw.replace(word + 'er', word);
raw = raw.replace(word + 'ed', word);

raw = raw.replace(word + 'ing', word)

# raw = raw.replace(word+'-years',word+' years');
raw = raw.replace(seedA + 's', seedA);
# raw = raw.replace(seedA+'al',seedA);
raw = raw.replace(seedB + 's', seedB);
raw = raw.replace(seedB + 'al', seedB);
# raw = raw.replace('weighed',seedB);
lines = sent_tokenize(raw)
my_dict = dict()
while True:
    (newA, newB, newC) = runOnSeeds(seedA, seedB, seedC)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!new seeds:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(newA)
    print(newB)
    print(newC)
    if newC == seedC and newA == seedA and newB == seedB:
        break
    else:
        seedA = newA
        seedB = newB
        seedC = newC
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
