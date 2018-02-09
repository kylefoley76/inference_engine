from general_functions import *
import copy, re, json

sentences = []
disjuncts = []
disjuncts_abb = []
translations = {}
greek_english = {}
greek_english_prop = {}
definiendum = ""
detach_type = ""
irule = ""
inference = ""
detached_prop = ""
def_prop = ""
detacher_prop = ""
new_definition = ""
natural_detacher = ""
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


def translate_sentences():
    global detach_type, def_prop, inference, natural_detacher
    global disjuncts, disjuncts_abb, new_definition
    def_prop = cls.def_stats.tot_greek_sent
    new_definition = cls.def_stats.tot_greek_sent
    kind = 'exclusive disjunct' if detach_type == 'exclusive disjunct' else "normal"
    if to_be_detached == 1:
        idx = cls.def_stats.con_index
    elif to_be_detached == 0:
        idx = cls.def_stats.ant_index

    disjuncts = []
    disjuncts_abb = []
    for disjunct in cls.def_stats.natural_disjuncts:
        if disjunct != 0:
            disjuncts.append(json.loads(json.dumps(disjunct[1])))
            disjuncts_abb.append(json.loads(json.dumps(disjunct[1])))

    if kind in 'normal':
        ante_prop = cls.def_stats.ant_greek
        natural_ante = cls.def_stats.ant_greek
        con_prop = cls.def_stats.con_greek
        natural_con = cls.def_stats.con_greek

    for k, v in greek_english.items():
        new_definition = new_definition.replace(k, v)
        if kind == 'normal':
            natural_ante = natural_ante.replace(k, v)
            natural_con = natural_con.replace(k, v)

        for e, disjunct in enumerate(disjuncts):
            disjuncts[e] = disjunct.replace(k, v)

    for k, v in greek_english_prop.items():
        def_prop = def_prop.replace(k, v)
        if kind == 'normal':
            ante_prop = ante_prop.replace(k, v)
            con_prop = con_prop.replace(k, v)

        for e, disjunct_abb in enumerate(disjuncts_abb):
            disjuncts_abb[e] = disjunct_abb.replace(k, v)

    if detacher == 0:
        inference = natural_con
        natural_detacher = natural_ante
    elif detacher > 0:
        inference = natural_ante
        natural_detacher = natural_con

    return get_inferences(ante_prop, con_prop, idx)


def get_inferences(ante_prop, con_prop, idx):
    global inference, detached_prop, detacher_prop, to_be_detached
    tvalue = ""
    double_neg = False
    if to_be_detached == 1:
        to_be_detached = cls.def_stats.con_index
        detached_prop = con_prop
        detacher_prop = ante_prop
        if not one_sentence(con_prop):
            tvalue = ""
        else:
            tvalue = sentences[idx[0]][3]

    elif to_be_detached == 0:
        to_be_detached = cls.def_stats.ant_index
        detached_prop = ante_prop
        detacher_prop = con_prop
        if one_sentence(ante_prop) and len(idx) == 1:
            tvalue = sentences[idx[0]][3]
        else:
            tvalue = ""

    if detach_type == 'ax ind tense':
        tvalue = ""
        double_neg = ""
        inference = "&&"
    elif one_sentence(inference):
        inference = inference.replace("~ ", "")
        inference = inference.replace("~", "")
        detached_prop = detached_prop.replace("~", "")

    return tvalue, double_neg


def replace_variables(sentences, dict1, first_time=True):
    if not first_time:
        bb = 8
    has_propositional_variable = False
    for sentence in sentences:

        if sentence[9] == mini_e and first_time:
            has_propositional_variable = True

        for n in sentence[42]:

            if sentence[n] == "f" + l1:
                bb = 8

            if sentence[n] not in output[10] and \
                    sentence[n] not in output[6].values() and \
                    sentence[n] not in output[6].keys():

                new_var = get_key(dict1, sentence[n])
                if new_var == None and first_time:

                    dict1.update({output[14][0]: sentence[n]})
                    translations.update({sentence[n]: output[14][0]})
                    sentence[n] = output[14][0]
                    del output[14][0]
                elif new_var == None and not first_time:
                    pass
                else:
                    sentence[n] = new_var

    if has_propositional_variable and first_time: sub_prop_var(dict1)


def sub_prop_var(abbrev_dict):
    new_abbrev_map = {}
    substitution_found = False
    for sentence in sentences:
        if sentence[9] == mini_e:
            list1 = copy.deepcopy(sentence)
            prop = list1[8]
            for x in [8, 9]: list1[54].remove(x)
            list1[8] = None
            list1[9] = None
            name_and_build(output, list1)
            var = get_key(output[6], list1[2])

            if var != None:
                new_abbrev_map.update({var: prop})
                translation = get_key(translations, prop)
                del abbrev_dict[prop]
                del translations[translation]
                sentence[8] = var
                substitution_found = True

    if substitution_found: replace_variables(sentences, new_abbrev_map, False)


def rename_prop(sentences):
    for sentence in sentences:
        name_and_build(output, sentence)
        greek_english.update({sentence[5]: sentence[0]})
        greek_english_prop.update({sentence[5]: sentence[3] + sentence[2]})


def get_detach_type():
    global detacher, to_be_detached, detach_type, irule
    detach_type = "normal"
    if detacher == 99:
        detach_type = 'ax ind tense'

    elif cls.def_stats.connection_type == 'x':
        detach_type = "exclusive disjunct"
        get_to_be_detached_num()
        irule = xorr + "E"
    elif detacher > 1:
        to_be_detached = 0
        irule = iff + "E"
        if not cls.def_stats.consequent_disjunct:
            detach_type = 'disj intro'
        else:
            detach_type = 'whole disj intro'

    elif detacher == 1:
        to_be_detached = 0
        irule = iff + "E"
    elif detacher == 0:
        to_be_detached = 1
        if cls.def_stats.consequent_disjunct:
            detach_type = 'detach disjunct'
        irule = iff + "E" if cls.def_stats.connection_type == 'e' else "MP"


def get_to_be_detached_num():
    global detacher, to_be_detached
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


def change_abbrev(abbrev_dict, cls2, conj_intro_pos, output2):
    global translations, to_be_detached, detach_type, cls
    global detacher, sentences, definiendum, output, consistent

    cls = cls2
    output = output2
    definiendum = cls.def_stats.def_word
    sentences = json.loads(json.dumps(cls.sentences))
    detacher = cls.def_stats.detacher
    definiendum2 = definiendum + str(cls.def_stats.def_number)

    if definiendum in ['natural' + ur, 'INM']:
        bb = 8

    for k, v in abbrev_dict.items(): output[10].append(k)

    get_detach_type()

    replace_variables(sentences, abbrev_dict)

    rename_prop(sentences)

    tvalue, double_neg = translate_sentences()

    build_rename_sent3(definiendum2, abbrev_dict)

    anc1 = add_untran_sent_2_tot_sent(abbrev_dict, definiendum2, conj_intro_pos)

    anc2 = conj_intro(conj_intro_pos)

    if redundant(tvalue): return True

    if detach_type != 'ax ind tense':
        add_to_tsent(output[0], inference, detached_prop, tvalue, irule, anc1, anc2)

    consistent = check_consistency(output)
    if not consistent: return False

    append_to_excl_disj()

    get_detached()

    add_new_sent_to_asent()

    return consistent


# 0 disjunct with neg value
# 1 abbreviate with neg value
# 2 loop for adding to output[0] and for elimination

def append_to_excl_disj():
    if cls.def_stats.consequent_disjunct and detacher == 0:
        new_cls = cls.embeds.get("1.2")
        new_cls.sentences = sentences
        definiendum3 = "1.2" + "," + definiendum
        output[15].update({definiendum3 + "0": new_cls})
        add_to_gsent([new_cls], output, definiendum3)
        list1 = []
        for disjunct in cls.disjuncts:
            nat_sent = disjunct.tot_greek
            abb_sent = disjunct.tot_greek
            list2 = []
            idx = disjunct.index1
            for num in idx:
                if isinstance(num, int):
                    list2.append([sentences[num][1], sentences[num][2], sentences[num][3]])
                    nat_sent = nat_sent.replace(sentences[num][5], sentences[num][0])
                    abb = sentences[num][3] + sentences[num][2]
                    abb_sent = abb_sent.replace(sentences[num][5], abb)
            list1.append([nat_sent, abb_sent, list2, 0])
        output[12].append(list1)
        check_initial_consist_excl_disj(output)


# 0 disjunct with neg value
# 1 abbreviate with neg value
# 2 loop for adding to output[0]2 and for elimination
def check_initial_consist_excl_disj(output):
    i = len(output[0])
    while i > -1:
        i -= 1
        if "PREM" in output[0][i][1]:
            return
        det_abb = output[0][i][2]
        det_abb_tv = output[0][i][3]
        if len(det_abb) < 3 and det_abb != "":
            neg_excl_disj_elim(det_abb, det_abb_tv, output, i, len(output[12]) - 2, 0)
            if not consistent:
                return

    pos_excl_disj_elim()


def adjust_conj_intro(conj_intro_pos, disjunct_abb):
    for lst in output[0]:
        if lst[2] in disjunct_abb and xorr not in lst[2]:
            conj_intro_pos.remove(lst[0])
            break


def add_untran_sent_2_tot_sent(dict1, definiendum2, conj_intro_pos, ax_ind_tense=False):
    if dict1 == {}:
        return cls.def_stats.tot_sent_idx
    if detach_type == 'ax ind tense': ax_ind_tense = True
    anc1 = cls.def_stats.tot_sent_idx
    anc4 = anc1 + 1
    rule = "SUBJ" if not ax_ind_tense else "AY IDT"
    assert anc1 != None
    anc2 = get_sn(output[0])
    if detach_type == 'disj intro':
        anc3 = anc1
        anc1 -= 1
        b = 0
        for disjunct, disjunct_abb in zip(disjuncts, disjuncts_abb):
            adjust_conj_intro(conj_intro_pos, disjunct_abb)
            add_to_tsent(output[0], disjunct, disjunct_abb, "", "SUBJ", anc3 + b, anc2)
            conj_intro_pos.append(get_sn(output[0]))
            b += 1

    add_to_tsent(output[0], new_definition, def_prop, "", rule, anc1, anc2)
    output[13].setdefault(definiendum2, []).append(output[0][-1])
    anc1 = get_sn(output[0])
    if detach_type == 'whole disj intro':
        add_to_tsent(output[0], natural_detacher, detacher_prop, "", rule, anc4, anc2)
        output[13].setdefault(xorr + " " + definiendum, []).append(output[0][-1])
        anc1 = get_sn(output[0]) - 1

    return anc1


def get_detached():
    global inference
    if detach_type == "exclusive disjunct":
        num = to_be_detached[0]
        if len(to_be_detached) == 1 and len(sentences[num][5]) == 1:
            raise Exception("this converts a string into a list")
            new_sent = sentences[num][5][0]
            new_sent[3] = "~"
            name_and_build(output, output[8])


        else:
            inference = "&&"


def pos_excl_disj_elim():
    for lst in output[12]:
        next_disjunct = False
        for e, lst2 in enumerate(lst):
            temp_disjuncts = json.loads(json.dumps(lst2[2]))
            for sent in lst2[2]:
                if next_disjunct:
                    break
                for lst1 in output[0]:
                    if lst1[2] == sent[1] and sent[2] == lst1[3]:
                        del temp_disjuncts[0]
                        if temp_disjuncts == []:
                            detach_disjunct(lst, e)

                        break
                else:
                    next_disjunct = True
    else:
        return True


def detach_disjunct(lst2, e):
    for f, disjunct in enumerate(lst2):
        list1 = []
        if f != e:
            for conjunct in disjunct[2]:
                list1.append([conjunct[1], conjunct[2], get_sn(output[0])])
            check_intitial_neg_conj_consist(list1)
            output[11].append(list1)


def check_intitial_neg_conj_consist(list1):
    list2 = json.loads(json.dumps(list1))
    for e, lst in enumerate(list1):
        for tot_sent in output[0]:
            if tot_sent[2] == lst[0] and tot_sent[3] == lst[1]:
                del list2[0]
                if list2 == []:
                    return
    return


def build_rename_sent3(definiendum2, dict1):
    if dict1 == {}: return
    str2 = " ".join(["(" + build_connection(v, mini_c, k) + ")" for k, v in dict1.items()])
    add_to_tsent(output[0], str2, "", "", "IN")

    if definiendum != "":
        output[13].setdefault(definiendum2, []).append(output[0][-1])
        if detach_type == 'whole disj intro':
            output[13].setdefault(xorr + " " + definiendum, []).append(output[0][-1])


def conj_intro(conj_intro_pos):
    if detach_type == 'ax ind tense': return conj_intro_pos[0]
    qn = conj_intro_pos[0]
    if len(conj_intro_pos) > 1:
        list1 = ["", "", "", ""]
        for i, num in enumerate(conj_intro_pos):
            tot_sent_pos = findposinmd(num, output[0], 0)
            conjunct = output[0][tot_sent_pos][2]
            assert conjunct in detacher_prop
            if len(conj_intro_pos) < 3:
                list1[i] = conj_intro_pos[i]

        if len(conj_intro_pos) > 2:
            list2 = [str(x) for x in conj_intro_pos]
            str1 = ",".join(list2)
            add_to_tsent(output[0], natural_detacher, detacher_prop, "", "&I", str1)

        else:
            add_to_tsent(output[0], natural_detacher, detacher_prop, "", "&I", list1[0], list1[1])
        qn = get_sn(output[0])

    if detach_type == 'whole disj intro':
        qn = get_sn(output[0])

    return qn


def redundant(tvalue, conj_elim=""):
    pos = find_2posinlist(detached_prop, tvalue, output[0], 2, 3)
    if pos > -1:
        if conj_elim == 'conj_elim':
            return True
        else:
            del output[0][-1]
            del output[0][-1]
            return True


def add_new_sent_to_asent():
    global to_be_detached
    if detach_type == 'ax ind tense':
        for lst in sentences[4]:
            sentences[5].append(lst)
        to_be_detached = 5

    mainc, _ = mainconn(detached_prop[1:-1])

    if mainc == "&":
        conjunction_elimination()
    elif one_sentence(inference):
        sentence = sentences[to_be_detached[0]]
        sentence[44] = get_sn(output[0])
        sentence[7] = "c"
        if sentence[58] == "I":
            sentence[58] = determine_constants(output[6], sentence)

        output[1].append(sentence)
        output[5].setdefault(sentence[58], []).append([len(output[1]) - 1])
        output[4].append(sentence[58])
        embedded_inference(sentence)
    elif detach_type == "exclusive disjunct" and len(to_be_detached) > 1:
        conjunction_elimination()
    elif detach_type != "detach disjunct":
        if detacher == 0:
            embed_num = cls.def_stats.con_hnum[0]
        else:
            embed_num = cls.def_stats.ant_hnum[0]
        embed = cls.embeds.get(embed_num)
        embed.sentences = sentences
        definiendum3 = embed.def_stats.def_word
        output[15].update({definiendum3 + "0": embed})
        done = universal_negations(output, embed)
        if done == 'not done':
            add_to_gsent([embed], output, definiendum3)
            # axiom_of_indicative_tense(instantiations)


def embedded_inference(sent):
    global consistent
    if sent[9] == mini_e:
        assert one_sentence(sent[0])
        list1 = json.loads(json.dumps(sent))
        for x in [8, 9]: list1[54].remove(x)
        list1[42].remove(8)
        for x in [8, 9]: list1[x] = None
        name_and_build(output, list1)
        add_to_tsent(output[0], list1[0], list1[2], list1[3], mini_e + "E", 0)
        list1[44] = get_sn(output[0])
        list1[7] = "c"
        const = determine_constants(output[6], list1)
        output[1].append(list1)
        output[5].setdefault(const, []).append([len(output[1]) - 1])
        output[4].append(const)
        consistent = check_consistency(output)


def conjunction_elimination():
    global consistent
    ancestor = get_sn(output[0])
    b = 0

    if detach_type == 'exclusive disjunct':
        for k in to_be_detached:
            embedded_inference(k)
            sent = sentences[k]
            if len(sent[5]) == 1:
                add_to_tsent(output[0], sent[5][0][0], sent[5][0][3] + sent[5][0][2], "~", "&E", ancestor)
                consistent = check_consistency(output)
                if not consistent: return

                if sent[5][0][2] == "~":
                    raise Exception("double neg")
            else:
                add_to_tsent(output[0], sent[2], sent[3], "~", "&E", ancestor, "")
                consistent = check_consistency(output)
                if not consistent: return


    else:
        q = -1
        for lst in to_be_detached:
            q += 1

            v = lst[1]

            if isinstance(lst, int):
                k = lst
                v = v[0]
                is_redundant = redundant(sentences[v][3], "conj_elim")
                if not is_redundant:
                    add_to_tsent(output[0], sentences[v][1], sentences[v][2], sentences[v][3], "&E", ancestor)
                    consistent = check_consistency(output)
                    if not consistent: return
                    sentences[v][44] = get_sn(output[0])
                    sentences[v][7] = "c"
                    const = determine_constants(output[6], sentences[v])
                    sentences[v][58] = const
                    output[1].append(sentences[v])
                    output[4].append(const)
                    output[5].setdefault(const, []).append([len(output[1]) - 1])
                    embedded_inference(v)

            else:
                if detacher == 1:
                    nat_greek = cls.def_stats.ant_comp_greek[b]
                    hnum = cls.def_stats.ant_hnum[b]
                    lsent_key = cls.def_stats.ant_comp_const[b]
                else:
                    nat_greek = cls.def_stats.con_comp_greek[b]
                    hnum = cls.def_stats.con_hnum[b]
                    lsent_key = cls.def_stats.con_comp_const[b]
                b += 1

                greek_abb = nat_greek

                for k, v in greek_english.items():
                    nat_greek = nat_greek.replace(k, v)
                for k, v in greek_english_prop.items():
                    greek_abb = greek_abb.replace(k, v)
                add_to_tsent(output[0], nat_greek, greek_abb, "", "&E", ancestor)

                new_cls = cls.embeds.get(hnum)
                new_cls.sentences = sentences
                gsent_key = new_cls.def_stats.def_word
                output[15].update({gsent_key: new_cls})
                add_to_gsent([new_cls], output)
                output[4].append(lsent_key)
                output[5].setdefault(lsent_key, []).append(lst)
                universal_negations(output, new_cls)


def already_exists(sentences):
    if sentences[10][13] == 'I':
        b = find_2posinlist(sentences[10][13], sentences[10][14], output[1], 13, 14)
        if b > -1:
            return True
    elif sentences[10][13] == 'W':
        b = find_2posinlist(sentences[10][13], sentences[10][10], output[1], 13, 10)
        if b > -1:
            return True
    return False


def axiom_of_indicative_tense(instantiations):
    global consistent, sentences

    if not already_exists(sentences[84][0]) and not sentences[84][0][85] == 'x' \
            and 'KN' not in sentences[84][0][81]:

        sentences = copy.deepcopy(sentences[84][0])

        for k, v in instantiations.items(): instantiations[k] = k

        pos = mainconn(sentences[2])

        sentences[2] = sentences[2][:pos[1]] + "&" + sentences[2][pos[1] + 1:]

        replace_variables(sentences, instantiations)

        rename_prop(sentences)

        _, _ = translate_sentences()

        build_rename_sent3(sentences[81], instantiations)

        add_untran_sent_2_tot_sent(instantiations, sentences[81], True)

        consistent = conjunction_elimination2(sentences)

        return


def conjunction_elimination2(sentences):
    global consistent
    m = 10
    ancestor = get_sn(output[0])
    while sentences[m] != None:
        if sentences[m][56] in ['cf', "cq", "b", "cb", "q", "a", 'f']:
            add_to_tsent(output[0], sentences[m][1], sentences[m][2], sentences[m][3], "&E", ancestor)
            consistent = check_consistency(output)
            if not consistent: return
            sentences[m][44] = get_sn(output[0])
            sentences[m][7] = "c"
            const = determine_constants(output[6], sentences[m])
            sentences[m][58] = const
            output[1].append(sentences[m])
            output[4].append(const)
            output[5].setdefault(const, []).append([len(output[1]) - 1])
        else:
            raise Exception('you havent coded for this yet')
        m += 1

    return True
