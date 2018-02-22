

from general_functions_old import *
from collections import defaultdict
from uninstantiable_definitions_old import define_irregular_terms
from search_for_instantiation_old import try_instantiation
import sys, operator
from put_words_in_slots_old import categorize_words, place_in_decision_procedure


prop_var = [chr(122 - t) for t in range(26)]
prop_var2 = [chr(122 - t) + "\u2081" for t in range(26)]
prop_var3 = [chr(122 - t) + "\u2082" for t in range(26)]
prop_var5 = [chr(122 - t) + "\u2083" for t in range(26)]
prop_var6 = [chr(122 - t) + "\u2084" for t in range(26)]
prop_var7 = [chr(122 - t) + "\u2085" for t in range(26)]
prop_var8 = [chr(122 - t) + "\u2086" for t in range(26)]
prop_var9 = [chr(122 - t) + "\u2087" for t in range(26)]
prop_var2 = prop_var9 + prop_var8 + prop_var7 + prop_var6 + prop_var5 + prop_var3 + prop_var2 + prop_var

variables = [chr(122 - t) for t in range(25)]
variables.remove("i")
variables.remove("l")
variables3 = [chr(122 - t) + l1 for t in range(26)]
variables3.remove("l" + l1)
variables4 = [chr(122 - t) + l2 for t in range(26)]
variables4.remove("l" + l2)
variables5 = [chr(122 - t) + l3 for t in range(26)]
variables5.remove("l" + l3)
variables2 = variables + variables3 + variables4 + variables5


inferences = []
get_words_used = 0
words_used = []


######### group: eliminate uninstantiable words part one

def get_super(str1):
    if str1 == "a":
        return "\u1d43"
    elif str1 == "b":
        return "\u1d47"
    elif str1 == "c":
        return "\u1d9c"
    elif str1 == "d":
        return "\u1d48"
    elif str1 == "e":
        return "\u1d49"
    elif str1 == "f":
        return "\u1da0"
    elif str1 == "g":
        return "\u1d4d"
    elif str1 == "h":
        return "\u02b0"
    elif str1 == "i":
        return "\u2071"
    elif str1 == "j":
        return "\u02B2"
    elif str1 == "k":
        return "\u1d4f"
    elif str1 == "l":
        return "\u02E1"
    elif str1 == "m":
        return "\u1d50"
    elif str1 == "n":
        return "\u207f"
    elif str1 == "o":
        return "\u1d52"
    elif str1 == "p":
        return "\u1d56"
    elif str1 == "r":
        return "\u02b3"
    elif str1 == "s":
        return "\u02e2"
    elif str1 == "t":
        return "\u1d57"
    elif str1 == "u":
        return "\u1d58"
    elif str1 == "v":
        return "\u1d5b"
    elif str1 == "w":
        return "\u02b7"
    elif str1 == "y":
        return "\u02b8"


def tran_str(str1, has_sentence_connectives=False):
    if str1 == "":
        return str1
    if "|" in str1:
        for i in range(len(str1)):
            if str1[i:i + 1] == "|":
                str3 = str1[i + 1:i + 2]
                str4 = get_super(str3)
                str1 = str1[:i] + str4 + str1[i + 2:]

    if has_sentence_connectives:

        if "t^" in str1:
            str1 = str1.replace("t^", conditional)
        if "nt+" in str1:
            str1 = str1.replace("nt+", neg)
        if "x^" in str1:
            str1 = str1.replace("x^", iff)
        if "b^" in str1:
            str1 = str1.replace("b^", mini_e)
        if "c^" in str1:
            str1 = str1.replace("c^", mini_c)
        if "ed^" in str1:
            str1 = str1.replace("ed^", xorr)
        if "v+" in str1:
            str1 = str1.replace("v+", idisj)

    return str1


def obtain_truth_value():
    sent = output[1][0]
    sent = sent.replace("!", "|")
    sentence = tran_str(sent)
    add_to_tsent(output[0], "CLAIM " + str(sent[0]) + ": " + sentence)
    add_to_tsent(output[0], "ABBREVIATIONS")

    if len(sentence) < 22:

        raise Exception(
            "Each sentence must begin with either 'it is|a consistent that' or 'it is|a contradictory that")

    else:
        if sentence[7:12] == 'consi':
            return True, sentence[len("It isa consistent that "):]
        elif sentence[7:12] == 'contr':
            return False, sentence[len("It isa contradictory that "):]
        else:
            raise Exception(
                "Each sentence must begin with either 'it is|a consistent that' or 'it is|a contradictory that")


def eliminate_logical_connectives():
    list1 = output[1][0].split(" and ")
    return list1


def step_one(sent):
    global definite_assignments, inferences
    global words_used, prop_var2
    global consistent, output

    artificial = False
    consistent = True
    inferences = []
    output = [[], [], [], [], [], {}, {}, [], {}, {}, [], [], [], {}, [], {}]
    words_used = []
    output[14] = copy.deepcopy(variables2)
    output[7] = copy.deepcopy(prop_var2)
    output[8] = defaultdict(lambda: output[7].pop(), {})

    if "(" in sent[0]:

        artificial = True
        truth_value = artificial_sentence(sent)

    else:

        output[1].append(sent[0])

        truth_value, output[1][0] = obtain_truth_value()

        output[1] = eliminate_logical_connectives()

        divide_sent()

        eliminate_redundant_words()

        replace_determinative_nouns()

        categorize_words2()

        replace_synonyms()

        replace_special_synonyms()

        word_sub()

        output[1] = remove_duplicates(output[1], 0)

        output, consistent = define_irregular_terms(output, inferences, words_used)

        output[1] = remove_duplicates(output[1], 0)

        shorten_sent()

    if consistent:

        output, consistent = try_instantiation(output, artificial)




    return truth_value == consistent, output[0]


def divide_sent():
    for i, sent in enumerate(output[1]):
        sent = sent.lower()
        sent = sent.strip()
        if "'s" not in sent: sent = sent.replace("'", "")
        if "," in sent: sent = sent.replace(",", " ,")
        sentp = name_sent(sent, output[8])
        output[9][sentp] = sent
        words_in_sent = sent.split()
        output[1][i] = [None] * 80
        output[1][i][0] = sent
        output[1][i][46] = sent
        output[1][i][2] = sentp
        output[1][i][3] = ""
        for j in range(len(words_in_sent)): output[1][i][j + 4] = words_in_sent[j]
        add_to_tsent(output[0], sent, sentp, "", "")
        output[1][i][44] = get_sn(output[0])

    return


def eliminate_redundant_words():
    # modify this if we start dealing with sentences longer than 41 words
    bool1 = False
    for sent in output[1]:
        ant_sent = sent[0]
        ant_sentp = sent[2]
        rule = "RD"
        anc1 = sent[44]
        j = 3
        while j < 55:
            j += 1
            if sent[j] == None:
                break
            pos = dictionary[0].get(sent[j])
            if pos != None and pos[0] == 't':
                if get_words_used == 1:
                    if not isvariable(sent[j]) and sent[j] not in words_used:
                        words_used.append(sent[j])
                bool1 = True
                if rule == 'RD':
                    rule += " " + sent[j]
                else:
                    rule += ", " + sent[j]
                del sent[j]
                j -= 1
                # this means that sentences must be shorter than 40 words
                sent.insert(40, None)
                if len(pos) > 2 and pos[2] == 's':
                    sent[78] = 'double subject'

        if bool1:
            bool1 = False
            sent[54] = [x for x in range(4,j)]
            sent[1] = build_sent_pos(sent)
            sent[3] = ""
            sent[0] = sent[3] + sent[1]
            sent[2] = name_sent(sent[46], output[8])

            direct_equivalence(output, ant_sent, ant_sentp, sent, rule)
            inferences.append([sent[0], sent[2], "", "EF", anc1, get_sn(output[0]), is_standard(sent)])


def replace_determinative_nouns():
    for sent in output[1]:
        replacement_made = False
        m = 4
        while sent[m] != None:
            if dictionary[10].get(sent[m]) == 19:
                ant_sent = sent[0]
                ant_sentp = sent[2]
                rule = "DE " + sent[m]
                synonym = dictionary[2].get(sent[m])
                determinative = synonym[:synonym.find(" ")]
                definition = dictionary[1].get(sent[m])
                noun = synonym[synonym.find(" ") + 1:]
                determinative.strip()
                noun.strip()
                sent[m] = determinative
                sent.insert(m + 1, "|" + noun)
                replacement_made = True
                m += 1
            m += 1

        if replacement_made:
            sent[54] = [x for x in range(4, m)]
            for x in range(4, m):
                if "|" in sent[x]: sent[x] = sent[x].replace("|", "")
            sent_name = "".join(sent[4:m])
            sent_name2 = " ".join(sent[4:m])
            sent_name = sent_name.replace("|", " ")
            sent_name2 = sent_name2.replace("|", "")
            sent[2] = name_sent(sent_name, output[8])
            sent[0] = "(" + sent_name2 + ")"
            sent[1] = sent[0]
            implication = build_connection(ant_sent, iff, sent[0])
            implicationp = build_connection(ant_sentp, iff, sent[2])
            qn = get_sn(output[0])
            add_to_tsent(output[0], implication, implicationp, "", rule)
            add_to_tsent(output[0], definition, "", "", rule)
            inferences.append([sent[0], sent[2], "", "EF", ant_sentp, qn, is_standard(sent)])


    return


def categorize_words2():
    for i, sent in enumerate(output[1]):
        comma_elimination = False
        if "," in sent[0]:
            ant_sent = sent[0]
            ant_sentp = sent[2]
            anc1 = sent[44]
            rule = "CME"
            comma_elimination = True
        b = sent[4:].index(None) + 4
        sent_num = sent[44]
        output[1][i] = categorize_words(output[6], sent[4:b], False, output[8], output[9], True)
        output[1][i][44] = sent_num
        if comma_elimination:
            direct_equivalence(output, ant_sent, ant_sentp, output[1][i], rule)
            inferences.append([output[1][i][0], output[1][i][2], "", "EF", anc1,
                               get_sn(output[0]), is_standard(output[1][i])])

    return


def replace_synonyms():
    definitions_added = []
    m = -1
    while m < len(output[1]) - 1:
        m += 1
        replacement_made = False
        word_order = output[1][m][45]
        j = 0
        while j < len(output[1][m][45]):
            if j == 6:
                bb = 8


            if word_order[j][1] == 18:
                i = word_order[j][0]

                ant_sent = output[1][m][0]
                ant_sentp = output[1][m][2]
                if i == 9:
                    bb = 8
                synonym = dictionary[2].get(output[1][m][i])
                assert synonym != None
                j = recategorize_word(synonym, m, i, j)
                definition = dictionary[1].get(output[1][m][i])
                if definition not in definitions_added:
                    definitions_added.append(definition)
                    add_to_tsent(output[0], definition, "", "", "DE " + output[1][m][i])
                replacement_made = True
                output[1][m][i] = synonym

            j += 1
        if replacement_made:
            direct_equivalence(output, ant_sent, ant_sentp, output[1][m], "SUB")
            output[1][m][45] = sorted(output[1][m][45], key=operator.itemgetter(1))
            inferences.append([output[1][m][0], output[1][m][2], "", "EF", ant_sentp, get_sn(output[0]), is_standard(output[1][m])])

    return


def recategorize_word(synonym, m, slot, j):
    # because we replace a word with a synonym we need to know it decision procedure
    # for elimination
    if j == 6:
        bb = 8

    raw_pos = dictionary[0].get(synonym)
    category = dictionary[10].get(synonym)
    if category != None:
        category = place_in_decision_procedure(category, slot, synonym, raw_pos)
        output[1][m][45][j] = tuple([slot, category])
    else:
        del output[1][m][45][j]
        j -= 1
    return j


def replace_special_synonyms():
    m = -1
    while m < len(output[1]) - 1:
        m += 1
        replacement_made = False
        j = 0
        word_order = output[1][m][45]
        while j < len(output[1][m][45]):
            if word_order[j][1] == 20:
                ant_sent = output[1][m][0]
                ant_sentp = output[1][m][1]
                i = word_order[j][0]
                rule = 'DE ' + output[1][m][i]
                replace_special_synonyms2(m, i)
                replacement_made = True
                del output[1][m][45][j]
            j += 1
        if replacement_made:
            direct_equivalence(output, ant_sent, ant_sentp, output[1][m], rule)
            inferences.append([output[1][m][0], output[1][m][2], "", "EF", ant_sentp, get_sn(output[0]), is_standard(output[1][m])])

    return


def replace_special_synonyms2(m, i):
    if output[1][m][i] == 'distinct from':
        output[1][m][i] = "="
        output[1][m][3] = "~"


def word_sub():
    m = -1
    while m < len(output[1]) - 1:
        m += 1
        replacement_made = False
        word_order = output[1][m][45]

        j = 0
        while j < len(output[1][m][45]):
            if word_order[j][1] == 0:
                ant_sent = output[1][m][0]
                ant_sentp = output[1][m][2]
                k = word_order[j][0]
                word = output[1][m][k]
                if word == 'which':
                    bb = 8

                if word == "not":
                    output[1][m][k] = "~"
                    output[1][m][3] = "~"
                    replacement_made = True
                elif word[-2:] == "'s":
                    replacement_made = True
                    word = word[:-2]
                    replace_word_w_variable(m, k, word)
                else:
                    pos = dictionary[0].get(word)
                    part_of_speech = parts_of_speech_dict.get(pos[0])
                    if part_of_speech == 'relation':
                        relat = dictionary[3].get(word)
                        if relat == None:
                            assert word in dictionary[3].values()
                        else:
                            replacement_made = True
                            output[6].update({word: relat})
                            output[1][m][k] = relat
                    else:
                        replacement_made = True
                        replace_word_w_variable(m, k, word)
                del output[1][m][45][j]
            else:
                j += 1

        if replacement_made:
            try:
                if output[1][m][54].index(12) > output[1][m][54].index(13):
                    g = output[1][m][54].index(12)
                    del output[1][m][54][g]
                    output[1][m][54].insert(g-1, 12)
            except:
                pass

            direct_equivalence(output, ant_sent, ant_sentp, output[1][m], "SUY")
            inferences.append([output[1][m][1], output[1][m][2], output[1][m][3], "EF", ant_sentp,
                               get_sn(output[0]), is_standard(output[1][m])])

    return


def replace_word_w_variable(m, k, str2):
    if isvariable(str2) == False:
        str3 = get_key(output[6], str2)
        if str3 == None:
            pos = dictionary[0].get(str2)
            if len(pos) > 1 and pos[1] == "u":

                list1 = svo_sent(output, output[14][0], "=", str2)
                add_to_tsent(output[0], list1[0], list1[2])
                list1[44] = get_sn(output[0])
                output[1].append(list1)
            if k == 134 or k == 135:
                output[1][m][k] = output[14][0] + "'s"
            else:
                output[1][m][k] = output[14][0]
            output[6].update({output[14][0]: str2})
            del output[14][0]
        elif k == 134 or k == 135:
            output[1][m][k] = str3 + "'s"
        else:
            output[1][m][k] = str3

    return


def artificial_sentence(sent):
    for snt in sent:
        output[1].append(snt)
    assert output[1][-1] == bottom or output[1][-1] == consist
    truth_value = False if output[1][-1] == bottom else True
    del output[1][-1]
    return truth_value


def shorten_sent():
    for j, sent in enumerate(output[1]):
        if len(sent) == 200:
            for i in range(140):
                del output[1][j][-1]

    return



