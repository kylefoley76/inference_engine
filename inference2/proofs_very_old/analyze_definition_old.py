from settings_old import *
from put_words_in_slots_old import categorize_words
from analyze_sentence_old import period_elimination
from general_functions_old import build_greek_num_dict
import copy

def build_hypo_list(def_info, definiendum="", abbreviations=[]):
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
                if one_sentence(sent) and "~" in sent:
                    tvalue = "~"
                    sent = sent[1:]
                    tvalue2 = "~ "

                sent = split_sentences(sent)
                sent = categorize_words(abbreviations, sent, True)
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


def embedded_hypothetical_sentences(def_info, sentences, dictionary, definiendum):
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

