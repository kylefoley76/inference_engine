


from standard_order import order_sentence
from general_functions import *
import itertools, operator, collections
from change_abbreviations import change_abbrev
from use_lemmas import use_basic_lemmas
from analyze_sentence import find_sentences
from pickle_dictionary import get_sets_of_conditions, string_constants_together, build_hypo_list, get_sent_kind
from put_words_in_slots import categorize_words, determine_constants
import time, json
from prepare_for_print import rearrange



abbreviations = {}
identities = []
all_sent = []
prop_name = []
total_sent = []
prop_var = []
constants = []
variables = []
consistent = True
artificial = False





############### THE FOLLOWING FUNCTIONS ARE RELATED TO THE USE OF IDENTITY


def identity():
    global identities
    names = {}
    props = {}
    tvalues = {}
    indexes = {}

    for sent in all_sent:
        if sent[13] == '=' and abbreviations.get(sent[10]) != sent[14]:
            names.update({sent[10]: sent[14]})
            props.update({sent[10]: set()})
            tvalues.update({sent[10]: {}})
            indexes.update({sent[10]: {}})
            props.update({sent[14]: set()})
            tvalues.update({sent[14]: {}})
            indexes.update({sent[14]: {}})


    identities = [names, props, tvalues, indexes]


def update_identity(begin, end):
    global identities
    names = identities[0]
    props = identities[1]
    tvalues = identities[2]
    indexes = identities[3]


    for k, v in names.items():
        properties1 = props.get(k)
        properties2 = props.get(v)
        tvalues1 = tvalues.get(k)
        tvalues2 = tvalues.get(v)
        idx1 = indexes.get(k)
        idx2 = indexes.get(v)
        for i in range(begin, end):
            sent = all_sent[i]
            if sent[13] != "=":
                build_identity(sent, k, tvalues1, properties1, idx1, i)

            if sent[13] != "=":
                build_identity(sent, v, tvalues2, properties2, idx2, i)

        props.update({k: properties1})
        props.update({v: properties2})
        tvalues.update({k: tvalues1})
        tvalues.update({v: tvalues2})
        indexes.update({k: idx1})
        indexes.update({v: idx2})



    identities = [names, props, tvalues, indexes]

    use_identity()


def build_identity(sent, obj, tv, properties, _index, asent_idx):
    list1 = []
    match = False
    for n in sent[54]:
        if sent[n] == obj:
            match = True
            list1.append(alpha)
        elif sent[n] != "~":
            list1.append(sent[n])
    if not match:
        return

    new_sent = "".join(list1)
    properties.add(new_sent)
    tv.update({new_sent: sent[3]})
    _index.update({new_sent: asent_idx})


def use_identity():
    for k, v in identities[0].items():
        properties1 = identities[1].get(k)
        properties2 = identities[1].get(v)
        tvalues1 = identities[2].get(k)
        tvalues2 = identities[2].get(v)
        idx1 = identities[3].get(k)
        idx2 = identities[3].get(v)

        properties3 = properties1 & properties2
        if properties3 != set():
            for sent in properties3:
                tv1 = tvalues1.get(sent)
                tv2 = tvalues2.get(sent)
                if tv1 != tv2:
                    num = idx1.get(sent)
                    num2 = idx2.get(sent)
                    construct_contr_identity(num, num2, k, v)
                    return


def construct_contr_identity(num, num2, k, v):
    global consistent
    sent1 = all_sent[num]
    sent2 = all_sent[num2]
    for pos in sent2[42]:
        if sent2[pos] == v:
            sent2[pos] = k
            break

    name_and_build(sent2, oprop_name, prop_name)
    anc1 = find_counterpart_inlist("(" + k + " = " + v + ")", total_sent, 1, 0)
    add_to_total_sent(total_sent, sent2[1], sent2[2], sent2[3], "SUB", sent2[44], anc1)
    build_contradiction(total_sent, sent1[44])
    consistent = False



##########group: prepare for instantiation #############



def get_range(sentences):
    x = 10
    list1 = []
    while sentences[x] != None:
        list1.append(x)
        x += 1
    return list1


def rearrange_sentence(def_info, sent, sentences, connected_const):
    definition, ordered = order_sentence([def_info], sent, sentences, True)
    if ordered:
        def_info = find_sentences(definition)
        sentences = build_hypo_list([def_info], "", abbreviations, connected_const)
        definition, translated = order_sentence([def_info], definition, sentences, True)
        assert not translated

    return sentences, def_info, ordered


def reduce_hypotheticals_in_premises():
    j = -1
    quant_counter = ""
    while j < len(all_sent) -1:
        j += 1
        sent = all_sent[j]
        len_asent = len(all_sent)
        quantifier = False
        if len(sent) == 46:
            quant_counter += "a"
            sent = sent[0]
            quantifier = True

        if isinstance(sent, str):
            if not one_sentence(sent):
                all_sent[j] = None
                j -= 1
                osent = sent
                def_info = find_sentences(sent)
                sentences = build_hypo_list([def_info], "", abbreviations, connected_const)
                anc1 = ""
                if quantifier:
                    anc1 = find_counterpart_inlist(sentences[0][0], total_sent, 1, 0)
                    assert anc1 != None
                subvalues = name_connected_sent(def_info, osent, sentences, True, quantifier)
                sentences, def_info, ordered = rearrange_sentence(def_info, sent, sentences, connected_const)
                universal_negations(sentences, abbreviations, gsent, trans_def)
                sent_kind = get_sent_kind([def_info])
                _ = get_sets_of_conditions([def_info], "", sentences, sent_kind, True)
                subvalues2 = get_range(sentences[0])
                str1, _, _ = string_constants_together(subvalues2, sentences, 0, 7, [], "", True)
                if ordered:
                    subvalues = name_connected_sent(def_info, def_info[3][0], sentences, False, quantifier, anc1)
                lindiv.append(str1)
                lsent.setdefault(str1, []).append(subvalues)
                if not quantifier:
                    do_not_instantiate.append([len(lsent)-1, len(gsent)-1])

        if quantifier:
            add_to_gsent(sentences, "qu" + quant_counter)
            trans_def.update({"qu" + quant_counter:sentences})
            for x in range(len_asent, len(all_sent)):
                do_not_instantiate.append([x, len(gsent) - 1])

    return


def name_connected_sent(def_info, osent, sentences, first, quantifier, anc1 = ""):
    m = 10
    # because we cannot delete sentences from the all sent otherwise we
    # mess up the order of the subvalues, we turn connected sentences into
    # nones in the all sent and then gradually replace the all sent with
    # the parts of the connected sent

    none_pos = [i for i, sent in enumerate(all_sent) if sent == None]
    subvalues = []
    greek_english = {}
    rule = "ASC" if not first else ""
    while sentences[0][m] != None:
        sentences[0][m][44] = get_sn(total_sent) + 1
        sent_abb = name_sent(sentences[0][m][1], prop_name)
        sentences[0][m][2] = sent_abb
        oprop_name[sent_abb] = sentences[0][m][1]
        if first:
            if none_pos != []:
                all_sent[none_pos[0]] = sentences[0][m]
                subvalues.append(none_pos[0])
                del none_pos[0]
            else:
                all_sent.append(sentences[0][m])
                subvalues.append(len(all_sent) - 1)
            greek_english.update({sentences[0][m][5]: sentences[0][m][3] + sent_abb})
            if artificial:
                for o in all_sent[subvalues[-1]][42]:
                    try:
                        variables.remove(all_sent[-1][o])
                    except:
                        pass
        else:
            pos = find_2posinlist(sentences[0][m][0], sentences[0][m][7], all_sent, 0, 7)
            all_sent[pos][44] = get_sn(total_sent) + 1
            subvalues.append(pos)
            greek_english.update({sentences[0][m][5]: sentences[0][m][3] + sent_abb})

        m += 1
    original_greek = def_info[5]
    for k, v in greek_english.items():
        def_info[5] = def_info[5].replace(k, v)
    if rule == "" and not quantifier:
        add_to_total_sent(total_sent, osent, def_info[5], "", rule)
    elif rule == "ASC" and not quantifier:
        add_to_total_sent(total_sent, osent, def_info[5], "", rule, get_sn(total_sent))
    elif rule == "ASC" and quantifier:
        add_to_total_sent(total_sent, osent, def_info[5], "", rule, anc1)


    def_info[5] = original_greek
    sentences[0][3] = get_sn(total_sent)
    return subvalues


def prepare_stan():
    if artificial:
        for i in range(len(all_sent)):
            if isinstance(all_sent[i], str):
                if one_sentence(all_sent[i][0]):
                    all_sent[i] = quick_reduction(all_sent[i])
                    all_sent[i][6] = str(get_sn(total_sent))
                    add_to_total_sent(total_sent, all_sent[i][1], all_sent[i][2], all_sent[i][3], "")
                    all_sent[i][44] = get_sn(total_sent)
                    all_sent[i][7] = "c"
                    lsent.setdefault(all_sent[i][58], []).append([i])
                    lindiv.append(all_sent[i][58])

                for j in all_sent[i][42]:
                    try:
                        variables.remove(all_sent[i][j])
                    except:
                        pass
    else:
        for e, sent in enumerate(all_sent):
            if one_sentence(sent[0]) and sent[7] == 'c':
                sent[58], sent[55] = determine_constants(abbreviations, sent[54], sent, connected_const)
                sent[7] = "c"
                lsent.setdefault(sent[58], []).append([e])
                lindiv.append(sent[58])
            # else:
            #     print (sent[0])

    return


def quick_reduction(sent):
    sent = sent.strip()
    sent = sent.replace("(", "")
    sent = sent.replace(")", "")
    sent = sent.split(" ")
    sent = [None] * 4 + sent + [None]
    sent = categorize_words(abbreviations, sent)
    sent[2] = name_sent(sent[1], prop_name)
    oprop_name[sent[1]] = sent[2]
    return sent


def get_propositional_variables():
    for sent in all_sent:
        if sent[9] == mini_e:
            # list1 = json.loads(json.dumps(sent))
            list1 = copy.deepcopy(sent)
            prop = list1[8]
            for x in [8,9]: list1[54].remove(x)
            list1[8] = None
            list1[9] = None
            name_and_build(list1, oprop_name, prop_name)
            abbreviations.update({prop: list1[1]})


def get_constants():
    for lst in all_sent:
        if lst[7] == 'c':
            for num in lst[42]:
                if lst[num] not in constants: constants.append(lst[num])

    for var in abbreviations.keys():
        if var not in constants: constants.append(var)


def get_abbreviations_standard():
    if not artificial: return
    i = 0
    list2 = []
    while "=" in all_sent[i]:
        sent = all_sent[i]
        if sent == None:
            break
        if "=" in sent:
            list2.append(sent)
            sent = sent.replace("(", "")
            sent = sent.replace(")", "")
            list1 = sent.split("=")
            list1[0] = list1[0].strip()
            list1[1] = list1[1].strip()

            abbreviations.update({list1[0]: list1[1]})
            try:
                variables.remove(list1[0])
            except:
                pass


        del all_sent[i]
    if list2 != []:
        sent1 = " & ".join(list2)
        add_to_total_sent(total_sent, sent1, "", "", "constants")


def add_disjuncts(list2, definiendum):
    for e, sent in enumerate(list2[79]):
        add_to_total_sent(total_sent, sent[0], "", "", "DF " + definiendum)
        sent[0] = sent[1]
        list2[84][e][3] = get_sn(total_sent)


def translate_abbreviations(lst, definiendum):
    # in the map var the old variables are on the left and the new ones are ont he right
    if definiendum == 'mind':
        bb = 8
    conjunctive_definition = False
    map_var = {}
    already_used_map = {}
    change_constants(already_used_map, abbreviations, variables, lst[0][9])
    if len(lst) == 1:
        n = 0
        b = 80
    else:
        conjunctive_definition = True
        n = 1
        b = 0
        add_to_total_sent(total_sent, lst[0][80], "", "", "DF " + definiendum)
        anc1 = get_sn(total_sent)
        substitutions.setdefault(definiendum, []).append(total_sent[-1])

    temp_constants = lst[0][9]
    for m in range(n, len(lst)):
        list2 = lst[m]
        if list2 != "":
            greek_definition = list2[2]
            definiendum2 = definiendum + str(m) if m > 0 else definiendum
            if conjunctive_definition:
                add_to_total_sent(total_sent, list2[b], "", "", "CE", anc1)
            else:
                add_to_total_sent(total_sent, list2[b], "", "", "DF " + definiendum)
            list2[3] = get_sn(total_sent)
            substitutions.setdefault(definiendum, []).append(total_sent[-1])
            pn = get_sn(total_sent)
            if list2[79] != None:
                add_disjuncts(list2, definiendum)

            i = 10
            while list2[i] != None:
                sent = list2[i]
                if i == 27:
                    bb = 8
                ogreek = sent[5]
                for j in sent[42]:
                    ovar = sent[j]
                    if ovar != None and ovar not in temp_constants.values():
                        nvar = already_used_map.get(ovar)
                        if nvar == None:
                            nvar = map_var.get(ovar)
                        else:
                            map_var.update({ovar: nvar})
                        if nvar != None:
                            sent[j] = nvar
                        else:
                            if ovar in temp_constants.keys():
                                value = temp_constants.get(ovar)
                                nvar = get_key(abbreviations, value)
                                if nvar != None:
                                    sent[j] = nvar
                                    map_var.update({ovar: nvar})
                                elif nvar == ovar:
                                    pass
                                elif ovar in variables:
                                    variables.remove(ovar)
                                    map_var.update({ovar: ovar})
                                else:
                                    map_var.update({ovar: variables[0]})
                                    del variables[0]
                            elif ovar in variables:
                                variables.remove(ovar)
                                map_var.update({ovar: ovar})
                            else:
                                sent[j] = variables[0]
                                map_var.update({ovar: variables[0]})
                                del variables[0]

                name_and_build(sent, oprop_name, prop_name)
                greek_definition = greek_definition.replace(ogreek, sent[0])
                translate_greek_disjuncts(ogreek, sent, list2)
                sent[44] = get_sn(total_sent) + 2
                i += 1

            if translations_made(map_var):
                rn_sent = build_trans_sent(map_var)
                already_used_map = {**map_var, **already_used_map}
                map_var = {}
                qn = get_sn(total_sent) + 1
                add_to_total_sent(total_sent, rn_sent, "", "", "TR")
                substitutions.setdefault(definiendum, []).append(total_sent[-1])
                add_to_total_sent(total_sent, greek_definition, "", "", "SUBI", pn, 0)
                substitutions.setdefault(definiendum, []).append(total_sent[-1])
                add_disjuncts_to_total_sent(list2, qn)
                list2[3] = get_sn(total_sent)
                list2[0] = greek_definition



    add_more_constants(temp_constants, already_used_map)


def translations_made(map_var):
    for k, v in map_var.items():
        if k != v:
            return True
    return False


def translate_greek_disjuncts(ogreek, sent, list2):
    for lst in list2[79]:
        lst[0] = lst[0].replace(ogreek, sent[0])


def add_disjuncts_to_total_sent(list2, qn):
    for e, lst in enumerate(list2[79]):
        add_to_total_sent(total_sent, lst[0], "", "", "SUBI", qn, qn + 1)
        list2[84][e][3] = get_sn(total_sent)
        m = 10
        while list2[m] != None:
            if list2[m][7][0] == "x" and list2[m][0] in lst[0]:
                list2[m][44] = get_sn(total_sent)
            m += 1


def build_trans_sent(map_var):
    list1 = []
    for k, v in map_var.items():
        if k != v:
            str1 = "(" + k + idd + v + ")"
            list1.append(str1)

    return " ".join(list1)


def add_more_constants(temp_constants, already_used_map):
    global total_sent
    lst_constants = []
    for k, v in temp_constants.items():
        new_var = already_used_map.get(k)
        if new_var != None and new_var not in abbreviations.keys():
            abbreviations.update({new_var: v})
            lst_constants.append("(" + new_var + "=" + v + ")")
    if lst_constants != []:
        str1 = " & ".join(lst_constants)
        g = findposinmd("constants", total_sent, 4)
        if g > -1:
            total_sent[g][1] = total_sent[g][1] + " & " + str1
        else:
            add_to_total_sent(total_sent, str1, "", "", "constants")


def time_count(time1):
    time2 = time.time() - time1
    time2 = time2 * 100000
    print(str("{0:.2f}".format(time2)))


def definition_constant(sent):
    if sent[13] in ["I", "J", "V"]:
        word = abbreviations.get(sent[14])
        if word != None:
            return word
        else:
            return sent[13]

    elif sent[13] == '=' and sent[14] in abbreviations.values():
        return sent[14]
    else:
        return sent[13]



def get_hypotheticals(start):
    global hypo_counter
    done = []

    for m in range(start, len(all_sent)):
        word = definition_constant(all_sent[m])
        assert word != None

        if findposinmd("DF " + word, total_sent, 4) == -1 and word not in done:
            item1 = dictionary[9].get(word)
            if item1 != None:
                item2 = copy.deepcopy(item1)
                add_to_gsent(item2, word)
                trans_def.update({word: item2})
                translate_abbreviations(item2, word)
                done.append(word)

    return


def add_to_gsent(item1, word):
    oword = word
    if word == 'KN':
        bb = 8

    n = 1 if len(item1) > 1 else 0
    for i in range(n, len(item1)):
        word = oword + str(i) if i > 0 else oword
        if word == '2.2.1,individual':
            bb = 8

        if findposinmd(word, gsent, 0) == -1:
            gsent.append([word, item1[i][60]])


def try_instantiation(all_sent2, prop_var20, oprop_name2, prop_name2, variables20, total_sent2, abbreviations2,
                      connected_const2, artificial2):

    global all_sent, prop_var, oprop_name, prop_name, abbreviations
    global total_sent, constants, consistent, variables
    global negated_conjunction, disjunction_elimination, identities
    global substitutions, trans_def, lsent, gsent, artificial, lindiv
    global do_not_instantiate, rel_abbrev, atomic_dict1, atomic_dict2
    global connected_const

    consistent = True
    gsent = []
    lindiv = []
    constants = []
    identities = []
    negated_conjunction = []
    disjunction_elimination = []
    do_not_instantiate = []
    rel_abbrev = []
    substitutions = {}
    trans_def = {}
    atomic_dict1 = {}
    atomic_dict2 = {}
    lsent = {}

    all_sent, prop_var, prop_name = all_sent2, prop_var20, prop_name2
    artificial = artificial2
    variables, total_sent = variables20, total_sent2
    abbreviations = abbreviations2
    oprop_name = oprop_name2
    connected_const = connected_const2

    step_one()

    return total_sent, consistent

def step_one():
    global total_sent

    get_abbreviations_standard()

    reduce_hypotheticals_in_premises()

    prepare_stan()

    get_propositional_variables()

    get_constants()

    get_relevant_abbreviations(0)

    get_hypotheticals(0)

    identity()

    use_basic_lemmas2(0, len(all_sent))

    loop_through_gsent()

    # for sent in total_sent:
    #     print (sent[3] + sent[1])
    # obtain_relevant_sentences()

    total_sent =  rearrange("last", total_sent, all_sent, consistent, abbreviations,
        substitutions, artificial, prop_name, oprop_name)



def use_basic_lemmas2(begin, end):
    global consistent
    if not consistent: return

    update_identity(begin, end)
    if not consistent: return

    for i in range(begin, end):
        sent = all_sent[i]
        if sent[7] == 'c':
            for pos in sent[42]:

                consistent = use_basic_lemmas(abbreviations, total_sent, variables, prop_name, oprop_name, prop_var,
                                              pos, sent, substitutions, atomic_dict1, atomic_dict2)


                if not consistent: return

######## group: loop until instantiation is done ##############



def get_relevant_abbreviations(begin):
    universal = lambda x, y: x[13] in ["I", "J", "V", "OFW"] and y == 14

    for sent in all_sent[begin:]:
        for noun in sent[42]:
            if sent[noun] == 'x':
                bb = 8

            if sent[noun] not in rel_abbrev and not universal(sent, noun):
                rel_abbrev.append(sent[noun])

    return


def delete_irrelevant_lsent(begin):
    list1 = []
    for e in range(begin, len(all_sent)):
        sent = all_sent[e]
        if all(sent[x] not in rel_abbrev for x in sent[42]):
            sent[0] = 'irrelevant'
            list1.append(e)

    if list1 != []:
        delete_this = []
        for k, v in lsent.items():
            j = 0
            while j < len(v):
                if v[j][0] in list1:
                    del v[j]
                    if v == []:
                        delete_this.append(k)
                        break
                else:
                    j += 1
        for k in delete_this: del lsent[k]
        for k in delete_this: lindiv.remove(k)




    return




def is_exceptional(matrix, j):
    if j == 25:
        bb = 8

    lesser_word = matrix[j][0]
    lesser_word = lesser_word.replace("~", "")
    if matrix[j][1] == "I":
        if lesser_word in dictionary[15]:
            return True
    elif matrix[j][1] == 'J':
        pos = dictionary[0].get(lesser_word)
        if pos[0] == 'a':
            return True

    return False


def build_matrix(matrix, gstart, gstop, lstart, lend):
    for lindex in range(lstart, lend):
        lconstant = lindiv[lindex]
        for gindex in range(gstart, gstop):
            gsent_lst = gsent[gindex]
            for e, gsent_sublst in enumerate(gsent_lst[1]):
                if gsent_sublst != []:
                    if gsent_sublst[0][0] == ' I':
                        bb = 8
                    # the last member is whether the gsent is ante or cond
                    matrix.append([lconstant, gsent_sublst[0][0], gindex, e])

    return


def loop_through_gsent():
    global lindiv
    if not consistent: return
    for x in abbreviations.values(): assert not x.islower() or len(x) > 1
    matrix = []
    lindiv = sorted(list(set(lindiv)))
    delete_irrelevant_lsent(0)
    build_matrix(matrix, 0, len(gsent), 0, len(lindiv))
    # in the matrix, the 2nd member is the index in the gsent, the 3rd member
    # is 0 for antecedent and 1 for consequent and the 4th member is the index
    # in the lsent
    j = 0
    z = 0
    while j < len(matrix):
        z += 1
        if z > 800: raise Exception ("caught in infinite loop")

        word = gsent[matrix[j][2]][0]
        if word == "" or j == 28:
            bb = 8

        detacher = matrix[j][3]
        len_gsent = len(gsent)
        len_lsent = len(lindiv)
        len_asent = len(all_sent)
        possibilities = []

        if matrix[j][0] == matrix[j][1] or is_exceptional(matrix, j):
            # print(word)

            if matrix[j][0] == "INM b" or j == 27 or word == '1.2.1,INM':
                bb = 8

            used_possibilities = loop_through_gsent2(possibilities, matrix, word, detacher, j)
            if used_possibilities != []:
                reconfigure_matrix(j, len_asent, len_gsent, len_lsent, matrix, used_possibilities)
                if not consistent: return

        elif j == len(matrix) - 1:
            last_resort_axioms(j, matrix)
            if not consistent: return

        j += 1

    if consistent:
        add_to_total_sent(total_sent, consist, consist, "", consist + "I")

    return

def reconfigure_matrix(j, len_asent, len_gsent, len_lsent, matrix, used_possibilities):
    global lindiv
    use_basic_lemmas2(len_asent, len(all_sent))
    if not consistent: return
    lindiv = lindiv[:len_lsent] + sorted(list(set(lindiv[len_lsent:])))
    get_hypotheticals(len_asent)
    # the point of the following is that if (b > c) & (b I d) = (b I e) in (b I d)
    # then it would be useless to (b > c) in (b I e)
    if used_possibilities != []:
        # if the used possibilities are blank then the ax id tense was used as last resort
        for snum in range(len_asent, len(all_sent)):
            do_not_instantiate.append([snum, matrix[j][2]])
        for possibility in used_possibilities:
            do_not_instantiate.append([possibility[0], matrix[j][2]])
        ax_idt_no_inst(len_asent, do_not_instantiate)
    delete_irrelevant_lsent(len_asent)
    build_matrix(matrix, 0, len(gsent), len_lsent, len(lindiv))
    build_matrix(matrix, len_gsent, len(gsent), 0, len_lsent)
    return

def ax_idt_no_inst(len_asent, do_not_instantiate):
    m = len(total_sent) - 1
    while total_sent[m][4] == "&E":
        m -= 1
    if total_sent[m][4] == 'AY IDT':
        for snum in range(len_asent, len(all_sent)):
            do_not_instantiate.append([snum, len(gsent) - 1])


def loop_through_gsent2(possibilities, matrix, word, detacher, j):
    fake_lsent = copy.deepcopy(lsent)
    gindex = matrix[j][2]
    k = matrix[j][3]
    remaining_conditions = gsent[gindex][1][k]
    possibilities.append(fake_lsent.get(matrix[j][0]))
    gsent_pos = copy.deepcopy(remaining_conditions[0][1])
    if [possibilities[0][0][0], gindex] in do_not_instantiate:
        return []
    elif len(remaining_conditions) > 1:
        b = 0
        for gside, gconstant in enumerate(remaining_conditions[1:]):
            lindexes = lsent.get(gconstant[0])
            if lindexes != None:
                for lst in lindexes:
                    if [lst[0], gindex] not in do_not_instantiate:
                        b += 1
                        gsent_pos += copy.deepcopy(gconstant[1])
                        possibilities.append(lindexes)
                        break
                else:
                    return []
            else:
                rearrange_matrix(matrix, j, b, remaining_conditions, gconstant)
                return []

    if len(remaining_conditions) == 1:
        i = 0
        while i < len(possibilities[0]):
            if [possibilities[0][i][0], gindex] in do_not_instantiate:
                del possibilities[0][i]
            else:
                i += 1


    return loop_through_gsent3(possibilities, word, detacher, gsent_pos, gindex)


def rearrange_matrix(matrix, j, b, remaining_conditions, gconstant):
    list1 = [remaining_conditions[0], gconstant]
    assert remaining_conditions[b + 1] == gconstant
    del remaining_conditions[b + 1]
    remaining_conditions.insert(0, gconstant)
    for lst in matrix[j:]:
        if lst[1] == list1[0]:
            raise Exception ("not tested yet")
            lst[1] = list1[1]
    return


def loop_through_gsent3(possibilities, word, detacher, gsent_pos, gindex):
    global all_sent, prop_var, prop_name, constants, consistent, variables
    global negated_conjunction, disjunction_elimination, total_sent, substitutions
    global lsent, gsent, abbreviations, oprop_name, lindiv

    dead_combinations = []
    conj_intro_pos = []
    possibilities = [i for i in itertools.product(*possibilities)]
    if gindex == 1:
        bb = 8
    combine_lists(possibilities, conj_intro_pos)
    used_possibilities = []

    for e, possibility in enumerate(possibilities):

        sentences2 = get_sentences(word, trans_def)
        abbrev_dict, match_found = variables_match(gsent_pos, possibility,
                            sentences2, dead_combinations, gindex, detacher)
        if match_found:
            if word == 'thing':
                pos = universal_instantiation(abbrev_dict, possibility)
                conj_intro_pos[e] = pos
            sentences = copy.deepcopy(sentences2)
            consistent = change_abbrev(abbrev_dict, word, detacher, conj_intro_pos[e], trans_def, oprop_name, prop_name,
                                       all_sent, constants, prop_var, negated_conjunction, disjunction_elimination,
                                       total_sent, substitutions, variables, sentences, abbreviations, gsent, lindiv,
                                       lsent)


            if not consistent:
                return used_possibilities.append(possibility)

            else:
                used_possibilities.append(possibility)

    return used_possibilities


def combine_lists(possibilities, conj_intro_pos):
    e = 0
    while e < len(possibilities):
        possibility = possibilities[e]
        list1 = []
        temp_conj = []
        for lst in possibility:
            list1 += lst
            temp_conj.append(all_sent[lst[0]][44])
        if len(list1) == len(set(list1)):

            possibilities[e] = list1
            conj_intro_pos.append(temp_conj)
            e += 1
        else:
            del possibilities[e]

    return


def are_identical_unique_obj(i, j, sentences):
    if all_sent[i][13] == '=' and sentences[j][13] == '=' and \
    all(all_sent[i][x] == sentences[j][y] for x, y in zip(all_sent[i][42], sentences[j][42])):
        return True
    return False


def variables_match(gsent_pos, possibility, sentences, dead_combinations, gindex, detacher):
    if is_dead_combination(dead_combinations, possibility):
        return {}, False
    abbrev_dict = {}
    used_lesser = []

    for e, i in enumerate(possibility):
        j = gsent_pos[e]
        used_lesser.append(i)
        if are_identical_unique_obj(i, j, sentences):
            return {}, True

        else:

            for pos in all_sent[i][42]:
                gvar = sentences[j][pos]
                lvar = all_sent[i][pos]
                # for those sentences of the form y = time, 'time' cannot be replaced
                if lvar != gvar and gvar not in constants \
                    and gvar not in abbreviations.values():
                    var = abbrev_dict.get(all_sent[i][pos])
                    if pos == 8 and lvar == None or sentences[j][pos] == None:
                        # this is because 8 is the place of the propositional variable and
                        # sometimes some sentences will have it and others won't
                        pass
                    elif (var == None and gvar in abbrev_dict.values()):
                        dead_combinations.append(copy.deepcopy(used_lesser))
                        return {}, False
                    elif var == None:
                        abbrev_dict.update({lvar: gvar})
                    elif var != sentences[j][pos]:
                        dead_combinations.append(copy.deepcopy(used_lesser))
                        return {}, False
                elif lvar in constants and gvar in constants \
                    and gvar != lvar:
                    return {}, False
            else:
                pair = gsent[gindex][1][detacher][0]
                del gsent[gindex][1][detacher][0]
                gsent[gindex][1][detacher].append(pair)



    if abbrev_dict == {}: return {}, False
    return abbrev_dict, True


def get_sentences(definiendum2, trans_def):
    if definiendum2 == 'thing':
        bb = 8
    try:
        hypo_num = int(definiendum2[-1])
        definiendum = definiendum2[:-1]
    except:
        hypo_num = 0
        definiendum = definiendum2

    reduced_def = trans_def.get(definiendum)
    sentences2 = reduced_def[hypo_num]

    return sentences2


def is_dead_combination(dead_detach, possibility):
    # if we know that detach sentences 6 and 4, for example, are impossible then any instantiation
    # which uses sentences 6 and 4 will also be impossible
    for dead_list in dead_detach:
        if len(set(dead_list).intersection(set(possibility))) == len(dead_list):
            return True
    return False


def universal_instantiation(abbrev_map, possibility):
    if len(possibility) > 1: raise Exception ('you havent coded for this yet')
    ant_set = []
    ant_setp = []
    ancestors = []

    for k, v in abbrev_map.items():
        str1 = "(" + k + " I " + get_key(abbreviations, 'thing') + ")"
        str1p = name_sent(str1, prop_name)
        oprop_name[str1p] = str1
        ant_set.append(str1)
        ant_setp.append(str1p)
        sent1 = all_sent[possibility[0]][0] + " " + implies + " " + str1
        sent1p = all_sent[possibility[0]][2] + " " + implies + " " + str1p
        add_to_total_sent(total_sent, sent1, sent1p, "", "LE ENT")
        add_to_total_sent(total_sent, str1, str1p, "", "MP", 0, all_sent[possibility[0]][44])
        ancestors.append(str(get_sn(total_sent)))

    if len(abbrev_map.keys()) > 1:
        antecedent = " & ".join(ant_set)
        antecedentp = " & ".join(ant_setp)
        add_to_total_sent(total_sent, antecedent, antecedentp, "", "&I", ",".join(ancestors))

    return [get_sn(total_sent)]


def last_resort_axioms(j, matrix):
    global lindiv, consistent
    len_gsent = len(gsent)
    len_lsent = len(lindiv)
    len_asent = len(all_sent)
    found = False
    for e, lst in enumerate(gsent):
        if lst[0].startswith("qu"):
            v = trans_def.get(lst[0])
            k = lst[0]
            if v[0][86] == None:
                v[0][86] = 'instantiated'
                abbrev_dict = {}
                found = True

                sentences = copy.deepcopy(v[0])
                pos = mainconn(v[0][2])

                sentences[2] = sentences[2][:pos[1]] + "&" + sentences[2][pos[1] + 1:]
                m = 10
                while sentences[m] != None and sentences[m][7][-1] in ['a', 'b']:
                    for var in sentences[m][42]:
                        if sentences[m][var] not in connected_const:
                            value = abbrev_dict.get(sentences[m][var])
                            if value == None:
                                abbrev_dict.update({variables[0]: sentences[m][var]})
                                del variables[0]
                    m += 1

                consistent = change_abbrev(abbrev_dict, k, 99, [sentences[3]], trans_def, oprop_name, prop_name,
                                           all_sent, constants, prop_var, negated_conjunction, disjunction_elimination,
                                           total_sent, substitutions, variables, sentences, abbreviations, gsent, lindiv,
                                           lsent)

                for num in range(len_asent, len(all_sent)):
                    do_not_instantiate.append([num, e])

    if found:
        get_relevant_abbreviations(len_asent)
        reconfigure_matrix(j, len_asent, len_gsent, len_lsent, matrix, [])

