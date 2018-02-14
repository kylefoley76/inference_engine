from general_functions import *
import copy, json

def get_list_of_conjuncts(sentences):
    list1 = []
    if len(sentences) > 1:
        for sentence in sentences:
            list1.append([sentence[2], sentence[3]])
        return list1
    else:
        return None


def translate_excl_disj():
    global def_prop, new_definition, inference, detached_prop
    global natural_detacher, detacher_prop
    if detach_type != 'exclusive disjunct':
        return 0, 0, 0
    inferences = []
    neg_conj = []
    new_definition = cls.def_stats.tot_greek_sent
    def_prop = new_definition
    inferencesp = []
    for e, disjunct in enumerate(cls.disjuncts):
        if e + 2 != detacher:
            nat_disj = disjunct.tot_greek
            abb_disj = disjunct.tot_greek
            for k, v in greek_english.items():
                nat_disj = nat_disj.replace(k, v)
                new_definition = new_definition.replace(k, v)

            for k, v in greek_english_prop.items():
                abb_disj = abb_disj.replace(k, v)
                def_prop = def_prop.replace(k, v)
            list1 = []
            for num in disjunct.index1:
                if len(disjunct.index1) == 1:
                    list1.append(num)
                elif isinstance(num, int):
                    list1.append([sentences[num][2], sentences[num][3], 0])
                else:
                    raise Exception
            neg_conj.append(list1)

            if not one_sentence(nat_disj):
                nat_disj = "~" + nat_disj
                abb_disj = "~" + abb_disj
            else:
                nat_disj = "~" + nat_disj
                abb_disj = "~" + abb_disj

            inferences.append(nat_disj)
            inferencesp.append(abb_disj)

        else:
            natural_detacher = disjunct.tot_greek
            detacher_prop = disjunct.tot_greek
            for k, v in greek_english.items():
                natural_detacher = natural_detacher.replace(k, v)

            for k, v in greek_english_prop.items():
                detacher_prop = detacher_prop.replace(k, v)

    if len(inferences) == 1:
        tvalue = "~"
        inference = inferences[0][1:]
        detached_prop = inferencesp[0][1:]
    else:
        tvalue = ""
        inference = " & ".join(inferences)
        detached_prop = " & ".join(inferencesp)

    inferences2 = []
    for x, y in zip(inferences, inferencesp):
        inferences2.append([x, y])

    return neg_conj, inferences2, tvalue


def translate_sentences(tvalue):
    global detach_type, def_prop, inference, natural_detacher
    global disjuncts, disjuncts_abb, new_definition
    if detach_type == 'exclusive disjunct':
        return tvalue, ""
    new_definition = cls.def_stats.tot_greek_sent
    def_prop = cls.def_stats.tot_greek_sent

    if to_be_detached == 1:
        idx = cls.def_stats.con_index
    elif to_be_detached == 0 or detach_type == 'ax ind tense':
        new_definition = change_connective()
        def_prop = new_definition
        idx = cls.def_stats.ant_index

    disjuncts = []
    disjuncts_abb = []
    for disjunct in cls.def_stats.natural_disjuncts:
        if disjunct != 0:
            disjuncts.append(json.loads(json.dumps(disjunct[1])))
            disjuncts_abb.append(json.loads(json.dumps(disjunct[1])))

    ante_prop = cls.def_stats.ant_greek
    natural_ante = cls.def_stats.ant_greek
    con_prop = cls.def_stats.con_greek
    natural_con = cls.def_stats.con_greek

    for k, v in greek_english.items():
        new_definition = new_definition.replace(k, v)
        natural_ante = natural_ante.replace(k, v)
        natural_con = natural_con.replace(k, v)

        for e, disjunct in enumerate(disjuncts):
            disjuncts[e] = disjunct.replace(k, v)

    for k, v in greek_english_prop.items():
        def_prop = def_prop.replace(k, v)
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
            for x in sentences[idx[0]][42]:
                if sentences[idx[0]][x] not in output[10]:
                    output[10].append(sentences[idx[0]][x])

    elif to_be_detached == 0:
        to_be_detached = cls.def_stats.ant_index
        detached_prop = ante_prop
        detacher_prop = con_prop
        if one_sentence(ante_prop) and len(idx) == 1:
            for x in sentences[idx[0]][42]:
                if sentences[idx[0]][x] not in output[10]:
                    output[10].append(sentences[idx[0]][x])
            tvalue = sentences[idx[0]][3]
        else:
            tvalue = ""

    if one_sentence(inference):
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
    if detach_type != 'ax ind tense':
        detach_type = "normal"
    else:
        return

    if cls.def_stats.connection_type == 'x':
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
    j = detacher - 2
    b = len(cls.disjuncts)
    to_be_detached = [x for x in range(b)]
    to_be_detached.remove(j)


def change_abbrev(abbrev_dict, cls2, conj_intro_pos, output2, detach_type2 = ""):
    global translations, to_be_detached, detach_type, cls
    global detacher, sentences, definiendum, output, consistent
    global disjuncts, disjuncts_abb, greek_english_prop
    global greek_english, irule, inference, detached_prop
    global def_prop, detacher_prop, new_definition, natural_detacher

    cls = cls2
    output = output2
    definiendum = cls.def_stats.def_word
    sentences = json.loads(json.dumps(cls.sentences))
    detacher = cls.def_stats.detacher
    detach_type = detach_type2
    cls.def_stats.already_instantiated = True
    consistent = True
    to_be_detached = 0
    disjuncts = []
    disjuncts_abb = []
    translations = {}
    greek_english = {}
    greek_english_prop = {}
    irule = ""
    inference = ""
    detached_prop = ""
    def_prop = ""
    detacher_prop = ""
    new_definition = ""
    natural_detacher = ""

    return begin_module(abbrev_dict, conj_intro_pos)


def begin_module(abbrev_dict, conj_intro_pos):
    global consistent
    if definiendum in ['INM', 'x']:
        bb = 8

    definiendum2 = cls.def_stats.def_word_num

    get_detach_type()

    replace_variables(sentences, abbrev_dict)

    rename_prop(sentences)

    neg_conj, inferences, tvalue = translate_excl_disj()

    tvalue, double_neg = translate_sentences(tvalue)

    build_rename_sent3(definiendum2, abbrev_dict)

    anc1 = add_untran_sent_2_tot_sent(abbrev_dict, definiendum2, conj_intro_pos)

    anc2 = conj_intro(conj_intro_pos)

    if redundant(detached_prop, tvalue, definiendum2): return True

    if detach_type != 'ax ind tense':
        add_to_tsent(output[0], inference, detached_prop, tvalue, irule, anc1, anc2)

    consistent = check_consistency(output)

    if not consistent: return False

    append_to_excl_disj()

    if not consistent: return False

    disjunction_elimination(neg_conj, inferences, definiendum2)

    add_new_sent_to_asent(definiendum2)

    return consistent


def append_to_excl_disj():
    if cls.def_stats.consequent_disjunct and detacher == 0:
        new_cls = cls.embeds.get("1.2")
        new_cls.sentences = sentences
        new_cls.def_stats.tot_sent_idx = get_sn(output[0])
        definiendum3 = "1.2" + "," + definiendum
        output[15].update({definiendum3 + "0": new_cls})
        add_to_gsent([new_cls], output)
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
                            if not consistent:
                                return
                        break
                else:
                    next_disjunct = True
    else:
        return True


def detach_disjunct(lst2, e):
    anc1 = get_sn(output[0])
    anc2 = anc1 - 1
    for f, disjunct in enumerate(lst2):
        list1 = []
        if f != e:
            add_to_tsent(output[0], disjunct[0], disjunct[1], "~", xorr + "E", anc1, anc2)
            for conjunct in disjunct[2]:
                list1.append([conjunct[1], conjunct[2], get_sn(output[0])])
            check_intitial_neg_conj_consist(list1, disjunct)
            if not consistent:
                return
            output[11].append(list1)


def check_intitial_neg_conj_consist(list1, disjunct):
    global consistent
    ancestors = []
    list2 = json.loads(json.dumps(list1))
    for e, lst in enumerate(list1):
        for tot_sent in output[0]:
            if tot_sent[2] == lst[0] and tot_sent[3] == lst[1]:
                ancestors.append(str(tot_sent[0]))
                del list2[0]
                if list2 == []:
                    anc1 = ",".join(ancestors)
                    add_to_tsent(output[0], disjunct[0][1:], disjunct[1][1:], "", "&I", anc1)
                    build_contradiction(output, len(output[0]) - 2)
                    consistent = False
                    return


def build_rename_sent3(definiendum2, dict1):
    if dict1 == {}: return
    str2 = " ".join(["(" + build_connection(v, mini_c, k) + ")" for k, v in dict1.items()])
    add_to_tsent(output[0], str2, "", "", "IN", "id")

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


def redundant(sent, tvalue, definiendum2, conj_elim=""):
    if detach_type == 'ax ind tense': return False
    pos = find_2posinlist(sent, tvalue, output[0], 2, 3)
    if pos > -1:
        if conj_elim == 'conj_elim':
            return True
        else:
            if detach_type == 'whole disj intro':
                definiendum3 = xorr + " " + definiendum
            else:
                definiendum3 = definiendum2
            del output[0][-1]
            del output[0][-1]
            lst = output[13].get(definiendum3)
            del lst[-1]
            del lst[-1]
            if lst == []:
                del output[13][definiendum3]

            return True

def change_connective():
    _, pos = mainconn(cls.def_stats.tot_greek_sent)
    assert cls.def_stats.tot_greek_sent[pos] in all_connectives
    str1 = cls.def_stats.tot_greek_sent
    return str1[:pos] + "&" + str1[pos + 1:]


def add_new_sent_to_asent(definiendum2):
    if detach_type == 'ax ind tense':
        ancestor = get_sn(output[0])
        for num in cls.def_stats.ant_index + cls.def_stats.con_index:
            if isinstance(num, int):
                add_one_sent(ancestor, num, definiendum2)
                if not consistent: return
            else:
                raise Exception('you havent coded for this yet')
        return

    mainc, _ = mainconn(detached_prop[1:-1])

    if mainc == "&":
        conjunction_elimination(definiendum2)
    elif one_sentence(inference):
        sentence = sentences[to_be_detached[0]]
        sentence[44] = get_sn(output[0])
        sentence[7] = "c"
        if sentence[58] == "I":
            sentence[58] = determine_constants(output[6], sentence)

        output[1].append(sentence)
        output[5].setdefault(sentence[58], []).append(len(output[1]) - 1)
        output[4].append(sentence[58])
        named_sentence(sentence)
    elif detach_type == "exclusive disjunct" and len(to_be_detached) > 1:
        pass
    elif detach_type != "detach disjunct":
        if detacher == 0:
            embed_num = cls.def_stats.con_hnum[0]
        else:
            embed_num = cls.def_stats.ant_hnum[0]
        embed = cls.embeds.get(embed_num)
        embed.sentences = sentences
        embed.def_stats.tot_sent_idx = get_sn(output[0])
        definiendum3, done = universal_negations(embed, output)
        if done == 'not done':
            definiendum3 = embed.def_stats.def_word_num
            definiendum3 + "0"
        output[15].update({definiendum3: embed})
        if done == 'not done':
            add_to_gsent([embed], output)
        exceptional_instantiation(sentences)

def named_sentence(sent):
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
        output[5].setdefault(const, []).append(len(output[1]) - 1)
        output[4].append(const)
        consistent = check_consistency(output)


def disjunction_elimination(neg_conj, inferences, definiendum2):
    if detach_type != 'exclusive disjunct': return
    ancestor = get_sn(output[0])
    for mem, sent in zip(neg_conj, inferences):
        if len(mem) > 1:
            output[11].append(mem)
            mem[0][2] = get_sn(output[0])
            check_intitial_neg_conj_consist(mem, sent)

        else:
            sentences[mem[0]][3] = "~" if sentences[mem[0]][3] == "" else ""
            name_and_build(output, sentences[mem[0]])
            add_one_sent(ancestor, mem[0], definiendum2)


def conjunction_elimination(definiendum2):
    ancestor = get_sn(output[0])
    b = 0
    for mem in to_be_detached:
        if isinstance(mem, int):
            add_one_sent(ancestor, mem, definiendum2)
            if not consistent: return
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
            new_cls.def_stats.tot_sent_idx = get_sn(output[0])
            gsent_key = new_cls.def_stats.def_word_num
            output[15].update({gsent_key: new_cls})
            add_to_gsent([new_cls], output)
            output[4].append(lsent_key)
            output[5].setdefault(lsent_key, []).append(mem)
            universal_negations(new_cls, output)
            exceptional_instantiation(sentences)


def add_one_sent(ancestor, mem, definiendum2):
    global consistent
    is_redundant = redundant(sentences[mem][2], sentences[mem][3], definiendum2, "conj_elim")
    if not is_redundant:
        anc2 = "ait" if detach_type == "ax ind tense" else ""
        add_to_tsent(output[0], sentences[mem][1], sentences[mem][2],
                     sentences[mem][3], "&E", ancestor, anc2)
        consistent = check_consistency(output)
        if not consistent: return
        sentences[mem][44] = get_sn(output[0])
        for x in sentences[mem][42]:
            if sentences[mem][x] not in output[10]:
                output[10].append(sentences[mem][x])
        sentences[mem][7] = "c"
        const = determine_constants(output[6], sentences[mem])
        sentences[mem][58] = const
        output[1].append(sentences[mem])
        output[4].append(const)
        output[5].setdefault(const, []).append(len(output[1]) - 1)
        named_sentence(sentences[mem])


def exceptional_instantiation(sentences):
    for sentence in sentences:
        if sentence[13] == 'W' and sentence[7][0] == 'b':
            output[10].append(sentence[10])