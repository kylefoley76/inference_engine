import copy
from settings_old import *




################ group: naming sentences

def build_sent_pos(sent):
    list1 = list(filter(lambda x: sent[x] != "~" and sent[x] != "", sent[54]))
    return nbuild_sent2(sent, sent, list1)


def name_and_build(output, list1):
    if list1[46] == 'do not rename': return
    list1[1] = build_sent_pos(list1)
    list1[2] = name_sent(list1[1], output[8])
    output[9][list1[2]] = list1[1]
    list1[0] = list1[3] + list1[1]


def direct_equivalence(output, ant_sent, ant_sentp, sent, rule):
    name_and_build(output, sent)
    sent1 = build_connection(ant_sent, iff, sent[0])
    sent1p = build_connection(ant_sentp, iff, sent[3] + sent[2])
    add_to_tsent(output[0], sent1, sent1p, "", rule)
    sent[44] = get_sn(output[0])


def svo_sent(output, subject, relation, object, tvalue=""):
    sent1 = [None] * 60
    sent1[3] = tvalue
    sent1[10], sent1[13], sent1[14] = subject, relation, object
    sent1[54] = [10,13,14]
    sent1[42] = [10,14]
    sent1[45] = []
    name_and_build(output, sent1)
    sent1[46] = "do not rename"

    return sent1

#####################group: index functions

def find_counterpart_inlist(str1, list1, i, j):
    # this function takes a string, matches it to an element in the first dimension
    # of the list, then returns the matching second element

    for d in range(len(list1)):
        if str1 == list1[d][i]:
            str2 = list1[d][j]
            return str2
    return None


def find_2posinlist(str1, str2, list1, p, q):
    for i, lst in enumerate(list1):
        if str1 == lst[p] and str2 == lst[q]:
            return i

    return -1


def findposinmd(str1, list1, p, start = 0, no_error = False):
    # this determines the position of an element in a multidimensional list

    for i in range(start, len(list1)):
        try:
            if list1[i][p] == str1:
                return i
        except:
            pass
    if no_error: raise Exception

    return -1


def findposinmdlistint(i, list1, p):
    for j in range(len(list1)):
        if list1[j][p] == i:
            return j
    else:
        return -1


def find_sibling_int(i, list1, p, q):
    for j in range(len(list1)):
        if list1[j][p] == i:
            return list1[j][q]
    else:
        return -1


############### the following functions are related to adding to the total sent
###############  and finding a contradiction


def check_consistency(output):
    new_sent_abbr = output[0][-1][2]
    tvalue = output[0][-1][3]
    for i in range(len(output[0]) - 2, -1, -1):
        if output[0][i][2] == new_sent_abbr and output[0][i][3] != tvalue:
            build_contradiction(output, i)
            return False

    for lst in output[11]:
        for sent in lst[0]:
            if sent[0] == new_sent_abbr and sent[1] == tvalue:
                del sent[0]
                del sent[1]
                lst[3].append(output[0][-1][0])
                if lst[0] == []:
                    build_contradictory_conjunction(output, lst[3])
                    return False

    if output[12] != []:
        if len(new_sent_abbr) < 3:
            neg_excl_disj_elim(new_sent_abbr, tvalue, output, len(output[0]) - 1, -1, get_sn(output[0]))

            return False

    return True


def neg_excl_disj_elim(det_abb, det_abb_tv, output, tot_sent_num, ex0, anc1):
    while ex0 < len(output[12]) - 1:
        ex0 += 1
        excl_disj = output[12][ex0]
        ex1 = -1
        while ex1 < len(excl_disj) - 1:
            ex1 += 1
            ex2 = -1
            while ex2 < len(excl_disj[ex1][2]) - 1:
                ex2 += 1
                dsent = excl_disj[ex1][2][ex2]
                if det_abb == dsent[1] and det_abb_tv != dsent[2]:
                    consistent = neg_excl_disj_elim2(ex0, ex1, tot_sent_num, output, anc1)

                    ex1 -= 1
                    return consistent


def neg_excl_disj_elim2(ex0, delex, tot_sent_num, output, anc3):
    excl_disj = output[12][ex0]
    anc1 = output[0][tot_sent_num][0]
    connector = " " + xorr + " "
    if len(excl_disj) > 2:
        list1 = []
        list1a = []
        anc2 = excl_disj[0][3]
        for d, lst in enumerate(excl_disj):
            if d != delex:
                list1.append(lst[0])
                list1a.append(lst[1])
        nat_sent = connector.join(list1)
        abb_sent = connector.join(list1a)
        del output[12][ex0][delex]
        add_to_tsent(output[0], nat_sent, abb_sent, "", xorr + "E", anc1, anc2)
    else:
        b = 1 if delex == 0 else 0
        anc1 = tot_sent_num
        anc2 = excl_disj[0][3]
        if len(excl_disj[b][2]) == 1:
            add_to_tsent(output[0], excl_disj[b][2][0][0], excl_disj[b][2][0][1], excl_disj[b][2][0][2],
                         xorr + "E", anc1, anc2)
            consistent = check_consistency(output)
            if not consistent: return
        else:
            add_to_tsent(output[0], excl_disj[b][0], excl_disj[b][1], "", xorr + "E", anc1, anc2)
            qn = anc3
            for lst in excl_disj[b][2]:
                add_to_tsent(output[0], lst[0], lst[1], lst[2], "&E", qn)
                consistent = check_consistency(output)
                if not consistent:
                    return False
        del output[12][ex0]

    return True


def build_contradictory_conjunction(output, list1):
    list3 = tuple(str(output[0][k][0]) for k in list1)
    anc1 = ",".join(list3)
    list2 = [output[0][j][3] + output[0][j][1] for j in list1]
    list2p = [output[0][j][3] + output[0][j][2] for j in list1]
    conjunction = "(" + " & ".join(list2) + ")"
    conjunctionp = "(" + " & ".join(list2p) + ")"
    add_to_tsent(output[0], conjunction, conjunctionp, "", "&I", anc1)
    build_contradiction(output, -2)


def build_contradiction(output, i):
    str1 = output[0][-1][1] + " & ~" + output[0][i][1]
    str2 = output[0][-1][2] + " & ~" + output[0][i][2]
    add_to_tsent(output[0], str1, str2, "", "&I", output[0][-1][0], output[0][i][0])
    add_to_tsent(output[0], bottom, bottom, "", bottom + "I", 0)


def get_sn(list1):
    if len(list1) > 0:
        if isinstance(list1[-1][0], int):
            return list1[-1][0]
        else:
            for lst in reversed(list1):
                if isinstance(lst[0], int):
                    return lst[0]
    else:
        return 0


def add_to_tsent(tsent, str1, str2="", tvalue="", rule="", anc1="", anc2="", anc3="", anc4=""):
    if anc1 == 0: anc1 = get_sn(tsent)
    if anc2 == 0: anc2 = get_sn(tsent)
    list2 = [""] * 9
    list2[0] = get_sn(tsent) + 1
    list2[1] = str1
    list2[2] = str2
    list2[3] = tvalue
    list2[4] = rule
    list2[5] = anc1
    list2[6] = anc2
    list2[7] = anc3
    list2[8] = anc4
    tsent.append(list2)



######################group: miscellanious functions

class ErrorWithCode(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(self.code)


def mainconn(str1):
    ostring = copy.copy(str1)
    if one_sentence(str1):
        return ["", 0]
    if str1.find("&") < -1 and str1.find(idisj) < -1 and str1.find(iff) < -1 and str1.find(conditional) < -1 and \
                    str1.find(implies) < -1 and str1.find(nonseq) < -1 and str1.find(xorr) < -1:
        return ["", 0]

    str3 = str1
    bool1 = False

    if str1[0] == "~":
        str1 = str1[1:]
        bool1 = True

    j = 0
    bool2 = False
    for i in range(0, len(str1)):
        str2 = str1[i:i + 1]
        if str2 == "(":
            j += 1
        elif str2 == ")":
            j -= 1

        if j == 0 and i + 1 != len(str1):
            break
        elif j == 0 and i + 1 == len(str1):
            str1 = str1[1:len(str1) - 1]
            bool2 = True

    j = -1
    for i in range(0, len(str1)):
        str2 = str1[i:i + 1]
        if str2 == conditional:
            f = -1
        if str2 == idisj or str2 == "&" or str2 == iff or str2 == implies or \
                        str2 == nonseq or str2 == conditional or str2 == xorr:
            if str3 != str2 and str3 != "":
                j = j + 1

            str3 = str2

    if j == -1:
        i = ostring.find(str3)
        return [str3, i]
    k = -1
    j = -1
    while True:
        k += 1
        if k > 150:
            break
        for i in range(0, len(str1)):
            str2 = str1[i:i + 1]

            if str2 == "(":
                j += 1
            elif str2 == ")":
                j -= 1

            if j == -1 and (str2 == idisj or str2 == "&" or str2 == iff or str2 == implies
                            or str2 == nonseq or str2 == conditional or str2 == xorr):
                if bool1 and bool2:
                    return [str2, i + 2]
                elif bool2 or bool1:
                    return [str2, i + 1]
                else:
                    return [str2, i]
        else:
            str1 = str1[1:-1]


def insert_new_word(new_word_pos, old_word_pos):
    list1 = []
    for idx in old_word_pos:
        if idx > 164:
            list1.append(list1[-1] + .01)
        else:
            list1.append(slot_order.index(idx))
    new_word_index = slot_order.index(new_word_pos)
    for i, num in enumerate(list1):
        if new_word_index < num:
            old_word_pos.insert(i, new_word_pos)
            return old_word_pos


def remove_duplicates(list1, i):
    list2 = []
    j = -1
    while j < len(list1) - 1:
        j += 1
        if list1[j][i] in list2:
            del list1[j]
            j -= 1
        else:
            list2.append(list1[j][i])

    return list1


def isvariable(str3, kind=""):
    bool2 = True
    if str3 == None or str3 == "":
        return False

    if str3 == 'a':
        return False
    elif str3 == 'i' and kind == "":
        return False
    elif str3 == "i":
        return True

    if str3 != "":
        str3 = str3.replace(l1, "")
        str3 = str3.replace(l2, "")
        str3 = str3.replace(l3, "")
        str3 = str3.replace(neg, "")
        if len(str3) == 1 and str3.islower():
            bool2 = True
        else:
            bool2 = False

    return bool2


def is_standard(sent):
    for num in sent[54]:
        if num not in standard_nouns + relational_positions + negative_positions:
            return "not standard"
    if sent[20] in ["AS", 'OFX'] or sent[10] == 'there':
        return "not standard"

    return "standard"



def determine_constants(dict1, sentence_slots):
    c_constants = [] # connected constants

    for num in sentence_slots[54]:

        if num in relational_positions:
            if sentence_slots[num] in ["I", "J", "V"]:
                word = dict1.get(sentence_slots[14])
                if word != None:
                    c_constants.append(word)
                else:
                    c_constants.append(sentence_slots[num])

            elif sentence_slots[13] == '=' and sentence_slots[14] in dict1.values():
                c_constants.append(sentence_slots[14])
            else:
                c_constants.append(sentence_slots[num])

        elif num in negative_positions:
            c_constants.append(sentence_slots[num])

    neg = " ".join(c_constants)
    if sentence_slots[3] == '~' and "~" not in neg:
        neg = neg.strip()
        neg = "~ " + neg

    return neg



def universal_negations(sentences, output, definiendum=""):
    if len(sentences) < 3:
        sentences = sentences[0]
    if definiendum == "": definiendum = 'thing'
    is_a_universal_sentence = False
    instantiates_thing = get_key(output[6], 'thing')
    if not_blank(instantiates_thing):
        m = 10
        while sentences[m] != None:
            if sentences[m][14] == instantiates_thing:
                is_a_universal_sentence = True
                break
            m += 1
        if is_a_universal_sentence:
            m = 10
            while sentences[m] != None:
                if "q" in sentences[m][7]:
                    list1 = []
                    sent_constant = sentences[m][58]
                    if "~" not in sentences[m][58]:
                        tvalue = "~ "
                    else:
                        sent_constant = sent_constant.replace("~ ","")
                        tvalue = ""

                    list1.append([tvalue + sent_constant, [m]])
                    output[2].append([definiendum, [list1]])
                m += 1

            output[15].update({'thing': [sentences]})
    return is_a_universal_sentence


def remove_outer_paren(str1, bool1=False):
    if str1 == "":
        return ""
    elif str1.count(")") == 0:
        if not bool1:
            return str1
        else:
            return False

    j = 0
    # on very rare occasions we will encounter strings of the following form ((p))
    if str1[0] != "(" and str1[-1] != ")":
        if not bool1:
            return str1
        else:
            return True
    if str1[:2] == "((" and str1[-2:] == "))":
        d = 2
    else:
        d = 1

    for k in range(0, d):
        for i in range(0, len(str1)):
            str2 = str1[i:i + 1]
            if str2 == "(":
                j += 1
            elif str2 == ")":
                j -= 1
            if j == 0 and i + 1 != len(str1):
                break
            elif j == 0 and i + 1 == len(str1):
                str1 = str1[1:len(str1) - 1]
                if bool1:
                    return True
    if not bool1:
        return str1
    else:
        return False


def get_key(dict1, val):
    for k, v in dict1.items():
        if v == val:
            return k
    else:
        return None


def list_set_default(list1, entity):

    try:
        g = findposinmd(entity[0], list1, 0)
        if g > -1:
            list1[g][1].append(entity[1])
        else:
            list1.append([entity[0], [entity[1]]])
    except:
        pass


def build_greek_num_dict(sentences, sub_def_info):
    greek_num_dict = {}
    m = 10
    while sentences[m] != None:
        if m > 53:
            bb = 8
        greek_num_dict.update({sentences[m][5]:m})
        m += 1
    sub_def_info[7] = greek_num_dict


def change_constants(already_used_map, output, from_definitions):
    for k, v in from_definitions.items():
        new_var = get_key(output[6], v)
        if new_var != None:
            already_used_map.update({k : new_var})
        else:
            old_value = v
            if k not in output[14]:
                v = output[14][0]
                del output[14][0]
                already_used_map.update({k: v})
                output[6].update({v: old_value})
            else:
                output[14].remove(k)
                already_used_map.update({k: k})
                output[6].update({k: old_value})
    return
