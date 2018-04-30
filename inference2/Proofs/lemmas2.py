from collections import defaultdict
import itertools
from itertools import combinations
import copy
import json, operator, collections
from openpyxl import load_workbook
from classes import implications, truth_table, truth_table2, truth_table_equiv
import time
from random import *

try:
    from settings import *
    from general_functions import *
    from classes import get_output
    from search_for_instantiation import loop_through_gsent, try_instantiation
    from prepare_for_print import rearrange
except:
    from .settings import *
    from .general_functions import *
    from .classes import get_output
    from .search_for_instantiation import loop_through_gsent, try_instantiation
    from .prepare_for_print import rearrange



def which_var(sentence, var):
    for x in sentence[42]:
        if sentence[x] == var:
            return x
    raise Exception


def fill_truth_values(otv, tv):
    done = False
    if tv.pp == "":
        tv = otv

    else:
        if otv.pp == True:
            tv.pp = True
        elif tv.pp != True and otv.pp == False:
            tv.pp = False

        if otv.pn == True:
            tv.pn = True
        elif tv.pn != True and otv.pn == False:
            tv.pn = False

        if otv.np == True:
            tv.np = True
        elif tv.np != True and otv.np == False:
            tv.np = False

        if tv.pp == True and tv.pn == True and tv.np == True:
            done = True

    return tv, done








def set_swap(set1, word, concepts):
    if word not in concepts:
        return False
    for word2 in set1:
        if word2 not in concepts:
            return False
    return True








def build_read_entail(ant_pos, ant_neg, con_pos, con_neg, word):
    antnw = ".".join(ant_neg) if ant_neg != set() else "0"
    antpw = ".".join(ant_pos) if ant_pos != set() else "0"
    connw = ".".join(con_neg) if con_neg != set() else "0"
    conpw = ".".join(con_pos) if con_pos != set() else "0"

    dictionary.read_entail.update({word: "|".join([antpw, antnw, conpw, connw])})


def get_reduced_def(word):
    if "," in word:
        e, key, pword = word.split(",")
        rd = dictionary.categorized_sent.get(pword)
        return [rd[int(e)].embeds.get(key)]
    else:
        return dictionary.categorized_sent.get(word)


def get_def_stats(word):
    if "," in word:
        e, key, pword = word.split(",")
        rd = dictionary.categorized_sent.get(pword)
        return rd[int(e)].embeds.get(key).def_stats
    else:
        return dictionary.categorized_sent.get(word)[0].def_stats




def get_lowest_group(groups):
    if len(groups) == 1: return groups[0]
    if groups[0] == 'thing':
        lowest = groups[1]
        if len(groups) == 2:
            return lowest
        else:
            start = 2
    else:
        lowest = groups[0]
        start = 1
    for group in groups[start:]:
        if group != 'thing':
            ancestors = dictionary.ontology[1].get(group)
            if lowest in ancestors:
                lowest = group
    return lowest






def unpack_entailments(by_basicity):
    sorted_dict = sorted(dictionary.variable_entail.items())
    for word, level in by_basicity:
        if level > 1 and word not in dictionary.disjunctive.keys():
            if "," in word:
                bb = 8

            is_relation = True if dictionary.kind.get(word) == 'r' else False
            reduced_def = get_reduced_def(word)
            for cls in reduced_def:
                unpack_entailments2(cls, is_relation, word, sorted_dict)


def unpack_entailments2(cls, is_relation, word, sorted_dict):
    implications = cls.def_stats.entailments
    con_pos = implications.con_pos
    con_pos_by_var = implications.con_pos_by_var
    con_neg_by_var = implications.con_neg_by_var
    con_neg = implications.con_neg
    con_var = implications.con_var
    for k, v in con_var.items():
        for const in v:
            if is_relation and word in const:
                new_nconst = set()
                new_pconst = set()
                st = dictionary.variable_entail.get(const)
                con_pos_by_var.update({k: st[0]})
                con_neg_by_var.update({k: st[1]})

                if st != None:
                    new_pconst = new_pconst | st[0] | {const}
                    new_nconst = new_nconst | st[1]
                else:
                    new_pconst.add(const)
                new_pconst = strip_const(new_pconst, True)
                new_nconst = strip_const(new_nconst, True)
                con_pos = con_pos | new_pconst
                con_neg = con_neg | new_nconst

    return


def strip_const2(const):
    if const in ["Hs", "Ho"]:
        relation = "H"
        relatum = const[-1]
    elif const[0].islower() or hprop(const):
        relation = const
        relatum = "s"
    elif const[0] in ["/", "+", "-", "*"]:
        relatum = const[-1]
        relation = const[0]
    else:
        relation = "".join(re.findall(r'[A-Z]', const))
        relatum = const[-1]
    return relation, relatum


def strip_const(new_const):
    new_const2 = set()
    for const in list(new_const):
        const, _ = strip_const2(const)
        new_const2.add(const)
    return new_const2


def print_rel_err(excel_group, pyth_group, word):
    if excel_group == None: return
    if excel_group == 's being' and pyth_group == 'sentient being':
        return

    if isinstance(pyth_group, set):
        pyth_group = ";".join(pyth_group)
    print (word + ": excel group: " + excel_group + " python group: " + pyth_group)


def match_relatum():
    for predicate, pgroups in dictionary.groups.items():

        if "," not in predicate and predicate not in dictionary.ontology[1].keys():
            if predicate == 'ITo':
                bb = 8
            bare_pred, relatum = strip_const2(predicate)
            relata = dictionary.relata.get(bare_pred)
            if relata != None:
                if relatum == "s":
                    if pgroups != relata.subject:
                        print_rel_err(relata.subject, pgroups, predicate)
                elif relatum == "o":
                    if pgroups != relata.object:
                        print_rel_err(relata.object, pgroups, predicate)
                elif relatum == "b":
                    if pgroups != relata.object2:
                        print_rel_err(relata.object2, pgroups, predicate)
                elif relatum == "c":
                    if pgroups != relata.object3:
                        print_rel_err(relata.object3, pgroups, predicate)
                elif relatum == "d":
                    if pgroups != relata.object4:
                        print_rel_err(relata.object4, pgroups, predicate)
            else:
                print (predicate + " has no group in excel")




def get_complete_entailments(by_basicity):
    sorted_dict = sorted(dictionary.variable_entail.items())

    for word, level in by_basicity:
        if word == 'person':
            bb = 8

        if level > 1 and word not in dictionary.disjunctive.keys():
            kind = dictionary.kind.get(word)
            if kind == 'r':
                def_stats1 = get_def_stats(word)
                arity = def_stats1.arity
                for num in [x[1] for x in arity]:
                    if word not in dictionary.disjunctive.keys():
                        temp_word = word + sent_pos_name[num]
                        get_complete_entailments2(temp_word, sorted_dict, level)
            else:
                get_complete_entailments2(word, sorted_dict, level)

    return


def get_complete_entailments2(temp_word, sorted_dict, level):
    if temp_word == 'ITo':
        bb = 8
    if temp_word in dictionary.disjunctive.keys(): return

    entailments = dictionary.variable_entail.get(temp_word)
    assert entailments != None or "," in temp_word
    if entailments != None:
        compl_entail = entailments[0]
        compl_neg_entail = entailments[1]
        for entailment in list(entailments[0]):
            if dictionary.variable_entail.get(entailment) != None:
                new_entailments = dictionary.variable_entail.get(entailment)
                compl_entail = {entailment} | compl_entail | new_entailments[0]
                compl_neg_entail = compl_neg_entail | new_entailments[1]

        dictionary.variable_entail[temp_word] = [compl_entail, compl_neg_entail, level]


def determine_class2(by_basicity):
    for word, level in by_basicity:
        if word == 'Hrelation':
            bb = 8

        if level > 0 and word not in dictionary.disjunctive.keys() \
                and word not in dictionary.ontology[1].keys():

            kind = dictionary.kind.get(word)
            def_stats1 = get_def_stats(word)
            if kind == 'r':
                if word == 'IT':
                    bb = 8

                for var, num in def_stats1.arity:
                    temp_word = word + sent_pos_name[num]
                    determine_class3(word, var, temp_word)
            else:
                var = def_stats1.arity[0][0]
                determine_class3(word, var, word)

    return


def get_whole_type(word, var, kind):
    default = 'whole' if kind == 'W' else 'thing'

    whole_types = {
        "letter": "word",
        "void": "physical space",
        "point": "region",
        "relatum": "relationship",
        "relation": "relationship",
        "particle": "body",
        "moment": "period",
        "physical object": "body"
    }
    htypes = {
        "body": "sentient being",
        "mind": "sentient being"
    }

    if word == 'LFG':
        bb = 8

    reduced_def = get_reduced_def(word)
    for cls in reduced_def:
        for num in cls.def_stats.flat_con_index:
            if cls.sentences[num][13] == kind and \
                    cls.sentences[num][10] == var:
                counterpart = cls.sentences[num][14]
                break
        else:
            return default

        for idx in cls.def_stats.flat_con_index:
            for idx2 in cls.sentences[idx][42]:
                var2 = cls.sentences[idx][idx2]
                if var2 == counterpart:
                    const = cls.sentences[idx][58]
                    if const[0].isupper() and const != kind:
                        str1 = sent_pos_name.get(idx2)
                        const += str1
                    group = dictionary.groups.get(const, "thing")
                    if group != "thing":
                        if kind == 'W':
                            group = whole_types.get(group)
                        else:
                            group = htypes.get(group)

                        if group != None:
                            return group
    return default


def determine_class3(word, var, temp_word):
    if temp_word == 'MVo':  # pear, HATs
        bb = 8

    current_groups = set()
    entailments = dictionary.variable_entail.get(temp_word)
    if entailments != None:
        group = ""
        for entailment in entailments[0]:
            if entailment == 'Ws':
                group = get_whole_type(word, var, "W")
            elif entailment == 'Hs':
                group = get_whole_type(word, var, "H")

            else:
                group = dictionary.groups.get(entailment, "thing")
            current_groups.add(group)
        if group == "":
            for entailment in entailments[1]:
                group = dictionary.groups.get(entailment, "thing")
                current_groups.add(group)

        if temp_word == 'relationship':
            bb = 8

        if len(current_groups) > 1:
            dictionary.groups[temp_word] = check_self_consistency(current_groups, temp_word)
        elif len(current_groups) == 1:
            dictionary.groups[temp_word] = list(current_groups)[0]

    return



def check_self_consistency(current_groups, temp_word):
    if temp_word == 'KNo':
        bb = 8
    power_set1 = powerset(list(current_groups))
    for lst in power_set1:
        if len(lst) == 2:
            list1 = [lst[0], lst[1]]
            list1.sort()
            pair = (".".join(list1))
            if "thing" not in pair:
                bool1 = dictionary.ontology[2].get(pair)
                if not bool1:
                    raise Exception("the definition of " + temp_word + " is inconsistent")

    return get_lowest_group(list(current_groups))


def consistent_conjunctions(word_list):
    lemmata = {}
    pair_prop = reorder()
    for pair1 in pair_prop:
        test_true_true(lemmata, pair1)

    print (str(len(lemmata)) + " lemmas")
    pkl_file = open('lemmata.pkl', 'wb')
    pickle.dump(lemmata, pkl_file)
    pkl_file.close()

    return len(lemmata)


def test_true_true(lemmata, pair1):
    if pair1[0] == 'LFDs.moment':
        bb = 8

    first = pair1[2]
    second = pair1[3]
    k = pair1[2][0]
    x = pair1[3][0]

    if k in dictionary.disjunctive.keys():
        # the ! means that it is not known yet whether x is disjunctive
        consistent_disjunctions(pair1, lemmata, k, "!" + x)
    elif x in dictionary.disjunctive.keys():
        consistent_disjunctions(pair1, lemmata, x, k)
    else:

        pair2 = pair(first[4], second[4], ".")
        if "Lo" in pair2:
            bb = 8

        if 'thing' in pair2 or first[4] == second[4]:
            truth_value = True
        else:
            truth_value = dictionary.ontology[2].get(pair2)
            assert truth_value != None
        ttable = truth_table()
        if pair1 == 'AGs.mind':
            bb = 8

        if truth_value != "absurd":
            falsify_by_definition(pair1, ttable)
        else:
            ttable.pn = truth_value
            ttable.np = truth_value
            ttable.nn = truth_value

        lemmata.update({pair1[0]: ttable})




def consistent_disjunctions(pair1, lemmata, dword, cword):
    if cword[0] == "!" and cword[1:] in dictionary.disjunctive.keys():
        tv = truth_table()
        lemmata.update({pair1[0]: tv})
        return
    elif cword[0] == "!":
        cword = cword[1:]

    if pair1[0] == "LFs.moment":
        bb = 8

    odword = dword
    var_pos = "s"
    if dword[0].isupper():
        odword = "".join(re.findall(r'[A-Z]', dword))
        var_pos = get_key(sent_pos_name, dword[-1])

    reduced_def = get_word_info(dictionary, odword, "")
    arity = reduced_def[0].def_stats.arity
    for var, num in arity:
        if var_pos == num:
            break

    if cword == 's':
        bb = 8

    tv = consistent_disjunctions2(cword, lemmata, reduced_def, var, dword)

    lemmata.update({pair1[0]: tv})

    if pair1[0] == "LFs.moment":
        print ("LFs.moment")
        print (tv.pp)

    return


def consistent_disjunctions2(cword, lemmata, reduced_def, var, dword):
    tv = truth_table2()
    for num in reduced_def[0].def_stats.flat_con_index:
        const = reduced_def[0].sentences[num][58]
        if const == 'L':
            bb = 8

        skind = dictionary.pos.get(const)
        if skind[0] == 'r':
            var_pos = which_var(reduced_def[0].sentences[num], var)
            str1 = sent_pos_name.get(var_pos)
            new_const = const + str1
            if new_const == cword:
                tv = truth_table_equiv
                break
            else:
                pair1 = pair(new_const, cword, ".")
                otv = lemmata.get(pair1)
                assert otv != None, pair1 + " is not a lemma"
                tv, done = fill_truth_values(otv, tv)
                if done: break
        else:
            pair1 = pair(const, cword, ".")
            otv = lemmata.get(pair1)
            assert otv != None, pair1 + " is not a lemma"
            tv, done = fill_truth_values(otv, tv)
            if done: break
    return tv


def reorder2():
    lst = []
    for k, v in dictionary.variable_entail.items():
        if "," not in k:
            group1 = dictionary.groups.get(k, 'thing')
            lst.append((k, v[0], v[1], v[2], group1))

    pred_list = []
    lst = combinations(lst, 2)
    for pair1 in lst:
        highest = max(pair1[0][3], pair1[1][3])
        pair2 = pair(pair1[0][0], pair1[1][0], ".")
        if pair2.startswith(pair1[0][0]):
            pred_list.append([pair2, highest, pair1[0], pair1[1]])
        else:
            pred_list.append([pair2, highest, pair1[1], pair1[0]])

    return sorted(pred_list, key=operator.itemgetter(1))


def reorder():
    for x, y in dictionary.variable_entail.items():
        if (x[0].isupper() and x[:-1] in dictionary.disjunctive.keys()) or \
                x in dictionary.disjunctive.keys():
            y[2] = (y[2] * 2) - 1
        else:
            y[2] = (y[2] * 2)

    return reorder2()


def falsify_by_definition(pair1, ttable):
    entail2 = [pair1[3][1], pair1[3][2]]
    entail1 = [pair1[2][1], pair1[2][2]]
    if (entail1[0] & entail2[1]) != set() or (entail1[1] & entail2[0]) != set():
        ttable.pp = False
    else:
        ttable.pp = True

    if (entail1[0] - entail2[0]) == set():
        # print (pair1 + " false by definition")
        ttable.pn = False
        ttable.np = False
    elif (entail1[0] - entail2[0]) == set():
        ttable.pn = False
        ttable.np = True
    elif (entail2[0] - entail1[0]) == set():
        ttable.pn = True
        ttable.np = False
    elif (entail2[0] & entail1[0]) == set():
        ttable.pn = True
        ttable.np = True
    elif len(entail2[0] & entail1[0]) > 0:
        ttable.pn = "maybe"
        ttable.np = "maybe"
    else:
        raise Exception

    return