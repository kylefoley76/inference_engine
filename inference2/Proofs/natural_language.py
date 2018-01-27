

from general_functions import *
from collections import defaultdict
from uninstantiable_definitions import define_irregular_terms
from search_for_instantiation import try_instantiation
import sys, operator
from put_words_in_slots import categorize_words, place_in_decision_procedure


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
all_sent = []
abbreviations = {}
total_sent = []
get_words_used = 0
words_used = []
oprop_name = {}
variables = []

prop_name = defaultdict(lambda: prop_var.pop(), {})

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


def check_mispellings(test_sent):
    if proof_type != 3:
        return
    global prop_name, total_sent, all_sent, attach_sent, detach_sent, prop_var, sn, abbreviations
    for k in order:
        print(k)
        prop_name = []
        total_sent = []
        all_sent = []
        attach_sent = []
        detach_sent = []
        abbreviations = [{}, {}, {}]
        prop_var = copy.deepcopy(prop_var2)
        sn = test_sent[k][-1][0] + 1

        divide_sent(test_sent[k])

        eliminate_redundant_words()
    sys.exit()


def obtain_truth_value(sent):
    sent = sent.replace("!", "|")
    sentence = tran_str(sent)
    add_to_total_sent(total_sent, "CLAIM " + str(sent[0]) + ": " + sentence)
    add_to_total_sent(total_sent, "ABBREVIATIONS")

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


def eliminate_logical_connectives(sentence):
    return sentence.split(" and ")


def step_one(all_sent2):
    global all_sent, definite_assignments, inferences, total_sent
    global prop_name, abbreviations, words_used, oprop_name
    global variables, consistent, connected_const

    artificial = False
    consistent = True
    inferences = []
    all_sent = all_sent2
    abbreviations = {}
    total_sent = []
    connected_const = []
    words_used = []
    variables = copy.deepcopy(variables2)
    prop_var = copy.deepcopy(prop_var2)

    oprop_name = {}
    prop_name = defaultdict(lambda: prop_var.pop(), {})



    if "(" in all_sent[0]:

        artificial = True
        truth_value = artificial_sentence(all_sent)

    else:

        truth_value, sentence = obtain_truth_value(all_sent[0])

        all_sent = eliminate_logical_connectives(sentence)

        divide_sent(all_sent)

        eliminate_redundant_words()

        replace_determinative_nouns()

        categorize_words2()

        replace_synonyms()

        replace_special_synonyms()

        word_sub()

        all_sent = remove_duplicates(all_sent, 0)

        all_sent, consistent = define_irregular_terms(all_sent, inferences,
                                                      abbreviations, total_sent,
                                                      words_used,
                                                      prop_name, oprop_name,
                                                      variables, connected_const,
                                                      prop_var)

        all_sent = remove_duplicates(all_sent, 0)

        shorten_sent()

    if consistent:

        total_sent, consistent = try_instantiation(all_sent, prop_var, oprop_name,
                                                   prop_name, variables, total_sent,
                                                   abbreviations, connected_const,
                                                   artificial)




    return truth_value == consistent, total_sent


def divide_sent(all_sent):
    for i, sent in enumerate(all_sent):
        sent = sent.lower()
        sent = sent.strip()
        if "'s" not in sent: sent = sent.replace("'", "")
        if "," in sent: sent = sent.replace(",", " ,")
        sentp = name_sent(sent, prop_name)
        oprop_name[sentp] = sent
        words_in_sent = sent.split()
        all_sent[i] = [None] * 80
        all_sent[i][0] = sent
        all_sent[i][46] = sent
        all_sent[i][2] = sentp
        all_sent[i][3] = ""
        for j in range(len(words_in_sent)): all_sent[i][j + 4] = words_in_sent[j]
        add_to_total_sent(total_sent, sent, sentp, "", "")
        all_sent[i][44] = get_sn(total_sent)

    return


def eliminate_redundant_words():
    # modify this if we start dealing with sentences longer than 41 words
    global all_sent
    bool1 = False
    for sent in all_sent:
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
            sent[2] = name_sent(sent[46], prop_name)

            direct_equivalence(total_sent, ant_sent, ant_sentp, sent, prop_name, oprop_name, rule)
            inferences.append([sent[0], sent[2], "", "EF", anc1, get_sn(total_sent), is_standard(sent)])


def replace_determinative_nouns():
    for sent in all_sent:
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
            sent[2] = name_sent(sent_name, prop_name)
            sent[0] = "(" + sent_name2 + ")"
            sent[1] = sent[0]
            implication = build_connection(ant_sent, iff, sent[0])
            implicationp = build_connection(ant_sentp, iff, sent[2])
            qn = get_sn(total_sent)
            add_to_total_sent(total_sent, implication, implicationp, "", rule)
            add_to_total_sent(total_sent, definition, "", "", rule)
            inferences.append([sent[0], sent[2], "", "EF", ant_sentp, qn, is_standard(sent)])


    return


def categorize_words2():
    global all_sent
    for i, sent in enumerate(all_sent):
        comma_elimination = False
        if "," in sent[0]:
            ant_sent = sent[0]
            ant_sentp = sent[2]
            anc1 = sent[44]
            rule = "CME"
            comma_elimination = True

        sent_num = sent[44]
        all_sent[i] = categorize_words(abbreviations, sent, False,[], prop_name, oprop_name,
                                       True)
        all_sent[i][44] = sent_num
        if comma_elimination:
            direct_equivalence(total_sent, ant_sent, ant_sentp, all_sent[i], prop_name, oprop_name, rule)
            inferences.append([all_sent[i][0], all_sent[i][2], "", "EF", anc1,
                               get_sn(total_sent), is_standard(all_sent[i])])

    return


def replace_synonyms():
    definitions_added = []
    m = -1
    while m < len(all_sent) - 1:
        m += 1
        replacement_made = False
        word_order = all_sent[m][45]
        j = 0
        while j < len(all_sent[m][45]):
            if j == 6:
                bb = 8


            if word_order[j][1] == 18:
                i = word_order[j][0]

                ant_sent = all_sent[m][0]
                ant_sentp = all_sent[m][2]
                if i == 9:
                    bb = 8
                synonym = dictionary[2].get(all_sent[m][i])
                assert synonym != None
                j = recategorize_word(synonym, m, i, j)
                definition = dictionary[1].get(all_sent[m][i])
                if definition not in definitions_added:
                    definitions_added.append(definition)
                    add_to_total_sent(total_sent, definition, "", "", "DE " + all_sent[m][i])
                replacement_made = True
                all_sent[m][i] = synonym

            j += 1
        if replacement_made:
            direct_equivalence(total_sent, ant_sent, ant_sentp, all_sent[m], prop_name, oprop_name, "SUB")
            all_sent[m][45] = sorted(all_sent[m][45], key=operator.itemgetter(1))
            inferences.append([all_sent[m][0], all_sent[m][2], "", "EF", ant_sentp, get_sn(total_sent), is_standard(all_sent[m])])

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
        all_sent[m][45][j] = tuple([slot, category])
    else:
        del all_sent[m][45][j]
        j -= 1
    return j


def replace_special_synonyms():
    m = -1
    while m < len(all_sent) - 1:
        m += 1
        replacement_made = False
        j = 0
        word_order = all_sent[m][45]
        while j < len(all_sent[m][45]):
            if word_order[j][1] == 20:
                ant_sent = all_sent[m][0]
                ant_sentp = all_sent[m][1]
                i = word_order[j][0]
                rule = 'DE ' + all_sent[m][i]
                replace_special_synonyms2(m, i)
                replacement_made = True
                del all_sent[m][45][j]
            j += 1
        if replacement_made:
            direct_equivalence(total_sent, ant_sent, ant_sentp, all_sent[m], prop_name, oprop_name, rule)
            inferences.append([all_sent[m][0], all_sent[m][2], "", "EF", ant_sentp, get_sn(total_sent), is_standard(all_sent[m])])

    return


def replace_special_synonyms2(m, i):
    if all_sent[m][i] == 'distinct from':
        all_sent[m][i] = "="
        all_sent[m][3] = "~"


def word_sub():
    m = -1
    while m < len(all_sent) - 1:
        m += 1
        replacement_made = False
        word_order = all_sent[m][45]

        j = 0
        while j < len(all_sent[m][45]):
            if word_order[j][1] == 0:
                ant_sent = all_sent[m][0]
                ant_sentp = all_sent[m][2]
                k = word_order[j][0]
                word = all_sent[m][k]
                if word == 'which':
                    bb = 8

                if word == "not":
                    all_sent[m][k] = "~"
                    all_sent[m][3] = "~"
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
                            abbreviations.update({word: relat})
                            all_sent[m][k] = relat
                    else:
                        replacement_made = True
                        replace_word_w_variable(m, k, word)
                del all_sent[m][45][j]
            else:
                j += 1

        if replacement_made:
            try:
                if all_sent[m][54].index(12) > all_sent[m][54].index(13):
                    g = all_sent[m][54].index(12)
                    del all_sent[m][54][g]
                    all_sent[m][54].insert(g-1, 12)
            except:
                pass

            direct_equivalence(total_sent, ant_sent, ant_sentp, all_sent[m], prop_name, oprop_name, "SUY")
            inferences.append([all_sent[m][1], all_sent[m][2], all_sent[m][3], "EF", ant_sentp,
                               get_sn(total_sent), is_standard(all_sent[m])])

    return


def replace_word_w_variable(m, k, str2):
    if isvariable(str2) == False:
        str3 = get_key(abbreviations, str2)
        if str3 == None:
            pos = dictionary[0].get(str2)
            if len(pos) > 1 and pos[1] == "u":

                list1 = svo_sent(prop_name, variables[0], "=", str2, oprop_name)
                add_to_total_sent(total_sent, list1[0], list1[2])
                list1[44] = get_sn(total_sent)
                all_sent.append(list1)
            if k == 134 or k == 135:
                all_sent[m][k] = variables[0] + "'s"
            else:
                all_sent[m][k] = variables[0]
            abbreviations.update({variables[0]: str2})
            del variables[0]
        elif k == 134 or k == 135:
            all_sent[m][k] = str3 + "'s"
        else:
            all_sent[m][k] = str3

    return


def artificial_sentence(all_sent):
    assert all_sent[-1] == bottom or all_sent[-1] == consist
    truth_value = False if all_sent[-1] == bottom else True
    del all_sent[-1]
    return truth_value


def shorten_sent():
    for j, sent in enumerate(all_sent):
        if len(sent) == 200:
            for i in range(140):
                del all_sent[j][-1]

    return



