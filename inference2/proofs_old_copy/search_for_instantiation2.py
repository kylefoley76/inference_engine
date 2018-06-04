import collections, itertools
import sys

from general_functions import *
from analyze_definition import process_sentences, get_lesser_skeleton
from put_words_in_slots import categorize_words, determine_constants
from prepare_for_print import rearrange
from classes import ErrorWithCode
from lemmas import determine_entailments, get_var_match

#
# try:
#     from general_functions import *
#     from change_abbreviations import change_abbrev
#     from use_lemmas import use_basic_lemmas
#     from analyze_definition import process_sentences, get_lesser_skeleton
#     from put_words_in_slots import categorize_words, determine_constants
#     from prepare_for_print import rearrange
#     from classes import ErrorWithCode
#     from lemmas import determine_entailments, get_var_match
#
# except:
#     from .general_functions import *
#     from .change_abbreviations import change_abbrev
#     from .use_lemmas import use_basic_lemmas
#     from .analyze_definition import process_sentences, get_lesser_skeleton
#     from .put_words_in_slots import categorize_words, determine_constants
#     from .prepare_for_print import rearrange
#     from .classes import ErrorWithCode
#     from .lemmas import determine_entailments


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


def add_to_lsent(cls):
    ant_pos = cls[0].def_stats.entailments.ant_pos
    ant_neg = cls[0].def_stats.entailments.ant_neg
    con_pos = cls[0].def_stats.entailments.con_pos
    con_neg = cls[0].def_stats.entailments.con_neg
    ant_var = cls[0].def_stats.entailments.ant_var
    con_var = cls[0].def_stats.entailments.con_var
    for const in ant_pos | con_pos:
        output.lcsent_pos.add(const)
    for const in ant_neg | con_neg:
        output.lcsent_neg.add(const)
    tot_var = {}
    for k, v in ant_var.items():
        if k in con_var.keys():
            tot_var.update({k: con_var.get(k) | v})
        else:
            tot_var.update({k: v})

    for var, st in tot_var.items():
        output.detach_var.update({var: st})

    return


def reduce_hypotheticals_in_premises():
    j = -1
    quant_counter = ""
    while j < len(output.all_sent) - 1:
        j += 1
        sent = output.all_sent[j]
        quantifier = False
        if len(sent) == 46:
            sent = sent[0]
            quantifier = True

        if isinstance(sent, str):
            if not one_sentence(sent):
                del output.all_sent[j]
                j -= 1
                osent = sent
                quant_counter += "a"
                definiendum = "qu" + quant_counter
                if quantifier:
                    anc1 = find_counterpart_inlist(osent, output.total_sent, 1, 0)
                    assert anc1 != None

                reduced_def, old_prop = process_sentences(sent, definiendum, dictionary, output)
                pred_combos(reduced_def)

                # determine_entailments([(definiendum, 1)], dictionary, reduced_def, output)
                # add_to_lsent(reduced_def)

                # if not quantifier:
                #     name_connected_sent(reduced_def, sent)

    return


def pred_combos(reduced_def):
    vars = {}
    location = {}
    positive = True
    flat_ant = reduced_def[0].def_stats.flat_ant_index
    for e, sent in enumerate(reduced_def[0].sentences):

        const = sent[58]
        if sent[3] == "~":
            positive = False
        ant = "ant" if e in flat_ant else "con"
        kind = dictionary.kind.get(const)
        location.update({const: ant})
        if kind == 'c':
            vars.setdefault(sent[10], []).append(const)
        elif kind == 'r':
            for num in sent[42]:
                pos = sent_pos_name.get(num)
                vars.setdefault(sent[num], []).append(const + pos)

    for var, properties in vars.items():
        if len(properties) > 1:
            j = 0
            for property in properties:
                if property in dictionary.ontology[2].keys():
                    j += 1
            if j == 2:
                loc = location.get(properties[0])
                if loc == 'ant':
                    str1 = properties[0] + "." + properties[1]
                else:
                    str1 = properties[1] + "." + properties[0]
                if positive:
                    output.pred_combos.update({str1: 'necessary'})
                else:
                    output.pred_combos.update({str1: 'impossible'})

            elif j > 2:
                raise Exception

            else:
                combos = combinations(properties, 2)
                for combo in combos:
                    str1 = pair(combo[0], combo[1], ".")
                    if positive:
                        output.pred_combos.update({str1: 'necessary'})
                    else:
                        output.pred_combos.update({str1: 'impossible'})

    return


def name_connected_sent(reduced_def, sent):
    for cls in reduced_def:
        greek_sent = cls.def_stats.tot_greek_sent
        for sentence in cls.sentences:
            sentp = name_sent(sentence[1], output.prop_name)
            sentence[2] = sentp
            output.oprop_name[sentp] = sentence[1]
            greek_sent = greek_sent.replace(sentence[5], sentence[3] + sentence[2])

    add_to_tsent(output, sent, greek_sent)


def quick_reduction(sent):
    sent = sent.strip()
    sent = sent.replace("(", "")
    sent = sent.replace(")", "")
    sent = sent.split(" ")
    sent = categorize_words(output.abbreviations, sent, dictionary)
    sent[2] = name_sent(sent[1], output.prop_name)
    output.oprop_name[sent[1]] = sent[2]
    return sent


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
                    if output.all_sent[i][3] == "~":
                        output.lsent_neg.add(output.all_sent[i][58])
                    else:
                        output.lsent_pos.add(output.all_sent[i][58])

                for j in output.all_sent[i][42]:
                    try:
                        output.variables.remove(output.all_sent[i][j])
                    except:
                        pass

    else:
        for e, sent in enumerate(output.all_sent):
            sent[58] = determine_constants(output.abbreviations, sent)
            if sent[3] == "~":
                output.lsent_neg.add(sent[58])
            else:
                output.lsent_pos.add(sent[58])

    return


def ax_ind_tense():
    if output.all_sent == []:
        for k, v in output.gsent.items():
            output.lsent_pos = output.lsent_pos | v.ant_pos | v.con_pos
            output.lsent_neg = output.lsent_neg | v.ant_neg | v.con_neg
            output.gstats.get(k).def_stats.already_instantiated = True
            sentences = output.gstats.get(k).sentences
            output.all_sent = [x for x in sentences]

    return


def get_detach_var():
    idx = [x for x in range(len(output.all_sent))]
    vars = get_var_match(output.all_sent, idx, output.abbreviations, "", {}, "", output)
    for k, v in vars.items(): output.detach_var.update({k: v})


def fill_gsent_dict():
    output.lsent_pos.add("thing")
    for const in output.lsent_pos:
        reduced_def = get_word_info(dictionary, const)
        for cls in reduced_def:
            con_pos = cls.def_stats.entailments.con_pos
            con_neg = cls.def_stats.entailments.con_neg
            output.lsent_pos = output.lsent_pos | con_pos
            output.lsent_neg = output.lsent_neg | con_neg

    for const in output.lsent_neg:
        reduced_def = get_word_info(dictionary, const)
        for cls in reduced_def:
            word_num = cls.def_stats.def_word_num
            output.gsent.update({word_num: cls.def_stats.entailments})
            output.gstats.update({word_num: cls})

    return


def explicit_contradiction():
    global consistent
    if len(output.lsent_pos & output.lsent_neg) > 0:
        consistent = False

def get_rest_of_predicates(species):
    for var in species:
        for sent in output.all_sent:
            if sent[13] not in ["I", "J"] and sent[3] == "":
                for num in sent[42]:
                    if sent[num] == var:
                        species.setdefault(sent[10], {}).update({sent[58]: ""})

    return species

def get_modality(possibility):
    obj = dictionary.groups.get(possibility[0])
    obj2 = dictionary.groups.get(possibility[1])


def check_species_error():
    global consistent, modal_value
    species = {}
    negated_noun = False
    for sent in output.all_sent:
        if sent[13] == 'I' and sent[14] in output.abbreviations.keys():
            if sent[3] == "~":
                negated_noun = True

            member = output.abbreviations.get(sent[14])
            species.setdefault(sent[10], {}).update({member: sent[3]})
        elif sent[13] == 'J' and sent[14] in output.abbreviations.keys():
            member = output.abbreviations.get(sent[14])
            species.setdefault(sent[10], {}).update({member: sent[3]})

    if negated_noun:
        species = get_rest_of_predicates(species)


    for entity, groups in species.items():
        neg_groups = []
        pos_groups = []
        for group, tv in groups.items():
            if tv == "~":
                neg_groups.append(group)
            else:
                pos_groups.append(group)
        if neg_groups != []:
            possibilities = [i for i in itertools.product(*[pos_groups, neg_groups])]
            for possibility in possibilities:
                str1 = possibility[0] + "." + possibility[1]
                if not exceptional_lemma(str1):
                    modality = lemmata.get(str1)
                    # get_modality(possibility)
                    if modality == 'necessary':
                        modal_value = 'impossible'
                        consistent = False
                        add_to_tsent(output, str1 + " = contradictory")
                        add_to_tsent(output, str1 + " = impossible")
                        add_to_tsent(output, bottom)
                        add_to_tsent(output, "contradictory")

                        return
                    else:
                        consistent = True
                        modal_value = modality
                        add_to_tsent(output, str1 + " = " + modality)
                        add_to_tsent(output, str1 + " = consistent")

        else:
            combos = combinations(pos_groups, 2)
            for combo in combos:
                str1 = combo[0] + "." + combo[1]
                if not exceptional_lemma(str1):

                    if "definite" in str1:
                        modal_value = "possible"
                        add_to_tsent(output, str1 + " = consistent")
                        add_to_tsent(output, str1 + " = " + modal_value)
                    else:

                        modality = lemmata.get(str1)
                        modal_value = modality
                        if modality == 'impossible':
                            consistent = False
                            add_to_tsent(output, str1 + " = contradictory")
                            add_to_tsent(output, str1 + " = impossible")
                            add_to_tsent(output, bottom)
                            add_to_tsent(output, "contradictory")
                            return
                        else:
                            consistent = True
                            add_to_tsent(output, str1 + " = consistent")
                            add_to_tsent(output, str1 + " = " + modal_value)
    return

def h_and_w_sent():
    if len(output.lsent_pos) > 1:
        for sent in output.all_sent:
            if sent[58] in ['H', "W"]:
                obj = sent[14]
                concept = output.abbreviations.get(obj)
                if concept != None:
                    sent[58] = sent[58] + concept
                else:
                    for sent2 in output.all_sent:
                        if sent2[10] == obj and sent2[13] == "I":
                            concept = output.abbreviations.get(sent2[14])
                            if concept != None:
                                sent[58] = sent[58] + concept
                                break
    return


def check_consist_dsent():
    if len(output.lsent_pos) > 1:
        entities = {}


        for sent in output.all_sent:
            kind = dictionary.kind.get(sent[58])
            if kind == 'r':
                for num in sent[42]:
                    idx = sent_pos_name.get(num)
                    str1 = sent[58] + idx
                    entities.setdefault(sent[num], []).append(str1)
            else:
                entities.setdefault(sent[10], []).append(sent[58])


        check_consist_dsent2(entities)
        if not consistent:
            return

    return

def exceptional_lemma(str1):
    bool1 = False
    if 'thing' in str1 or "EXs" in str1 or 'extant' in str1:
        bool1 = True
    elif "definite" in str1:
        bool1 =  True
    elif str1.startswith('Hs.') or str1.endswith(".Hs"):
        bool1 = True
    if bool1:
        add_to_tsent(output, str1 + " = consistent")
        add_to_tsent(output, str1 + " = possible")
    return bool1



def check_consist_dsent2(entities):
    global consistent, modal_value
    for entity, predicates in entities.items():
        if len(predicates) > 1:
            pred_sets = [x for x in predicates]
            combos = combinations(pred_sets, 2)
            for combo in combos:
                str1 = pair(combo[0], combo[1], ".")

                if not exceptional_lemma(str1):

                    modal_value = lemmata.get(str1)
                    if modal_value == None:
                        print ("missing " + str1)
                    elif modal_value == 'impossible':
                        consistent = False
                        add_to_tsent(output, str1 + " = contradictory")
                        add_to_tsent(output, str1 + " = impossible")
                        add_to_tsent(output, bottom)
                        add_to_tsent(output, "contradictory")
                        return
                    else:
                        add_to_tsent(output, str1 + " = consistent")
                        add_to_tsent(output, str1 + " = " + modal_value)



def match_var(dict1):
    done = []
    abbrev_dict = {}
    for b, c in dict1.items():
        found = False
        for x, y in output.detach_var.items():
            if len(c) <= len(y):
                if len(y & c) == len(y):
                    abbrev_dict.update({x: b})
                    done.append(x)
                    found = True
                    break
    else:
        if not found:
            return {}
    return abbrev_dict


def satisfies_conditions(k, v):
    tot_pos = output.lsent_pos | output.lcsent_pos
    tot_neg = output.lsent_neg | output.lcsent_neg
    positive = False if k[:-1] in output.lsent_neg else True
    abbrev_dict = {}

    if k.startswith('qu'):
        if len(v.ant_pos & output.lsent_pos) == len(v.ant_pos) and \
                len(v.ant_neg & output.lsent_neg) == len(v.ant_neg):
            abbrev_dict = match_var(v.pos_var)
            side = "ant"

    elif positive:
        if len(v.ant_pos & tot_pos) == len(v.ant_pos) and \
                len(v.ant_neg & tot_neg) == len(v.ant_neg):
            abbrev_dict = match_var(v.pos_var)
            side = "con"

    else:
        if len(v.con_pos & tot_pos) == len(v.con_pos) and \
                len(v.con_neg & tot_neg) == len(v.con_neg):
            abbrev_dict = match_var(v.con_var)
            side = "ant"

    if abbrev_dict != {}:
        detach(v, side, abbrev_dict)
        return True
    else:
        return False


def detach(v, side, abbrev_dict):
    dict_pos = v.ant_pos if side == 'ant' else v.con_pos
    dict_neg = v.ant_neg if side == 'ant' else v.con_neg
    dict_var = v.ant_var if side == 'ant' else v.con_var

    for const in dict_pos:
        if "." in const:
            output.lcsent_pos.add(const)
        else:
            output.lsent_pos.add(const)
    for const in dict_neg:
        if "." in const:
            output.lcsent_neg.add(const)
        else:
            output.lsent_neg.add(const)
    for var, const in dict_var.items():
        new_var = abbrev_dict.get(var)
        for dvar, st in output.detach_var.items():
            if dvar == new_var:
                if const not in st:
                    st.add(const)
                else:
                    print ("do later")

    return


def use_conditionals():
    fill_gsent_dict()
    if output.gsent != {}:
        for k, v in output.gsent.items():
            if not output.gstats.get(k).def_stats.already_instantiated:
                if satisfies_conditions(k, v):
                    explicit_contradiction()
                    if not consistent:
                        return

    return


def try_instantiation(output2, dictionary2, lemmata2, proof_kind2=""):
    global consistent, identities, proof_kind, output, reduced
    global do_not_instantiate, rel_abbrev, atomic_dict1, atomic_dict2
    global dictionary, lemmata, modal_value

    consistent = True
    reduced = False
    identities = []
    do_not_instantiate = []
    rel_abbrev = set()
    atomic_dict1 = {}
    atomic_dict2 = {}
    modal_value = ""
    output = output2
    proof_kind = proof_kind2
    dictionary = dictionary2
    lemmata = lemmata2

    step_one()

    if consistent:
        add_to_tsent(output, consist)
        add_to_tsent(output, "consistent")

    return output, consistent, reduced


def step_one():
    get_abbreviations_standard()

    reduce_hypotheticals_in_premises()

    prepare_stan()

    ax_ind_tense()

    get_detach_var()

    h_and_w_sent()

    check_species_error()
    if not consistent: return

    check_consist_dsent()
    if not consistent: return

    # use_conditionals()
