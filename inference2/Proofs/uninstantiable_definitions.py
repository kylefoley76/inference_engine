

from general_functions import *
from put_words_in_slots import categorize_words

definite_assignments = []
inferences = []
words_used = []
i_defined = False
consistent = True

first_person_pronoun = lambda x: x != 'i' or not i_defined

####### group: preliminary to eliminate uninstantiable words part two


def detach_inferences():
    global consistent
    for lst in inferences:
        if lst[1] == "k":
            bb = 8

        if lst[3] == 'AE':
            pot_ancestor = lst[4]
            lst[4] = find_counterpart_inlist(pot_ancestor, output[0], 6, 0)
            assert lst[4] != -1
        elif isinstance(lst[4], str):

            for tlst in output[0]:
                if tlst[3] + tlst[2] == lst[4]:
                    lst[4] = tlst[0]
                    break
            else:
                raise Exception ('you failed to find the ancestor')


        add_to_tsent(output[0], lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6])
        consistent = check_consistency(output)
        if not consistent:
            return

    for sent in output[1]:
        if len(sent) != 46:
            g = find_2posinlist(sent[2], sent[3], output[0], 2, 3)
            assert g > -1
            sent[44] = output[0][g][0]
            sent[7] = 'c'
    return


def define_irregular_terms(output2, inferences2, words_used2):


    global inferences, consistent
    global words_used, definite_assignments, i_defined
    global output
    
    output = output2
    definite_assignments = {}
    inferences = inferences2
    words_used = words_used2
    i_defined = False
    consistent = True

    main_loop(output[1])

    detach_inferences()

    return output, consistent




def main_loop(list1, kind="", kind2 = ""):
    m = -1
    while m < len(list1) - 1:
        m += 1
        while list1[m][45] != []:
            category = list1[m][45][0][1]
            slot = list1[m][45][0][0]
            del list1[m][45][0]

            if category == 30 or list1[m][slot] == 'aa' or slot == 61:
                bb = 8

            if not lies_wi_scope_of_univ_quant(list1[m], slot) and \
                first_person_pronoun(list1[m][slot]):

                antecedent = copy.deepcopy(list1[m])
                determine_which_function_to_use(antecedent, list1, m, slot, category, kind, kind2)
                if category not in [.4, .5, 13]:
                    del list1[m]
                m -= 1
                break

    return list1



def determine_which_function_to_use(antecedent, list1, m, slot, category, kind, kind2):
    anc1 = list1[m][44]
    consequent = None
    if category not in [2, .4, .5, 13, 13.5]:
        list1[m][54].remove(slot)
    if category == .4:
        consequent, rule = eliminate_negative_determiners(slot, list1, m)
    elif category == .5:
        consequent, rule = infer_first_pronoun()
    elif category == 1:
        consequent, rule = eliminate_determiners(list1[m], slot)
    elif category == 2:
        consequent, rule = eliminate_pronouns(list1[m], slot)
    elif category == 3:
        consequent, rule = eliminate_common_name_possessives(list1[m], slot)
    elif category == 4:
        consequent, rule = eliminate_proper_name_possessives3(list1[m], slot)
    elif category == 5:
        consequent, rule = eliminate_and_coordinator(list1[m], slot)
    elif category == 6:
        consequent, rule = eliminate_adjectives(list1[m], slot)
    elif category == 7:
        consequent, rule = eliminate_concept_instance_apposition(list1[m], slot)
    elif category == 9:
        consequent, rule = eliminate_relative_pronouns(list1[m], slot)
    elif category == 11:
        consequent, rule = eliminate_as(list1[m], slot)
    elif category == 13 and kind2 in ["", "consequent"]:
        consequent, rule = divide_relations(list1[m], slot)
    elif category == 13.5 and kind2 in ["", "consequent"]:
        consequent, rule = divide_relations2(list1[m], slot)
    elif category == 14:
        consequent, rule = eliminate_there(slot, list1[m])
    elif category == 15:
        consequent, rule = eliminate_universals(antecedent, list1[m], slot)
    elif category == 16:
        return
        # consequent, rule = eliminate_many(list1[m], slot, list3)

    if consequent == None: return
    final_step(list1, antecedent, consequent, rule, category, anc1, kind)


def final_step(list1, antecedent, consequent2, rule, category, anc1, kind):
    assert anc1 != None
    conn = conditional if category in [.5, 13] else iff
    irule = "IF" if category in [.5, 13] else "EF"
    consequent = copy.deepcopy(consequent2)
    conjunction = []
    conjunctionp = []

    for sent in consequent: name_and_build(output, sent)
    if len(consequent) > 1:
        for sent in consequent: conjunction.append(sent[0])
        for sent in consequent: conjunctionp.append(sent[3] + sent[2])
        consequent_str = build_conjunction(conjunction)
        consequent_strp = build_conjunction(conjunctionp)
        standard = "not standard"
        tvalue = ""
    else:
        standard = is_standard(consequent[0])
        consequent_str = consequent[0][1]
        consequent_strp = consequent[0][2]
        tvalue = consequent[0][3]

    if kind == "":
        implication = build_connection(antecedent[0], conn, consequent_str)
        implicationp = build_connection(antecedent[3] + antecedent[2], conn, consequent_strp)
        add_to_tsent(output[0], implication, implicationp, "", rule)
        inferences.append([consequent_str, consequent_strp, tvalue, irule,
            antecedent[3] + antecedent[2], get_sn(output[0]), standard])

    for sent in consequent:
        if kind == "":
            sent[44] = get_sn(output[0])
            if len(consequent) > 1:
                inferences.append([sent[1], sent[2], sent[3], "AE",
                        get_sn(output[0]), "", is_standard(sent)])
        list1.append(copy.deepcopy(sent))


    return

######group: eliminate uninstantiable words part two



def eliminate_negative_determiners(slot, list1, m):
    # modify this if the category number of the universals change
    # modify this if we allow for two negative determiners in a sentence
    dict1 = {12:63, 121:65, 122:66, 123:67, 125:68, 149:61}
    dict2 = {125:68, 149:61}

    special_determinatives = ['a', 'every', 'many' + un, 'any' + un, 'many' + ud, 'few']
    sent = list1[m]
    counterpart = dict1.get(slot)
    if counterpart == None: return None, None
    if sent[counterpart] in special_determinatives:
        position = dict2.get(slot, counterpart)
        sent[slot] = None
        sent[3] = ""
        if sent[position] == 'every':
            raise Exception ("untested")
            sent[position] = 'many' + un
            g = sent[45].index((position, 15))
            sent[45].append((position, 1))
            rule = "DE ~ every"
        else:
            rule = "DE ~ " + sent[position]
            if sent[position] == 'many' + ud:
                g = sent[45].index((position, 16))
            elif sent[position] not in ['any' + un, 'many' + un]:
                g = sent[45].index((position, 1))

            if sent[position] == 'many' + un:
                raise Exception ("untested")
                sent[position] = 'few'
            else:
                sent[position] = 'no'
                sent[45].append((position, 15))
        sent[54].remove(slot)
        del sent[45][g]
        del list1[m]

        return [sent], rule
    else:
        return None, None


def infer_first_pronoun():
    global i_defined
    var = get_key(output[6], "person")
    if var == None:
        output[6].update({output[14][0]: 'person'})
        var = output[14][0]
        del output[14][0]
    cons = svo_sent(output, "i", "I", var)
    i_defined = True

    return [cons], "AY FPP"


def eliminate_determiners(list1, slot):
    word = list1[slot]
    list1[slot] = ""
    consequent = []
    cls = get_word_info(word)
    cls = cls[0]
    def_constants = dictionary[18].get(word)
    sentences = json.loads(json.dumps(cls.sentences))
    abbrev_dict = {}
    change_constants(abbrev_dict, output, def_constants)
    instance = None
    new_pos = determiner_dict.get(slot)
    if word == 'the':
        instance = definite_assignments.get(list1[new_pos])

    if instance == None:
        if word == 'the':
            definite_assignments.update({list1[new_pos]:output[14][0]})
        concept = cls.def_stats.concept
        instance = cls.def_stats.instance
        abbrev_dict.update({concept: list1[new_pos], instance[0]: output[14][0]})
        list1[new_pos] = output[14][0]
        del output[14][0]
    else:
        old_concept = cls.def_stats.concept
        old_instance = cls.def_stats.instance
        abbrev_dict.update({old_concept: list1[new_pos], old_instance[0]: instance})
        list1[new_pos] = instance

    replace_variables2(abbrev_dict, consequent, list1, sentences)

    consequent.append(list1)
    rule = "DE " + word

    return consequent, rule


def replace_variables2(abbrev_dict, consequent, list1, sentences):
    sentences[0] = list1
    for sentence in sentences[1:]:
        if sentence[13] != "R":
            for noun in sentence[42]:
                if sentence[noun] != "i":
                    var = abbrev_dict.get(sentence[noun])
                    if var == None:
                        abbrev_dict.update({sentence[noun]: output[14][0]})
                        sentence[noun] = output[14][0]
                        del output[14][0]
                    else:
                        sentence[noun] = var
            consequent.append(sentence)


def eliminate_pronouns(list1, slot):
    word = list1[slot]
    consequent = []
    cls = get_word_info(word)
    cls = cls[0]
    sentences = json.loads(json.dumps(cls.sentences))
    abbrev_dict = {}
    def_constants = dictionary[18].get(word)
    change_constants(abbrev_dict, output, def_constants)
    new_var = get_key(output[6], word)
    abbrev_dict.update({cls.def_stats.instance[0]: new_var})
    list1[slot] = new_var
    replace_variables2(abbrev_dict, consequent, list1, sentences)
    consequent.append(list1)
    rule = "DE " + word

    return consequent, rule


def eliminate_proper_name_possessives3(list1, slot):
    concept_position = 10 if slot == 134 else 14
    new_possessor = list1[slot][:-2]
    possessee_concept = list1[concept_position]
    new_possessee = definite_assignments.get(possessee_concept)
    if new_possessee == None:
        definite_assignments[possessee_concept] = output[14][0]
        new_possessee = output[14][0]
        del output[14][0]
    list1[slot] = None
    list1[concept_position] = new_possessee
    cons2 = svo_sent(output, new_possessor, "OWN", new_possessee)
    cons3 = svo_sent(output, new_possessee, "I", possessee_concept)

    return [list1, cons2, cons3], "PPE"


def eliminate_common_name_possessives(list1, slot):
    concept_position = 10 if slot == 134 else 14
    possessor_concept = list1[slot][:-2]
    possessee = list1[concept_position]
    new_possessor = definite_assignments.get(possessor_concept)
    if new_possessor == None:
        definite_assignments[possessor_concept] = output[14][0]
        new_possessor = output[14][0]
        del output[14][0]
    list1[slot] = None
    cons2 = svo_sent(output, new_possessor, "OWN", possessee)
    cons3 = svo_sent(output, new_possessor, "I", possessor_concept)

    return [list1, cons2, cons3], "CPE"


def eliminate_and_coordinator(list1, slot):
    # todo this might need to come before the definite articles
    dict1 = {132:11, 133:15}
    old_noun_pos = dict1.get(slot)
    new_noun_pos = old_noun_pos - 1
    new_var = list1[old_noun_pos]
    list1[slot] = None
    list1[54].remove(old_noun_pos)
    list1[old_noun_pos] = None
    list1[42].remove(old_noun_pos)
    list2 = copy.deepcopy(list1)
    list2[new_noun_pos] = new_var

    return [list1, list2], "DE and" + uc


def eliminate_adjectives(list1, slot):
    dict1 = {76: 12, 78: 12, 80: 121}
    relat_to_adj = {78: 13, 80: 20, 76: 13}
    neg_pos = dict1.get(slot)
    relat_pos = relat_to_adj.get(slot)
    # the point of the code below is that when I say b is a green c, 'green'
    # modifies b not c
    if list1[relat_pos] == "I":
        dict2 = {78: 10, 80: 14}
        noun_pos = dict2.get(slot)
        rule = 'CADJ E'
    else:
        noun_pos = pos_counterpart(modifiable_nouns, adjective_positions, slot)
        rule = 'ADJ E'
    cons2 = svo_sent(output, list1[noun_pos], "J", list1[slot], list1[neg_pos])

    list1[slot] = None
    if list1[neg_pos] == "~":
        list1[3] = ""
        list1[neg_pos] = ""
        list1[54].remove(neg_pos)

    return [list1, cons2], rule


def eliminate_concept_instance_apposition(list1, slot):
    dict1 = {91: 10, 93: 14, 95: 21, 96: 23}
    j = dict1.get(slot)
    cons2 = svo_sent(output, list1[slot], "I", list1[j])
    list1[j] = list1[slot]
    list1[slot] = None
    list1[42].remove(slot)

    return [list1, cons2], "CIA"


def eliminate_relative_pronouns(cons1, slot):
    rule = "DE " + cons1[slot]
    pos = relative_pronoun_positions.index(slot)
    noun = standard_nouns[1:][pos]
    clause_members = cons1[47].get(slot)
    del cons1[47][slot]
    cons2 = list(map(lambda x: cons1[x], clause_members))
    cons2.insert(0, cons1[noun])
    for x in clause_members:
        cons1[x] = None
        cons1[54].remove(x)
    try:
        cons2[cons2.index('not')] = "~"
    except:
        pass

    cons2 = categorize_words(output[6], cons2, False, output[8], output[9])

    return [cons1, cons2], rule


def eliminate_as(list1, slot):
    # modify this if 'as' can be placed in a location other than 15
    list1[slot] = None
    list1[54].remove(21)
    cons2 = svo_sent(output, list1[21], list1[13], list1[14])
    list1[21] = None

    return [list1, cons2], "DE AS"


def divide_relations(list1, slot):
    # b R c S d > b S d
    subject = 10 if slot == 20 else slot - 1
    tvalue, rule = axiom_of_prepositional_non_existence(list1, slot, "RDA")
    cons = svo_sent(output, list1[subject], list1[20], list1[slot + 1], tvalue)

    return [cons], rule


def divide_relations2(list1, slot):
    # (b R c S d T e) = (b R c & b S d T e)

    tvalue, rule = axiom_of_prepositional_non_existence(list1, slot, "RDB")
    cons1 = svo_sent(output, list1[10], list1[13], list1[14])
    cons2 = svo_sent(output, list1[10], list1[20], list1[21], tvalue)

    return [cons1, cons2], "RDB"


def axiom_of_prepositional_non_existence(list1, slot, rule):
    if list1[13] == 'EX' and list1[3] == "~": #todo this is a hard-coded rule
        return "~", rule + ",NT"
    return "", rule


def eliminate_there(slot, list1):
    list1[slot] = None
    if slot == 10:
        dict1 = {14: 10, 63: 61, 78: 76}
    assert slot == 10
    list54 = []
    list42 = []
    for k, v in dict1.items():
        list1[v] = list1[k]
        if not_blank(list1[k]):
            list54.append(v)
            if v in standard_nouns: list42.append(v)
        list1[k] = None
    list1[13] = 'EX'
    list54.append(13)
    list1[54] = list54
    list1[42] = list42

    return [list1], "DE there"



####################
##### The following functions are related to the definition of
####### every, no, many, only and some


def lies_wi_scope_of_univ_quant(list1, slot):
    # modify this if you allow for more than one universal quantifier in a sentence
    # or you allow for more than one subclause
    # or you increase the number of determinatives

    bool1 = False
    univ_pos = find_sibling_int(15, list1[45], 1, 0)
    if univ_pos > -1:
        # 15 means there is a universal quantifier in the sentence

        current_universal = list1[univ_pos]

        if slot in adjective_positions:
            bool1 = lies_wi_scope_of_univ2(list1, current_universal, slot, univ_pos, adjective_positions)
        elif slot in relative_pronoun_positions:
            bool1 = lies_wi_scope_of_univ2(list1, current_universal, slot, univ_pos, relative_pronoun_positions)
        elif list1[slot] in dictionary[8]:
            if any([x[1] in [15, 16] for x in list1[45]]):
                return True
            else:
                return False

    return bool1

def lies_wi_scope_of_univ2(list1, current_universal, slot, univ_pos, pos_position):
    determiner = pos_counterpart(determinative_positions, pos_position, slot)
    if list1[determiner] in ['a' + uh, 'every', 'no']:
        return True
    else:
        return False

def eliminate_universals(orig_sent, list1, slot):
    word = list1[slot]
    rule = "DE " + list1[slot]
    new_var = output[14][0]
    del output[14][0]
    rel_pro = pos_counterpart(relative_pronoun_positions, determinative_positions, slot)
    noun_c = pos_counterpart(standard_nouns[1:], determinative_positions, slot)
    class_sent = svo_sent(output, new_var, "I", list1[noun_c])
    list1[rel_pro] = None
    if rel_pro in list1[54]: list1[54].remove(rel_pro)
    subclause = list1[47].get(rel_pro)
    list1[noun_c] = new_var
    ant_done = False


    if subclause != None:
        antecedent = list(map(lambda x: list1[x], subclause))
        antecedent.insert(0, new_var)
        consequent = list(filter(lambda x: x not in subclause, list1[54]))
        consequent = list(map(lambda x: list1[x], consequent))
    elif slot == 61 and list1[13] in dictionary[8] + dictionary[17]:
        antecedent, consequent = backwards_conditional(list1, slot, noun_c, new_var)
    elif slot == 61 and list1[13] not in dictionary[8]:
        antecedent = class_sent[0]
        antecedentp = class_sent[2]
        ant_done = True
        consequent = [list1[x] for x in list1[54]]
    else:
        if slot in [63, 64]:
            next_rel = 20
        else:
            det_idx = determinative_positions[4:].index(slot)
            next_rel = relational_positions[2:][det_idx]
        if list1[next_rel] == None:
            antecedent = class_sent[0]
            antecedentp = class_sent[2]
            ant_done = True
            consequent = [list1[x] for x in list1[54]]
        else:
            raise Exception

    if not ant_done:
        antecedent, antecedentp = put_in_main_loop(antecedent, class_sent, "antecedent", word)
    consequent, consequentp = put_in_main_loop(consequent, class_sent, "consequent", word)

    list2 = [None] * 46
    list2[0] = build_connection(antecedent, conditional, consequent)
    list2[2] = build_connection(antecedentp, conditional, consequentp)
    list2[45] = []
    output[1].append(list2)


    implication = build_connection(orig_sent[0], iff, "(" + list2[0] + ")")
    implicationp = build_connection(orig_sent[3] + orig_sent[2], iff, "(" + list2[2] + ")")
    add_to_tsent(output[0], implication, implicationp, "", rule)
    inferences.append([list2[0], list2[2], "", "EF",
                       orig_sent[3] + orig_sent[2], get_sn(output[0]), "standard"])

    return None, None


def backwards_conditional(list1, slot, noun_c, new_var):
    m = slot
    antecedent = []
    for num in list1[54]:
        word = list1[num]
        if num in relational_positions and list1[m] not in dictionary[8] + dictionary[17] \
            and num != 13:
            break
        elif num != noun_c:
            antecedent.append(word)
        elif num == noun_c:
            antecedent.append(new_var)

    idx = list1[54].index(num)
    consequent = [list1[x] for x in list1[54][idx:]]
    consequent.insert(0, list1[noun_c])

    return antecedent, consequent







def put_in_main_loop(list2, class_sent, kind, word):
    for i, obj in enumerate(list2):
        obj = 'a' if obj == 'a' + uh else obj
        list2[i] = obj

    list2 = categorize_words(output[6], list2, False, output[8], output[9], False, True)

    if kind == 'consequent' and word == 'no':
        list2[3] = "" if list2[3] == "~" else "~"

    list2[44] = 0
    if list2[45] != [] or kind == 'antecedent':
        if list2[45] != []:
            list2 = main_loop([list2], "recursive", kind)
        if kind == 'antecedent':
            if len(list2) > 12:
                list2 = [list2]
            list2.append(class_sent)
    else:
        list2 = [list2]

    for lst in list2:
        if lst[0] == None: name_and_build(output, lst)

    list3 = [x[0] for x in list2]
    list3p = [x[3] + x[2] for x in list2]
    if len(list3) > 1:
        final = "(" + " & ".join(list3) + ")"
        finalp = "(" + " & ".join(list3p) + ")"
    else:
        final = list2[0][3] + list2[0][1]
        finalp = list2[0][3] + list2[0][2]


    return final, finalp

