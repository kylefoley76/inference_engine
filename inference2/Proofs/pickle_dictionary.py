from general_functions import *
from settings import *
from openpyxl import load_workbook
import pickle
import json
import re, sys
from standard_order import order_sentence
from analyze_sentence import find_sentences, period_elimination, eliminate_conjuncts_from_definition
from put_words_in_slots import categorize_words


variables = [chr(122 - t) for t in range(25)]
variables.remove("i")
variables.remove("l")
variables3 = [chr(122 - t) + l1 for t in range(26)]
variables3.remove("l" + l1)
variables4 = [chr(122 - t) + l2 for t in range(26)]
variables4.remove("l" + l2)
variables5 = [chr(122 - t) + l3 for t in range(26)]
variables5.remove("l" + l3)
variables = variables + variables3 + variables4 + variables5



def update_synonyms(definition):

    str6 = definition[definition.find("=") + 1:-1]
    str6 = str6.strip()
    str7 = definition[1:definition.find("=")]
    str7 = str7.strip()
    dictionary[2].update({str7: str6})
    dictionary[1].update({str7: definition})


def cut_word(word):
    try:
        if "(" in word:
            cc = word.index("(")
            word = word[:cc - 1]
            word = word.strip()
        else:
            word = word.strip()
    except:
        word = ""

    return word


def is_a_definition(str1):
    if str1 == None:
        return False
    if "e.g." in str1:
        return False
    formal_symbols = ["&", "=", conditional, iff, xorr]
    for n in formal_symbols:
        if n in str1:
            return True
    return False


def get_prepositional_relations():
    str1 = third_sheet.cell(row=2, column=5).value
    str1a = third_sheet.cell(row=3, column=5).value
    str2 = third_sheet.cell(row=6, column=5).value
    str2a = third_sheet.cell(row=7, column=5).value
    str3 = third_sheet.cell(row=10, column=5).value
    str3a = third_sheet.cell(row=11, column=5).value
    prepositional = str1.split() + str1a.split()
    non_spatio_temporal = str2.split() + str2a.split()
    spatio_temporal = str3.split() + str3a.split()

    dictionary[8] = prepositional
    dictionary[13] = spatio_temporal
    dictionary[14] = non_spatio_temporal


def build_dictionary():
    global ws, wsar, third_sheet, dictionary
    dictionary = [{}, {}, {}, {}, {}, {}, [], {}, [], {}, {}, [], [], [], [], [], {}, []]

    #	0	parts of speech
    #	1	definitions
    #	2	synonyms
    #	3	abbreviated relations
    #	4	doubles
    #	5	triples
    #	6	individuals
    #	7	words to row
    #	8	prepositional relations
    #	9	categorized sent
    #	10	word decision procedure
    #	11	list of easy embeds
    #	12	embed type {}
    #	13	spatio temporal relations
    #	14	non spatio temporal relations
    #	15	concepts
    #   16  number of conjunctions
    #   17  past participles

    worksheet = ws

    get_prepositional_relations()


    i = 25
    while i < 3000:

        i += 1
        row_num = worksheet.cell(row=i, column=1).value
        pos = worksheet.cell(row=i, column=3).value
        word = worksheet.cell(row=i, column=4).value
        next_word = worksheet.cell(row=i + 1, column=4).value
        abbrev_relat = worksheet.cell(row=i, column=5).value
        defin = worksheet.cell(row=i, column=6).value
        next_defin = worksheet.cell(row=i + 1, column=6).value
        edisj = worksheet.cell(row=i, column=13).value
        embed = worksheet.cell(row=i, column=7).value
        easy_embed = worksheet.cell(row=i, column=8).value

        if word == 'spies on':
            bb = 8

        if not not_blank(word) and not not_blank(next_word) and i > 300:
            break

        if not_blank(pos):
            if easy_embed in [1,6]: embed = False
            if embed == 'done': embed = False
            if not isinstance(pos, int): pos = pos.strip()
            if isinstance(word, int): word = str(word)
            if word == "true*": word = "true"
            if word == "false*": word = "false"
            word = cut_word(word)
            next_word = cut_word(next_word)

            fir_let, sec_let = put_in_categories(abbrev_relat, pos, row_num, word, defin)

            # universals are not defined, synonyms and determinative nouns are already done
            if sec_let not in ['a', 'b', 's', 'd'] and not embed and not_blank(defin):

                defin = defin.strip()

                if next_word == word and "e.g." not in next_defin:
                    while is_a_definition(worksheet.cell(row=i + 1, column=6).value) \
                    and next_word == word:
                        i += 1
                        defin += "| " + worksheet.cell(row=i, column=6).value.strip()
                        next_word = worksheet.cell(row=i + 1, column=4).value
                        next_word = cut_word(next_word)


                if fir_let == "r":
                    dictionary[1].update({abbrev_relat: defin})
                    if easy_embed in [1,6] and fir_let == 'd':
                        dictionary[11].append(abbrev_relat)
                        dictionary[12].update({abbrev_relat: easy_embed})


                else:
                    if easy_embed in [1,6] and fir_let == 'd':
                        dictionary[11].append(word)
                        # embed_type.update({word: easy_embed})
                    dictionary[1].update({word: defin})





def put_in_categories(abbrev_relat, pos, row_num, word, defin):
    if len(pos) == 1: pos += "z"
    dictionary[0].update({word: pos})
    fir_let = pos[0]
    sec_let = pos[1]
    thir_let = pos[2] if len(pos) > 2 else ""
    four_let = pos[3] if len(pos) > 3 else ""
    fif_let = pos[4] if len(pos) > 4 else ""
    place_in_decision_procedure2(word, fir_let, sec_let, dictionary[10])
    if " " in word: make_doubles(word)
    dictionary[7].update({word: row_num})
    if pos[1] in ['s', "d"]: update_synonyms(defin)
    if not_blank(abbrev_relat):
        place_in_decision_procedure2(abbrev_relat, fir_let, sec_let, dictionary[10])
        if abbrev_relat not in dictionary[7].keys():
            dictionary[7].update({abbrev_relat: row_num})
        if fir_let == 'r': dictionary[0].update({abbrev_relat: pos})
        if fir_let == 'r': dictionary[3].update({word: abbrev_relat})
        if len(abbrev_relat) == 4 and abbrev_relat[-1] == "P":dictionary[17].append(abbrev_relat)
    if fir_let == 'r' and sec_let not in ['s','a'] and not not_blank(abbrev_relat):
        raise Exception (f"you forgot to give {word} an abbreviation")

    return fir_let, sec_let

def make_doubles(word):
    m = word.count(" ")
    if m == 1:
        word1 = copy.copy(word)
        y = word1.find(" ")
        word1 = word1[:y]
        dictionary[4].setdefault(word1, []).append(word)
    if m == 2:
        word1 = copy.copy(word)
        y = word1.find(" ")
        word1 = word1[:y]
        dictionary[5].setdefault(word1, []).append(word)


def place_in_decision_procedure2(word, part_of_speech, sub_part, categories):
    category = None
    if sub_part == 'd':  # determinative nouns
        category = 19
    elif word in ['distinct from', 'different']:  # special synonyms, distinct from
        category = 20
    elif sub_part == 's':  # synonyms
        category = 18
    elif word == "i":
        category = .5
    elif part_of_speech == 'd' and sub_part not in ['b', 'i', 'e', 'd']:
        category = 1  # determinative, possessive pronouns
    elif part_of_speech == 'p':
        category = 2
    elif word == 'and' + uc:
        category = 5  # and
    elif part_of_speech == 'u':  # relative pronouns
        category = 9
    elif word in ['AS', 'as']:  # AS
        category = 11
    elif word in dictionary[13]:
        category = 13
    elif word in dictionary[14]:
        category = 13.5

    elif word == 'there':  # there
        category = 14
    elif part_of_speech == 'd' and sub_part == 'b':  # universals
        category = 15
    elif part_of_speech == 'd' and sub_part == 'e':  # many
        category = 16
    elif part_of_speech == 'm':  # negative determiners
        category = .4

    if category != None: categories.update({word: category})


#######################
########  the following are children of get sets of conditions


def get_connection_type(sentences):
    if sentences[10][7][-1] in ['b', 'f']:
        sentences[85] = 'e'
    elif sentences[10][7][-1] in ['a', 'q']:
        sentences[85] = 'c'
    elif sentences[10][7][-1] == "x":
        sentences[85] = 'x'
    elif sentences[10][7][-1] == "d":
        sentences[85] = 'd'


def get_sent_kind(def_info2):
    sent_kind = []
    if len(def_info2) > 1:
        n = 1
        sent_kind.append("")
    else:
        n = 0

    for o in range(n, len(def_info2)):
        def_info = def_info2[o]
        e = -1
        temp_kind = ["","",""]
        dict1 = {xorr: 'x', conditional: 'c', iff: 'b'}
        dict2 = {"&": '&', xorr: 'd', iff: 'b', conditional: 'c', '': 's'}
        for lst, sent, esent, fam_num in zip(def_info[4], def_info[6], def_info[3], def_info[1]):
            e += 1
            if e > 1:
                parent = ".".join(fam_num[:-1])
                parent_type = def_info[4][def_info[2].index(parent)][1]

            if lst[0].count(".") == 0:
                temp_kind[0] = dict1.get(lst[1])
                assert temp_kind[0] != None
            elif lst[0].count(".") == 1:
                if fam_num[1] == '1' and temp_kind[1] == "":
                    temp_kind[1] = dict2.get(lst[1])
                elif fam_num[1] == '2' and temp_kind[2] == "":
                    temp_kind[2] = dict2.get(lst[1])
            # these are sentences of the form p <> (q & r & (s v t))
            elif lst[0].count(".") == 2 and lst[1] in [xorr, idisj] \
                 and parent_type == "&" and fam_num[1] == '2':
                temp_kind[2] = 't'
        sent_kind.append(temp_kind)

    return sent_kind


def get_sets_disjunct(lst, side, sentences, embed, word, size):
    conditions = {}
    loc = 0 if side == "1" else 1
    b = 0 if embed else 1
    # if re.search(r'[qabf]', sent[7]):
    i = 0
    for lst1, lst6 in zip(lst[1], lst[6]):
        if i == 3:
            bb = 8
        if len(lst1) == 1:
            pass
        elif lst1[loc] != side:
            pass
        elif len(lst1) > 1 and lst1[loc] == side:
            parent = ".".join(lst1[:size])
            if lst[4][i][1] == "":
                sent_index = lst[7].get(lst6)
                if embed:
                    sent_type = sentences[sent_index][56]
                else:
                    sent_type = sentences[sent_index][7][:-b]
            else:
                sent_index = str(i)

            if len(lst1) == 2 and lst[4][i][1] == xorr:
                pass

            elif len(lst1) == size and lst[4][i][1] != "":
                conditions.update({lst[2][i]: {}})

            elif len(lst1) == size and lst[4][i][1] == "":
                conditions.update({lst[2][i]: {lst[2][i]: [sent_index]}})
                assert isinstance(sent_index, int)

            elif len(lst1) > size and lst[4][i][1] in [conditional, iff]:
                dict2 = conditions.get(parent)
                dict2.update({lst[2][i]:[]})

            elif len(lst1) > size and lst[4][i][1] == "":
                dict2 = conditions.get(parent)


                if not re.search(r'[qabf]', sent_type):
                    dict2.update({lst[2][i]: [sent_index]})
                    assert isinstance(sent_index, int)
                else:
                    for k, v in dict2.items():

                        if lst[2][i].startswith(k + "."):
                            v.append(sent_index)
                            assert isinstance(sent_index, int)
                            break

                    else:
                        raise Exception ("failed to find conditional parent in disjunct")

            elif len(lst1) > size and lst[4][i][1] == "&":
                pass
            else:
                raise Exception("failed to find conditional parent in disjunct")










        i += 1

    return conditions


def get_sets_of_conditions2(lst, side, sent_kind):
    conditions = {}
    dict1 = {"s":2, "c":2, "b":2, "&":3, "d":3}
    size = dict1.get(sent_kind)


    i = 0
    for lst1, lst6 in zip(lst[1], lst[6]):
        if len(lst1) > size - 1 and lst1[1] == side:

            if len(lst1) == size and lst[4][i][1] != "":
                conditions.update({lst[2][i]: []})
            elif len(lst1) == size and lst[4][i][1] == "":
                sent_index = lst[7].get(lst6)
                assert sent_index != None
                conditions.update({lst[2][i]: [sent_index]})
            elif len(lst1) > size and lst[4][i][1] == "":
                parent = ".".join(lst1[:size])
                sent_index = lst[7].get(lst6)
                assert sent_index != None
                conditions.setdefault(parent, []).append(sent_index)
            elif len(lst1) > size and lst[4][i][1] != "":
                pass



        i += 1


    return conditions

#sent_kinds

# first letter represents whether the whole is bicond = b, cond = c, disj = d
# second letter represents whether the antecedent is conj = &, cond = c, bicond = b, single = s
# third letter represents whether the consequent is bicond = b, cond = c, disj = d, cong = &, single = s
# if third letter is t then the consequent must be distributed

def get_sets_of_conditions(def_info, word, sentences, sent_kind, combine=False, embed = False):
    n = 1 if len(def_info) > 1 else 0
    if word == 'LFT': #
        bb = 8
    ex_conditions = {}
    conditions2 = {}
    conditions = {}
    for g in range(n, len(def_info)):
        get_connection_type(sentences[g])
        lst = def_info[g]
        if sent_kind[g][0] != 'x':
            conditions = get_sets_of_conditions2(lst, "1", sent_kind[g][1])

            if sent_kind[g][2] == "d":
                ex_conditions = get_sets_disjunct(lst, "2", sentences[g], embed, word, 3)

            elif sent_kind[g][2] == "t":
                ex_conditions = distribute(lst)
            else:
                conditions2 = get_sets_of_conditions2(lst, "2", sent_kind[g][2])

        else:
            ex_conditions = get_sets_disjunct(lst, "1", sentences[g], embed, word, 2)

        greek_hypotheticals = get_greek_hypotheticals(lst)
        conditions3 = build_all_conditions(conditions, conditions2, ex_conditions)

        b = 7 if combine else 56
        sentences[g][60] = build_sentence_shape(conditions3, sentences, greek_hypotheticals, sent_kind, word, g, b)

    return def_info


def build_all_conditions(conditions, conditions2, ex_conditions):
    conditions3 = [0, 0]
    conditions3[0], conditions3[1] = conditions, conditions2
    if ex_conditions != {}:
        for v in ex_conditions.values():
            conditions3.append(v)
    return conditions3


def get_greek_hypotheticals(list1):
    greek_hypotheticals = []
    i = 0
    for lst2, lst4, lst6 in zip(list1[2], list1[4], list1[6]):
        if i > 0 and lst4[1] in [conditional, iff, xorr, idisj]:
            greek_hypotheticals.append([lst2, lst6])
        i += 1
    return greek_hypotheticals


def get_parent_conn_type(def_info, i, grandparent = False):
    b = 2 if grandparent else 1
    if i > 0:
        parent = ".".join(def_info[1][i][:-b])
        parent_pos = def_info[2].index(parent)
        return def_info[4][parent_pos][1]
    return ""


def distribute(lst):
    i = 0
    conditions = {}
    gparent_conn_type = ""
    disjunctions = {}
    for lst1, lst6 in zip(lst[1], lst[6]):
        if i == 9:
            bb = 8
        if len(lst1) > 1 and lst1[1] == "2":
            parent_conn_type = get_parent_conn_type(lst, i)
            if len(lst1) > 2:
                gparent_conn_type = get_parent_conn_type(lst, i, True)

            if parent_conn_type == xorr and lst[4][i][1] == "":
                sent_index = lst[7].get(lst6)
                disjunctions.update({lst[2][i]: [sent_index]})
            elif parent_conn_type == xorr and lst[4][i][1] == "&":
                disjunctions.update({lst[2][i]: {}})

            elif gparent_conn_type == xorr and parent_conn_type == "&" \
                and lst[4][i][1] == "":

                parent = ".".join(lst1[:4])
                sent_index = lst[7].get(lst6)
                assert sent_index != None
                dict2 = disjunctions.get(parent)
                dict2.update({lst[2][i]: [sent_index]})

            elif lst[4][i][1] == xorr:
                pass
            elif len(lst1) == 2:
                conditions.update({lst[2][i]: {}})
            elif lst[4][i][1] == "" and len(lst1) == 3:
                parent = ".".join(lst1[:2])
                sent_index = lst[7].get(lst6)
                assert sent_index != None
                dict2 = conditions.get(parent)
                dict2.update({lst[2][i]: [sent_index]})

            else:
                print('you havent does this type of distribution')
        i += 1
    i = 0

    for k, v in disjunctions.items():
        if i == 0:
            temp = conditions.get("2.2")
            temp2 = copy.deepcopy(temp)
            if len(v) > 1:
                for y,z in v.items(): temp.update({y:z})
            else:
                temp.update({k: v})

        else:
            temp3 = temp2
            str1 = str(i)
            if len(v) > 1:
                for y, z in v.items(): temp3.update({y :z})
            else:
                temp3.update({k :v})
            conditions.update({str1: copy.deepcopy(temp3)})
            if i == 3:
                raise Exception('check this')

        i += 1

    return conditions


def build_sentence_shape(conditions3, sentences, greek_hypotheticals, kind, word, g, b):
    k = 0
    for j, dict1 in enumerate(conditions3):
        if word == 'KN':#
            bb = 8

        for_detach = []
        for_conj_elimination = {}
        for_conj_elimination2 = []

        for subkey, subvalues in dict1.items():

            str1, str2, conj_elim2 = string_constants_together(subvalues,
            sentences, g, b, greek_hypotheticals, kind, False, subkey)

            if (sentences[g][85] != "c" or j != 1):
                for_detach.append([str1, subvalues])
            if isinstance(str2, str) and j < 2:
                for_conj_elimination.update({str2: subvalues})
                for_conj_elimination2.append([str2, subvalues])

            elif isinstance(str2, list) and j < 2:
                k += 1
                for_conj_elimination.update({k: str2})
                # for_conj_elimination2.append([k, conj_elim2])
                for_conj_elimination2.append(conj_elim2)

        c = 4 if j == 0 else 5
        sentences[g][c] = for_conj_elimination2
        sentences[g][c + 57] = for_conj_elimination

        conditions3[j] = for_detach

    return copy.deepcopy(conditions3)


def string_together(sent, premise):
    if premise:
        if re.search(r'[qabf]', sent[7]):
            return True
        else:
            return False
    else:
        if re.search(r'[qabf]', sent[7][:-1]):
            return True
        else:
            return False


def string_constants_together(subvalues, sentences, g, b, greek_hypotheticals, kind, premise=False, subkey = []):
    for_detach = []
    for_conj_elim = []
    embedded_hypothesis = False
    ant = []
    con = []
    list1 = []
    lesser_sent = {}
    lesser_sent_key = ""
    new_definiendum = ""
    greater_sent = {}
    conj_elim2 = []

    list2 = []
    meets_conditions = string_together(sentences[g][subvalues[0]], premise)

    for value in subvalues:
        if len(subvalues) == 1 and not premise:
            for_detach.append(sentences[g][value][58])

        elif meets_conditions:
            temp_skeleton = sentences[g][value][59] + "." + sentences[g][value][b] + "." \
                + sentences[g][value][58]
            for_detach.append(temp_skeleton)
        else:
            temp_skeleton = sentences[g][value][58]
            for_detach.append(temp_skeleton)


        if len(subvalues) > 1 and not premise:
            embedded_hypothesis = True
            lesser_sent_key += sentences[g][value][59] + "." + sentences[g][value][b] \
                        + "." + sentences[g][value][58]
            if sentences[g][value][56][-1] in ['a', 'b']:
                ant.append([sentences[g][value][58],[value]])
                if new_definiendum == "":
                    new_definiendum = greek_hypotheticals[0][0] + "," + sentences[g][value][4]

            elif sentences[g][value][56][-1] == 'f':
                con.append([sentences[g][value][58], [value]])


    if embedded_hypothesis:
        try:
            list1.append(ant)
            if con != []: list1.append(con)
            greater_sent[new_definiendum] = list1
            greater_sent2 = [new_definiendum, list1]
            lesser_sent[lesser_sent_key] = subvalues
            lesser_sent2 = [lesser_sent_key,subvalues]
            list2 = [lesser_sent, greater_sent, greek_hypotheticals[0][1]]
            conj_elim2 = [lesser_sent2, greater_sent2, greek_hypotheticals[0][1]]
            del greek_hypotheticals[0]
        except:
            list2 = [{}, {}, ""]
            conj_elim2 = [[], [], ""]


    for_detach.sort()
    str1 = " ".join(for_detach)

    if len(subvalues) == 1:
        str2 = str1
        conj_elim2 = str1
    else:
        str2 = list2


    return str1, str2, conj_elim2


def build_hypo_list(def_info, definiendum = "", abbreviations = [], connected_const = []):
    if definiendum == "ABF":
        bb = 8


    definition = def_info[0][3][0]
    sentences = []

    if "." in definition:
        def_info, definition = period_elimination(def_info, definition)
    if len(def_info) > 1:
        m = 1
        list1 = [None] * 100
        list1[79] = []
        list1[0] = def_info[0][3][0]
        list1[9] = abbreviations
        list1[2] = def_info[0][5]
        sentences.append(list1)
    else:
        m = 0
    for k in range(m, len(def_info)):
        j = -1
        list1 = [None] * 100
        list1[79] = []
        lst = def_info[k]
        for i, sent in enumerate(lst[3]):
            if lst[4][i][1] == "":
                j += 1
                tvalue = ""
                tvalue2 = ""
                if one_sentence(sent) and sent[0] == "~":
                    tvalue = "~"
                    sent = sent[1:]
                    tvalue2 = "~ "

                sent = split_sentences(sent)
                sent = [None] * 4 + sent + [None]
                sent = categorize_words(abbreviations, sent, True, connected_const)
                sent[3] = tvalue
                sent[5] = lst[6][i]
                sent[6] = lst[2][i]
                sent[4] = definiendum
                sent[7] = get_sent_type(sent[6], lst)
                sent[56] = get_match_type(sent[7])
                sent[58] = tvalue2 + sent[58]
                list1[j + 10] = sent
            if lst[2][i].count(".") == 1:
                list4 = lst[2][i].split(".")
                if list4[1] == "1":
                    list1[7] = lst[6][i]
                else:
                    list1[8] = lst[6][i]

        list1[0] = lst[3][0]
        list1[9] = abbreviations
        list1[2] = lst[5]


        sentences.append(list1)


    return sentences


def get_sent_type(sent_num, def_info):
    num_list = sent_num.split(".")
    sent_type = ""

    while len(num_list) > 1:
        current_num = num_list[-1]
        del num_list[-1]
        str1 = ".".join(num_list)
        connective = def_info[4][def_info[2].index(str1)][1]
        temp_type = convert_con_to_letter(connective, current_num)
        sent_type += temp_type

    return sent_type


def convert_con_to_letter(str1, str2):
    if str1 == iff and str2 == '1':
        return 'b'
    elif str1 == iff and str2 == '2':
        return 'f'
    elif str1 == conditional and str2 == '1':
        return 'a'
    elif str1 == conditional and str2 == '2':
        return 'q'
    elif str1 == xorr:
        return 'x'
    elif str1 == idisj:
        return 'd'
    elif str1 == "&":
        return "c"


def split_sentences(sent):
    if "~ =" in sent:
        pass
    elif "=" in sent:
        sent = sent.replace("=", " = ")
    sent = sent.replace("(", "")
    sent = sent.replace(")", "")
    return sent.split(" ")


def get_abbreviations_from_definition(def_info):
    # this function picks out that variables in the id sentences of the
    # definition

    constants = {}
    constant_map = {}
    temp_propositional_constants = {}

    list3 = []
    for i in range(len(def_info[3])):
        if one_sentence(def_info[3][i]) and mini_e in def_info[3][i]:
            list3.append(def_info[3][i])
        elif one_sentence(def_info[3][i]) and "=" in def_info[3][i]:
            str1 = def_info[3][i]
            g = str1.find("=")
            var = str1[1:g]
            word = str1[g + 1:-1]
            if isvariable(var):
                if not isvariable(word):
                    constants.update({var: word})

    return constants


def get_match_type(str1):
    if len(str1) == 1:
        if str1 in ["b","f","a","x","d"]:
            str1 = "c"
        else:
            str1 = "q"
    elif len(str1) == 2:
        if str1[0] == "x":
            str1 = "c"
        else:
            str1 = str1[:-1]
    elif len(str1) > 3 and str1[-3:] == 'cxf':
        str1 = str1[:-3]
    else:
        str1 = str1[:-1]
        if str1[-1] in ["c","x"]:
            str1 = str1[:-1]
        if str1[0] == "x":
            str1 = "c"

    return str1


#############################
##########  the following are for the determiners

def get_determiner_info(pos, definiendum, sentences):
    if definiendum == 'he':
        bb = 8

    instance_names = []
    instance_position = []
    concept_names = []
    concept_positions = []
    tvalue = []
    rsent_positions = []
    m = 11
    while sentences[0][m] != None:
        if sentences[0][m][13] == "R":
            rsent_positions.append(m)
            tvalue.append(sentences[0][m][3])
        if sentences[0][m][13] == "I":
            instance_names.append(sentences[0][m][10])
            instance_position.append([m, 10])
            concept_names.append(sentences[0][m][14])
            concept_positions.append([m, 14])
        m += 1
    sentences[0][30] = instance_names
    sentences[0][31] = instance_position
    sentences[0][32] = concept_names
    sentences[0][33] = concept_positions
    sentences[0][34] = tvalue
    sentences[0][35] = rsent_positions
    sentences[0][45] = []


#########################
######## the following are children of embedded hypothetical sentences

def get_disjuncts(def_info, sentences):
    n = 1 if len(sentences) > 1 else 0
    for m in range(n, len(def_info)):
        list1 = []
        if xorr in def_info[m][5] or idisj in def_info[m][5]:
            for i, lst in enumerate(def_info[m][4]):
                if lst[1] == xorr or lst[1] == idisj:
                    list1.append([def_info[m][3][i], def_info[m][6][i]])
            sentences[m][79] = list1


def exclusive_disjunct(real_sentences, def_info):
    if real_sentences == []:
        raise Exception("you have not coded for this type yet")
    if xorr not in real_sentences[0][2]:
        return
    sent_types = real_sentences[0][82]
    i = 10
    j = 0
    dict1 = {}
    dict2 = {}
    conjunctions = {}
    while real_sentences[0][i] != None:
        list1 = real_sentences[0][i][6].split(".")
        if sent_types[j] == "cx":
            num = list1[-2]
        elif sent_types[j] == "x":
            num = list1[-1]
        else:
            raise Exception("you haven't coded for this type yet")
        conjunctions.setdefault(num, []).append(real_sentences[0][i])

        group = dict1.get(num)
        if group == None:
            group = [real_sentences[0][i][6]]
            group_sent = [real_sentences[0][i]]
        else:
            group.append(real_sentences[0][i][6])
            group_sent.append(real_sentences[0][i])
        # dict1.update({num: group})
        dict2.update({num: real_sentences[0][i]})
        i += 1
        j += 1
    num = 69
    for k, v in dict2.items():
        num += 1
        temp = conjunctions.get(k)
        real_sentences[0][num] = get_disjunct_info(temp, def_info[0], v)

    # return list(dict1.values())


def get_disjunct_info(conjuncts, def_info, sentence):
    list1 = [None] * 15
    if sentence[7] == 'xf':
        list1[2] = sentence[5]
    else:
        num = conjuncts[0][6]
        list3 = num.split(".")
        del list3[-1]
        parent_num = ".".join(list3)
        for i in range(len(def_info[2]) - 1, -1, -1):
            if def_info[2][i] == parent_num:
                greek_sent = def_info[6][i]
                list1[2] = greek_sent
                break

    list1[5] = conjuncts

    return list1


def conjunctive_disjunct(sentences, sets_of_conditions):
    for i in range(10, 100):
        if sentences[i][7][-1] == "b":
            # if we should get sentences of the form (p & q) = (r & s & (t v u))
            # that is to say a conjunction on the left of = then this will be revised
            sets_of_conditions.insert(0, [sentences[i][6]])
            j = i
            break
    i = 10
    while sentences[i] != None:
        if i != j:
            if sentences[i][7][-2:] == 'cf' and sentences[i][7][-3:] != 'xcf':
                for set1 in sets_of_conditions:
                    list2 = set1[0].split(".")
                    if list2[1] == "2":
                        set1.append(sentences[i][6])
        i += 1


def get_original_list(list4, original_list):
    parent_num = list4[0]
    if len(original_list) == 1:
        return 0
    else:
        for i in range(1, len(original_list)):
            if original_list[i][10][6][0] == parent_num:
                return i


def link_sets_to_sentences(set_of_sentences, total_sets, embed):
    i = 10
    while set_of_sentences[i] != None:
        k = 50 if embed else 46
        for j, lst in enumerate(total_sets):
            for m, lst2 in enumerate(lst):
                if set_of_sentences[i][6] in lst2:
                    set_of_sentences[i][k] = lst2
                    k += 1
                    set_of_sentences[i][k] = str(j) + str(m)
                    k += 1
        i += 1


def cut_def_info(new_def_info, num_period, father):
    # adjustments to def info affect this function
    delete_this = []
    for m, num in enumerate(new_def_info[2]):
        if not num.startswith(father):
            delete_this.append(new_def_info[6][m])

    n = 0
    while n < len(new_def_info[6]):
        if new_def_info[6][n] in delete_this:
            del new_def_info[1][n]
            del new_def_info[2][n]
            del new_def_info[3][n]
            del new_def_info[4][n]
            del new_def_info[6][n]
        else:
            n += 1

    for j, num in enumerate(new_def_info[2]):
        list2 = num.split(".")
        m = 0
        while m < num_period:
            del new_def_info[1][j][0]
            del list2[0]
            m += 1
        list2[0] = '1'
        new_def_info[1][j][0] = "1"
        new_def_info[2][j] = ".".join(list2)
        new_def_info[4][j][0] = ".".join(list2)
    return


def get_ante_n_consq(def_info, real_new_sent):
    if def_info[4][0][1] in [conditional, iff]:
        for i, num in enumerate(def_info[2]):
            if num.count(".") == 1:
                list1 = num.split(".")
                if list1[1] == "1":
                    real_new_sent[7] = def_info[6][i]
                else:
                    real_new_sent[8] = def_info[6][i]


def embedded_hypothetical_sentences(def_info, sentences, definiendum):
    if definiendum == 'OFW':
        nn = 2
    dict1 = {xorr: "x", conditional: "c", iff: "e", idisj: "d"}
    original_list = dictionary[9].get(definiendum)
    j = 0 if len(def_info) == 1 else 1
    for k in range(j, len(def_info)):
        set1 = def_info[k]
        for i, lst in enumerate(set1[4]):
            if set1[2][i].count(".") in [1, 2] and lst[1] in [conditional, iff, xorr, idisj]:

                new_def_info = copy.deepcopy(def_info[k])
                num = set1[2][i]
                list4 = num.split(".")
                cut_def_info(new_def_info, set1[2][i].count("."), num)
                orig_num = get_original_list(list4, original_list)
                real_new_sent = [None] * 100
                real_new_sent[2] = set1[6][i]
                real_new_sent[79] = []
                get_ante_n_consq(new_def_info, real_new_sent)
                definiendum2 = build_embed_sent(definiendum, k, num, real_new_sent, sentences)
                build_greek_num_dict(real_new_sent, new_def_info)
                sent_kind = get_sent_kind([new_def_info])
                get_sets_of_conditions([new_def_info], definiendum2, [real_new_sent], sent_kind, False, True)

                if lst[1] == xorr and definiendum != 'LFT':
                    exclusive_disjunct([real_new_sent], def_info)

                if original_list[orig_num][84] == None:
                    original_list[orig_num][84] = [real_new_sent]
                else:
                    original_list[orig_num][84].append(real_new_sent)

                real_new_sent[85] = dict1.get(lst[1])
                dictionary[9].update({definiendum2: [real_new_sent]})


def build_embed_sent(definiendum, k, num, real_new_sent, sentences):
    n = 9
    m = 10
    num = num + "."
    reserve_sent_type = []
    definiendum2 = ""
    while sentences[k][m] != None:
        list2 = sentences[k][m]
        if num in list2[6] and num != list2[6]:
            n += 1
            diff = list2[6].count(".") - num.count(".")
            diff += 1
            if definiendum2 == "":
                definiendum2 = sentences[k][m][6] + "," + definiendum
            sent_change = [None] * 60
            sent_change[6] = list2[6]
            sent_change[7] = list2[7][:diff]
            reserve_sent_type.append(list2[7][:diff])
            real_new_sent[n] = list2
        m += 1
    real_new_sent[82] = reserve_sent_type
    real_new_sent[81] = definiendum2
    return definiendum2


def build_greek_num_dict2(sentences, def_info):
    for i, sentence in enumerate(sentences):
        build_greek_num_dict(sentence, def_info[i])

#############################

def is_a_concept(sentences):
    n = 0 if len(sentences) == 1 else 1
    m = 10
    while sentences[n][m] != None:
        if sentences[n][m][6] in ['1.1', '2.1', '3.1']:
            if sentences[n][m][13] == 'I':
                dictionary[15].append(sentences[n][m][4])
            elif sentences[n][m][13] == "=":
                dictionary[6].append(sentences[n][m][4])
            break
        m += 1
    return


def renumber_sentences(definition, definiendum):

    def_info = find_sentences(definition)

    constants = get_abbreviations_from_definition(def_info)

    def_info = eliminate_conjuncts_from_definition(def_info)

    sentences = build_hypo_list(def_info, definiendum, constants)

    build_greek_num_dict2(sentences, def_info)

    definition, ordered = order_sentence(def_info, definition, sentences)

    assert not ordered

    return def_info, sentences, definition


def unembed(def_info, definiendum, red_kind):
    abbrev = []
    ogreek = def_info[5]
    type3 = False
    if red_kind == 6:
        type3 = True

    for sent, greek_sent in zip(def_info[3], def_info[6]):
        if mini_e in sent and len(greek_sent) == 1:
            abbrev.append(greek_sent)





    new_conjunct = " & ".join(abbrev)
    new_conjunct = " & " + new_conjunct

    e = 0
    special = False
    for lst1, lst2, lst3, lst4, lst6 in zip(def_info[1], def_info[2], def_info[3], def_info[4], def_info[6]):
        e += 1

        if e > 1:
            parent = ".".join(lst1[:-1])
            parent_pos = def_info[2].index(parent)
            parent_type = def_info[4][parent_pos][1]

            if parent_type == iff and parent in ['1', '1.1', '1.2']:
                if lst1[-1] == "2":



                    ogreek_definiens = lst6
                    if "&" not in ogreek_definiens:
                        special = True

                    break

    for gsent in abbrev: ogreek = ogreek.replace(" & " + gsent, "")



    if special:
        ngreek_definiens = "(" + ogreek_definiens + new_conjunct + ")"

    elif type3:

        ngreek_definiens = ogreek_definiens[:-2] + new_conjunct + "))"
    else:
        ngreek_definiens = ogreek_definiens[:-1] + new_conjunct + ")"
    ogreek = ogreek.replace(ogreek_definiens, ngreek_definiens)




    for greek_sent, english in zip(def_info[6], def_info[3]):
        ogreek = ogreek.replace(greek_sent, english)

    ogreek = ogreek.strip()
    ogreek = remove_outer_paren(ogreek)


    return find_sentences(ogreek, definiendum), ogreek


def print_new_definitions():
    for word in dictionary[11]:
        definition = dictionary[1].get(word)
        row_num = dictionary[7].get(word)
        if "|" in definition:
            list1 = definition.split("|")
            for i, part in enumerate(list1):
                ws.cell(row=row_num + i, column=6).value = part


        else:

            ws.cell(row=row_num, column=6).value = definition
        ws.cell(row=row_num, column=8).value = "done"
    return


def reduce_definitions():
    debug = False#


    for definiendum, definition in dictionary[1].items():

        pos = dictionary[0].get(definiendum)

        if definiendum == "individual":
            bb = 8

        if pos[1] not in ["s", "d"]:
            bb = 8

            definition = dictionary[1].get(definiendum)

            definition = definition.replace("|", "")

            try:

                def_info = find_sentences(definition, definiendum)



                # if definiendum in dictionary[11]:
                #
                #     embed_type = dictionary[12].get(definiendum)
                #
                #     def_info, definition = unembed(def_info, definiendum, embed_type)
                #
                #     dictionary[1][definiendum] = definition



                constants = get_abbreviations_from_definition(def_info)

                def_info = eliminate_conjuncts_from_definition(def_info)

                n = len(def_info) - 1 if len(def_info) > 1 else len(def_info)

                dictionary[16].update({definiendum: n})

                sentences = build_hypo_list(def_info, definiendum, constants)

                is_a_concept(sentences)

                sent_kind = get_sent_kind(def_info)

                if pos[0] not in ["d", "p"]:

                    definition, ordered = order_sentence(def_info, definition, sentences)

                    if ordered:
                        def_info, sentences, definition = renumber_sentences(definition, definiendum)

                    def_info = get_sets_of_conditions(def_info, definiendum, sentences, sent_kind)

                    get_disjuncts(def_info, sentences)


                else:

                    get_determiner_info(pos, definiendum, sentences)

                sentences[0][80] = definition

                dictionary[9].update({definiendum: sentences})

                embedded_hypothetical_sentences(def_info, sentences, definiendum)


            except ErrorWithCode as e:

                print(e.code)




arguments = sys.argv

if len(arguments) > 1:
    kind = int(arguments[1])
else:
    print ('dictionary was not built')
    kind = 0




if kind == 5:
    print("dictionary built")
    reduce_definitions()

    output = open('z_dict_words.pkl', 'wb')
    pickle.dump(dictionary, output)
    output.close()
    # with open("z_dictionary.json", "w") as fp:
    #     json.dump(dictionary, fp)


elif kind == 6:
    wb4 = load_workbook('/Users/kylefoley/Desktop/inference_engine/dictionary5.xlsx')
    ws = wb4.worksheets[0]
    third_sheet = wb4.worksheets[2]
    print ('dictionary built')
    build_dictionary()
    reduce_definitions()

    output = open('z_dict_words.pkl', 'wb')
    pickle.dump(dictionary, output)
    output.close()





elif kind == 7:
    wb4 = load_workbook('/Users/kylefoley/Desktop/inference_engine/dictionary5.xlsx')
    ws = wb4.worksheets[0]
    dictionary = build_dictionary()
    for word in dictionary[11]:

        definition = dictionary[1].get(word)
        definition = adjust_definition(word, definition, dictionary)
        dictionary[1][word] = definition

    print_new_definitions()
    wb4.save('/Users/kylefoley/Desktop/inference_engine/dictionary5.xlsx')
























