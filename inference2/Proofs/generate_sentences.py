

import pickle
from random import *

try:
    from general_functions import get_key
    from main_loop import get_result
    from settings import *
    from classes import get_words
except:
    from .general_functions import get_key
    from .main_loop import get_result
    from .settings import *
    from .classes import get_words


# from general_functions import get_key
# from main_loop import get_result
# from settings import *
# from classes import get_words





def test_sentences(arg1):
    if arg1 == 1:
        pkl_file = open('temp_list.pkl', 'rb')
        list1 = pickle.load(pkl_file)
        pkl_file.close()

        order = [x for x in range(9)]
        output = get_result(list1, "", "31", order, 0)
        for list2 in output[:9]:
            print (list2[1][1])
            print (list2[len(list2) - 1][1])
            print ("")

    else:
        get_sentences()




def get_sentences():
    global concepts, two_relations, h_relations, dictionary

    pkl_file = open("" + 'z_dict_words.pkl', 'rb')
    dictionary = pickle.load(pkl_file)
    pkl_file.close()


    cat_words = get_words(dictionary)

    concepts = [x[0] for x in dictionary.popular if x[2] == 'n' and x[0][0] != "H"]
    two_relations = [x[0] for x in dictionary.popular if x[2] == 'r' and x[3] == 2]
    h_relations2 = [x[0] for x in dictionary.popular if x[2] == 'n' and x[3] == 2 and x[0][0] == "H"]
    h_relations = []
    for word in h_relations2:
        word = word[1:]
        h_relations.append("have a" + word)

    list1 = form1()

    list2 = open('temp_list.pkl', 'wb')
    pickle.dump(list1, list2)
    list2.close()







def form1():



    syno = []
    list1 = []

    for word in dictionary.popular:
        if word[0] in dictionary.synonyms.values() or \
                word[1] in dictionary.synonyms.values():
            syn = get_key(dictionary.synonyms, word[0])
            concepts.append(syn)
        elif word[1] in dictionary.synonyms.values():
            syn = get_key(dictionary.synonyms, word[0])
            concepts.append(syn)



    for i in range(10):
        lenc = randint(0, len(concepts)-1)
        lend = randint(0, len(concepts)-1)
        lenr = randint(0, len(two_relations)-1)
        concept1 = concepts[lenc]
        concept2 = concepts[lend]
        relation1 = two_relations[lenr]
        str1 = " ".join(["it is consistent that some", concept1, relation1, "the", concept2])
        list1.append([str1])

    return list1






