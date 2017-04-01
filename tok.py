from nltk import pos_tag, word_tokenize
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

path = nltk.data.find('C:\\Dropbox\\My-Dir\\University\\Sixth\\B\\temp.txt');
raw = open(path, 'rU').read();
raw = raw.replace('<s>','');
raw = raw.replace('</s>','');
lines = sent_tokenize(raw);
word = 'light';
seedA = 'reflect';
seedB = 'weight'
for line in lines:
    if word in line:
        split = (line.split( ));
        index = split.index(word);


def cutAWindow (line ):
   "This prints a passed string into this function"
   split = (line.split());
   index = split.index(word);
   return