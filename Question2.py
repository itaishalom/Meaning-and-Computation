from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet
from math import log10


def lin(anc,c1,c2):
    print ((2*log10(anc['val']))/(log10(c1['val'])+ log10(c2['val'])))
    print(anc['name']+" / " +c1['name'] +"+"+c2['name']);

arr = [51912,229,425,28696,16088,695,445,307,12323,233];
arr_names = ["organism","prokaryote","eukaryote","animal","plant","fungus","pet","scavenger","adult","crop"];
num_of_words_in_corpus = 9267200;
i = 0;
#for num in arr:
     #arr[i]=((num/num_of_words_in_corpus));
     #i= i+1;
organism = {'val':arr[0]/num_of_words_in_corpus,'name':"organism"};
prokaryote = {'val':arr[1]/num_of_words_in_corpus,'name':"prokaryote"};
eukaryote = {'val':arr[2]/num_of_words_in_corpus,'name':"eukaryote"};
animal = {'val':arr[3]/num_of_words_in_corpus,'name':"animal"};
plant = {'val':arr[4]/num_of_words_in_corpus,'name':"plant"};
fungus = {'val':arr[5]/num_of_words_in_corpus,'name':"fungus"};
pet = {'val':arr[6]/num_of_words_in_corpus,'name':"pet"};
scavenger = {'val':arr[7]/num_of_words_in_corpus,'name':"scavenger"};
adult = {'val':arr[8]/num_of_words_in_corpus,'name':"adult"};
crop = {'val':arr[9]/num_of_words_in_corpus,'name':"crop"};

lin(animal,pet,scavenger);
lin(animal,pet,adult);
lin(animal,pet,animal);
lin(organism,pet,crop);
lin(organism,pet,prokaryote);
lin(organism,pet,eukaryote);
lin(organism,pet,plant);
lin(organism,pet,fungus);

lin(animal,scavenger,adult);
lin(animal,scavenger,animal);
lin(organism,scavenger,crop);
lin(organism,scavenger,prokaryote);
lin(organism,scavenger,eukaryote);
lin(organism,scavenger,plant);
lin(organism,scavenger,fungus);

lin(animal,adult,animal);
lin(organism,adult,crop);
lin(organism,adult,prokaryote);
lin(organism,adult,eukaryote);
lin(organism,adult,plant);
lin(organism,adult,fungus);

lin(plant,crop,plant);
lin(organism,crop,prokaryote);
lin(organism,crop,eukaryote);
lin(organism,crop,animal);
lin(organism,crop,fungus);

lin(organism,prokaryote,organism);
lin(organism,prokaryote,eukaryote);
lin(organism,prokaryote,animal);
lin(organism,prokaryote,plant);
lin(organism,prokaryote,fungus);


lin(organism,eukaryote,organism);
lin(organism,eukaryote,animal);
lin(organism,eukaryote,plant);
lin(organism,eukaryote,fungus);

lin(organism,animal,organism);
lin(organism,animal,plant);
lin(organism,animal,fungus);

lin(organism,plant,organism);
lin(organism,plant,fungus);

lin(organism,fungus,organism);