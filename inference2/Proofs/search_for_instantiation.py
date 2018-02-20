import itertools

from general_functions import *
from change_abbreviations import change_abbrev
from use_lemmas import use_basic_lemmas
from analyze_definition import process_sentences, get_lesser_skeleton
from put_words_in_slots import categorize_words, determine_constants
from prepare_for_print import rearrange
from classes import ErrorWithCode
import copy


############### THE FOLLOWING FUNCTIONS ARE RELATED TO THE USE OF IDENTITY


def identity():
    global identities
    names = {}
    props = {}
    tvalues = {}
    indexes = {}

    for sent in output.all_sent:
        if sent[13] == '=' and output.abbreviations.get(sent[10]) != sent[14]:
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
            sent = output.all_sent[i]
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
    sent1 = output.all_sent[num]
    sent2 = output.all_sent[num2]
    for pos in sent2[42]:
        if sent2[pos] == v:
            sent2[pos] = k
            break

    name_and_build(output, sent2)
    anc1 = find_counterpart_inlist("(" + k + " = " + v + ")", output.total_sent, 1, 0)
    add_to_tsent(output, sent2[1], sent2[2], sent2[3], "SUB", sent2[44], anc1)
    build_contradiction(output, sent1[44])
    consistent = False


##########group: prepare for instantiation #############


def get_range(sentences):
    x = 10
    list1 = []
    while sentences[x] != None:
        list1.append(x)
        x += 1
    return list1


def reduce_hypotheticals_in_premises():
    j = -1
    quant_counter = ""
    while j < len(output.all_sent) - 1:
        j += 1
        sent = output.all_sent[j]
        len_asent = len(output.all_sent)
        quantifier = False
        if len(sent) == 46:
            quant_counter += "a"
            sent = sent[0]
            quantifier = True

        if isinstance(sent, str):
            if not one_sentence(sent):
                output.all_sent[j] = None
                j -= 1
                osent = sent
                sent_class, old_prop = process_sentences(sent, quant_counter, dictionary, output)
                sent_class = sent_class[0]
                anc1 = ""
                sentences = sent_class.sentences
                definiendum, done = universal_negations(sent_class, output)

                if quantifier:
                    definiendum = "qu" + quant_counter
                    anc1 = find_counterpart_inlist(osent, output.total_sent, 1, 0)
                    assert anc1 != None

                asent_idx = name_connected_sent(osent, old_prop, sent_class, quantifier, anc1)
                lst = [x for x in range(len(sentences))]
                skeleton = get_lesser_skeleton(lst, sentences)
                output.lsent_list.append(skeleton)
                output.lsent_dict.setdefault(skeleton, []).append(asent_idx)
                if quantifier or definiendum == 'thing':
                    sent_class.def_stats.def_word = definiendum
                    sent_class.def_stats.def_word_num = definiendum + "0"
                    if quantifier: add_to_gsent([sent_class], output)
                    output.trans_def.update({definiendum + "0": sent_class})
                    do_not_instantiate.append([j + 1, definiendum])
                    for x in range(len_asent, len(output.all_sent)):
                        do_not_instantiate.append([x, definiendum])

    return


def name_connected_sent(osent, old_prop, sent_class, quantifier, anc1=""):
    # because we cannot delete sentences from the all sent otherwise we
    # mess up the order of the subvalues, we turn connected sentences into
    # nones in the all sent and then gradually replace the all sent with
    # the parts of the connected sent
    sentences = sent_class.sentences
    none_pos = [i for i, sent in enumerate(output.all_sent) if sent == None]
    asent_idx = []
    greek_english = {}
    greek_english_abb = {}
    for sentence in sentences:
        if osent != sent_class.def_stats.natural_sent:
            sentence[44] = output.tindex + 2
        else:
            sentence[44] = output.tindex + 1
        sent_abb = name_sent(sentence[1], output.prop_name)
        sentence[2] = sent_abb
        output.oprop_name[sent_abb] = sentence[1]
        if none_pos != []:
            output.all_sent[none_pos[0]] = sentence
            asent_idx.append(none_pos[0])
            del none_pos[0]
        else:
            output.all_sent.append(sentence)
            asent_idx.append(len(output.all_sent) - 1)
        greek_english.update({sentence[5]: sentence[0]})
        greek_english_abb.update({sentence[5]: sentence[3] + sent_abb})
        if proof_kind:
            for o in sentence[42]:
                try:
                    output.variables.remove(sentence[o])
                except:
                    pass

    new_greek = sent_class.def_stats.tot_greek_sent
    new_greek_abb = sent_class.def_stats.tot_greek_sent
    for k, v in greek_english.items():
        new_greek = new_greek.replace(k, v)
    for k, v in greek_english_abb.items():
        new_greek_abb = new_greek_abb.replace(k, v)

    add_to_tsent(output, osent, old_prop)

    if osent != sent_class.def_stats.natural_sent:
        if quantifier:
            add_to_tsent(output, new_greek, new_greek_abb, "", "ASC", output.tindex)
        else:
            add_to_tsent(output, new_greek, new_greek_abb, "", "ASC", output.tindex)

    sent_class.def_stats.tot_sent_idx = output.tindex

    return asent_idx


def prepare_stan():
    if proof_kind == 'artificial':
        for i in range(len(output.all_sent)):
            if isinstance(output.all_sent[i], str):
                if one_sentence(output.all_sent[i][0]):
                    output.all_sent[i] = quick_reduction(output.all_sent[i])
                    output.all_sent[i][6] = str(output.tindex)
                    add_to_tsent(output, output.all_sent[i][1], output.all_sent[i][2], output.all_sent[i][3], "")
                    output.all_sent[i][44] = output.tindex
                    output.all_sent[i][7] = "c"
                    output.lsent_dict.setdefault(output.all_sent[i][58], []).append(i)
                    output.lsent_list.append(output.all_sent[i][58])

                for j in output.all_sent[i][42]:
                    try:
                        output.variables.remove(output.all_sent[i][j])
                    except:
                        pass
    else:
        for e, sent in enumerate(output.all_sent):
            if one_sentence(sent[0]) and sent[7] == 'c':
                sent[58] = determine_constants(output.abbreviations, sent)
                output.lsent_dict.setdefault(sent[58], []).append(e)
                output.lsent_list.append(sent[58])
                if proof_kind == 'lemmas':
                    add_to_tsent(output, sent[1], sent[2], sent[3])
                    output.all_sent[e][44] = output.tindex

    return


def quick_reduction(sent):
    sent = sent.strip()
    sent = sent.replace("(", "")
    sent = sent.replace(")", "")
    sent = sent.split(" ")
    sent = categorize_words(output.abbreviations, sent, dictionary)
    sent[2] = name_sent(sent[1], output.prop_name)
    output.oprop_name[sent[1]] = sent[2]
    return sent


def get_propositional_variables():
    for sent in output.all_sent:
        if sent[9] == mini_e:
            list1 = json.loads(json.dumps(sent))
            prop = list1[8]
            for x in [8, 9]: list1[54].remove(x)
            list1[8] = None
            list1[9] = None
            name_and_build(output, list1)
            output.abbreviations.update({prop: list1[1]})


def get_constants():
    for lst in output.all_sent:
        if lst[7] == 'c':
            for num in lst[42]:
                if lst[num] not in output.constants: output.constants.add(lst[num])

    for var in output.abbreviations.keys():
        if var not in output.constants: output.constants.add(var)


def get_abbreviations_standard():
    if proof_kind in ["", "lemmas"]: return
    i = 0
    list2 = []
    while "=" in output.all_sent[i]:
        sent = output.all_sent[i]
        if sent == None:
            break
        if "=" in sent:
            list2.append(sent)
            sent = sent.replace("(", "")
            sent = sent.replace(")", "")
            list1 = sent.split("=")
            list1[0] = list1[0].strip()
            list1[1] = list1[1].strip()

            output.abbreviations.update({list1[0]: list1[1]})
            try:
                output.variables.remove(list1[0])
            except:
                pass

        del output.all_sent[i]


def add_disjuncts(cls, definiendum):
    for disjunct in cls.def_stats.natural_disjuncts:
        if disjunct != 0:
            add_to_tsent(output, disjunct[0], "", "", xorr + " " + definiendum)
            output.substitutions.setdefault(xorr + " " + definiendum, []).append(output.total_sent[-1])


def add_disjuncts2(tran_disjuncts, qn, definiendum, rn_list):
    for disjunct in tran_disjuncts:
        if disjunct != 0:
            output.substitutions.setdefault(xorr + " " + definiendum, []).append(rn_list)
            add_to_tsent(output, disjunct[1], "", "", "SUBI", qn - 1, qn)
            output.substitutions.setdefault(xorr + " " + definiendum, []).append(output.total_sent[-1])


def translate_abbreviations(lst, definiendum):
    # in the map var the old output.variables are on the left and the new ones are ont he right
    if definiendum == 'GN':
        bb = 8
    conjunctive_definition = False
    map_var = {}
    already_used_map = {}
    temp_constants = dictionary.def_constants.get(definiendum, {})
    change_constants(already_used_map, output, temp_constants)

    if len(lst) > 1:
        conjunctive_definition = True
        add_to_tsent(output, dictionary.definitions.get(definiendum), "", "", "DF " + definiendum)
        anc1 = output.tindex

    for m, cls in enumerate(lst):
        def_stats = cls.def_stats
        sentences = cls.sentences
        tran_disjuncts = json.loads(json.dumps(cls.def_stats.natural_disjuncts))
        greek_definition = def_stats.tot_greek_sent

        if conjunctive_definition:
            add_to_tsent(output, def_stats.natural_sent, "", "", "CE", anc1)
        else:
            add_to_tsent(output, def_stats.natural_sent, "", "", "DF " + definiendum)
        output.substitutions.setdefault(definiendum + str(m), []).append(output.total_sent[-1])
        def_stats.tot_sent_idx = output.tindex
        pn = output.tindex
        add_disjuncts(cls, definiendum)

        for e, sent in enumerate(sentences):
            if e == 6:
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
                    elif ovar in output.variables:
                        output.variables.remove(ovar)
                        map_var.update({ovar: ovar})
                    else:
                        sent[j] = output.variables[0]
                        map_var.update({ovar: output.variables[0]})
                        del output.variables[0]

            name_and_build(output, sent)
            greek_definition = greek_definition.replace(ogreek, sent[0])
            tran_disjuncts = translate_greek_disjuncts(ogreek, sent, tran_disjuncts)
            sent[44] = output.tindex + 2

        if translations_made(map_var):
            rn_sent = build_trans_sent(map_var)
            already_used_map = {**map_var, **already_used_map}
            map_var = {}
            qn = output.tindex + 1
            add_to_tsent(output, rn_sent, "", "", "TR", "id")
            rn_list = output.total_sent[-1]
            output.substitutions.setdefault(definiendum + str(m), []).append(output.total_sent[-1])
            add_to_tsent(output, greek_definition, "", "", "SUBI", pn, 0)
            output.substitutions.setdefault(definiendum + str(m), []).append(output.total_sent[-1])
            def_stats.tot_sent_idx = output.tindex
            add_disjuncts2(tran_disjuncts, qn, definiendum, rn_list)
            def_stats.natural_sent = greek_definition

    return


def translations_made(map_var):
    for k, v in map_var.items():
        if k != v:
            return True
    return False


def translate_greek_disjuncts(ogreek, sent, tran_disjuncts):
    for tran_disjunct in tran_disjuncts:
        if tran_disjunct != 0:
            tran_disjunct[1] = tran_disjunct[1].replace(ogreek, sent[0])

    return tran_disjuncts


def build_trans_sent(map_var):
    list1 = []
    for k, v in map_var.items():
        if k != v:
            str1 = "(" + k + idd + v + ")"
            list1.append(str1)

    return " ".join(list1)


def definition_constant(sent):
    if sent[13] in ["I", "J", "V"]:
        word = output.abbreviations.get(sent[14])
        if word != None:
            return word
        else:
            return sent[13]

    elif sent[13] == '=' and sent[14] in output.abbreviations.values():
        return sent[14]
    else:
        return sent[13]


def is_exceptional2(output, word, m):
    if proof_kind == 'lemmas' and word == 'point':
        if output.all_sent[m][10] in output.main_var:
            return False
        else:
            return True
    return False


def get_hypotheticals(start):
    if proof_kind == 'lemmas2': return
    done = []
    for m in range(start, len(output.all_sent)):
        word = definition_constant(output.all_sent[m])
        assert word != None

        if findposinmd("DF " + word, output.total_sent, 4) == -1 and word not in done:
            if word in dictionary.categorized_sent.keys() and \
                    not is_exceptional2(output, word, m):
                item1 = get_word_info(dictionary, output.user, word)

                add_to_gsent(item1, output)
                for j, itm in enumerate(item1):
                    output.trans_def.update({word + str(j): itm})
                translate_abbreviations(item1, word)
                done.append(word)

    return


def try_instantiation(output2, dictionary2, proof_kind2=""):
    global consistent, identities, proof_kind, output, reduced
    global do_not_instantiate, rel_abbrev, atomic_dict1, atomic_dict2
    global dictionary

    consistent = True
    reduced = False
    identities = []
    do_not_instantiate = []
    rel_abbrev = set()
    atomic_dict1 = {}
    atomic_dict2 = {}
    output = output2
    proof_kind = proof_kind2
    dictionary = dictionary2

    step_one()

    return output, consistent, reduced


def step_one():
    global output

    get_abbreviations_standard()

    reduce_hypotheticals_in_premises()

    prepare_stan()

    get_propositional_variables()

    get_constants()

    get_relevant_abbreviations(0)

    get_hypotheticals(0)

    identity()

    first_resort()

    use_basic_lemmas2(0, len(output.all_sent))

    loop_through_gsent()

    output = rearrange("last", output, consistent, proof_kind, rel_abbrev)


def first_resort():
    if output.lsent_list == [] and proof_kind == 'lemmas':
        last_resort_axioms(0, [], True)


def use_basic_lemmas2(begin, end):
    global consistent
    if proof_kind == 'lemmas2': return
    if not consistent: return

    update_identity(begin, end)
    if not consistent: return

    for i in range(begin, end):
        sent = output.all_sent[i]
        if sent[7] == 'c':
            for pos in sent[42]:

                consistent = use_basic_lemmas(output, pos, sent, atomic_dict1, atomic_dict2)

                if not consistent: return


######## group: loop until instantiation is done ##############


def get_relevant_abbreviations(begin):
    universal = lambda x, y: x[13] in ["I", "J", "V", "OFW"] and y == 14
    if begin == 0:
        for k in output.abbreviations.keys():
            if isvariable(k):
                rel_abbrev.add(k)  # todo this rule might contradict the one below

    for sent in output.all_sent[begin:]:
        for noun in sent[42]:
            if sent[noun] == 'x':
                bb = 8

            if not universal(sent, noun):
                rel_abbrev.add(sent[noun])

    return


def delete_irrelevant_lsent(begin):
    if proof_kind == 'lemmas': return
    list1 = []
    for e in range(begin, len(output.all_sent)):
        sent = output.all_sent[e]
        if sent[13] == 'I':
            if any(sent2[10] in rel_abbrev and sent2[13] == 'H'
                   and sent2[14] == sent[10] for sent2 in output.all_sent):
                pass
            else:
                sent[0] = 'irrelevant'

        elif all(sent[x] not in rel_abbrev for x in sent[42]):
            sent[0] = 'irrelevant'
            list1.append(e)

    if list1 != []:
        delete_this = []
        for k, v in output.lsent_dict.items():
            j = 0
            while j < len(v):
                if v[j] in list1:
                    del v[j]
                    if v == []:
                        delete_this.append(k)
                        break
                else:
                    j += 1
        for k in delete_this: del output.lsent_dict[k]
        for k in delete_this: output.lsent_list.remove(k)

    return


def is_exceptional(matrix, j):
    if j == 25:
        bb = 8

    lesser_word = matrix[j][0]
    lesser_word = lesser_word.replace("~", "")
    if matrix[j][1] == "I":
        if dictionary.kind.get(lesser_word) == 'c':
            return True
    elif matrix[j][1] == 'J':
        pos = dictionary.pos.get(lesser_word)
        if pos[0] == 'a':
            return True
    elif matrix[j][3] in output.near_matches.keys():
        return True

    return False


def instantiable(lconstant, gconstant):
    lst = output.lsent_dict.get(lconstant)
    for num in lst:
        if [num, gconstant[0]] not in do_not_instantiate:
            return True



    return False


def build_matrix(matrix, gstart, gstop, lstart, lend):
    for lconstant in output.lsent_list[lstart:lend]:
        for gconstant in output.gsent[gstart: gstop]:
            if instantiable(lconstant, gconstant):
                matrix.append([lconstant, gconstant[0], gconstant[1], gconstant[2]])

    return


def lemma_non_instantiation():
    global do_not_instantiate
    if proof_kind == 'lemmas2':
        do_not_instantiate = output.disj_elim
        output.disj_elim = []


def loop_through_gsent():
    global output, reduced
    if not consistent: return
    for x in output.abbreviations.values(): assert not x.islower() or len(x) > 1
    matrix = []
    prev_instant = []
    output.lsent_list = sorted(list(set(output.lsent_list)))
    lemma_non_instantiation()
    delete_irrelevant_lsent(0)
    build_matrix(matrix, 0, len(output.gsent), 0, len(output.lsent_list))
    # in the matrix, the 2nd member is the index in the output.gsent, the 3rd member
    # is 0 for antecedent and 1 for consequent and the 4th member is the index
    # in the output.lsent_dict
    j = 0
    z = 0
    while j < len(matrix):
        z += 1
        if z > 600: raise ErrorWithCode("caught in infinite loop")

        word = matrix[j][3]
        len_gsent = len(output.gsent)
        len_lsent = len(output.lsent_list)
        len_asent = len(output.all_sent)
        possibilities = []
        if j == 10:
            bb = 8

        if matrix[j][0] == matrix[j][1] or is_exceptional(matrix, j):
            # print(word)

            if matrix[j][3] == "INE0" or j == 22 or word == 'natural' + ur:
                bb = 8

            used_possibilities = loop_through_gsent2(possibilities, matrix, prev_instant, j)
            if used_possibilities != []:
                reduced = True
                reconfigure_matrix(j, len_asent, len_gsent, len_lsent, matrix, used_possibilities)
                if not consistent: return

        elif j == len(matrix) - 1:
            last_resort_axioms(j, matrix)
            if not consistent: return
        j += 1

    if consistent:
        add_to_tsent(output, consist, consist, "", consist + "I")

    return reduced


def reconfigure_matrix(j, len_asent, len_gsent, len_lsent, matrix, used_possibilities, definiendum=""):
    global output
    use_basic_lemmas2(len_asent, len(output.all_sent))
    if not consistent: return
    output.lsent_list = output.lsent_list[:len_lsent] + sorted(list(set(output.lsent_list[len_lsent:])))
    # the point of the following is that if (b > c) & (b I d) = (b I e) in (b I d)
    # then it would be useless to (b > c) in (b I e)
    if used_possibilities != []:
        # if the used possibilities are blank then the ax id tense was used as last resort
        for snum in range(len_asent, len(output.all_sent)):
            do_not_instantiate.append([snum, matrix[j][3]])
        for possibility in used_possibilities:
            do_not_instantiate.append([possibility[0], matrix[j][3]])
    else:
        for snum in range(len_asent, len(output.all_sent)):
            do_not_instantiate.append([snum, definiendum + "0"])
    delete_irrelevant_lsent(len_asent)
    get_hypotheticals(len_asent)
    build_matrix(matrix, 0, len(output.gsent), len_lsent, len(output.lsent_list))
    build_matrix(matrix, len_gsent, len(output.gsent), 0, len_lsent)
    return


def eliminate_impossibilities(possibilities, ndefiniendum):
    i = 0
    while i < len(possibilities):
        k = 0
        while k < len(possibilities[i]):
            if isinstance(possibilities[i][k], int):
                if [possibilities[i][k], ndefiniendum] in do_not_instantiate:
                    del possibilities[i][k]
                    k -= 1
            k += 1
        i += 1

    return


def loop_through_gsent2(possibilities, matrix, prev_instant, j):
    ndefiniendum = matrix[j][3]
    detacher = matrix[j][2]
    fake_lsent = copy.deepcopy(output.lsent_dict)
    cls = output.trans_def.get(ndefiniendum)
    disj_cls = ""
    if detacher == 0:
        cls.def_stats.detacher = 0
        remaining_conditions = cls.def_stats.ant_index
    elif detacher == 1:
        cls.def_stats.detacher = 1
        remaining_conditions = cls.def_stats.con_index
    elif cls.def_stats.def_word == 'thing':
        cls.def_stats.now_disjunctive = cls.disjuncts[detacher - 2]
        remaining_conditions = cls.disjuncts[detacher - 2]
        cls.def_stats.detacher = 0
        detacher = 0
    else:
        disj_cls = cls.disjuncts[detacher - 2]
        remaining_conditions = disj_cls.index1

    possibilities.append(fake_lsent.get(matrix[j][0]))
    gsent_pos = copy.deepcopy(remaining_conditions)
    gconstants = []
    eliminate_impossibilities(possibilities, ndefiniendum)

    if possibilities == [[]]:
        return []
    elif len(remaining_conditions) > 1:
        comp_num = 0
        sentences = cls.sentences
        for gindex in remaining_conditions[1:]:
            if isinstance(gindex, list):
                gconstant, comp_num = get_complex_constant(cls, comp_num, detacher, disj_cls)
            else:
                gconstant = sentences[gindex][58]
            if gconstant == matrix[j][0] or gconstant == 'thing':
                gsent_pos.remove(gindex)
            else:
                lindexes = output.lsent_dict.get(gconstant)
                if lindexes != None:
                    for lst in lindexes:
                        if [lst, ndefiniendum] not in do_not_instantiate:
                            possibilities.append(lindexes)
                            gconstants.append(gconstant)
                            break
                    else:
                        return []
                else:
                    rearrange_matrix(matrix, j, detacher, remaining_conditions, gconstant, gindex)
                    return []

    if len(remaining_conditions) == 1:
        i = 0
        while i < len(possibilities):
            if [possibilities[0][i], ndefiniendum] in do_not_instantiate:
                del possibilities[0]
            else:
                i += 1

    cls.def_stats.detacher = detacher
    _ = loop_through_gsent3(possibilities, cls, prev_instant, flatten_list(gsent_pos))
    used_possibilities, failed = _

    if failed != [] and len(failed[0]) > 1:
        add_to_failures(failed, ndefiniendum, cls)

    return used_possibilities


def add_to_failures(failed, ndefiniendum, cls):
    if ndefiniendum not in output.near_matches.keys():
        output.near_matches.update({cls.def_stats.def_word_num: failed})
    else:
        failures = output.near_matches.get(ndefiniendum)
        for fail in failed:
            failures.append(fail)


def flatten_list(lst):
    list2 = []
    for x in lst:
        if isinstance(x, list):
            for y in x: list2.append(y)
        else:
            list2.append(x)

    return list2


def get_complex_constant(cls, comp_num, detacher, disj_cls):
    if detacher == 0:
        gconstant = list(cls.def_stats.ant_comp_const)[comp_num]
    elif detacher == 1:
        gconstant = list(cls.def_stats.con_comp_const)[comp_num]
    else:
        gconstant = disj_cls.comp_const[comp_num]
    comp_num += 1

    return gconstant, comp_num


def rearrange_matrix(matrix, j, detacher, remaining_conditions, gconstant, gindex):
    if matrix[j][3] in output.near_matches.keys():
        return
    remaining_conditions.remove(gindex)
    gsent = matrix[j][3]
    remaining_conditions.insert(0, gindex)
    for k in range(j + 1, len(matrix)):
        if matrix[k][3] == gsent and matrix[k][2] == detacher:
            matrix[k][1] = gconstant

    for e, lst in enumerate(output.gsent):
        if lst[2] == gsent:
            lst[0] = gconstant
            break

    return


def loop_through_gsent3(possibilities, cls, prev_instant, gsent_pos):
    global output, consistent

    dead_combinations = []
    conj_intro_pos = []
    possibilities = [i for i in itertools.product(*possibilities)]
    combine_lists(possibilities, conj_intro_pos)
    used_possibilities = []
    failed_possibilities = []
    failures = output.near_matches.get(cls.def_stats.def_word_num, [])
    if failures != []:
        bb = 8

    for e, possibility in enumerate(possibilities):

        if possibility not in failures:
            abbrev_dict, match_found = variables_match(gsent_pos, possibility, cls, dead_combinations)
            if match_found:
                if cls.def_stats.def_word == 'thing':
                    pos = universal_instantiation(abbrev_dict, possibility, cls)
                    conj_intro_pos[e] = pos
                if [possibility, cls.def_stats.def_word_num] not in prev_instant:
                    consistent = change_abbrev(abbrev_dict, cls, conj_intro_pos[e], output, dictionary)
                    prev_instant.append([possibility, cls.def_stats.def_word_num])

                    if not consistent:
                        return used_possibilities.append(possibility), []
                    else:
                        used_possibilities.append(possibility)
            else:
                failed_possibilities.append(possibility)

    return used_possibilities, failed_possibilities


def combine_lists(possibilities, conj_intro_pos):
    e = 0
    while e < len(possibilities):
        possibility = possibilities[e]
        list1 = []
        temp_conj = []
        for lst in possibility:

            if isinstance(lst, list):
                temp_conj.append(output.all_sent[lst[0]][44])
                list1 += lst
            else:
                temp_conj.append(output.all_sent[lst][44])
                list1.append(lst)
        if len(list1) == len(set(list1)):
            possibilities[e] = list1
            conj_intro_pos.append(temp_conj)
            e += 1
        else:
            del possibilities[e]

    return


def are_identical_unique_obj(i, j, sentences):
    if output.all_sent[i][13] == '=' and sentences[j][13] == '=' and \
            all(output.all_sent[i][x] == sentences[j][y] for x, y in zip(output.all_sent[i][42], sentences[j][42])):
        return True
    return False


def variables_match(gsent_pos, possibility, cls, dead_combinations):
    if is_dead_combination(dead_combinations, possibility):
        return {}, False
    abbrev_dict = {}
    used_lesser = []
    sentences = cls.sentences
    detacher = cls.def_stats.detacher
    if cls.def_stats.def_word_num == 'qua0':
        bb = 8

    for e, i in enumerate(possibility):
        j = gsent_pos[e]
        if j == 6:
            bb = 8
        used_lesser.append(i)
        if are_identical_unique_obj(i, j, sentences):
            return {}, True

        else:

            for pos in output.all_sent[i][42]:
                gvar = sentences[j][pos]
                lvar = output.all_sent[i][pos]
                if lvar == 'f' + l1:
                    bb = 8

                # for those sentences of the form y = time, 'time' cannot be replaced
                if lvar != gvar and gvar not in output.constants \
                        and gvar not in output.abbreviations.values():
                    var = abbrev_dict.get(output.all_sent[i][pos])
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
                elif lvar in output.constants and gvar in output.constants \
                        and gvar != lvar:
                    return {}, False
            else:
                if detacher == 0:
                    idx = cls.def_stats.ant_index[0]
                    del cls.def_stats.ant_index[0]
                    cls.def_stats.ant_index.append(idx)
                elif detacher == 1:
                    idx = cls.def_stats.con_index[0]
                    del cls.def_stats.con_index[0]
                    cls.def_stats.con_index.append(idx)

    if abbrev_dict == {}: return {}, False
    return abbrev_dict, True


def is_dead_combination(dead_detach, possibility):
    # if we know that detach sentences 6 and 4, for example, are impossible then any instantiation
    # which uses sentences 6 and 4 will also be impossible
    for dead_list in dead_detach:
        if len(set(dead_list).intersection(set(possibility))) == len(dead_list):
            return True
    return False


def get_detach_idx(possibility, k):
    for num in possibility:
        sent = output.all_sent[num]
        for noun in sent[42]:
            if sent[noun] == k:
                return num
    raise Exception('you failed to find the thing sentence')


def universal_instantiation(abbrev_map, possibility, cls):
    # the thing conditional's remaining conditions always has the consq
    # first, so for conj intro, we must use all of the nums in the possibility
    # except the first one
    ant_set = []
    ant_setp = []
    ancestors = []
    sentences = cls.sentences
    thing_concept = get_key(output.abbreviations, 'thing')

    for k, v in abbrev_map.items():
        for sent in sentences:
            if sent[10] == v and sent[13] == 'I' and sent[14] == thing_concept:
                str1 = "(" + k + " I " + thing_concept + ")"
                str1p = name_sent(str1, output.prop_name)
                output.oprop_name[str1p] = str1
                ant_set.append(str1)
                ant_setp.append(str1p)
                if len(possibility) > 1:
                    idx = get_detach_idx(possibility, k)
                else:
                    idx = possibility[0]

                sent1 = output.all_sent[idx][0] + " " + implies + " " + str1
                sent1p = output.all_sent[idx][3] + output.all_sent[idx][2] + " " + implies + " " + str1p
                add_to_tsent(output, sent1, sent1p, "", "LE ENT")
                add_to_tsent(output, str1, str1p, "", "MP", 0, output.all_sent[possibility[0]][44])
                ancestors.append(output.tindex)

    for num in possibility[1:]:
        ancestors.append(output.all_sent[num][44])

    return ancestors


def last_resort_axioms(j, matrix, first_resort=False):
    global output, consistent, rel_abbrev
    len_gsent = len(output.gsent)
    len_lsent = len(output.lsent_list)
    len_asent = len(output.all_sent)
    total_constants = set(output.abbreviations.keys()) | output.constants
    for con in total_constants:
        if isvariable(con): rel_abbrev.add(con)

    n = len(output.trans_def) if not first_resort else 1
    for itm in range(n):
        item1 = list(output.trans_def)[itm]
        cls = output.trans_def.get(item1)
        if cls.def_stats.already_instantiated == False:
            sentences = cls.sentences
            definiendum = cls.def_stats.def_word
            abbrev_dict = {}
            relevant = False
            for num in cls.def_stats.ant_index:
                if isinstance(num, int):
                    for idx in sentences[num][42]:
                        if sentences[num][idx] not in total_constants and \
                                sentences[num][idx] not in abbrev_dict.values():
                            abbrev_dict.update({output.variables[0]: sentences[num][idx]})
                            del output.variables[0]
                        if sentences[num][idx] in rel_abbrev:
                            relevant = True
                        elif sentences[num][58] not in output.lsent_list:
                            relevant = True

            if relevant:
                tot_idx = cls.def_stats.tot_sent_idx
                cls.def_stats.detacher = 0
                consistent = change_abbrev(abbrev_dict, cls, [tot_idx], output, dictionary, "ax ind tense")
                get_relevant_abbreviations(len_asent)
                if not first_resort:
                    reconfigure_matrix(j, len_asent, len_gsent, len_lsent, matrix, [], definiendum)
                len_gsent = len(output.gsent)
                len_lsent = len(output.lsent_list)
                len_asent = len(output.all_sent)

    return
