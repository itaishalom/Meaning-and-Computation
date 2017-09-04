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


def one_sense_per_discourse(this_seed_a, this_seed_b, this_seed_c, my_dict):
    from sentence import sentence
    is_changed = False
    for entry in my_dict:
        seed_counter_a = 0
        seed_counter_b = 0
        seed_counter_c = 0
        toCheck = my_dict[entry]
        if type(toCheck) is sentence:
            if toCheck.get_label() == this_seed_a:
                answer = original_seedA
            if toCheck.get_label() == this_seed_b:
                answer = original_seedB
            if toCheck.get_label() == this_seed_c:
                answer = original_seedC
            if entry not in wiki_entries_senses:

                wiki_entries_senses[entry] = answer
                is_changed = True
            else:
                tempSenses = wiki_entries_senses[entry];
                splited = tempSenses.split(" -> ")
                lastSense = splited[len(splited)-1]
                if lastSense != answer:
                    print(entry + ": " + wiki_entries_senses[entry] + " -> " + answer)
                    wiki_entries_senses[entry] += " -> " + answer
                    is_changed = True
        else:
            for all_play_sententces in toCheck:
                if all_play_sententces.get_label() == this_seed_a:
                    seed_counter_a = seed_counter_a + 1
                if all_play_sententces.get_label() == this_seed_b:
                    seed_counter_b = seed_counter_b + 1
                if all_play_sententces.get_label() == this_seed_c:
                    seed_counter_c = seed_counter_c + 1
            sum_of_all = seed_counter_a + seed_counter_b + seed_counter_c
            answer = ""
            if seed_counter_a / sum_of_all > accepted_percentage:
                answer = original_seedA
            if seed_counter_b / sum_of_all > accepted_percentage:
                answer = original_seedB
            if seed_counter_c / sum_of_all > accepted_percentage:
                answer = original_seedC
            if answer == "": #Undecided
                continue
            if entry not in wiki_entries_senses:
                wiki_entries_senses[entry] = answer
                is_changed = True
            else:
                tempSenses = wiki_entries_senses[entry];
                splited = tempSenses.split(" -> ")
                lastSense = splited[len(splited)-1]
                if lastSense != answer:
                    print(entry + ": " + wiki_entries_senses[entry] + " -> " + answer)
                    wiki_entries_senses[entry] += " -> " + answer
                    is_changed = True
    return is_changed


def runOnSeeds(seedA, seedB, seedC):
    my_dict = dict()
    from sentence import sentence
    senseA = []
    senseB = []
    senseC = []
    allOccurences = []
    for line in lines:
        if "<text id=" in line:
            header = line
            headerSplit = header.split("wikipedia:")
            header = headerSplit[1]
            headerSplit = header.split(">")
            header = headerSplit[0]
            header = header.replace("\"", "");
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
                    new_sentence = sentence(window, seedC)

                if new_sentence is not None:
                    if header not in my_dict:
                        my_dict[header] = new_sentence
                    else:
                        wordList = my_dict[header]
                        if type(wordList) is sentence:
                            listOfSents = [wordList, new_sentence]
                            my_dict[header] = listOfSents
                        else:
                            wordList.append(new_sentence)
                            my_dict[header] = wordList

    should_continue = one_sense_per_discourse(seedA, seedB, seedC, my_dict)
    if not should_continue:
        return seedA, seedB, seedC
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
        if (word in key) or (key in all_seeds_a) or (key in all_seeds_b) or (key in all_seeds_c) or (key == 's') or (key == 'two')\
                or (key == 'one') or ( key == 'also') or (key == 'may') or (key == 'would') or (key == 'first')\
                or (key == 'often') or ( key == 'many')or ( key == 'new'):
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


        if keyInSenseA == max(keyInSenseA, keyInSenseB, keyInSenseC):
            if keyInSenseA == keyInSenseB or keyInSenseC == keyInSenseA:
                continue
            dividor = max(0.1, keyInSenseB + keyInSenseC)
            grade = log10(keyInSenseA / dividor)
            if grade > MaxSenseA and key not in all_seeds_a:
                MaxSenseA = grade
                MaxWordSenseA = key

        if keyInSenseB == max(keyInSenseA, keyInSenseB, keyInSenseC):
            if keyInSenseA == keyInSenseB or keyInSenseC == keyInSenseB:
                continue
            dividor = max(0.1, keyInSenseA + keyInSenseC)
            grade = log10(keyInSenseB / dividor)
            if grade > MaxSenseB and key not in all_seeds_b:
                MaxSenseB = grade
                MaxWordSenseB = key

        if keyInSenseC == max(keyInSenseA, keyInSenseB, keyInSenseC):
            if keyInSenseC == keyInSenseB or keyInSenseC == keyInSenseA:
                continue
            dividor = max(0.1, keyInSenseA + keyInSenseB)
            grade = log10(keyInSenseC / dividor)
            if grade > MaxSenseC and key not in all_seeds_c:
                MaxSenseC = grade
                MaxWordSenseC = key

        i = i + 1
     #   print(key + " " + str(value))
     #   print("The word " + key + " with the seed " + seedA + " occurs: " + str(keyInSenseA))
     #   print("The word " + key + " with the seed " + seedB + " occurs: " + str(keyInSenseB))
     #   print("The word " + key + " with the seed " + seedC + " occurs: " + str(keyInSenseC))
     #   print("--------------------------------------------------------------------------------")
        if i == 25:
            return (MaxWordSenseA, MaxWordSenseB, MaxWordSenseC)


import os

cwd = os.getcwd()
path = nltk.data.find(cwd + '\\coprs\\corpus_ex2_3.txt');
# path = nltk.data.find(cwd+'\\temp.txt');
word = 'play'
original_seedA = 'game'
original_seedB = 'role'
original_seedC = 'instrument'
raw = open(path, 'rU', encoding="utf8").read();
raw = raw.replace('<s>', '');
raw = raw.replace('</s>', '');

raw = raw.lower();
raw = raw.replace(word + 's', word);
raw = raw.replace(word + 'er', word);
raw = raw.replace(word + 'ed', word);

raw = raw.replace(word + 'ing', word)

# raw = raw.replace(word+'-years',word+' years');
raw = raw.replace(original_seedA + 's', original_seedA);
# raw = raw.replace(seedA+'al',seedA);
raw = raw.replace(original_seedB + 's', original_seedB);
raw = raw.replace(original_seedC + 's', original_seedC);
raw = raw.replace(original_seedC + 'al', original_seedB);
# raw = raw.replace('weighed',seedB);
lines = sent_tokenize(raw)

allPerc = [0.5,0.6,0.7,0.8]

for per in allPerc:
    wiki_entries_senses = dict()
    accepted_percentage = per

    seedA = original_seedA
    seedB = original_seedB
    seedC = original_seedC

    all_seeds_a = [seedA]
    all_seeds_b = [seedB]
    all_seeds_c = [seedC]
    file_name = open(cwd + '\\projectResultFor' + str(accepted_percentage) + '.txt', 'w');
    file_name.write("Starting seeds: \n")
    file_name.write(seedA+"\n")
    file_name.write(seedB+"\n")
    file_name.write(seedC+"\n")
    for x in range(0, 3):
        (newA, newB, newC) = runOnSeeds(seedA, seedB, seedC)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!new seeds:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(newA)
        print(newB)
        print(newC)
        if newC == seedC and newA == seedA and newB == seedB:
            for line in wiki_entries_senses:
                file_name.write(line+": "+wiki_entries_senses[line]+"\n")
            file_name.close()
            break
        else:
            all_seeds_a.append(newA)
            all_seeds_b.append(newB)
            all_seeds_c.append(newC)
            file_name.write("new seeds: \n")
            seedA = newA
            seedB = newB
            seedC = newC
            file_name.write(seedA+"\n")
            file_name.write(seedB+"\n")
            file_name.write(seedC+"\n")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    for line in wiki_entries_senses:
        file_name.write(line+": "+wiki_entries_senses[line] + "\n")
    file_name.close()
