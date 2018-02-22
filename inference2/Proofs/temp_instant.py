
from general_functions import *
from settings import *
from openpyxl import load_workbook
from analyze_sentence import find_sentences

greek = [chr(945 + t) for t in range(40)]


def no_space_around_sym(sent, sym):
    if sym + " " in sent:
        sent = sent.replace(sym + " ", sym)
    if " " + sym in sent:
        sent = sent.replace(" " + sym, sym)
    if sym in sent:
        sent = sent.replace(sym, " " + sym + " ")
    return sent



def adjust_definition(word, definition, dictionary):
    # pkl_file = open('z_dict_words.pkl', 'rb')
    # dictionary = pickle.load(pkl_file)
    # pkl_file.close()

    pos = dictionary[0].get(word)
    sent = definition
    if sent.count("(") == 1:
        sent = sent.replace("= ", "=")
        sent = sent.replace(" =", "=")
        sent = sent.replace("=", " = ")
    else:
        variables6 = copy.copy(variables9)
        def_info = find_sentences(sent)
        def_info[5] = no_space_around_sym(def_info[5], mini_e)

        for i in range(len(def_info[3])):
            sent = def_info[3][i]
            if def_info[4][i][1] == "":
                try:
                    if word in sent:
                        if (pos[0] == "r" and "=" in sent) or (pos[0] != 'r' and "=" not in sent):
                            sent = sent.replace(word, "%")
                            sent = "*" + sent
                except:

                    pass

                if "=" in sent:
                    sent = sent.replace("= ", "=")
                    sent = sent.replace(" =", "=")
                else:
                    sent = sent.replace(" ", "")
                    # sent = no_space_around_sym(sent, mini_e)
                    sent_list = list(sent)
                    j = 0
                    while j < len(sent_list) - 2:
                        j += 1
                        if sent_list[j + 1] not in [")", "."]:
                            if sent_list[j] not in ["(", ")", neg, "."]:
                                if sent_list[j].isupper():
                                    if not sent_list[j + 1].isupper():
                                        sent_list.insert(j + 1, " ")
                                        j += 1
                                else:
                                    sent_list.insert(j + 1, " ")
                                    j += 1
                    sent = "".join(sent_list)
                def_info[5] = def_info[5].replace(def_info[6][i], sent)
        def_info[5] = replace_letters(def_info[5], {}, "4", variables6)
        def_info[5] = def_info[5].replace("%", word + " ")
        def_info[5] = def_info[5].replace(" )", ")")
        def_info[5] = def_info[5].replace("  ", " ")
        sent = def_info[5]

    return sent

def new_func(b):
    b += 1
    return b