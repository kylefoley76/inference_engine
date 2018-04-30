import json

try:
    from general_functions import *
except:
    from .general_functions import *


# from general_functions import *


def disam_is(sent, num, dictionary, abbreviations):
    a_found = False
    aidx = 0
    for num2, word2 in enumerate(sent):
        if num2 > num:
            if isvariable(word2):
                word2 = abbreviations.get(word2)
                pos = dictionary.pos.get(word2)
                isconcept = True if dictionary.kind.get(word2) == 'c' else False
            else:
                pos = dictionary.pos.get(word2, "xx")
                isconcept = True if dictionary.kind.get(word2) == 'c' else False

            if word2 in ['a', "an"]:
                a_found = True
                aidx = num2

            if a_found and isconcept:
                sent[num] = 'I'
                del sent[aidx]
                return sent

            elif pos[0] == 'n' and dictionary.kind.get(word2) == 'i':
                sent[num] == '='
                return sent

            elif pos[0] == 'a' and not a_found:
                sent[num] = "J"

                return sent
    return






def disambiguate_sentence(output, dictionary):
    for e, sent in enumerate(output.all_sent):
        b = sent[4:].index(None) + 4

        sent = eliminate_blanks(sent[4:b])

        sent = determine_if_compound_word(sent, dictionary)

        eliminate_particles(sent, output, dictionary, e)

        disambiguate_pos(sent, dictionary, output, e)

        disam_is2(sent, dictionary, output, e)

    return


def disam_is2(sent, dictionary, output, m):
    replacement_made = False
    got_orig = False
    for num, word in enumerate(sent):
        if word == 'is':
            if not got_orig:
                olist = json.loads(json.dumps(sent))
                ant_sent, ant_sentp = get_ant_sent(olist, output)
                got_orig = True

            replacement_made = True
            sent = disam_is(sent, num, dictionary, output.abbreviations)
            rule = "D is"
            output.all_sent[m] = sent

    if replacement_made:
        name_build_pre_cat(output, sent, ant_sent, ant_sentp, rule, "")


def disambiguate_pos(list1, dictionary, output, e):
    last_pos = "bbb"
    relation_type = 0
    am_dict = {}
    replacement_made = False
    for i, word in enumerate(list1):
        if word == 'causes':
            bb = 8

        raw_pos, word = get_part_of_speech(word, dictionary, output.abbreviations, output)

        if raw_pos[0] == 'r':
            relation_type += 1

        if raw_pos[0] == 'y':
            olist = json.loads(json.dumps(list1))
            replacement_made = True
            old_word = word
            possible_plural = False
            if word in dictionary.plurals.keys() and\
                    dictionary.plurals.get(word) != word:
                possible_plural = True

            if last_pos[0] in ['d', 'a', "r"]:
                raw_pos = "n"

            elif last_pos[0] in ['n', 'u']:
                next_word = list1[i + 1]
                npos = dictionary.pos.get(next_word)
                if npos[0] in ['r', 'e', 'w']:
                    raw_pos = "n"
                else:
                    if word[-1] != "s": word += "s"
                    word = word + uv

            if raw_pos[0] == 'n':
                if possible_plural:
                    word = dictionary.plurals.get(old_word)
                    word = word + un
                else:
                    word = word + un

            am_dict.update({old_word: word})
            raw_pos = dictionary.pos.get(word)
            if raw_pos[0] == "w":
                disam_intran(dictionary, list1, i, am_dict, old_word)

        last_pos = raw_pos


    if replacement_made:
        ant_sent, ant_sentp = get_ant_sent(olist, output)
        output.all_sent[e] = list1
        anc1 = ""
        rule = "D " + ",".join(am_dict.keys())
        replace_words(list1, am_dict)
        name_build_pre_cat(output, list1, ant_sent, ant_sentp, rule, anc1)


def replace_words(list1, am_dict):
    for e, word in enumerate(list1):
        new_word = am_dict.get(word)
        if new_word != None:
            list1[e] = new_word



def eliminate_particles(list1, output, dictionary, aidx):
    particle_found = False
    got_orig_list = False
    i = 0
    deleted = []
    am_dict = {}
    location = 0
    particles = {}
    olist = []

    while i < len(list1):
        word = list1[i]
        if word not in particles.keys():
            pos, word = get_part_of_speech(word, dictionary, output.abbreviations, output)

        if word in dictionary.particles.keys() and not particle_found:
            list2 = dictionary.particles.get(word)
            particle_found = True
            particles = dictionary.ambiguous3.get(word)
            location = i
            if not got_orig_list:
                olist = json.loads(json.dumps(list1))
                got_orig_list = True

        elif particle_found and word in list2:
            deleted.append(list1[i])
            if particles != None:
                new_word = particles.get(word)
                am_dict.update({location: new_word})

            del list1[i]
            i -= 1
        elif pos[0] == 'u' or word == ',' and particle_found:
            particle_found = False

        i += 1

    if particles != {}:
        ant_sent, ant_sentp = get_ant_sent(olist, output)
        rule = build_rule(am_dict, deleted, list1, location, particles)
        output.all_sent[aidx] = list1
        anc1 = ""
        name_build_pre_cat(output, list1, ant_sent, ant_sentp, rule, anc1)
    return


def build_rule(am_dict, deleted, list1, location, particles):
    old_words = []
    if am_dict != {}:

        for k, v in am_dict.items():
            k = int(k)
            old_words.append(list1[k])
            list1[k] = v
        rule = "RD " + ",".join(deleted)

    else:
        old_word = list1[location]
        rule = "D " + old_word
        new_word = particles.get("0")
        list1[location] = new_word
    return rule


def get_ant_sent(olist, output):
    ant_sent =  " ".join(olist)
    ant_sent_ns = ant_sent.replace(" ", "")
    ant_sentp = output.prop_name.get(ant_sent_ns)
    return ant_sent, ant_sentp


def disam_intran(dictionary, list1, i, am_dict, old_word):
    oword = old_word
    if not old_word.endswith("s"): old_word += "s"
    if i + 1 == len(list1):
        new_word = old_word + ui
    else:
        next_word = list1[i + 1]
        pos = dictionary.pos.get(next_word)
        if pos[0] in ["d", "n"]:
            new_word = old_word + ut
        else:
            new_word = old_word + ui

    am_dict.update({oword: new_word})
