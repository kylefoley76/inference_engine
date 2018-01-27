
from settings import *
from general_functions import add_to_total_sent, \
    build_contradiction2, get_key, name_and_build, get_sn

import copy


exclusive_class = ['moment', 'relationship', 'point', 'number',
            'imagination', 'concept' + un, "property" + un, 'property',
            'possible world', 'letter', 'mind', 'matter', 'sensorium']

abbreviations = [{}, {}]
total_sent = []
atomic_dict1 = {}
atomic_dict2 = {}
substitutions = {}
prop_var = []
variables = []
prop_name = {}
oprop_name = {}
first_sent = []
cond1 = []
cond2 = []
thing_sent = []
lemma_name = ""
build_rename = lambda x: " ".join(x)

def use_basic_lemmas(abbreviations2, total_sent2, variables2, prop_name2, oprop_name2, prop_var2, pos, sent,
                     substitutions2, atomic_dict3, atomic_dict4):

    global total_sent, abbreviations, atomic_dict1, atomic_dict2, substitutions
    global variables, prop_name, oprop_name, prop_var, second_sent
    abbreviations = abbreviations2
    total_sent = total_sent2
    atomic_dict1 = atomic_dict3
    atomic_dict2 = atomic_dict4
    prop_var = prop_var2
    variables = variables2
    prop_name = prop_name2
    oprop_name = oprop_name2
    substitutions = substitutions2
    second_sent = sent

    return add_to_class(pos, sent, atomic_dict1, atomic_dict2)

def add_to_class(pos, sent, atomic_dict1, atomic_dict2):
    global first_sent
    group = get_class(sent, pos, abbreviations)
    abbrev = sent[pos]
    if group in exclusive_class:
        if abbrev in atomic_dict1.keys() and group != atomic_dict1.get(abbrev):
            first_sent = atomic_dict2.get(abbrev)
            add_basic_lemmas(abbrev)
            return False
        else:
            atomic_dict1.update({abbrev: group})
            atomic_dict2.update({abbrev: sent})

    return True


def add_basic_lemmas(abbrev):
    global  cond1, cond2, thing_sent, lemma_name

    obj_pos1 = 10 if first_sent[10] == abbrev else 14
    obj_pos2 = 10 if second_sent[10] == abbrev else 14

    sent_pos = [10, 13, 14]
    cond1 = [None] * 60
    cond1[3] = ""
    thing_sent = [None] * 60
    thing_sent[3] = ""
    cond2 = [None] * 60
    cond2[3] = "~"
    second_sent[3] = "~"

    cond1[10], cond1[13], cond1[14], cond1[54] = 'b', first_sent[13], "c", sent_pos
    thing_sent[10], thing_sent[13], thing_sent[14], thing_sent[54] = "d", "I", "e", sent_pos
    cond2[13], cond2[54] = second_sent[13], sent_pos

    if obj_pos1 == 10 and obj_pos2 == 10:
        name = "SS"
    elif obj_pos1 == 10 and obj_pos2 == 14:
        name = "SO"
    elif obj_pos1 == 14 and obj_pos2 == 10:
        name = "OS"
    elif obj_pos1 == 14 and obj_pos2 == 14:
        name = "OO"

    implication_template(name, cond2, thing_sent, "b", "c", "d")
    lemma_name = "LY." + first_sent[13] + "." + second_sent[13] + "." + name
    build_sentences(cond1, cond2, thing_sent, lemma_name)
    substitutions.setdefault(lemma_name, []).append(total_sent[-1])

    #(b S c) & (d I e) ⊢ (d ~ B b) & (e=thing)

    build_translated_lemma(name, cond1, cond2, thing_sent)

def build_translated_lemma(name, cond1, cond2, thing_sent):

    old_var = ["b", "c", "d", "e"]
    new_var = [variables[x] for x in range(3)]
    for x in range(3): del variables[0]
    concept_thing = get_concept_thing()
    new_var.append(concept_thing)
    cond1[10], cond1[14], thing_sent[14] = new_var[0], new_var[1], concept_thing
    implication_template(name, cond2, thing_sent, new_var[0], new_var[1], new_var[2])
    rename_template(old_var, new_var, "TR", idd)

    #(b > w) (c > u) (d > v) (e > t)

    del new_var[-1]
    build_sentences(cond1, cond2, thing_sent, "SUBI")
    substitutions.setdefault(lemma_name, []).append(total_sent[-1])
    build_instantiated_lemma(name, new_var)

    # (w S c) & (u I t) ⊢ (u ~ B w)

    return

def build_instantiated_lemma(kind, new_var):
    var1, var2 = first_sent[10], first_sent[14]

    if kind in ["SS", "OS"]: var3 = second_sent[14]

    elif kind in ["SO", "OO"]: var3 = second_sent[10]


    instantiated_var = [var1, var2, var3]

    thing_sent2 = copy.deepcopy(thing_sent)
    thing_sent2[10] = var3
    name_and_build(thing_sent2, oprop_name, prop_name)
    anc1 = get_sn(total_sent)
    total_sent[-1][5] = anc1 - 1
    total_sent[-1][6] = anc1 - 2


    sent1 = build_connection(second_sent[0], implies, thing_sent2[0])
    sent1p = build_connection(second_sent[2], implies, thing_sent2[2])

    #(d B b) ⊢ (d I t)

    add_to_total_sent(total_sent, sent1, sent1p, "", "LE ENT")

    # (d I t)

    add_to_total_sent(total_sent, thing_sent2[1], thing_sent2[2], "", "MP", get_sn(total_sent), second_sent[44] )

    conjunction = build_conjunction([first_sent[1], thing_sent2[1]])
    conjunctionp = build_conjunction([first_sent[2], thing_sent2[2]])

    #(d B b) & (d I t)

    add_to_total_sent(total_sent, conjunction, conjunctionp, "", "&I", get_sn(total_sent), first_sent[44])

    implication = build_connection(conjunction, implies, second_sent[3] + second_sent[1])
    implicationp = build_connection(conjunctionp, implies, second_sent[3] + second_sent[2])
    contradiction = build_contradiction2(second_sent[1])
    contradictionp = build_contradiction2(second_sent[2])

    #(w > b) (u > c) (v > d)

    rename_template(new_var, instantiated_var, "IN", mini_c)

    # (b S c) & (d I e) ⊢ ~(d B b)
    anc1 = get_sn(total_sent)
    add_to_total_sent(total_sent, implication, implicationp, "", "SUBJ", anc1, anc1 - 4)
    substitutions.setdefault(lemma_name, []).append(total_sent[-1])

    # (d B b)
    anc1 = get_sn(total_sent)
    add_to_total_sent(total_sent, second_sent[1], second_sent[2], "~", "MP", anc1, anc1 - 2)
    add_to_total_sent(total_sent, contradiction, contradictionp, "", "&I", get_sn(total_sent), second_sent[44])
    add_to_total_sent(total_sent, bottom, bottom, "", bottom +"I", get_sn(total_sent))

    return



def get_concept_thing():
    concept_thing = get_key(abbreviations, "thing")
    if concept_thing == None:
        concept_thing = variables[0]
        del variables[0]
        abbreviations.update({concept_thing: 'thing'})

    return concept_thing


def rename_template(ovar, new_var, rule, sign):
    list2 = ["(" + build_connection(x, sign, y) + ")" for x, y in zip(ovar, new_var)]
    rename_sent = build_conjunction(list2)
    add_to_total_sent(total_sent, rename_sent, "", "", rule)
    substitutions.setdefault(lemma_name, []).append(total_sent[-1])



def implication_template(kind, cond2, thing_sent, var1, var2, var3):
    thing_sent[10] = var3
    if kind == "SS":
        cond2[10], cond2[14] = var1, var3

    elif kind == "SO":
        cond2[10], cond2[14] = var3, var1

    elif kind == "OS":
        cond2[10], cond2[14] = var2, var3

    elif kind == "OO":
        cond2[10], cond2[14] = var3, var2


def build_sentences(cond1, cond2, thing_sent, rule):

    first = True if rule.startswith("LY") else False
    othing_sent = "(e = thing)"
    name_and_build(cond1, oprop_name, prop_name)
    name_and_build(cond2, oprop_name, prop_name)
    name_and_build(thing_sent, oprop_name, prop_name)

    conjunction = build_conjunction([cond1[0], thing_sent[0]])
    implication =  build_connection(conjunction, implies, cond2[0])
    implication = "(" + implication + ") & " + othing_sent if first else implication

    implicationp = ""
    if not first:
        conjunctionp = build_conjunction([cond1[2], thing_sent[2]])
        implicationp = build_connection(conjunctionp, implies, cond2[3] + cond2[2])

    ## (b S c) & (d I e) ⊢ ~(d B b)

    add_to_total_sent(total_sent, implication, implicationp, "", rule)



def get_class(sent, pos, abbreviations, property=""):
    # this determines what class or category an object belongs to
    relat_pos = 13 if pos < 21 else pos - 1

    relat = sent[relat_pos]
    pos = 10 if pos == 11 else pos
    if property == "relationship":
        return "relationship"

    if sent[3] == "~":
        kind = ''
    elif relat in ["/", "+", "ID", "-"]:
        kind = 'number'
    elif relat == "A" or (relat == 'T' and pos == 14):
        kind = 'moment'
    elif relat == "T" and pos == 10:
        kind = 'non-moment'
    elif relat == 'AB' or relat == "L" or relat == 'AB' or (relat == 'S' and pos == 14):
        kind = 'point'
    elif relat == "G" or (relat == 'N' and pos == 14):
        kind = 'number'
    elif relat == "M" and pos == 10 or (relat == 'B' and pos == 14):
        kind = 'relationship'
    elif relat == "M" and pos == 14:
        kind = 'imagination'
    elif relat == "I" and pos == 10:
        group = sent[14]
        kind = abbreviations.get(group)
        if kind == 'thing':
            kind = ""
        elif kind == None:
            kind = sent[14] + "-object"
    elif relat == "I" and pos == 14:
        kind = "concept" + un
    elif relat == "H" and pos == 14:
        kind = "property" + un
    elif relat == "J" and pos == 14:
        kind = "property"
    elif relat == "W" and pos == 10:
        kind = "whole"
    elif relat == "W" and pos == 14:
        kind = "part"
    # elif relat == "W" and pos == 14:
    #     kind = ''
    # elif relat == "TK" and pos == 10:
    #     kind = 'mind'
    # elif relat == "TK" and pos == 14:
    #     kind = 'relationship'

    elif relat == 'P' and pos == 14:
        kind = 'possible world'
    elif relat == "D" and pos == 14:
        kind = 'relationship'
    elif relat == 'AL':
        kind = 'letter'
    elif (relat == 'B' or relat == "D") and pos == 10:
        kind = 'mind'
    elif relat == "S" and pos == 10:
        kind = 'matter'
    elif relat == "O" and pos == 14:
        kind = 'sensorium'
    else:
        kind = ""
    kind = "thing" if kind == "" else kind

    return kind


def kind_exception(str1):
    # since everything belongs to the class 'whole' or 'part' these are not
    # genuine classes
    exceptions = ['whole', 'part']
    if str1 in exceptions:
        return 'thing'
    elif str1 == None:
        return 'thing2'
    return str1
    # if str1 equals none then that means the subject belongs to an indefinite
    # concept
