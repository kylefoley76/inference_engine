import operator
# try:
from settings import *
from general_functions import *
from grammar import check_grammar
# except:
#     from .settings import *
#     from .general_functions import *
#     from .grammar import check_grammar



category = 0
sentence_slots = []
relation_type = 0
slot = 0
subclause_counter = 164
word = ""
ad_hoc_sentence = False
is_a_standard_sent = True
order_of_definition = []


def is_ad_hoc_sentence(list1):
    global ad_hoc_sentence
    if "concept" + ua in list1:
        ad_hoc_sentence = True


def categorize_words(abbreviations, list1, dictionary2, output=[], kind=""):
    global slot, category, relation_type, word, sentence_slots, is_a_standard_sent
    global subclause_counter, order_of_definition, dictionary
    dictionary = dictionary2
    is_a_standard_sent = False if kind in ['not standard', "sub words", "recursive"] else True
    sub_words = True if kind == 'sub words' else False
    if output != []:
        abbreviations = output.abbreviations


    list1 = [None] * 4 + list1 + [None]
    list1[3] = ""
    sentence_slots = [None] * 200
    for pos in negative_positions: sentence_slots[pos] = ""
    sentence_slots[3] = ""
    relation_type = 0
    subclause_counter = 164
    order_of_definition = []
    places_used = []
    noun_pos = []
    subclauses = {}
    is_ad_hoc_sentence(list1)
    special_tilde = False

    i = 3
    while list1[i] != None:
        i += 1
        if list1[i] == ',':
            del list1[i]

        word = list1[i]
        slot = 0

        if word == '&':
            return
            bb = 8

        if not_blank(word):

            if output != []:
                if not isvariable(word):
                    output.words_used.add(word)

            i, word = determine_if_compound_word(word, i, list1)

            category = dictionary.decision_procedure.get(word)

            raw_pos, word = get_part_of_speech(word, abbreviations, output)

            part_of_speech = parts_of_speech_dict.get(raw_pos[0])

            insert_tilde = False

            ################# the mini_e symbol ############

            if word == mini_e:
                slot = 9

            ############### determiners #################

            elif part_of_speech == "determiner":

                d_dict = {0: 61, 1: 63, 2: 65, 3: 66, 4: 67, 5: 68, 6: 69}
                slot = d_dict.get(relation_type)

            ################ possessives ############

            elif part_of_speech == 'possessor':

                if relation_type == 0 and sentence_slots[10] == None:
                    slot = 134
                elif relation_type == 1 and sentence_slots[14] == None:
                    slot = 135

            ########## adjectives #########

            elif part_of_speech == 'adjective':

                str1 = get_adjective_positions()
                if str1 != "":
                    get_noun_positions(noun_pos, list1, i)
                else:
                    if category == 18:
                        order_of_definition.append((slot, category))
                    category = 6

            ######### negations ###########

            elif part_of_speech == 'negator':

                insert_tilde, special_tilde = get_negation_positions()
                if word == "~": sentence_slots[3] = "~"

            ########### nouns #############

            elif part_of_speech == 'noun':

                get_noun_positions(noun_pos, list1, i)

            ######### and coordinator ###########

            elif part_of_speech == 'and coordinator':

                and_coordinator()

            ########### relative pronouns ##########

            elif part_of_speech == 'relative pronoun':

                get_relative_pronoun_positions()

            ################## relations #############

            elif part_of_speech == 'relation':

                slot = relational_positions[relation_type]
                relation_type += 1

            if slot == 0:
                print(list1)
                raise Exception("our system does not have this grammatical syntax yet")

            final_categories(insert_tilde, places_used, raw_pos, sub_words)

            if part_of_speech == 'relative pronoun':
                i = build_subclause(list1, i, subclauses, abbreviations, places_used)

    sentence_slots[45] = sorted(order_of_definition, key=operator.itemgetter(1))
    sentence_slots[42] = noun_pos
    sentence_slots[54] = places_used
    sentence_slots[47] = subclauses

    if output != []:
        str1 = check_grammar(sentence_slots)
        if str1 != "":
            return str1

    if kind != "recursive":
        sentence_slots[58] = determine_constants(abbreviations, sentence_slots)

        if output != []:
            name_and_build(output, sentence_slots)
        else:
            sentence_slots[1] = build_sent_pos(sentence_slots)
            sentence_slots[0] = nbuild_sent(sentence_slots, sentence_slots)
        if special_tilde:
            sentence_slots[0] = sentence_slots[0].replace("(~ ", "~(")


    return sentence_slots


def final_categories(insert_tilde, places_used, raw_pos, sub_words):
    global category

    if ad_hoc_sentence: raw_pos = exceptional_parts_of_speech(raw_pos)

    sentence_slots[slot] = word

    if insert_tilde:
        places_used.insert(-1, slot)
    else:
        places_used.append(slot)

    if not is_a_standard_sent:

        category = place_in_decision_procedure(category, slot, word, raw_pos)

        divide_the_i_relation()

        if category in [13, 13.5] and slot == 13:
            pass
        elif category != None:
            order_of_definition.append((slot, category))

        slots_word_sub = standard_nouns + adjective_positions + instantial_nouns + \
                         possessor_positions + relational_positions + \
                         negative_positions

        if slot in slots_word_sub and \
                category not in [2, .5, 14, 19] and \
                sub_words and \
                raw_pos[:2] != "rs":
            order_of_definition.append((slot, 0))


def and_coordinator():
    global slot
    slot = 0
    if relation_type == 0 and sentence_slots[10] != None:
        slot = 132  # uuu
    elif relation_type == 1 and sentence_slots[14] != None:
        slot = 133
    return


def get_negation_positions():
    global slot
    insert_tilde = False
    special_tilde = False
    slot = 0

    if sentence_slots[60] == None and sentence_slots[10] == None:
        if word == "~":
            slot = 3
            special_tilde = True
        else:
            slot = 149
    elif relation_type == 0:
        slot = 12
    elif (relation_type == 1 and sentence_slots[14] == None and sentence_slots[108] == None):
        slot = 12
        # because 'not' in this location comes after the relation we must
        # insert to before the relation
        insert_tilde = True
    elif relation_type == 1:
        slot = 121
    elif relation_type == 2 and sentence_slots[20] in spec_rel:
        slot = 121
        insert_tilde = True
    elif relation_type == 2:
        slot = 122
    elif relation_type == 3 and sentence_slots[21] in spec_rel:
        slot = 122
        insert_tilde = True
    elif relation_type == 3:
        slot = 123
    elif relation_type == 4 and sentence_slots[23] in spec_rel:
        slot = 123
        insert_tilde = True
    elif relation_type == 4 or sentence_slots[26] in spec_rel:
        slot = 124

    if word == 'not':
        insert_tilde = False

    return insert_tilde, special_tilde


def get_adjective_positions():
    global slot
    if relation_type == 0:
        slot = 76 if sentence_slots[10] == None else 77
    else:
        relevant_relation = relational_positions[relation_type - 1]
        if sentence_slots[relevant_relation] not in the_is_of_adjective:
            if relation_type == 1:
                slot = 78 if sentence_slots[14] == None else 79
            else:
                slot = relation_type + 78
        else:
            return "is predicative complement"
    return ""


def get_relative_pronoun_positions():
    global slot
    if relation_type == 0:
        slot = 106 if sentence_slots[11] == None else 107
    else:
        if relation_type == 1:
            slot = 108 if sentence_slots[14] != None else 109
        else:
            slot = relation_type + 104

    return


def build_subclause(list1, i, subclauses, abbreviations, placed_used):
    global subclause_counter
    i += 1
    list2 = []
    list3 = []
    num_of_relations = 0
    while list1[i] != None:
        temp_word = list1[i]
        if temp_word == ',':
            subclauses.update({slot: list3})
            return i - 1
        i, temp_word = determine_if_compound_word(temp_word, i, list1)
        raw_pos = get_part_of_speech(temp_word, abbreviations)
        list2.append(raw_pos[0])
        subclause_counter += 1
        sentence_slots[subclause_counter] = temp_word
        list3.append(subclause_counter)
        placed_used.append(subclause_counter)
        if temp_word == 'is' + ua:
            bb = 8

        if raw_pos[0] == 'r':
            num_of_relations += 1

        try:
            # this is because words in the subclause have to be replaced with variables
            if raw_pos[0] in ['n', 'a', 'r', 'o', 's'] and not isvariable(temp_word) and \
                    not raw_pos[1] == 'y':
                order_of_definition.append((subclause_counter, 0))
        except:
            pass
        if len(raw_pos) > 2 and raw_pos[2] == 'd':
            order_of_definition.append((subclause_counter, 19))
        if len(raw_pos) > 1 and raw_pos[1] == 's':
            order_of_definition.append((subclause_counter, 18))

        i += 1

    if relation_type == 0:
        if list2.count("r") == 1:
            raise Exception("grammatical error")
        else:
            i -= 1
            while list2 != []:

                sentence_slots[subclause_counter] = None
                placed_used.remove(subclause_counter)
                subclause_counter -= 1
                del list2[-1]
                del list3[-1]
                del order_of_definition[-1]
                i -= 1

                if list2[-1][0] == 'r':
                    sentence_slots[subclause_counter] = None
                    placed_used.remove(subclause_counter)
                    subclause_counter -= 1
                    del list2[-1]
                    del list3[-1]
                    del order_of_definition[-1]
                    subclauses.update({slot: list3})
                    i -= 1
                    return i

        raise Exception("either ungrammatical or wrong syntax")

    else:
        subclauses.update({slot: list3})
        return i - 1


def get_noun_positions(noun_pos, list1, i):
    global slot
    slot = 0
    try:
        next_word = list1[i + 1]
    except:
        next_word = ""

    if is_a_standard_sent:
        get_standard_noun_positions(next_word)
    else:

        if relation_type == 0:
            if next_word == mini_e:
                slot = 8

            elif sentence_slots[10] == None:
                slot = 10
            elif sentence_slots[132] != None:
                if sentence_slots[11] == None:
                    slot = 11
                else:
                    slot = 92
            else:
                slot = 91

        elif relation_type == 1:
            if sentence_slots[14] == None:
                slot = 14
            elif sentence_slots[133] != None:
                if sentence_slots[15] == None:
                    slot = 15
                else:
                    slot = 94
            else:
                slot = 93

        else:
            c = (relation_type * 2) + 17
            if sentence_slots[c] == None:
                slot = c
            else:
                slot = 93 + relation_type

    noun_pos.append(slot)
    return


def get_standard_noun_positions(next_word):
    global slot
    if next_word == mini_e:
        slot = 8
        return
    if relation_type == 0:
        slot = 10 if sentence_slots[10] == None else 11
    elif relation_type == 1:
        for m in range(14, 20):
            if sentence_slots[m] == None:
                slot = m
                return
    else:
        slot = standard_nouns[relation_type + 7]


def divide_the_i_relation():
    global category
    if slot in relational_positions2:
        b = relational_positions.index(slot)
        i_relation = relational_positions[b - 1]
        if sentence_slots[i_relation] in the_is_of_group:
            dict2 = {20: 108, 22: 110, 24: 111}
            rel_pronoun_pos = dict2.get(slot)
            if sentence_slots[rel_pronoun_pos] == None:
                category = 13.5

    return category


def place_in_decision_procedure(category, slot, word, raw_pos):
    if raw_pos[0] == 'o':
        category = 3  # common name possessives
    elif raw_pos[0] == 's':
        category = 4  # proper name possessives
    elif slot in instantial_nouns:  # CIA
        category = 7

    return category

def rename_sentences(old_word, new_word, output):
    for e, sent in enumerate(output.all_sent):
        if old_word in sent[0]:
            output.all_sent[e][0] = output.all_sent[e][0].replace(old_word, new_word)
            for j, slot in enumerate(sent):
                if slot == old_word:
                    sent[j] = new_word
                    break

    for var, prop in output.oprop_name.items():
        if old_word in prop:
            prop = prop.replace(old_word, new_word)
            output.oprop_name[var] = prop
    for prop, var in output.prop_name.items():
        if old_word in prop:
            new_prop = prop
            del output.prop_name[prop]
            new_prop = new_prop.replace(old_word, new_word)
            output.prop_name.update({new_prop: var})
            break
    for sent in output.total_sent:
        if old_word in sent[1]:
            sent[1] = sent[1].replace(old_word, new_word)

    output.words_used.remove(old_word)
    output.words_used.add(new_word)
    return



def get_part_of_speech(word, abbreviations, output=[]):
    while True:
        pos = dictionary.pos.get(word)
        if isvariable(word):
            reference = abbreviations.get(word)
            pos = dictionary.pos.get(reference)
            pos = 'ny' if pos == None or pos[0] != 'a' else 'ay'
            break
        elif word[-2:] == "'s":
            pos = 's' if dictionary.kind.get(word[:-2]) == 'i' else 'o'
            break
        elif pos == None:
            if output == []:
                print ('you mispelled ' + word)
                raise Exception ('you mispelled ' + word)
            else:
                old_word = word
                print ('you mispelled ' + old_word)
                new_word = input("new word: ")
                while True:
                    if new_word in dictionary.pos.keys():
                        pos = dictionary.pos.get(new_word)
                        break
                    else:
                        print (f'{new_word} is also a mispelling')
                        new_word = input("new word: ")

                rename_sentences(old_word, new_word, output)
                word = new_word
                break
        else:
            break


    return pos, word


def determine_if_compound_word(word3, i, list1):
    if word3 == "not":
        bb = 8

    double = dictionary.doubles.get(word3)
    triple = dictionary.triples.get(word3)
    triple_word = ""

    if triple != None:
        if list1[i + 1] != None and list1[i + 2] != None:

            after_next_word = list1[i + 2]
            next_word = list1[i + 1]
            triple_word = word3 + " " + next_word + " " + after_next_word
            if triple_word in triple:
                i += 2
                word3 = triple_word
            else:
                triple_word = ""
        else:
            triple_word = ""

    if triple_word == "" and double != None:
        if list1[i + 1] != None:
            next_word = list1[i + 1]
            double_word = word3 + " " + next_word
            if double_word in double:
                i += 1
                word3 = double_word

    return i, word3


def exceptional_parts_of_speech(raw_pos):
    global slot
    if word == 'doglike':
        bb = 8
    noun_pos = slot + 1
    dict1 = {5: 35, 14: 36, 18: 37, 22: 38}
    if sentence_slots[noun_pos] == 'concept' + ua and raw_pos[0] == "a":
        slot = dict1.get(noun_pos)
        raw_pos = 'n' if len(raw_pos) > 1 else "n" + raw_pos[1:]

    return raw_pos
