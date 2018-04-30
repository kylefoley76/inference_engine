import copy
import operator

try:
    from settings import *
    from general_functions import *
except:
    from .settings import *
    from .general_functions import *
#
# from settings import *
# from general_functions import *


premise = False
def_info = []
definition = ""
sentences = []
set_sentences = []
main_dict = {}
mixed_dict = {}
sent_types = {}
families = {}
set1 = []


def is_ordered():
    for k, v in main_dict.items():
        if not value_is_fixed(v):
            return False
    return True


def order_conn_pairs(set1):
    for k, v in main_dict.items():
        if len(v) == 2:
            sent1 = sentences[set1[7].get(set1[6][v[0]])]
            sent2 = sentences[set1[7].get(set1[6][v[1]])]
            if sent1[7][0] == 'a':
                assert sent2[7][0] == 'q'
                main_dict[k] = [[v[0]], [v[1]]]
            elif sent1[7][0] == 'q':
                print("it might be impossible for this to happen")
                assert sent2[7][0] == 'a'
                main_dict[k] = [[v[1]], [v[0]]]
            elif sent1[7][0] in ['b', 'f']:
                if sent1[13] == 'W':
                    main_dict[k] = [[v[0]], [v[1]]]
                elif sent2[13] == 'W':
                    main_dict[k] = [[v[1]], [v[0]]]


def value_is_fixed(v):
    if len(v) > 1:
        if isinstance(v[0], int):
            return False
        elif not all(len(i) == 1 for i in v):
            return False
    return True


# bbb
def order_by_conn_type():
    conn_order = {"": 0, xorr: 1, idisj: 2, conditional: 2, iff: 3}
    for k, v in main_dict.items():
        if len(v) > 1:
            if k == "1.2.3.1.4.2":
                bb = 8
            temp_dict = {}
            for sent in v:
                heir_lst = set1[1][sent]
                parent = ".".join(heir_lst[:-1])
                parent_pos = set1[2].index(parent)
                parent_type = set1[4][parent_pos][1]
                if parent_type == "&":
                    sent_type = sent_types.get(sent)
                    conn_value = conn_order.get(sent_type)
                    temp_dict.setdefault(conn_value, []).append(sent)
                else:
                    break

            if len(temp_dict.keys()) > 1:
                temp_dict = sorted(temp_dict.items())
                list1 = []
                for lst in temp_dict:
                    list1.append(lst[1])
                main_dict[k] = list1

    return


def order_biconditionals():
    for k, v in main_dict.items():
        if isinstance(v[0], int) and len(v) == 2:

            heir_lst = set1[1][v[0]]
            parent = ".".join(heir_lst[:-1])
            parent_pos = set1[2].index(parent)
            parent_type = set1[4][parent_pos][1]

            if parent_type == iff:

                if len(set1[6][v[0]]) < len(set1[6][v[1]]):
                    main_dict[k] = [[v[0]], [v[1]]]
                elif len(set1[6][v[0]]) > len(set1[6][v[1]]):
                    main_dict[k] = [[v[1]], [v[0]]]
                elif len(set1[6][v[0]]) == 1:
                    sent1 = sentences[set1[7].get(set1[6][v[0]])]
                    sent2 = sentences[set1[7].get(set1[6][v[1]])]
                    if sent1[13] == "W" and sent2[13] != "W":
                        main_dict[k] = [[v[0]], [v[1]]]
                    elif sent2[13] == "W" and sent1[13] != "W":
                        main_dict[k] = [[v[1]], [v[0]]]
                    else:
                        if ord(sent1[13][0]) > ord(sent2[13][0]):
                            main_dict[k] = [[v[0]], [v[1]]]
                        elif ord(sent1[13][0]) < ord(sent2[13][0]):
                            main_dict[k] = [[v[1]], [v[0]]]

                else:
                    pass
                    # raise Exception('you havent done this yet')

            elif parent_type == conditional:
                main_dict[k] = [[v[0]], [v[1]]]
    return


def order_sets_of_biconditionals():
    for k, v in main_dict.items():
        if isinstance(v[0], list) and len(v) > 1:
            lst_counter = 0
            while lst_counter < len(v):
                lst = v[lst_counter]
                if len(lst) > 1:
                    num = lst[0]
                    if def_info[0][4][num][1] in [conditional, iff]:
                        lst_counter = order_sets_of_biconditionals2(lst, k, v, lst_counter)
                    else:
                        lst_counter += 1
                else:
                    lst_counter += 1

    return


def order_sets_of_biconditionals2(lst, k, v, lst_counter):
    rel_dict = {}
    for num in lst:
        children = families.get(num)
        score = 0
        for child in children:
            greek = def_info[0][6][child]
            if len(greek) == 1:
                g = findposinmd(greek, sentences, 5, 0, True)
                score += ord(sentences[g][13][0])
                if sentences[g][3] == "~":
                    score += 100
        rel_dict.setdefault(score, []).append(num)
    rel_dict = sorted(rel_dict.items())

    if len(rel_dict) > 1:
        new_list = [lst2[1] for lst2 in rel_dict]
        v[lst_counter] = new_list[0]
        del new_list[0]
        e = lst_counter + 1
        for sub_list in new_list:
            lst_counter += 1
            v.insert(e, sub_list)
        main_dict[k] = v

    lst_counter += 1
    return lst_counter


def use_alpha_relations_test(set1):
    for k, v in main_dict.items():
        if not value_is_fixed(v):
            temp_list = [v] if isinstance(v[0], int) else v
            e = 0
            while e < len(temp_list):
                lst = temp_list[e]
                list2 = []
                if len(lst) > 1:
                    rel_dict = {}
                    for num in lst:
                        if sent_types.get(num) == "":
                            sent = sentences[set1[7].get(set1[6][num])]
                            str1 = "".join(sent[58])
                            rel_dict.setdefault(str1, []).append(num)
                    if rel_dict != {}:
                        rel_dict = sorted(rel_dict.items())
                        list1 = []
                        for lst in rel_dict:
                            list1.append(lst[1])
                        list2.append(copy.deepcopy(list1))

                    if len(rel_dict) > 1:

                        f = e
                        del temp_list[e]
                        f -= 1
                        for lst in list2:
                            for sub_list in reversed(lst):
                                temp_list.insert(e, sub_list)
                                f += 1
                        e = f
                e += 1

            main_dict[k] = temp_list

    return


# sent_kinds

# first letter represents whether the whole is bicond = b, cond = c, disj = d
# second letter represents whether the antecedent is conj = &, cond = c, bicond, single = s
# third letter represents whether the consequent is bicond = b, cond = c, disj = d, cong = &, single = s
# if third letter is t then the consequent must be distributed


def get_conn_conjuncts(conn_conjuncts):
    for side in ["1", "2"]:
        e = -1
        for lst, sent, esent, fam_num in zip(set1[4], set1[6], set1[3], set1[1]):
            e += 1
            if e > 0 and fam_num[1] == side:
                if lst[0].count(".") == 1 and lst[1] == "&":
                    sent_type = 'conjunct'
                elif lst[0].count(".") == 1 and lst[1] in [xorr, idisj]:
                    sent_type = 'disjunct'
                elif lst[0].count(".") == 1 and lst[1] in [conditional, iff, "#"]:
                    conn_conjuncts.append([lst[0], sent, esent])
                    break
                elif lst[0].count(".") > 1:

                    if sent_type == 'conjunct' and lst[0].count(".") == 2 and lst[1] in [conditional, iff]:
                        conn_conjuncts.append([lst[0], sent, esent])
                    elif sent_type == 'conjunct' and lst[0].count(".") > 2:
                        break
                    elif sent_type == 'disjunct' and lst[0].count(".") == 3 and lst[1] in [conditional, iff]:
                        conn_conjuncts.append([lst[0], sent, esent])
                    elif sent_type == 'disjunct' and lst[0].count(".") > 3:
                        break
    return



def order_sentence(def_info2, definition2, reduced_def2, definiendum, premise2=False):
    global sentences, def_info, definition, set1
    global families, set_sentences, mixed_dict, premise
    reduced_def = reduced_def2
    ordered = False
    def_info = def_info2
    definition = definition2
    renumber = [0] * len(def_info)
    if 'concept' + un in definition:
        bb = 8

    premise = premise2
    o = 0
    def_part = []
    for set1, tlist in zip(def_info, reduced_def):
        econd_var = tlist.def_stats.embedded_conditionals
        sentences = tlist.sentences
        conn_conjuncts = []
        if premise:
            conn_conjuncts = [["1", set1[6][0], set1[3][0]]]
        else:
            get_conn_conjuncts(conn_conjuncts)

        if conn_conjuncts != []:
            for z, conn_conjunct2 in enumerate(conn_conjuncts):
                conn_conjunct = conn_conjunct2[0]
                build_main_dict(conn_conjunct, set1)
                if is_ordered() and needs_translation():
                    translate_sentence(conn_conjunct2)
                elif not is_ordered() or needs_translation():
                    mixed_dict = copy.deepcopy(main_dict)
                    families = get_families(set1, "get_conjunctive_families")
                    order_sentence2(definiendum)
                    if needs_translation():
                        swap_sentences(conn_conjunct2, o)
                        ordered = True

            translate_sentence(o)
            def_part.append(def_info[o][5])
            if ordered:
                renumber[o] = def_info[o][5]

        else:
            def_part.append(set1[3][0])
        o += 1

    if ordered:
        if o > 1:
            definition = " & ".join(def_part)
        else:
            definition = def_part[0]

    return definition, ordered, renumber


# if conjunctive then the eldest generation has 3 dots if no sibling, 4 dots if siblings
# so in (p & q) > r, r has not sibling and has 2 dots, but p & q have 3 dots

# if disjunctive then the eldest generation has 2 dots if no siblings, 3 dots if siblings

def build_main_dict(conn_conjunct, set1):
    global main_dict, sent_types
    main_dict = {}
    sent_types = {}
    for e, lst in enumerate(set1[4]):
        if e == 30:
            bb = 8
        if (not premise and lst[0].count(".") > 1) or (premise and lst[0].count(".") > 0):
            parent = set1[1][e]
            tparent = ".".join(parent[:-1])
            if tparent.startswith(conn_conjunct):
                sent_types.update({e: lst[1]})
                main_dict.setdefault(tparent, []).append(e)
            elif premise:
                sent_types.update({e: lst[1]})
                main_dict.setdefault(tparent, []).append(e)


def order_sentence2(definiendum):
    fixed_abbrev = []
    order_by_conn_type()
    if is_ordered(): return
    order_biconditionals()
    if is_ordered(): return
    order_sets_of_biconditionals()
    if is_ordered(): return
    use_alpha_relations_test(set1)
    if is_ordered(): return
    unfixed_children, unfixed_families = all_children_are_fixed()
    get_fixed_abbreviations(families, unfixed_children, fixed_abbrev)
    use_alpha_abbrev_test(fixed_abbrev, unfixed_children, families, definiendum, unfixed_families)


def get_families(set1, str1=""):
    if str1 == "get_conjunctive_families":
        connects = [iff, conditional, xorr, idisj, "&"]
    else:
        connects = [iff, conditional, xorr, idisj]
    families = {}
    for e, lst in enumerate(set1[4]):
        if lst[1] in connects:
            heir_num = lst[0]
            for g in range(e + 1, len(set1[4])):
                if set1[4][g][0].startswith(heir_num + ".") and set1[4][g][1] == "":
                    families.setdefault(e, []).append(g)

    return families


def all_kids_are_fixed(families, list1, unfixed_children):
    for num in list1:
        children = families.get(num)
        if children == None:
            return True
        else:
            for child in children:
                if child in unfixed_children:
                    return False
    return True


def all_children_are_fixed():
    unfixed_children = []
    unfixed_families = {}
    j = -1
    for k, v in main_dict.items():
        j += 1
        if j > 0:
            if isinstance(v[0], list):
                for family in v:
                    if len(family) > 1:
                        unfixed_children += family
                        if j not in unfixed_families:
                            unfixed_families.update({k: v})

    return unfixed_children, unfixed_families


def get_fixed_abbreviations(families, unfixed_children, fixed_abbrev):
    found = False
    for k, v in main_dict.items():
        list1 = [v] if isinstance(v[0], int) else v
        for lst in list1:
            if len(lst) == 1:
                children = families.get(lst[0])
                if children == None:
                    sent = sentences[set1[7].get(set1[6][lst[0]])]
                    get_fixed_abbreviations2(fixed_abbrev, sent)
                    found = True
                else:
                    for child in children:
                        if child in unfixed_children:
                            if found:
                                return
                            else:
                                break
                    else:
                        for child in children:
                            sent = sentences[set1[7].get(set1[6][child])]
                            get_fixed_abbreviations2(fixed_abbrev, sent)
                            found = True

            elif found:
                return
            else:
                break

    return


def get_fixed_abbreviations2(fixed_abbrev, sent):
    for x in sent[42]:
        if sent[x] not in fixed_abbrev:
            fixed_abbrev.append(sent[x])


def get_fixed_abbreviations3(list1, fixed_abbrev, families):
    for num in list1:
        if num[0] not in families.keys():
            list2 = [num[0]]
        else:
            list2 = families.get(num[0])
        for nnum in list2:
            sent = sentences[set1[7].get(set1[6][nnum])]
            get_fixed_abbreviations2(fixed_abbrev, sent)


def use_alpha_abbrev_test(fixed_abbrev, unfixed_children, families, definiendum, unfixed_families):
    while True:
        ordering_occurred = False
        unfixed_parent_exists = False
        for k, v in main_dict.items():
            for e, lst in enumerate(v):
                if isinstance(lst, list) and len(lst) > 1:
                    list1 = []
                    if all_kids_are_fixed(families, lst, unfixed_children):
                        list1 = use_alpha_abbrev_test2(fixed_abbrev, lst, families)
                    else:
                        unfixed_parent_exists = True
                    if not unfixed_parent_exists and list1 != []:
                        get_fixed_abbreviations3(list1, fixed_abbrev, families)
                    if list1 != []:
                        ordering_occurred = True
                        reformat_list(v, e, list1, unfixed_children)

        if is_ordered():
            return
        elif not ordering_occurred:
            # print (f"you failed to order {definiendum}")
            # raise Exception('you failed to order ' + definition)
            return
    return


def use_alpha_abbrev_test2(fixed_abbrev, lst, families):
    dict2 = {}
    backup_dict = {}
    temp_dict = {}

    for sent_num in lst:
        if set1[4][sent_num][1] != "":
            list2 = families.get(sent_num)
        else:
            list2 = [sent_num]

        backup_score, score = get_score(fixed_abbrev, list2)
        backup_dict.setdefault(backup_score, []).append(sent_num)
        dict2.setdefault(score, []).append(sent_num)

    if len(dict2.keys()) == 1 and len(backup_dict.keys()) == 1:
        return use_neg_test(lst)

    dict2 = sorted(dict2.items())
    backup_dict = sorted(backup_dict.items())

    if all(len(i[1]) == 1 for i in dict2):
        temp_dict = dict2
    elif all(len(i[1]) == 1 for i in backup_dict):
        temp_dict = backup_dict

    list1 = []
    for lst in temp_dict: list1.append(lst[1])

    return list1


def use_neg_test(lst):
    if len(lst) == 2:
        if lst[0] in families.keys():
            list1 = families.get(lst[0])
        else:
            list1 = [lst[0]]
        if lst[1] in families.keys():
            list2 = families.get(lst[1])
        else:
            list2 = [lst[1]]

        for sent_num in list1:
            score1 = 0
            if sent_num not in families.keys():
                sent = set1[7].get(set1[6][sent_num])
                if sentences[sent][3] == "":
                    score1 += 1
        for sent_num in list2:
            score2 = 0
            if sent_num not in families.keys():
                sent = set1[7].get(set1[6][sent_num])
                if sentences[sent][3] == "":
                    score2 += 1

        if score1 > score2:
            return [[lst[0]], [lst[1]]]
        elif score1 < score2:
            return [[lst[0]], [lst[1]]]

    return []


def get_score(fixed_abbrev, list2):
    score = 0
    back_up_score = 0
    for num in list2:
        sent = sentences[set1[7].get(set1[6][num])]
        for pos in sent[42]:
            var = sent[pos]
            if var in fixed_abbrev:
                if score == 0:
                    score = fixed_abbrev.index(var) + 1
                back_up_score += fixed_abbrev.index(var) + 1

    return back_up_score, score


def reformat_list(v, e, list1, unfixed_children):
    del v[e]
    list2 = copy.deepcopy(list1)
    for num in reversed(list2):
        if num[0] in unfixed_children: unfixed_children.remove(num[0])
        v.insert(e, num)


def needs_translation():
    for k, v in main_dict.items():
        old_num = 0
        for lst in v:
            if len(v) > 1:
                num = lst[0]
                if num < old_num:
                    return True
                old_num = num

    return False


def swap_sentences(conn_conjunct2, o):
    current_sent = conn_conjunct2[1]

    old_fvalues = list(mixed_dict.values())
    new_values = list(main_dict.values())
    new_fvalues = []
    if o > 0:
        original_greek = set1[5]

    for lst in new_values:
        if len(lst) > 1:
            list1 = []
            for sent in lst:
                list1.append(sent[0])
            new_fvalues.append(copy.deepcopy(list1))
        else:
            new_fvalues.append([])

    var = [chr(97 + x) for x in range(25)]
    for new, old in zip(new_fvalues, old_fvalues):
        if new != []:
            greek_english = {}
            english_greek = {}
            j = -1
            for nnum, onum in zip(new, old):
                j += 1
                old_greek = set1[6][onum]
                new_greek = set1[6][nnum]
                english = var[j]
                greek_english.update({old_greek: english})
                english_greek.update({english: new_greek})

            for k, v in greek_english.items():
                def_info[0][5] = def_info[0][5].replace(k, v)

                # set1[5] = set1[5].replace(k, v)
                current_sent = current_sent.replace(k, v)
            for k, v in english_greek.items():
                if k == 'h':
                    bb = 8
                def_info[0][5] = def_info[0][5].replace(k, v)
                # set1[5] = set1[5].replace(k, v)
                current_sent = current_sent.replace(k, v)

    old_sent = conn_conjunct2[1]
    for greek in def_info[o][6]:
        if greek == old_sent:
            def_info[o][5] = def_info[o][5].replace(greek, current_sent)
    for english, greek in def_info[o][10].items():
        def_info[o][5] = def_info[o][5].replace(greek, english)

    return




def translate_sentence(o):
    for greek, english in zip(def_info[o][6], def_info[o][3]):
        if len(greek) == 1:
            def_info[o][5] = def_info[o][5].replace(greek, english)
    for english, greek in def_info[o][10].items():
        def_info[o][5] = def_info[o][5].replace(greek, english)

    return


