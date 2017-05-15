import gensim
import re
import nltk
import os
from scipy.stats import spearmanr

def prepare_file(filename):
    f = tuple(open(filename, 'r',encoding="utf8"))
   # f = open(filename, 'rU').read();
    sentences = []
    cur_sent = []
    for line in f:
        line = line.strip()
        if line == '</s>':
            sentences.append(cur_sent)
            cur_sent = []
        elif line == '<s>' or line.startswith('<text'):
            continue
        else:
            cur_sent.append(line)
    return sentences;


def create_file_and_spearman(sentences, window, size,simlex):
    lines = tuple(open(simlex, 'r'))
    file_name = open(cwd + '\\size' + str(size) + '_window' + str(window) + '.txt', 'w');
    word_to_vec = gensim.models.Word2Vec(sentences,min_count=5,window=window,size=size);
    list_pos__a = [];
    list_pos_n = [];
    list_pos__v = [];
    list_pos_all = [];

    list_pos__a_simlex = [];
    list_pos__n_simlex = [];
    list_pos__v_simlex = [];
    list_pos_all_simlex = [];

    for line in lines:
        list_words = re.split(r'\t+', line);
        word1 = list_words[0];
        word2 = list_words[1];
        POS = list_words[2];
        simlex_val = list_words[3];
        try:
            val = word_to_vec.similarity(word1,word2);
        except:
            print("error in words " + word1 + " " + word2);
            val = 0;
        finally:
            file_name.write(word1 + " " + word2 + " " + POS + " " + str(val) + '\n');
            list_pos_all.append(val);
            list_pos_all_simlex.append(simlex_val);
            if POS == 'A':
                list_pos__a.append(val);
                list_pos__a_simlex.append(simlex_val);
            if POS == 'N':
                list_pos_n.append(val);
                list_pos__n_simlex.append(simlex_val);
            if POS == 'V':
                list_pos__v.append(val);
                list_pos__v_simlex.append(simlex_val);
        continue;
    file_name.close();
    print("Spearman for window " + str(window) + " and size " + str(size) + " A: " + str(spearmanr(list_pos__a,list_pos__a_simlex)))
    print("Spearman for window " + str(window) + " and size " + str(size) + " N: " + str(spearmanr(list_pos_n, list_pos__n_simlex)))
    print("Spearman for window " + str(window) + " and size " + str(size) + " V: " + str(spearmanr(list_pos__v, list_pos__v_simlex)))
    print("Spearman for window " + str(window) + " and size " + str(size) + " ALL: " + str(spearmanr(list_pos_all, list_pos_all_simlex)))

cwd = os.getcwd()
path_corp = nltk.data.find(cwd+'\\corpus_ex2_3.txt');
path_simlex = nltk.data.find(cwd+'\\SimLex-999_2.txt');
sentences = prepare_file(path_corp)
create_file_and_spearman(sentences,10,100,path_simlex);
print('==================================================')
create_file_and_spearman(sentences,10,1000,path_simlex);
print('==================================================')
create_file_and_spearman(sentences,2,1000,path_simlex);
print('==================================================')
create_file_and_spearman(sentences,2,100,path_simlex);
print('==================================================')