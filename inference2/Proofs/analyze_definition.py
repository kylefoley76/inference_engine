from settings import *
from general_functions import *
from put_words_in_slots import categorize_words
from analyze_sentence import period_elimination, find_sentences
from standard_order import order_sentence
import copy
from classes import *


def is_a_concept(sentences):
    for sentence in sentences:
        if sentence[6] in ['1.1', '1.1.1']:
            if sentence[13] == 'I':
                dictionary[15].append(definiendum)
            elif sentence[13] == '=':
                dictionary[6].append(definiendum)

    return


def get_determiner_info(reduced_def):
    def_stats = reduced_def[0].def_stats
    sentences = reduced_def[0].sentences
    instance_names = []
    for sentence in sentences:
        if sentence[13] == "I":
            instance_names.append(sentence[10])
            def_stats.concept = sentence[14]

    def_stats.instance = instance_names


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
    elif "~(" in sent:
        sent = sent.replace("~(", "~ (")
    elif "=" in sent:
        sent = sent.replace("=", " = ")
    sent = sent.replace("(", "")
    sent = sent.replace(")", "")
    return sent.split(" ")


def get_abbreviations_from_definition(def_info):
    # this function picks out that variables in the id sentences of the
    # definition

    abbreviations = {}
    for i in range(len(def_info[3])):
        if one_sentence(def_info[3][i]) and "=" in def_info[3][i]:
            str1 = def_info[3][i]
            g = str1.find("=")
            var = str1[1:g]
            word = str1[g + 1:-1]
            if isvariable(var):
                if not isvariable(word):
                    abbreviations.update({var: word})

    return abbreviations


def name_conn_sent(output, reduced_def):
    sentences = reduced_def[0].sentences
    greek = reduced_def[0].def_stats.tot_greek_sent
    greek_english_abb = {}
    for sentence in sentences:
        sent_abb = name_sent(sentence[1], output[8])
        sentence[2] = sent_abb
        output[9][sent_abb] = sentence[1]
        greek_english_abb.update({sentence[5]: sentence[3] + sentence[2]})

    for k, v in greek_english_abb.items():
        greek = greek.replace(k, v)
    return greek


def process_sentences(definition, definiendum2, dictionary2, output=[]):
    global premise, embeds, is_embedded, definiendum, dictionary
    is_embedded = False
    premise = True
    definiendum = definiendum2
    dictionary = dictionary2

    if definiendum == 'KN':
        bb = 8

    def_info = find_sentences(definition, definiendum)

    if output == []:
        premise = False
        abbreviations = get_abbreviations_from_definition(def_info)
        if abbreviations != {}:
            dictionary[18].update({definiendum: abbreviations})
    else:
        abbreviations = output[6]

    conjuncts = build_conjuncts(def_info)

    temp_definition = " & ".join(conjuncts) if len(conjuncts) > 1 else conjuncts[0]

    embed = True if len(conjuncts) > 1 else False

    def_info = [find_sentences(conjunct, "", embed) for conjunct in conjuncts]

    if len(conjuncts) > 1 and not premise: dictionary[16].update({definiendum: conjuncts})

    def_info, temp_definition = period_elimination(def_info, temp_definition)

    renumber = [1 for x in range(len(def_info))]

    reduced_def = [[] for x in range(len(def_info))]

    reduced_def = unpack_definition(abbreviations, def_info, renumber, definiendum, reduced_def)

    reduced_def, sent_abb = order_sent(abbreviations, def_info,
                                       definiendum, output, reduced_def, temp_definition)

    if output == []: is_a_concept(reduced_def[0].sentences)

    sent_kind = get_sent_kind(def_info)

    number_embeds(def_info, reduced_def)

    reduced_def = get_sets_of_conditions(def_info, reduced_def, sent_kind)

    if not premise:

        lst2 = [x.sentences for x in reduced_def]
        with open("json_dict/" + definiendum + ".json", "w") as fp:
            json.dump(lst2, fp)
        for x in reduced_def: x.sentences = None

        dictionary[9].update({definiendum: reduced_def})

    if output != []:
        return reduced_def, sent_abb
    else:
        return dictionary


def order_sent(abbreviations, def_info, definiendum, output, reduced_def, temp_definition):
    sent_abb = ""
    if premise: sent_abb = name_conn_sent(output, reduced_def)
    pos = dictionary[0].get(definiendum, "z")
    if pos[0] not in ["d", "p"]:
        _ = order_sentence(def_info, temp_definition, reduced_def, premise)
        temp_definition, ordered, renumber = _
        if ordered:
            if premise:
                sent_abb = name_conn_sent(output, reduced_def)

            renumber_sentences(renumber, def_info)
            reduced_def = unpack_definition(abbreviations, def_info, renumber, definiendum, reduced_def)
    else:
        get_determiner_info(reduced_def)
    return reduced_def, sent_abb


def build_conjuncts(result):
    conjuncts = []
    if result[4][0][1] in [iff, conditional]:
        conjuncts.append(result[3][0])
    else:
        for lst3, lst in zip(result[3], result[4]):
            if lst[0].count(".") == 1 and lst[1] in [iff, conditional]:
                conjuncts.append(lst3)
    return conjuncts


def renumber_sentences(renumber, def_info):
    for e, conjunct in enumerate(renumber):
        if conjunct != 0:
            new_result = find_sentences(conjunct)
            def_info[e] = new_result


def unpack_definition(abbreviations, def_info, renumber, definiendum, reduced_def=[], kind=""):
    if kind in ["detach disjunct", "embed"]:
        renumber = [1 for x in range(len(reduced_def))]
    for j, num in enumerate(renumber):
        if num != 0:
            result = def_info[j]
            tsentences = []
            if kind == "":
                def_stats1 = def_stats(definiendum, j)
            else:
                def_stats1 = reduced_def[j].def_stats
            lst = result[3]
            k = -1
            greek_to_num = {}

            for i, sentence in enumerate(lst):
                greek = result[6][i]
                if i == 0: def_stats1.tot_greek_sent = greek
                hnum = result[1][i]
                hnum2 = result[2][i]
                connect = result[4][i]
                if len(hnum) > 1 and len(hnum) == 2 and kind != "detach disjunct":
                    if hnum[1] == "1":
                        def_stats1.ant_greek = greek
                    else:
                        def_stats1.con_greek = greek

                if connect[1] == "" and kind == "":
                    k += 1
                    sentence = split_sentences(sentence)
                    tvalue, tvalue2 = get_tvalue(sentence)
                    sentence = categorize_words(abbreviations, sentence, True)
                    sentence[3] = tvalue
                    sentence[5] = greek
                    sentence[6] = hnum2
                    sentence[4] = definiendum + str(j)
                    greek_to_num.update({greek: k})
                    sentence[7] = get_sent_type(hnum2, result)
                    sentence[56] = get_match_type(sentence[7])
                    if tvalue == "~" and "~" not in sentence[58]:
                        sentence[58] = tvalue2 + sentence[58]
                    tsentences.append(sentence)

            if kind == "": get_connection_type(result, def_stats1)
            def_stats1.natural_sent = result[3][0]
            def_stats1.def_number = j
            mem_reduced_def = mem_reduced_def1(tsentences, def_stats1)
            reduced_def[j] = mem_reduced_def
            result[7] = greek_to_num

    return reduced_def


def get_tvalue(sentence):
    tvalue = ""
    tvalue2 = ""
    if "~" in sentence:
        tvalue = "~"
        tvalue2 = "~ "
    return tvalue, tvalue2


def get_match_type(str1):
    if len(str1) == 1:
        if str1 in ["b", "f", "a", "x", "d"]:
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
        if str1[-1] in ["c", "x"]:
            str1 = str1[:-1]
        if str1[0] == "x":
            str1 = "c"

    return str1


def number_embeds(def_info, reduced_def):
    sent_types = {}
    for e, sub_set in enumerate(def_info):

        sentences = reduced_def[e].sentences
        for i, sent_num in enumerate(sub_set[2]):

            sent_type = get_sent_type(sent_num, sub_set)
            sent_types.update({sent_num: sent_type})
            conn = sub_set[4][i]
            sentence = sub_set[3][i]
            osent_num = sub_set[2][i]

            if conn[1] in special_connectives and "a" not in sent_type and i != 0:
                new_def_info = find_sentences(sentence, "", True)
                index1 = []
                embed_num = {}

                for j, lst in enumerate(new_def_info[4]):
                    embed_sent = new_def_info[3][j]
                    sent_num2 = new_def_info[2][j]
                    greek = get_ogreek(osent_num, embed_sent, def_info[e])
                    new_def_info[6][j] = greek
                    if lst[1] == "":

                        for idx, sent in enumerate(sentences):
                            temp_sent = sent[0].replace(" ", "")
                            tembed_sent = embed_sent.replace(" ", "")

                            if temp_sent == tembed_sent and sent[6].startswith(conn[0] + "."):
                                break
                        else:
                            raise Exception

                        index1.append(idx)
                        sentences[idx][48] = new_def_info[2][j]
                        sentences[idx][50] = get_sent_type(sent_num2, new_def_info)
                        embed_num.update({greek: idx})

                new_def_info[8] = embed_num
                reduced_def[e].embeds.update({sent_num: [index1, new_def_info]})

    return


def get_ogreek(sent_num, embed_sent, def_info):
    for e, lst in enumerate(def_info[2]):
        if sent_num in lst and \
                (embed_sent == def_info[3][e] or embed_sent == def_info[3][e][1:-1]):
            return def_info[6][e]
    raise Exception


def build_greek_num_dict2(sentences, def_info):
    for i, sentence in enumerate(sentences):
        build_greek_num_dict(sentence, def_info[i])


def build_greek_num_dict(sentences, sub_def_info):
    greek_num_dict = {}
    for m, sentence in enumerate(sentences):
        greek_num_dict.update({sentence[5]: m})
    sub_def_info[7] = greek_num_dict


def get_connection_type(result, def_stats1):
    idx = findposinmd("1.2", result, 2)
    if result[4][idx][1] == xorr:
        def_stats1.consequent_disjunct = result[3][idx]
        # the sole purpose of this is that the consequent does not
        # fill the output.gsent
    if result[4][0][1] == xorr:
        def_stats1.connection_type = 'x'
    elif result[4][0][1] == iff:
        def_stats1.connection_type = 'e'
    elif result[4][0][1] == idisj:
        def_stats1.connection_type = 'd'
    elif result[4][0][1] == conditional:
        def_stats1.connection_type = 'c'
    else:
        raise Exception


def get_sent_kind(def_info2):
    sent_kind = []

    for def_info in def_info2:
        e = -1
        temp_kind = ["", "", ""]
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


def get_sets_disjunct(lst, side, sentences, size):
    conditions = {}
    natural_disjuncts = []
    loc = 0 if side == "1" else 1
    b = 0 if is_embedded else 1
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
                if is_embedded:
                    sent_type = sentences[sent_index][56]
                else:
                    sent_type = sentences[sent_index][7][:-b]
            else:
                sent_index = str(i)
            if lst[4][i][1] == xorr:
                natural_disjuncts.append([lst[3][i], lst[6][i]])

            if len(lst1) == 2 and lst[4][i][1] == xorr:
                pass

            elif len(lst1) == size and lst[4][i][1] != "":
                conditions.update({lst[2][i]: {}})

            elif len(lst1) == size and lst[4][i][1] == "":
                conditions.update({lst[2][i]: {lst[2][i]: sent_index}})
                assert isinstance(sent_index, int)

            elif len(lst1) > size and lst[4][i][1] in [conditional, iff]:
                dict2 = conditions.get(parent)
                dict2.update({lst[2][i]: []})

            elif len(lst1) > size and lst[4][i][1] == "":
                dict2 = conditions.get(parent)

                if not re.search(r'[qabf]', sent_type):
                    dict2.update({lst[2][i]: sent_index})
                    assert isinstance(sent_index, int)
                else:
                    for k, v in dict2.items():

                        if lst[2][i].startswith(k + "."):
                            v.append(sent_index)
                            assert isinstance(sent_index, int)
                            break

                    else:
                        raise Exception("failed to find conditional parent in disjunct")

            elif len(lst1) > size and lst[4][i][1] == "&":
                pass
            else:
                raise Exception("failed to find conditional parent in disjunct")

        i += 1

    return conditions, natural_disjuncts


def get_sets_of_conditions2(lst, side, sent_kind):
    conditions = {}
    dict1 = {"s": 2, "c": 2, "b": 2, "&": 3, "d": 3}
    size = dict1.get(sent_kind)
    b = 8 if is_embedded else 7

    if is_embedded:
        bb = 8

    i = 0
    for lst1, lst6 in zip(lst[1], lst[6]):
        if len(lst1) > size - 1 and lst1[1] == side:

            if len(lst1) == size and lst[4][i][1] != "":
                conditions.update({lst[2][i]: []})
            elif len(lst1) == size and lst[4][i][1] == "":
                sent_index = lst[b].get(lst6)
                assert sent_index != None
                conditions.update({lst[2][i]: sent_index})
            elif len(lst1) > size and lst[4][i][1] == "":
                parent = ".".join(lst1[:size])
                sent_index = lst[b].get(lst6)
                assert sent_index != None
                conditions.setdefault(parent, []).append(sent_index)
            elif len(lst1) > size and lst[4][i][1] != "":
                pass

        i += 1

    return conditions


# sent_kinds

# first letter represents whether the whole is bicond = b, cond = c, disj = d
# second letter represents whether the antecedent is conj = &, cond = c, bicond = b, single = s
# third letter represents whether the consequent is bicond = b, cond = c, disj = d, cong = &, single = s
# if third letter is t then the consequent must be distributed

def get_sets_of_conditions(def_info, class_def, sent_kind):
    kind = ""
    ex_conditions = {}
    conditions2 = {}
    conditions = {}
    natural_disjuncts = []
    for def_num, lst in enumerate(def_info):
        sentences = class_def[def_num].sentences
        if sent_kind[def_num][0] != 'x':
            conditions = get_sets_of_conditions2(lst, "1", sent_kind[def_num][1])

            if sent_kind[def_num][2] == "d":
                _ = get_sets_disjunct(lst, "2", sentences, 3)
                ex_conditions, natural_disjuncts = _
                kind = 'detach disjunct'
            elif sent_kind[def_num][2] == "t":
                ex_conditions, natural_disjuncts = distribute(lst)
            else:
                conditions2 = get_sets_of_conditions2(lst, "2", sent_kind[def_num][2])

        else:
            _ = get_sets_disjunct(lst, "1", sentences, 2)
            ex_conditions, natural_disjuncts = _

        for lst1 in natural_disjuncts: class_def[def_num].def_stats.natural_disjuncts.append(lst1)
        greek_conn = get_greek_hypotheticals(lst)
        conditions3 = build_all_conditions(conditions, conditions2, ex_conditions)
        add_conj_elim_info(conditions3, greek_conn, def_num, class_def, kind, def_info)

    return class_def


def add_conj_elim_info(conditions3, greek_conn, def_num, class_def, kind, def_info):
    for k, item_ in enumerate(conditions3):
        if k == 0:
            add_conj_elim2(item_, "antecedent", greek_conn, class_def, def_num)
        elif k == 1:
            add_conj_elim2(item_, "consequent", greek_conn, class_def, def_num)
        else:
            disju = disjunction()
            add_conj_elim2(item_, "disjunct", greek_conn, class_def, def_num, disju, def_info[0])
    if kind == 'detach disjunct':
        greek = greek_conn.get("1.2")
        prepare_embed_class(class_def, 0, [], "1.2", class_def[0].sentences, "detach disjunct", greek)

    return


def prepare_embed_class(class_def, def_num, hnum, k, sentences, kind, greek):
    global is_embedded
    list1 = class_def[def_num].embeds.get(k)
    sent_kind = get_sent_kind([list1[1]])
    is_embedded = True
    definiendum3 = k + "," + definiendum
    def_stats1 = def_stats(definiendum3, def_num)
    mreduced_def = mem_reduced_def1(sentences, def_stats1)
    if kind != "detach disjunct":
        list2 = get_sets_of_conditions([list1[1]], [mreduced_def], sent_kind)
        hnum.append(k)
    else:
        list2 = [mreduced_def]
        class_def[def_num].def_stats.con_hnum = ["1.2"]
    is_embedded = False
    get_connection_type(list1[1], def_stats1)
    list2 = unpack_definition({}, [list1[1]], [], definiendum3, list2, kind)
    list2[0].sentences = None
    list2[0].def_stats.tot_greek_sent = greek
    if kind == 'detach disjunct':
        list2[0].disjuncts = class_def[0].disjuncts
    class_def[def_num].embeds.update({k: list2[0]})


def add_conj_elim2(item_, kind, greek_conn, class_def, def_num, disju=[], def_info=[]):
    global is_embedded

    sentences = class_def[def_num].sentences
    index1 = []
    comp_const = []
    comp_greek = []
    hnum = []

    for k, v in item_.items():
        index1.append(v)
        if isinstance(v, list):
            greek = greek_conn.get(k)
            comp_greek.append(greek)

            if is_embedded:
                bb = 8

            comp_const.append(get_lesser_skeleton(v, sentences))
            if k in class_def[def_num].embeds.keys():
                prepare_embed_class(class_def, def_num, hnum, k, sentences, "embed", greek)

    if kind == "disjunct":
        disju.index1 = index1
        disju.comp_const = comp_const
        disju.hnum = hnum
        disju.comp_greek = comp_greek
        disju.tot_greek = get_tot_greek(item_, def_info)
        class_def[def_num].disjuncts.append(disju)
    elif kind == "antecedent":
        class_def[def_num].def_stats.ant_index = index1
        class_def[def_num].def_stats.ant_comp_const = comp_const
        class_def[def_num].def_stats.ant_comp_greek = comp_greek
        class_def[def_num].def_stats.ant_hnum = hnum
    else:
        class_def[def_num].def_stats.con_index = index1
        class_def[def_num].def_stats.con_comp_const = comp_const
        class_def[def_num].def_stats.con_comp_greek = comp_greek
        class_def[def_num].def_stats.con_hnum = hnum

    return


def get_tot_greek(item_, def_info):
    k = list(item_.keys())[0]
    if len(item_.keys()) == 1:
        pos = def_info[2].index(k)
    else:
        list1 = k.split(".")
        parent = ".".join(list1[:-1])
        pos = def_info[2].index(parent)
    return def_info[6][pos]


def get_lesser_skeleton(num, sentences):
    b = 6 if premise else 48
    c = 7 if premise else 50

    lesser_sent_key = ""
    for value in num:

        if sentences[value][b] == None: b = 56
        if sentences[value][c] == None: c = 56

        lesser_sent_key += sentences[value][b] + "." + \
                           sentences[value][c] \
                           + "." + sentences[value][58]

    return lesser_sent_key


def build_all_conditions(conditions, conditions2, ex_conditions):
    conditions3 = [0, 0]
    conditions3[0], conditions3[1] = conditions, conditions2
    if ex_conditions != {}:
        for v in ex_conditions.values():
            conditions3.append(v)
    return conditions3


def get_greek_hypotheticals(list1):
    greek_hypotheticals = {}
    i = 0
    for lst2, lst4, lst6 in zip(list1[2], list1[4], list1[6]):
        if i > 0 and lst4[1] in [conditional, iff, xorr, idisj]:
            greek_hypotheticals.update({lst2: lst6})
        i += 1
    return greek_hypotheticals


def get_parent_conn_type(def_info, i, grandparent=False):
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
    natural_disjuncts = []
    for lst1, lst6 in zip(lst[1], lst[6]):
        if i == 9:
            bb = 8
        if len(lst1) > 1 and lst1[1] == "2":
            parent_conn_type = get_parent_conn_type(lst, i)
            if len(lst1) > 2:
                gparent_conn_type = get_parent_conn_type(lst, i, True)

            if lst[4][i][1] == xorr:
                natural_disjuncts.append([lst[3][i], lst[6][i]])

            if parent_conn_type == xorr and lst[4][i][1] == "":
                sent_index = lst[7].get(lst6)
                disjunctions.update({lst[2][i]: sent_index})
            elif parent_conn_type == xorr and lst[4][i][1] == "&":
                disjunctions.update({lst[2][i]: {}})

            elif gparent_conn_type == xorr and parent_conn_type == "&" \
                    and lst[4][i][1] == "":

                parent = ".".join(lst1[:4])
                sent_index = lst[7].get(lst6)
                assert sent_index != None
                dict2 = disjunctions.get(parent)
                dict2.update({lst[2][i]: sent_index})

            elif lst[4][i][1] == xorr:
                pass
            elif len(lst1) == 2:
                conditions.update({lst[2][i]: {}})
            elif lst[4][i][1] == "" and len(lst1) == 3:
                parent = ".".join(lst1[:2])
                sent_index = lst[7].get(lst6)
                assert sent_index != None
                dict2 = conditions.get(parent)
                dict2.update({lst[2][i]: sent_index})

            else:
                print('you havent does this type of distribution')
        i += 1
    i = 0

    for k, v in disjunctions.items():
        if i == 0:
            temp = conditions.get("1.2")
            temp2 = copy.deepcopy(temp)
            if isinstance(v, list):
                for y, z in v.items(): temp.update({y: z})
            else:
                temp.update({k: v})

        else:
            temp3 = temp2
            str1 = str(i)
            if isinstance(v, list):
                for y, z in v.items(): temp3.update({y: z})
            else:
                temp3.update({k: v})
            conditions.update({str1: copy.deepcopy(temp3)})
            if i == 3:
                raise Exception('check this')

        i += 1

    g = len(conditions) - len(natural_disjuncts)
    for x in range(g): natural_disjuncts.append(0)

    return conditions, natural_disjuncts
