
from general_functions import *
import copy, re, json


all_sent = []
prop_var = []
constants = []
negated_conjunction = []
disjunction_elimination = []
total_sent = []
variables = []
sentences = []
lsent = []
gsent = []
prop_name = {}
oprop_name = {}
substitutions = {}
translations = {}
greek_english = {}
greek_english_prop = {}
abbreviations = {}
definiendum = ""
detach_type = ""
irule = ""
inference = ""
detached_prop = ""
def_prop = ""
detacher_prop = ""
consistent = True
to_be_detached = 0
detacher = 0





def get_list_of_conjuncts(sentences):
    list1 = []
    if len(sentences) > 1:
        for sentence in sentences:
            list1.append([sentence[2], sentence[3]])
        return list1
    else:
        return None


def translate_sentences(sentences):
    global detach_type, def_prop
    def_prop = sentences[2]
    kind = 'normal' if detach_type in ["detach disjunct", "disj intro", "ax ind tense"] else detach_type
    embed_hyp_abb = []

    if sentences[85] != "x":
        for lst in sentences[to_be_detached]:
            if len(lst) == 3:
                embedded_hypothetical = lst[2]
                embed_abb = embedded_hypothetical

                for greek, english in greek_english.items():
                    embedded_hypothetical = embedded_hypothetical.replace(greek, english)

                lst[2] = embedded_hypothetical

                for greek, english in greek_english_prop.items():
                    embed_abb = embed_abb.replace(greek, english)
                embed_hyp_abb.append(embed_abb)



    if kind == 'normal':
        ante_prop = sentences[7]
        con_prop = sentences[8]
    else:
        ante_prop = ""
        con_prop = ""
        j = 70
        disjuncts = []
        while sentences[j] != None:
            disjuncts.append(sentences[j][2])
            j += 1

    for k, v in greek_english.items():
        sentences[2] = sentences[2].replace(k, v)
        if detach_type == 'disj intro':
            sentences[79][0][1] = sentences[79][0][1].replace(k, v)

        if kind == 'normal':
            sentences[7] = sentences[7].replace(k, v)
            sentences[8] = sentences[8].replace(k, v)
        else:
            j = 70
            while sentences[j] != None:
                sentences[j][2] = sentences[j][2].replace(k, v)
                sentences[j][4] = get_list_of_conjuncts(sentences[j][5])
                j += 1

    detach_disjuncts = []
    for lst in sentences[79]:
        if lst[1] != con_prop:
            detach_disjuncts.append(copy.deepcopy(lst[1]))

    for k, v in greek_english_prop.items():
        def_prop = def_prop.replace(k, v)
        if detach_type == 'disj intro':
            sentences[84][0][2] = sentences[84][0][2].replace(k, v)

        if kind == 'normal':
            ante_prop = ante_prop.replace(k, v)
            con_prop = con_prop.replace(k, v)
        else:
            for m, sent in enumerate(disjuncts):
                disjuncts[m] = sent.replace(k, v)
                sentences[70 + m][3] = disjuncts[m]

    sentences[83] = embed_hyp_abb


    return get_inferences(ante_prop, con_prop)


def get_inferences(ante_prop, con_prop):
    global inference, detached_prop, detacher_prop
    tvalue = ""
    double_neg = False
    if to_be_detached == 5:
        detached_prop = con_prop
        detacher_prop = ante_prop
        if not one_sentence(con_prop):
            tvalue = ""
        else:
            sent_pos = sentences[5][0][1][0]
            tvalue = sentences[sent_pos][3]

    elif to_be_detached == 4:
        detached_prop = ante_prop
        detacher_prop = con_prop
        if one_sentence(ante_prop) and sentences[5] != []:
            sent_pos = sentences[4][0][1][0]
            tvalue = sentences[sent_pos][3]
        else:
            tvalue = ""
    if detach_type == "exclusive disjunct":
        detacher_prop = sentences[detacher][3]
        double_neg, tvalue = pos_excl_disj_elim()
    elif detach_type == 'ax ind tense':
        tvalue = ""
        double_neg = ""
        inference = "&&"
    else:
        inference = sentences[to_be_detached + 3]
    if one_sentence(inference):
        inference = inference.replace("~ ", "")
        inference = inference.replace("~", "")
        detached_prop = detached_prop.replace("~", "")

    return tvalue, double_neg


def replace_variables(sentences, dict1, first_time=True):
    m = 10
    if not first_time:
        bb = 8
    has_propositional_variable = False
    while sentences[m] != None:

        if sentences[m][9] == mini_e and first_time:
            has_propositional_variable = True

        for n in sentences[m][42]:
            if sentences[m][n] not in constants and \
            sentences[m][n] not in abbreviations.values() and \
            sentences[m][n] not in abbreviations.keys():

                new_var = get_key(dict1, sentences[m][n])
                if new_var == None and first_time:

                    dict1.update({variables[0]: sentences[m][n]})
                    translations.update({sentences[m][n]: variables[0]})
                    sentences[m][n] = variables[0]
                    del variables[0]
                elif new_var == None and not first_time:
                    pass
                else:
                    sentences[m][n] = new_var
        m += 1

    if has_propositional_variable and first_time: sub_prop_var(dict1)


def sub_prop_var(abbrev_dict):
    m = 10
    new_abbrev_map = {}
    substitution_found = False
    while sentences[m] != None:
        if sentences[m][9] == mini_e:
            # list1 = json.loads(json.dumps(sentences[m]))
            list1 = copy.deepcopy(sentences[m])
            prop = list1[8]
            for x in [8, 9]: list1[54].remove(x)
            list1[8] = None
            list1[9] = None
            name_and_build(list1, oprop_name, prop_name)
            var = get_key(abbreviations, list1[2])

            if var != None:
                new_abbrev_map.update({var: prop})
                translation = get_key(translations, prop)
                del abbrev_dict[prop]
                del translations[translation]
                sentences[m][8] = var
                substitution_found = True

        m += 1
    if substitution_found: replace_variables(sentences, new_abbrev_map, False)


def rename_prop(sentences):
    m = 10
    while sentences[m] != None:
        name_and_build(sentences[m], oprop_name, prop_name)
        greek_english.update({sentences[m][5]: sentences[m][0]})
        greek_english_prop.update({sentences[m][5]: sentences[m][3] + sentences[m][2]})
        m += 1


def get_detach_type():
    global detacher, to_be_detached, detach_type, irule
    detach_type = "normal"
    if detacher == 99:
        detach_type = 'ax ind tense'

    elif detacher > 1 and sentences[85] == 'e':
        to_be_detached = 4
        irule = iff + "E"
        detacher = 5
        detach_type = 'disj intro'
    elif sentences[85] == 'x':
        detach_type = "exclusive disjunct"
        get_to_be_detached_num()
        irule = xorr + "E"
    elif detacher == 1:
        to_be_detached = 4
        detacher = 5
        irule = iff + "E"
    elif detacher == 0:
        to_be_detached = 5
        detacher = 4
        if sentences[5] == [] and sentences[60][1] == []:
            detach_type = 'detach disjunct'
        irule = iff + "E" if sentences[85] == 'e' else "MP"


def get_to_be_detached_num():
    global detacher, to_be_detached
    temp_num = sentences[60][detacher][0][1]
    # temp_num = list(sentences[60][detacher].values())[0]
    temp_num = temp_num[0] if isinstance(temp_num, list) else temp_num
    temp_sent = sentences[temp_num][0]
    detacher = 0
    m = 70
    while sentences[m] != None:
        for lst in sentences[m][5]:
            if lst[0] == temp_sent:
                detacher = m
                break
        m += 1
    assert detacher != 0
    m = 70
    list1 = []
    while sentences[m] != None:
        if m != detacher:
            list1.append(m)
        m += 1
    to_be_detached = list1


def change_abbrev(abbrev_dict, definiendum2, detacher3, conj_intro_pos, trans_def, oprop_name3, prop_name3, all_sent3,
                  constants3, prop_var13, negated_conjunction3, disjunction_elimination3, total_sent3, substitutions3,
                  variables13, sentences3, abbreviations3, gsent3, lindiv3, lsent3):

    global all_sent, prop_var, prop_name, oprop_name, constants, negated_conjunction
    global disjunction_elimination, total_sent, substitutions, consistent, variables
    global translations, to_be_detached, detach_type, abbreviations
    global detacher,sentences, definiendum, lsent, gsent, lindiv

    if definiendum2 in ['personhood']:
        # print ('GM')
        bb = 8

    detacher = detacher3
    all_sent = all_sent3
    prop_var = prop_var13
    prop_name = prop_name3
    oprop_name = oprop_name3
    constants = constants3
    abbreviations = abbreviations3
    negated_conjunction = negated_conjunction3
    disjunction_elimination = disjunction_elimination3
    total_sent = total_sent3
    substitutions = substitutions3
    variables = variables13
    sentences = sentences3
    lsent = lsent3
    lindiv = lindiv3
    gsent = gsent3
    instantiations = json.loads(json.dumps(abbrev_dict))
    definiendum = re.sub("[\d+,\.]", "", definiendum2)

    for k, v in abbrev_dict.items(): constants.append(k)

    get_detach_type()

    replace_variables(sentences, abbrev_dict)

    rename_prop(sentences)

    tvalue, double_neg = translate_sentences(sentences)

    build_rename_sent3(definiendum2, abbrev_dict)

    anc1 = add_untran_sent_2_tot_sent(abbrev_dict, definiendum2, sentences)

    anc2 = conj_intro(conj_intro_pos)

    if redundant(inference, detached_prop): return True

    if detach_type != 'ax ind tense':
        add_to_total_sent(total_sent, inference, detached_prop, tvalue, irule, anc1, anc2)

    consistent = check_consistency(total_sent, negated_conjunction, disjunction_elimination)
    if not consistent: return False

    append_to_excl_disj(0)

    get_detached()

    add_new_sent_to_all_sent(instantiations, trans_def)

    return consistent



# 0 disjunct with neg value
# 1 abbreviate with neg value
# 2 loop for adding to total_sent and for elimination

def append_to_excl_disj(k):
    try:
        if sentences[84][0][85] == "x" and to_be_detached == 5:
            new_sentences = copy.deepcopy(sentences[84][0])
            pass
        else:
            return
    except:
        return
    list1 = []
    m = 70
    while new_sentences[m] != None:
        list2 = []
        nat_sent = new_sentences[m][2]
        abb_sent = new_sentences[m][2]
        for sent in new_sentences[m][5]:
            # sent = copy.deepcopy(sent)
            nat_sent = nat_sent.replace(sent[5], sent[0])
            abb_sent = abb_sent.replace(sent[5], sent[3] + sent[2])
            list2.append([sent[1], sent[2], sent[3]])
        list1.append([nat_sent, abb_sent, list2, 0])
        m += 1
    disjunction_elimination.append(list1)
    check_initial_consist_excl_disj(total_sent, disjunction_elimination)

#0 disjunct with neg value
#1 abbreviate with neg value
#2 loop for adding to total_sent2 and for elimination
def check_initial_consist_excl_disj(total_sent, disjunction_elimination):
    i = len(total_sent)
    while i > -1:
        i -= 1
        if "PREM" in total_sent[i][1]:
            return
        det_abb = total_sent[i][2]
        det_abb_tv = total_sent[i][3]
        if len(det_abb) < 3 and det_abb != "":
            neg_excl_disj_elim(det_abb, det_abb_tv, i, len(disjunction_elimination) - 2, 0,
                               disjunction_elimination, total_sent, negated_conjunction)
            if not consistent:
                return



def add_untran_sent_2_tot_sent(dict1, definiendum2, sentences, ax_ind_tense=False):
    if dict1 == {}:
        return sentences[3]
    if detach_type == 'ax ind tense': ax_ind_tense = True
    anc1 = sentences[3]
    rule = "SUBJ" if not ax_ind_tense else "AY IDT"
    assert anc1 != None
    anc2 = get_sn(total_sent)
    if detach_type == 'disj intro':
        add_to_total_sent(total_sent, sentences[79][0][1], sentences[84][0][2], "", "SUBJ", anc1 + 1, 0)
        anc2 = get_sn(total_sent)
    add_to_total_sent(total_sent, sentences[2], def_prop, "", rule, anc1, anc2)
    substitutions.setdefault(definiendum2, []).append(total_sent[-1])
    return get_sn(total_sent)


def get_detached():
    global inference
    if detach_type == "exclusive disjunct":
        num = to_be_detached[0]
        if len(to_be_detached) == 1 and len(sentences[num][5]) == 1:
            raise Exception ("this converts a string into a list")
            new_sent = sentences[num][5][0]
            new_sent[3] = "~"
            name_and_build(prop_name, oprop_name, new_sent)


        else:
            inference = "&&"


def pos_excl_disj_elim():
    global inference, detached_prop
    list1 = []
    list2 = []
    double_neg = False
    j = 70
    while sentences[j] != None:
        if j != detacher:
            if len(sentences[j][5]) > 1:
                negated_conjunction.append([sentences[j][4],
                                            "~" + sentences[j][2], "~" + sentences[j][3], []])
            else:
                if sentences[j][5][0][3] == "~":
                    double_neg = True
                else:
                    double_neg = False
            list1.append(sentences[j][2])
            list2.append(sentences[j][3])
        j += 1

    if len(list1) == 1:
        inference = list1[0]
        detached_prop = list2[0]
        return  double_neg, "~"
    else:
        list3 = []
        list4 = []
        for e, sent in enumerate(list1):
            list3.append("~" + sent)
            list4.append("~" + list2[e])
        inference = " & ".join(list3)
        detached_prop = " & ".join(list4)

        return double_neg, ""


def convert_sets_of_conditions(list_of_dictionaries, dict1):
    for dict2 in list_of_dictionaries:
        for k, v in dict2.items():
            for s, old_num in enumerate(v):
                new_num = dict1.get(old_num)
                v[s] = new_num


def build_rename_sent3(definiendum2, dict1):
    if dict1 == {}: return
    str2 = " ".join(["(" + build_connection(v, mini_c, k) + ")" for k, v in dict1.items()])
    add_to_total_sent(total_sent, str2, "", "", "IN")
    if definiendum != "": substitutions.setdefault(definiendum2, []).append(total_sent[-1])


def get_parent_disjunct(conjunct, conj_intro_pos, i):
    for lst in total_sent:
        if xorr in lst[2] and conjunct in lst[2]:
            conj_intro_pos[i] = lst[0]
            return True
    return False


def conj_intro(conj_intro_pos):
    if detach_type == 'ax ind tense': return conj_intro_pos[0]
    greek_detacher = sentences[detacher + 3] if detacher < 70 else sentences[detacher][2]
    qn = conj_intro_pos[0]
    if len(conj_intro_pos) > 1:
        list1 = ["", "", "", ""]
        qn = get_sn(total_sent)
        disj_found = False
        for i, num in enumerate(conj_intro_pos):
            tot_sent_pos = findposinmd(num, total_sent, 0)
            conjunct = total_sent[tot_sent_pos][2]
            assert conjunct in def_prop
            if detach_type == 'disj intro' and not disj_found:
                disj_found = get_parent_disjunct(conjunct, conj_intro_pos, i)
            if len(conj_intro_pos) < 3:
                list1[i] = conj_intro_pos[i]

        if len(conj_intro_pos) > 2:
            bb = 8

            list2 = [str(x) for x in conj_intro_pos]
            str1 = ",".join(list2)
            add_to_total_sent(total_sent, greek_detacher, detacher_prop, "", "&I", str1)
        else:
            add_to_total_sent(total_sent, greek_detacher, detacher_prop, "", "&I", list1[0], list1[1])

        if detach_type == 'disj intro':
            assert disj_found

    return qn


def redundant(inference, tvalue, conj_elim = ""):
    pos = find_2posinlist(inference, tvalue, total_sent, 2, 3)
    if pos > -1:
        if conj_elim == 'conj_elim':
            return True
        else:
            raise Exception ('check this')
            del total_sent[-1]
            del total_sent[-1]
            return True


def add_new_sent_to_all_sent(instantiations, trans_def):
    global to_be_detached
    if detach_type == 'ax ind tense':
        for lst in sentences[4]:
            sentences[5].append(lst)
        to_be_detached = 5

    if detach_type not in ["exclusive disjunct", 'detach disjunct'] \
        and len(list(sentences[to_be_detached])) > 1:
        conjunction_elimination(instantiations, trans_def)
    elif one_sentence(inference):
        num = sentences[to_be_detached][0][1]
        sentences[num[0]][44] = get_sn(total_sent)
        sentences[num[0]][7] = "c"
        all_sent.append(sentences[num[0]])
        lsent.setdefault(sentences[to_be_detached][0][0], []).append([len(all_sent)-1])
        lindiv.append(sentences[to_be_detached][0][0])
        embedded_inference(num[0])
    elif detach_type == "exclusive disjunct" and len(to_be_detached) > 1:
        conjunction_elimination(instantiations, trans_def)
    elif detach_type == "detach disjunct" or len(sentences[to_be_detached]) == 1:
        definiendum3 = sentences[84][0][81]
        trans_def[definiendum3] = [sentences[84][0]]
        sentences[84][0][3] = get_sn(total_sent)
        done = universal_negations(sentences[84][0], abbreviations, gsent, trans_def, definiendum3)
        if not done:
            if definiendum3 == '2.2.1,individual':
                bb = 8
            gsent.append([definiendum3, sentences[84][0][60]])
            axiom_of_indicative_tense(instantiations)


def embedded_inference(pos):
    global consistent
    sent = sentences[pos]
    if sent[9] == mini_e:
        assert one_sentence(sent[0])
        list1 = copy.deepcopy(sentences[pos])
        for x in [8, 9]: list1[54].remove(x)
        list1[42].remove(8)
        for x in [8, 9]: list1[x] = None
        name_and_build(list1, oprop_name, prop_name)
        add_to_total_sent(total_sent, list1[0], list1[2], list1[3], mini_e + "E", 0)
        list1[44] = get_sn(total_sent)
        list1[7] = "c"
        all_sent.append(list1)
        lsent.setdefault(sentences[to_be_detached][0][0], []).append([len(all_sent)-1])
        lindiv.append(sentences[to_be_detached][0][0])
        consistent = check_consistency(total_sent, negated_conjunction, disjunction_elimination)


def conjunction_elimination(instantiations, trans_def):
    global consistent
    ancestor = get_sn(total_sent)
    if sentences[7] == '(e FF b)':
        bb = 8

    if detach_type != "exclusive disjunct":
        range1 = [x for x in range(len(sentences[to_be_detached]))]
    else:
        range1 = to_be_detached

    if detach_type == 'exclusive disjunct':
        for k in range1:
            embedded_inference(k)
            sent = sentences[k]
            if len(sent[5]) == 1:
                add_to_total_sent(total_sent, sent[5][0][0], sent[5][0][3] + sent[5][0][2], "~", "&E", ancestor)
                consistent = check_consistency(total_sent, negated_conjunction, disjunction_elimination)
                if not consistent: return

                if sent[5][0][2] == "~":
                    raise Exception("double neg")
            else:
                add_to_total_sent(total_sent, sent[2], sent[3], "~", "&E", ancestor, "")
                consistent = check_consistency(total_sent, negated_conjunction, disjunction_elimination)
                if not consistent: return


    else:
        q = -1
        for lst in sentences[to_be_detached]:
            q += 1
            k = lst[0]
            v = lst[1]

            if len(v) == 1:
                v = v[0]
                is_redundant = redundant(sentences[v][2], sentences[v][3], "conj_elim")
                if not is_redundant:
                    add_to_total_sent(total_sent, sentences[v][1], sentences[v][2], sentences[v][3], "&E", ancestor)
                    consistent = check_consistency(total_sent, negated_conjunction, disjunction_elimination)
                    if not consistent: return
                    sentences[v][44] = get_sn(total_sent)
                    sentences[v][7] = "c"
                    all_sent.append(sentences[v])
                    lindiv.append(k)
                    lsent.setdefault(k, []).append([len(all_sent)-1])
                    embedded_inference(v)

            else:
                new_sent_type = sentences[84][0][82]
                new_temp_list = []
                new_sent = sentences[84][0]
                m = 10
                n = 0
                while new_sent[m] != None:
                    new_sent[m][7] = new_sent_type[n]
                    new_sent[m][44] = get_sn(total_sent) + 1
                    all_sent.append(new_sent[m])
                    new_temp_list.append(len(all_sent)-1)
                    m += 1
                    n += 1
                trans_def[v[0]] = [new_sent]
                gsent_key = sentences[to_be_detached][q][1][0]
                lsent_key = sentences[to_be_detached][q][0][0]
                lindiv.append(lsent_key)
                lsent.setdefault(lsent_key, []).append(new_temp_list)
                done = universal_negations(sentences[84][0], abbreviations, gsent, trans_def, gsent_key)
                if not done:
                    gsent_value = sentences[to_be_detached][q][1][1]
                    if gsent_key == '2.2.1,individual':
                        bb = 8
                    gsent.append([gsent_key, gsent_value])
                    axiom_of_indicative_tense(instantiations)
                add_to_total_sent(total_sent, lst[2], sentences[83][0], "", "&E", ancestor)
                del sentences[83][0]

def already_exists(sentences):
    if sentences[10][13] == 'I':
        b = find_2posinlist(sentences[10][13], sentences[10][14], all_sent, 13, 14)
        if b > -1:
            return True
    elif sentences[10][13] == 'W':
        b = find_2posinlist(sentences[10][13], sentences[10][10], all_sent, 13, 10)
        if b > -1:
            return True
    return False





def axiom_of_indicative_tense(instantiations):
    global consistent, sentences


    if not already_exists(sentences[84][0]) and not sentences[84][0][85] == 'x'\
            and 'KN' not in sentences[84][0][81]:
        
        sentences = copy.deepcopy(sentences[84][0])

        for k, v in instantiations.items(): instantiations[k] = k

        pos = mainconn(sentences[2])

        sentences[2] = sentences[2][:pos[1]] + "&" + sentences[2][pos[1] + 1:]

        replace_variables(sentences, instantiations)

        rename_prop(sentences)

        _, _ = translate_sentences(sentences)

        build_rename_sent3(sentences[81], instantiations)

        add_untran_sent_2_tot_sent(instantiations, sentences[81], sentences, True)

        consistent = conjunction_elimination2(sentences)

        return



def conjunction_elimination2(sentences):
    global consistent
    m = 10
    ancestor = get_sn(total_sent)
    while sentences[m] != None:
        if sentences[m][56] in ['cf', "cq", "b", "cb", "q", "a", 'f']:
            k = sentences[m][58]
            add_to_total_sent(total_sent, sentences[m][1], sentences[m][2], sentences[m][3], "&E", ancestor)
            consistent = check_consistency(total_sent, negated_conjunction, disjunction_elimination)
            if not consistent: return
            sentences[m][44] = get_sn(total_sent)
            sentences[m][7] = "c"
            all_sent.append(sentences[m])
            lindiv.append(k)
            lsent.setdefault(k, []).append([len(all_sent)-1])
        else:
            raise Exception ('you havent coded for this yet')
        m += 1

    return True

