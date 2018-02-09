from settings import *
from general_functions import *
import copy
from classes import *
import collections

import re
# one_sentence = lambda x: not re.search(xorr + "|" + iff + "|" + idisj + "|" +
#                                            conditional + "|&", x)
# cond_r = chr(8835)
# consist = "\u2102"  # consistency
# top = chr(8868)
# bottom = chr(8869)
# neg = chr(172)
# idd = chr(8781)  # translation symbol
# iff = chr(8801)
# mini_c = chr(8658)
# mini_e = chr(8703)
# implies = chr(8866)
# conditional = chr(8594)
# nonseq = chr(8876)
# xorr = chr(8891)
# idisj = chr(8744)
# cj = chr(8896)
# aid = chr(8776)
# disj = chr(8855)
# equi = chr(8660)

def replace_w_greek(sentence):
    j = 947
    list1 = [x for x in sentence]
    erase_next_parent = False
    for i, letter in enumerate(list1):
        if i > 0 and list1[i - 1] == "(" and letter.islower():
            j += 1
            list1[i] = chr(j)
            list1[i - 1] = " "
            erase_next_parent = True
        elif erase_next_parent and letter == ")":
            list1[i] = " "
            erase_next_parent = False
        elif letter not in ["(", ")", "&", conditional, xorr, iff, idisj, "|"]:
            list1[i] = " "

    sent = "".join(list1)

    return sent


def find_sentences(sentence, definiendum="", embed = False):
    if sentence == None:
        raise Exception("\n missing word in dictionary \n")

    if one_sentence(sentence):
        if definiendum != "":
            # raise Exception("\n you cannot reduce this word: " + "\n" + definiendum + "\n")
            raise ErrorWithCode(f"\n you cannot reduce {definiendum} \n  in {sentence} \n")
        else:
            raise ErrorWithCode(f"\n you cannot reduce {definiendum} \n  in {sentence} \n")
            # raise Exception("\n you cannot reduce this word: " + "\n" + sentence + "\n")
    if sentence.count('(') != sentence.count(')'):
        print("( paren = " + str(sentence.count("(")))
        print(") paren = " + str(sentence.count(")")))

        raise Exception(" \nwrong number of parentheses in sentence: " + sentence + "\n ")

    if definiendum == 'BTP':
        bb = 8

    sentence = remove_extra_paren(sentence, embed)
    result = [None] * 9
    sentences = []
    greek_sent = replace_w_greek(sentence)
    greek_sentences = []
    greek_sentences.append(greek_sent)
    assert len(greek_sent) == len(sentence)
    mainc = []
    num_to_conn = {}
    sent_numbers = []
    add_sibling = False
    gen = 1
    gener = ['1']
    sentences.append(sentence)
    sent_numbers.append("1")
    idx_dict = {}
    # sent_to_num = {"1": sentence}
    size_index = [0]

    for idx, letter in enumerate(sentence):
        if letter in all_connectives:
            sent_num2 = ".".join(gener[:-1])

            num_to_conn.update({sent_num2: letter})

        if letter == "(":
            if add_sibling:
                del gener[-1]
                gen += 1
            else:
                gen = 1

            gener.append(str(gen))
            sent_num = ".".join(gener)
            idx_dict.update({sent_num:idx})
            add_sibling = False

        elif letter == ")":
            if add_sibling:
                del gener[-1]
                sent_num = ".".join(gener)
                list1 = sent_num.split(".")
                gen = int(list1[-1])
            num_periods = sent_num.count(".")
            begin = idx_dict.get(sent_num)
            add_sibling = True
            if sent_num == '1.2.3':
                bb = 8

            if len(sent_num) >= len(sent_numbers[-1]):
                sent_numbers.append(sent_num)
                sentences.append(sentence[begin: idx + 1])
                greek_sentences.append(greek_sent[begin: idx + 1])
                size_index.append(num_periods)
            else:
                b = get_sent_position(size_index, num_periods)
                sent_numbers.insert(b, sent_num)
                size_index.insert(b, num_periods)
                sentences.insert(b, sentence[begin: idx + 1])
                greek_sentences.insert(b, greek_sent[begin: idx + 1])


            # sent_to_num.update({sent_num: sentence[begin: idx + 1]})

    for sent_number in sent_numbers:
        if sent_number not in num_to_conn.keys():
            num_to_conn.update({sent_number: ""})
        mainc.append([sent_number, num_to_conn.get(sent_number)])


    result[0] = num_to_conn
    result[1] = split_numbers(sent_numbers)
    result[2] = sent_numbers
    result[3] = sentences
    result[4] = mainc
    result[6] = adjust_greek_sent(greek_sentences)
    result[5] = greek_sentences[0]

    if "," in greek_sent[0]: check_that_paren_in_right_order(result)

    # greek_english = {}
    # for sent, greek in zip(result[3], result[6]):
    #     greek_english.update({greek: sent})
    # # result[7] = greek_english
    # result[8] = sent_to_num

    return result


def get_sent_position(size_index, num_periods):
    j = 0
    while True:
        if size_index[j] > num_periods:
            return j
        j += 1
    raise Exception

#
# def find_sentences2(sentence, definiendum="", embed = False):
#
#     if sentence == None:
#         raise Exception("\n missing word in dictionary \n")
#
#     if one_sentence(sentence):
#         if definiendum != "":
#             # raise Exception("\n you cannot reduce this word: " + "\n" + definiendum + "\n")
#             raise ErrorWithCode(f"\n you cannot reduce {definiendum} \n  in {sentence} \n")
#         else:
#             raise ErrorWithCode(f"\n you cannot reduce {definiendum} \n  in {sentence} \n")
#             # raise Exception("\n you cannot reduce this word: " + "\n" + sentence + "\n")
#     if sentence.count('(') != sentence.count(')'):
#         print("( paren = " + str(sentence.count("(")))
#         print(") paren = " + str(sentence.count(")")))
#
#         raise Exception(" \nwrong number of parentheses in sentence: " + sentence + "\n ")
#
#     marker = False
#     total = -1
#     sentences = []
#     result = [None] * 9
#     sent_number = []
#
#     # sentence = remove_extra_paren(sentence, embed)
#     # output = find_sentences2(sentence, definiendum, embed)
#
#     # ogreek = output[7]
#
#
#     list1 = mainconn(sentence)
#     sentence = sentence.strip()
#     if sentence.startswith("(b LFT c)"):
#         bb = 8
#     greek_sent = replace_w_greek(sentence)
#     if sentence.find("~(") > -1:
#         sentence = sentence.replace("~(", "(!")
#     greek_sentences = []
#     greek_sentences.append(greek_sent)
#     assert len(greek_sent) == len(sentence)
#     main_connect = []
#     sent_number.append("1")
#     main_connect.append(["1", list1[0]])
#     father_number = "1"
#     v = 0
#     conn_dict = {}
#     sibling_number = 0
#     connectives = ["&", idisj, iff, conditional, nonseq, implies, xorr, "#"]
#     sentences.append(sentence)
#
#     j = 0
#     n = 0
#     for i in range(0, len(sentence)):
#         str1 = sentence[i:(i + 1)]
#         for o in connectives:
#             if str1 == o:
#                 j += 1
#
#     while n < j + 1:
#
#         l = len(sentence)
#         x = -1
#         while x < l - 1:
#             x += 1
#
#             if sentence[x:x + 1] == "(":
#
#                 if marker == False:
#                     z = x
#                     marker = True
#
#                 total += 1
#             elif sentence[x: x + 1] == ")":
#                 total -= 1
#                 if total == -1:
#                     marker = False
#                     temp_sent = sentence[z: x + 1]
#                     temp_greek = greek_sent[z: x + 1]
#
#                     if (len(sentence) - len(temp_sent)) > 2:
#                         if one_sentence(temp_sent): n += 1
#                         sibling_number += 1
#                         num3 = father_number + "." + str(sibling_number)
#                         main_co = mainconn(temp_sent)
#                         sentences.append(temp_sent)
#                         main_connect.append([num3, main_co[0]])
#                         conn_dict.update({num3: main_co[0]})
#                         sent_number.append(num3)
#                         greek_sentences.append(temp_greek)
#                     else:
#                         sentence = sentence[1:len(sentence) - 1]
#                         greek_sent = greek_sent[1:len(greek_sent) - 1]
#                         l = len(sentence)
#                         x = -1
#
#         total = -1
#         marker = False
#
#         if n < j + 1:
#             if len(sentences) > v:
#                 while v + 1 < len(sentences):
#                     v += 1
#                     father = sentences[v]
#                     greek_father = greek_sentences[v]
#                     father_number = sent_number[v]
#                     sibling_number = 0
#                     if not one_sentence(father):
#                         sentence = father
#                         greek_sent = greek_father
#                         break
#
#     result[0] = conn_dict
#     result[1] = split_numbers(sent_number)
#     result[2] = sent_number
#     result[3] = sentences
#     result[4] = main_connect
#     result[6] = adjust_greek_sent(greek_sentences)
#     result[5] = greek_sentences[0]

    # if "," in greek_sent[0]: check_that_paren_in_right_order(result)


    # print (definiendum)
    #
    # for j, sentence in enumerate(result[3]):
    #     sent_num = result[2][j]
    #     greek = result[6][j]
    #     mainc = result[4][j][1]
    #
    #     osent = output[8].get(sent_num)
    #     omainc = output[0].get(sent_num)
    #     o_index = output[2].index(sent_num)
    #     ogreek = output[6][o_index]
    #     osent_num = output[2][o_index]
    #
    #     assert greek == ogreek
    #     assert mainc == omainc
    #     assert osent == sentence
    #     assert osent_num == sent_num







    # for sent, num in zip(result[3], result[2]):
    #     osent = sent_to_num.get(num)
    #     if osent != sent and once:
    #         print (definiendum)
    #         once = False


    # return result


def split_numbers(sent_number):
    list1 = []
    for num in sent_number:
        list2 = num.split(".")
        list1.append(list2)
    return list1


def check_that_paren_in_right_order(output):
    for i, sent in enumerate(output[3]):
        if "," in sent:
            num_periods = output[2][i].count(".")
            str1 = sent[output[4][i][2]:output[4][i][2] + 7]
            num_pipe = str1.count(",")
            if num_pipe != 0 and num_pipe - 1 != num_periods:
                print("\n parentheses are in wrong location in " + output[3][0] + "\n")
                assert num_pipe - 1 == num_periods
            output[3][i] = output[3][i].replace(",", "")


def adjust_greek_sent(greek_sentences):
    connectives = ["&", idisj, iff, conditional, nonseq, implies, xorr, "#"]
    for i, sent in enumerate(greek_sentences):
        sent = sent.replace(" ", "")
        for conn in connectives:
            sent = sent.replace(conn, " " + conn + " ")
        greek_sentences[i] = sent

    return greek_sentences


def get_sent_from_period(sent, per_pos):
    end = sent.find(" ", per_pos)
    if end == -1:
        end = len(sent) - 1
    while True:
        per_pos -= 1
        if sent[per_pos] in [" ", "("]:
            beg = per_pos + 1
            break

    to_be_replaced = sent[beg: end]
    letters = to_be_replaced.split(".")
    new_sentences = []
    for letter in letters:
        new_sent = copy.copy(sent)
        new_sent = new_sent.replace(to_be_replaced, letter)
        new_sentences.append(new_sent)

    return new_sentences


def append_def_info(def_info, greatest_num, new_greek, new_sentences,
                    greek_letter, parent, fam_num):
    k = 0

    for sentence in new_sentences:
        fam_num2 = copy.deepcopy(fam_num)
        greek_letter += 1
        k += 1
        new_num = str(greatest_num + k)
        fam_num2.append(new_num)
        def_info[1].append(fam_num2)
        def_info[3].append(sentence)
        def_info[2].append(parent + "." + new_num)
        def_info[4].append([parent + "." + new_num, ""])
        new_greek.append(chr(greek_letter))
        def_info[6].append(chr(greek_letter))

    return greek_letter


def adjust_def_info(def_info, i, new_sentences, already_conjunctive, greek_letter):
    greek_letter += 1
    new_greek = []
    sent_num = def_info[2][i]
    size = sent_num.count(".")
    parent = ".".join(def_info[1][i][:-1])
    old_greek = def_info[6][i]
    sibling_numbers = []
    if already_conjunctive:
        del def_info[1][i][-1]
        new_greek = [chr(greek_letter)]
        def_info[3][i] = new_sentences[0]
        def_info[6][i] = chr(greek_letter)
        del new_sentences[0]

    if already_conjunctive:
        for j, num in enumerate(def_info[2]):
            if num.startswith(parent + ".") and num.count(".") == size and j != i:
                sibling_numbers.append(int(def_info[1][j][-1]))
        greatest_num = max(sibling_numbers)
    else:
        greatest_num = 0
        parent = sent_num

    greek_letter = append_def_info(def_info, greatest_num, new_greek,
                                   new_sentences, greek_letter, parent, def_info[1][i])

    new_greek = " & ".join(new_greek)
    if not already_conjunctive:
        new_greek = "(" + new_greek + ")"

    def_info[5] = def_info[5].replace(old_greek, new_greek)
    for n, lst in enumerate(def_info[6]):
        lst = lst.replace(old_greek, new_greek)
        def_info[6][n] = lst

    return def_info, greek_letter


def period_elimination(def_info2, definition):
    if "." not in definition:
        return def_info2, definition
    hypo_conn = [iff, idisj, xorr, conditional]
    i = -1
    greek_letter = 999
    for def_info in def_info2:
        while i < len(def_info[3]) - 1:
            i += 1
            sent = def_info[3][i]
            if "." in sent and one_sentence(sent):
                # if the sentence is the sole sentence on one side of a hypothetical
                # then we have to add additional parentheses
                paren_num = ".".join(def_info[1][i][:-1])
                g = findposinmd(paren_num, def_info[4], 0)
                paren_conn = def_info[4][g][1]
                assert paren_conn != ""
                per_pos = sent.find(".")
                new_sentences = get_sent_from_period(sent, per_pos)
                new_conjunct = " & ".join(new_sentences)
                already_conjunctive = True
                if paren_conn in hypo_conn:
                    new_conjunct = "(" + new_conjunct + ')'
                    already_conjunctive = False
                    def_info[4][i][1] = "&"
                    def_info[3][i] = new_conjunct

                definition = definition.replace(sent, new_conjunct)
                for j in range(len(def_info[3])):
                    def_info[3][j] = def_info[3][j].replace(sent, new_conjunct)
                def_info, greek_letter = adjust_def_info(def_info, i, new_sentences,
                                                         already_conjunctive, greek_letter)

    return def_info2, definition
