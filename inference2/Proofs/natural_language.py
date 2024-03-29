
from collections import defaultdict
import operator



try:
    from put_words_in_slots import categorize_words, place_in_decision_procedure
    from classes import get_output
    from general_functions import *
    from uninstantiable_definitions import define_irregular_terms
    from search_for_instantiation2 import try_instantiation
    from disambiguation import disambiguate_sentence
except:
    from .put_words_in_slots import categorize_words, place_in_decision_procedure
    from .classes import get_output
    from .general_functions import *
    from .uninstantiable_definitions import define_irregular_terms
    from .search_for_instantiation import try_instantiation
    from .disambiguation import disambiguate_sentence



# from put_words_in_slots import categorize_words, place_in_decision_procedure
# from classes import get_output
# from general_functions import *
# from uninstantiable_definitions import define_irregular_terms
# from search_for_instantiation2 import try_instantiation
# from disambiguation import disambiguate_sentence, build_ambig_sent



######### group: eliminate uninstantiable words part one




def obtain_truth_value():
    sent = output.all_sent[0]
    sent = sent.strip()
    if sent[-1] == ".":
        sent = sent[:-1]
    sent = sent.lower()
    sent = sent.replace("!", "|")
    sentence = tran_str(sent)
    if sentence.startswith("1"):
        sentence = sentence.replace("1", "it is consistent that")
    elif sentence.startswith("0"):
        sentence = sentence.replace("0", "it is contradictory that")


    add_to_tsent(output, "CLAIM " + str(sent[0]) + ": " + sentence, "", "", "", "natural")

    if len(sentence) < 22:
        raise Exception(
            "Each sentence must begin with either 'it is consistent that' or 'it is contradictory that")

    else:
        if sentence.startswith("it is consistent"):
            return True, sentence[len("It is consistent that "):]
        elif sentence.startswith("it is contradictory"):
            return False, sentence[len("It is contradictory that "):]
        else:
            raise Exception(
                "Each sentence must begin with either 'it is consistent that' or 'it is contradictory that")


def eliminate_logical_connectives():
    list1 = output.all_sent[0].split(" and ")
    return list1

def step_one(dictionary2, user, sent, lemmata, cat_num):
    global definite_assignments
    global prop_var2, dictionary
    global consistent, output

    proof_kind = ""
    sent = sent[cat_num]
    consistent = True
    dictionary = dictionary2
    output = get_output()
    output.variables = get_variables()
    output.prop_var = get_prop_var()
    output.prop_name = defaultdict(lambda: output.prop_var.pop(), {})
    output.user = user
    output.catalogue_num = cat_num

    if "(" in sent[0]:

        proof_kind = "artificial"

        truth_value = artificial_sentence(sent)

    else:

        output.all_sent.append(sent[0])

        truth_value, output.all_sent[0] = obtain_truth_value()

        output.all_sent = eliminate_logical_connectives()

        divide_sent()

        eliminate_redundant_words()

        replace_determinative_nouns()

        disambiguate_sentence(output, dictionary)

        categorize_words2()

        if not consistent: return False, output.total_sent, output.words_used

        replace_synonyms()

        replace_special_synonyms()

        word_sub()

        output.all_sent = remove_duplicates(output.all_sent, 0)

        output, consistent = define_irregular_terms(output, dictionary)

        output.all_sent = remove_duplicates(output.all_sent, 0)

        shorten_sent()

    if consistent:
        output, consistent, _ = try_instantiation(output, dictionary, lemmata, proof_kind)

    return truth_value == consistent, output.total_sent, output.words_used


def divide_sent():
    for i, sent in enumerate(output.all_sent):
        sent = sent.strip()
        if "'s" not in sent: sent = sent.replace("'", "")
        if "," in sent: sent = sent.replace(",", " ,")
        sentp = name_sent(sent, output.prop_name)
        output.oprop_name[sentp] = sent
        words_in_sent = sent.split()
        output.all_sent[i] = [None] * 80
        output.all_sent[i][0] = sent
        output.all_sent[i][46] = sent
        output.all_sent[i][2] = sentp
        output.all_sent[i][3] = ""
        for j in range(len(words_in_sent)): output.all_sent[i][j + 4] = words_in_sent[j]
        add_to_tsent(output, sent, sentp, "", "", "natural")
        output.all_sent[i][44] = output.tindex

    return


def eliminate_redundant_words():
    # modify this if we start dealing with sentences longer than 41 words
    bool1 = False
    for sent in output.all_sent:
        ant_sent = sent[0]
        ant_sentp = sent[2]
        rule = "RD"
        anc1 = sent[44]
        j = 3
        while j < 55:
            j += 1
            if sent[j] == None:
                break
            pos = dictionary.pos.get(sent[j])
            if pos != None and pos[0] == 't':
                if not isvariable(sent[j]):
                    output.words_used.add(sent[j])
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
            sent[54] = [x for x in range(4, j)]
            sent[1] = build_sent_pos(sent)
            sent[3] = ""
            sent[0] = sent[3] + sent[1]
            sent[2] = name_sent(sent[46], output.prop_name)

            direct_equivalence(output, ant_sent, ant_sentp, sent, rule)
            output.inferences.append([sent[0], sent[2], "", "EF", anc1, output.tindex, is_standard(sent)])


def replace_determinative_nouns():
    for sent in output.all_sent:
        replacement_made = False
        m = 4
        while sent[m] != None:
            if dictionary.decision_procedure.get(sent[m]) == 19:
                ant_sent = sent[0]
                ant_sentp = sent[2]
                rule = "DE " + sent[m]
                synonym = dictionary.synonyms.get(sent[m])
                determinative = synonym[:synonym.find(" ")]
                definition = dictionary.definitions.get(sent[m])
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
            sent[2] = name_sent(sent_name, output.prop_name)
            sent[0] = "(" + sent_name2 + ")"
            sent[1] = sent[0]
            implication = build_connection(ant_sent, iff, sent[0])
            implicationp = build_connection(ant_sentp, iff, sent[2])
            qn = output.tindex
            add_to_tsent(output, implication, implicationp, "", rule)
            add_to_tsent(output, definition, "", "", rule)
            output.inferences.append([sent[0], sent[2], "", "EF", ant_sentp, qn, is_standard(sent)])

    return


def categorize_words2():
    global consistent
    for i, sent in enumerate(output.all_sent):
        comma_elimination = False
        # if "," in sent[0]:
        #     ant_sent = sent[0]
        #     ant_sentp = sent[2]
        #     anc1 = sent[44]
        #     rule = "CME"
        #     comma_elimination = True
        categorized = categorize_words({}, sent, dictionary, output, "sub words")
        if isinstance(categorized, str):
            print (categorized)
            consistent = False
            return
        else:
            output.all_sent[i] = categorized

        if comma_elimination:
            direct_equivalence(output, ant_sent, ant_sentp, output.all_sent[i], rule)
            output.inferences.append([output.all_sent[i][0], output.all_sent[i][2], "", "EF", anc1,
                               output.tindex, is_standard(output.all_sent[i])])


    return


def replace_synonyms():
    definitions_added = []
    m = -1
    while m < len(output.all_sent) - 1:
        m += 1
        replacement_made = False
        word_order = output.all_sent[m][45]
        j = 0
        while j < len(output.all_sent[m][45]):
            if j == 6:
                bb = 8

            if word_order[j][1] == 18:
                i = word_order[j][0]

                ant_sent = output.all_sent[m][0]
                ant_sentp = output.all_sent[m][2]
                if i == 9:
                    bb = 8
                synonym = dictionary.synonyms.get(output.all_sent[m][i])
                assert synonym != None
                j = recategorize_word(synonym, m, i, j)
                definition = dictionary.definitions.get(output.all_sent[m][i])
                if definition not in definitions_added:
                    definitions_added.append(definition)
                    add_to_tsent(output, definition, "", "", "DE " + output.all_sent[m][i])
                replacement_made = True
                output.all_sent[m][i] = synonym

            j += 1
        if replacement_made:
            direct_equivalence(output, ant_sent, ant_sentp, output.all_sent[m], "SUZ", output.tindex)
            output.all_sent[m][45] = sorted(output.all_sent[m][45], key=operator.itemgetter(1))

            output.inferences.append(
                [output.all_sent[m][0], output.all_sent[m][2], "", "EF", ant_sentp, output.tindex, is_standard(output.all_sent[m])])

    return


def recategorize_word(synonym, m, slot, j):
    # because we replace a word with a synonym we need to know it decision procedure
    # for elimination
    if j == 6:
        bb = 8

    raw_pos = dictionary.pos.get(synonym)
    category = dictionary.decision_procedure.get(synonym)
    if category != None:
        category = place_in_decision_procedure(category, slot, synonym, raw_pos)
        output.all_sent[m][45][j] = tuple([slot, category])
    else:
        del output.all_sent[m][45][j]
        j -= 1
    return j


def replace_special_synonyms():
    m = -1
    while m < len(output.all_sent) - 1:
        m += 1
        replacement_made = False
        j = 0
        word_order = output.all_sent[m][45]
        while j < len(output.all_sent[m][45]):
            if word_order[j][1] == 20:
                ant_sent = output.all_sent[m][0]
                ant_sentp = output.all_sent[m][1]
                i = word_order[j][0]
                rule = 'DE ' + output.all_sent[m][i]
                replace_special_synonyms2(m, i)
                replacement_made = True
                del output.all_sent[m][45][j]
            j += 1
        if replacement_made:
            direct_equivalence(output, ant_sent, ant_sentp, output.all_sent[m], rule)
            output.inferences.append(
                [output.all_sent[m][0], output.all_sent[m][2], "", "EF", ant_sentp, output.tindex, is_standard(output.all_sent[m])])

    return


def replace_special_synonyms2(m, i):
    if output.all_sent[m][i] == 'distinct from':
        output.all_sent[m][i] = "="
        output.all_sent[m][3] = "~"


def word_sub():
    m = -1
    while m < len(output.all_sent) - 1:
        m += 1
        replacement_made = False
        word_order = output.all_sent[m][45]

        j = 0
        while j < len(output.all_sent[m][45]):
            if word_order[j][1] == 0:
                ant_sent = output.all_sent[m][0]
                ant_sentp = output.all_sent[m][2]
                k = word_order[j][0]
                word = output.all_sent[m][k]
                if word == 'which':
                    bb = 8
                if isvariable(word):
                    pass

                elif word == "not":
                    output.all_sent[m][k] = "~"
                    output.all_sent[m][3] = "~"
                    replacement_made = True
                elif word[-2:] == "'s":
                    replacement_made = True
                    word = word[:-2]
                    replace_word_w_variable(m, k, word)
                else:
                    pos = dictionary.pos.get(word)
                    part_of_speech = parts_of_speech_dict.get(pos[0])
                    if part_of_speech == 'relation':
                        relat = dictionary.rel_abbrev.get(word)
                        if relat == None:
                            assert word in dictionary.rel_abbrev.values()
                        else:
                            replacement_made = True
                            output.abbreviations.update({word: relat})
                            output.all_sent[m][k] = relat
                    else:
                        replacement_made = True
                        replace_word_w_variable(m, k, word)
                del output.all_sent[m][45][j]
            else:
                j += 1

        if replacement_made:
            try:
                if output.all_sent[m][54].index(12) > output.all_sent[m][54].index(13):
                    g = output.all_sent[m][54].index(12)
                    del output.all_sent[m][54][g]
                    output.all_sent[m][54].insert(g - 1, 12)
            except:
                pass

            direct_equivalence(output, ant_sent, ant_sentp, output.all_sent[m], "SUY")
            output.inferences.append([output.all_sent[m][1], output.all_sent[m][2], output.all_sent[m][3], "EF", ant_sentp,
                               output.tindex, is_standard(output.all_sent[m])])

    return


def replace_word_w_variable(m, k, word):
    if isvariable(word) == False:
        str3 = get_key(output.abbreviations, word)
        if str3 == None:
            pos = dictionary.pos.get(word)
            if dictionary.kind.get(word) == "i":
                list1 = svo_sent(output, output.variables[0], "=", word)
                add_to_tsent(output, list1[0], list1[2], "", "ABB", "", "","standard")
                list1[44] = output.tindex
                output.all_sent.append(list1)
            if k == 134 or k == 135:
                output.all_sent[m][k] = output.variables[0] + "'s"
            else:
                output.all_sent[m][k] = output.variables[0]
            output.abbreviations.update({output.variables[0]: word})
            del output.variables[0]
        elif k == 134 or k == 135:
            output.all_sent[m][k] = str3 + "'s"
        else:
            output.all_sent[m][k] = str3

    return


def artificial_sentence(sent):
    for snt in sent:
        output.all_sent.append(snt)
    assert output.all_sent[-1] == bottom or output.all_sent[-1] == consist
    truth_value = False if output.all_sent[-1] == bottom else True
    del output.all_sent[-1]
    return truth_value


def shorten_sent():
    for j, sent in enumerate(output.all_sent):
        if len(sent) == 200:
            for i in range(140):
                del output.all_sent[j][-1]

    return
