from general_functions import *
import copy
import collections
import operator
import json


intro_sent = []
subst_rules = ["DF", "TR", "LY", "SUB", "SUBI", "SUBJ", "IN", "AX", "CE", xorr]
subst_sent = []
uninstant_prem_rules = ["DE", "SUY"]
uninstant_prem = []
uninstant_infer_rules = ["EF", "IF", "AE"]
uninstant_infer = []
stan_prem_rules = ["SUBI", "LE"]
stan_prem_sent = []
st_infer_rules = [iff + "E", "MP", "MT", "EN", "&I", "&E", idisj + "E", "ASC",
                  mini_e + "E", "~~E", bottom + "I", consist + "I", xorr + "E", "SUBJ",
                   "AY"]
stan_infer_sent = []
constant_sent = ""


def build_temp_total(new_numbers, pn, list1, temp_total_sent, sub_dict, heading):

    if list1 == []: return pn

    add_heading(heading, temp_total_sent)

    for lst in list1:
        if lst[0] == 25:
            bb = 8

        if lst[3] + lst[2] in sub_dict.keys():
            lst[0] = sub_dict.get(lst[3] + lst[2])

        if lst[0] not in new_numbers.keys():
            pn += 1
            if lst[0] == 22:
                bb = 8
            new_numbers.update({lst[0]: pn})
            lst[0] = pn
        else:
            lst[0] = new_numbers.get(lst[0])




        temp_total_sent.append(lst)

    return pn


def rearrange_subst_sent(new_numbers, pn, sub_dict, remainder, temp_total_sent, put_in_premise):
    if output[13] == {}: return
    sub_sentences = []
    for k, v in output[13].items():
        if k == 'personhood':
            bb = 8
        rule_counter = collections.Counter([x[4] for x in v])
        try:
            conj_number = len(dictionary[16].get(k))
        except:
            conj_number = 0
        subi_count = rule_counter.get('SUBI', 0)
        subj_count = rule_counter.get('SUBJ', 0)

        kind = 0
        if k[:2] == "qu":
            kind = 3

        elif subi_count > 1 and subj_count == 0 and subi_count > conj_number + 1:
            kind = 1
        elif subj_count > 1 and subj_count > conj_number + 1:
            kind = 2
        subi_counter = 0
        subj_counter = 0
        if k[0] in ['1','2','3','4', '5'] or kind == 2:
            m = 0
            while v[m][4] not in ['SUBJ', 'AY IDT']:
                m += 1
            anc1 = new_numbers.get(v[m][5])
            pos = findposinmd(anc1, output[0], 0)
            orig_subi = output[0][pos]
            if k[0] in ['1','2','3','4', '5']:
                subj_counter = 1
                sub_sentences.append(orig_subi)

        for j, lst in enumerate(v):

            if j == 0:
                odef_name = lst[4]
            if lst in sub_sentences: # this is because sometimes the same sentence
                pass # will appear twice in the substitutions
            elif lst[4] not in ['SUBI', 'SUBJ', 'AY IDT'] and kind != 3 and \
                lst[4] not in put_in_premise:
                pn += 1
                new_numbers.update({lst[0]: pn})
                lst[0] = pn
                v[j][0] = pn
            if lst[4] == 'SUBI':
                subi_counter += 1
                sub_dict.update({lst[0]: odef_name})
                if subj_count == 0:
                    remainder.append(lst)


            elif lst[4] in 'SUBJ':
                subj_counter += 1
                if subj_counter > conj_number and kind == 2:
                    sub_sentences.insert(len(sub_sentences)-1, orig_subi)


            sub_sentences.append(lst)

    if consistent:
        add_heading("REMAINDER", temp_total_sent)
        remainder.sort()
        for sent in remainder: temp_total_sent.append(json.loads(json.dumps(sent)))
    add_heading("SUBSTITUTIONS", temp_total_sent)
    for sent in sub_sentences: temp_total_sent.append(json.loads(json.dumps(sent)))
    for lst in temp_total_sent:
        if lst[1].startswith("SUB"):
            break
        lst[4] = sub_dict.get(lst[0], lst[4])

    return sub_sentences


def rearrange(kind, output2, consistent2, artificial2):
    global consistent, output, artificial, constant_sent

    output = output2
    consistent = consistent2
    artificial = artificial2
    temp_total_sent = []
    new_numbers = {}

    # 1 - SUBSTITUTIONS (substitute)  sub, subi, subj, not suy, IN, TR
    # 2 - NATURAL LANGUAGE PREMISES (nl_premise)  (everything else is a nl_premise,)
                # and that includes blanks
    # 3 - NATURAL LANGUAGE INFERENCES  (nl_inferences)
    # 4 - STANDARD PREMISES  (st_premises)  SUBI,
    # 5 - STANDARD INFERENCES (st_inferences) SUBJ
    # if the argument is completely artificial then we do not need a heading
    # saying 'natural language premises'


    insert_quantifiers(output)

    build_constant_sent(output)

    put_in_premise = categorize_by_rule(output)

    pn = build_intro_sent(new_numbers, temp_total_sent)

    constant_list, pn = build_constant_sent2(new_numbers, pn, temp_total_sent)

    sub_dict = {}

    standard_premises = []

    if uninstant_prem != [] and not artificial:

        pn = build_temp_total(new_numbers, pn, uninstant_prem, temp_total_sent, sub_dict, "UNINSTANTIABLE PREMISES")

        pn = build_temp_total(new_numbers, pn, uninstant_infer, temp_total_sent, sub_dict, "UNINSTANTIABLE INFERENCES")

        repeat_standard_premises(kind, standard_premises, temp_total_sent)

        temp_total_sent.append([""] * 7)

        temp_total_sent.append(constant_list)

        standard_premises += stan_prem_sent

        standard_premises.sort()

        pn = build_temp_total(new_numbers, pn, standard_premises, temp_total_sent, sub_dict, "INSTANTIABLE PREMISES")

    else:

        artificial_sent = uninstant_prem + stan_prem_sent

        pn = build_temp_total(new_numbers, pn, artificial_sent, temp_total_sent, {}, "PREMISES")

    heading = 'INFERENCES' if artificial else "INSTANTIABLE INFERENCES"

    pn = build_temp_total(new_numbers, pn, stan_infer_sent, temp_total_sent, {}, heading)

    remainder = build_remainder(consistent, standard_premises)

    rearrange_subst_sent(new_numbers, pn, sub_dict, remainder, temp_total_sent, put_in_premise)

    output[0] = temp_total_sent
    renumber_sentences(new_numbers)
    assert isinstance(output[0][-1][0], int)
    if kind == 'last':
        rearrange_sent_abbrev(artificial)
        rename_rules()

    return output


def insert_quantifiers(output):
    for k, v in output[13].items():
        if k[:3] == 'qua':
            anc1 = v[1][5]
            line = findposinmd(anc1, output[0], 0)
            v.insert(0, output[0][line])


def build_remainder(consistent, standard_premises):
    remainder = []
    if consistent:
        temp_list = standard_premises + stan_infer_sent
        for x in temp_list:
            if one_sentence(x[1]) and x not in remainder:
                remainder.append(x)
    return remainder


def repeat_standard_premises(kind, standard_premises, temp_total_sent):
    for lst in reversed(temp_total_sent):
        if lst[7] == 'standard' or lst[4] == 'SUBI' or lst[4].startswith("LE"):
            standard_premises.append(lst)
            if kind == "last":
                lst[7] = ""
        elif kind == 'last':
            lst[7] = ""
        if lst[1].startswith("UNINST"):
            break


def build_intro_sent(new_numbers, temp_total_sent):
    pn = 0
    for lst in intro_sent:
        pn += 1
        new_numbers.update({lst[0]: pn})
        lst[0] = pn
        temp_total_sent.append(lst)
    return pn


def build_constant_sent2(new_numbers, pn, temp_total_sent):
    constant_list = []
    if constant_sent != "":
        add_heading("ABBREVIATIONS", temp_total_sent)
        old_num = find_counterpart_inlist("ABBREVIATIONS", output[0], 1, 0)
        pn += 1
        new_numbers.update({old_num: pn})
        constant_list = [pn, constant_sent, "", "", "", "", "", ""]
        temp_total_sent.append(constant_list)
    return constant_list, pn


def build_constant_sent(output):
    global constant_sent
    constan = []
    if output[6] != {}:
        for k, v in output[6].items():
            sent = build_connection(k, "=", v)
            constan.append("(" + sent + ")")
        constant_sent = build_conjunction(constan)
        constant_sent = constant_sent[1:-1]


def categorize_by_rule(output):
    g = findposinmd("ABBREVIATIONS", output[0], 1)
    put_in_premise = put_def_in_premise(output)
    for e, lst in enumerate(output[0]):
        if lst[0] == 21:
            bb = 8

        if not_blank(lst[4]) and " " in lst[4]:
            rule_prefix = lst[4][:lst[4].index(" ")]
        elif lst[4].startswith("LY"):
            rule_prefix = "LY"
        elif not_blank(lst[4]):
            rule_prefix = lst[4]
        else:
            rule_prefix = ""

        if rule_prefix in subst_rules:
            subst_sent.append(lst)

        if lst[0] == "" and lst[1] == "":
            pass
        if lst[4] in put_in_premise:
            stan_prem_sent.append(lst)
        elif rule_prefix == consist + "I":
            stan_infer_sent.append(lst)
        elif lst[1].isupper():
            pass
        elif e < g:
            intro_sent.append(lst)
        elif rule_prefix in uninstant_infer_rules:
            uninstant_infer.append(lst)
        elif rule_prefix in stan_prem_rules:
            stan_prem_sent.append(lst)
        elif rule_prefix in st_infer_rules:
            stan_infer_sent.append(lst)
        elif lst[4] == "" and lst[7] == 'not standard':
            uninstant_prem.append(lst)
        elif rule_prefix not in subst_rules:
            uninstant_prem.append(lst)
        elif rule_prefix in subst_rules:
            pass
        else:
            raise Exception("you forgot a rule")

    return put_in_premise


def put_def_in_premise(output):
    put_in_premise = True
    exceptions = []
    for k, v in output[13].items():
        for lst in v:
            if lst[4] == 'TR':
                put_in_premise = False
        if put_in_premise:
            exceptions.append(v[0][4])

    return exceptions


def add_heading(str1, temp_total_sent):
    temp_total_sent.append(copy.deepcopy(nine_blanks))
    list1 = copy.deepcopy(nine_blanks)
    list1[1] = str1
    temp_total_sent.append(list1)


def renumber_sentences(new_numbers):
    # this gives attach_sent their proper number according to the new
    # numbering system as arrived at in the rearrange_total_sent function
    # n = 0

    if new_numbers != {}:
        for lst in output[1]:
            lst[44] = new_numbers.get(lst[44])
            assert lst[44] != None

        for e, lst in enumerate(output[0]):
            if lst[1] == '(w I y)':
                bb = 8

            if lst[0] == 78:
                bb = 8

            if isinstance(lst[5], str) and lst[5] != "":
                list1 = lst[5].split(",")
                for k, num in enumerate(list1):
                    num = int(num)


                    list1[k] = new_numbers.get(num)
                    list1[k] = str(list1[k])
                lst[5] = ",".join(list1)
            else:
                if lst[5] == 96:
                    bb = 8

                lst[5] = new_numbers.get(lst[5], "")
                lst[6] = new_numbers.get(lst[6], "")

    return


def rearrange_sent_abbrev(artificial):
    st_infer_rules2 = [iff + "E", "MP", "MT", "EN", "&I", "&E", idisj + "E", "ASC",
                      mini_e + "E", "~~E", bottom + "I", consist + "I", xorr + "E",
                      "AE", "IF", "EF", "AY IDT"]

    abbrev_sent = []

    for sent in output[0]:
        if sent[2] != "" and sent[4] not in ['SUY', "SUBI"]:

            list1 = [sent[0], sent[2], "", sent[3], sent[4], sent[5], sent[6], ""]
            if list1 not in abbrev_sent:
                abbrev_sent.append(list1)

    abbrev_sent = sorted(abbrev_sent, key=operator.itemgetter(0))

    list1 = [""] * 8
    list1[1] = "PREMISES"
    abbrev_sent.insert(0, list1)

    list1 = [""] * 8
    list1[1] = "INFERENCES"
    for i, sent in enumerate(abbrev_sent):

        if sent[4] in st_infer_rules2:
            abbrev_sent.insert(i, list1)
            abbrev_sent.insert(i, [""] * 8)
            break
        else:
            sent[4] = ""


    output[0].append([""] * 8)
    sent_names = build_sent_name()
    for sent in sent_names:
        lst = [""] * 8
        lst[1] = sent
        output[0].append(lst)
    output[0].append([""] * 8)
    for sent in abbrev_sent: output[0].append(sent)

    return


def build_sent_name():
    str2 = ''
    list1 = []

    i = 0
    for k, v in output[9].items():

        v = remove_extra_paren(v)
        str1 = '(' + k + mini_e + v + ')'
        if len(str2) == 0 and len(str1) > 57:
            list1.append(str1)
        elif (len(str2) + len(str1)) > 57:
            list1.append(str2)
            str2 = str1
            if i + 1 == len(output[9]):
                list1.append(str2)
        elif (len(str2) + len(str1)) <= 57:
            if len(str2) == 0:
                str2 = str1
            else:
                str2 = str2 + ' ' + str1
            if i + 1 == len(output[9]):
                list1.append(str2)
        i += 1
    return list1


def obtain_relevant_sentences():
    if not consistent:
        relevant_sentences = [output[0][-2][5], output[0][-2][6]]
        i = -1
        while i < len(relevant_sentences) - 1:
            i += 1
            k = findposinmdlistint(relevant_sentences[i], output[0], 0)
            output[0][k][8] = "*"

            for j in [5, 6]:
                if output[0][k][j] != "":
                    if isinstance(output[0][k][j], str):
                        list1 = output[0][k][j].split(",")
                        list1 = [int(m) for m in list1]
                        for m in list1:
                            if m not in relevant_sentences:
                                relevant_sentences.append(m)
                    else:
                        if output[0][k][j] not in relevant_sentences:
                            relevant_sentences.append(output[0][k][j])
        relevant_sentences.sort()
        rel_sent_str = [str(m) for m in relevant_sentences]
        rel_sent = " ".join(rel_sent_str)
        add_to_tsent(output[0], "RELEVANT SENTENCES: " + rel_sent)

    return


def rename_rules():
    for lst in output[0]:

        lst[4] = lst[4].replace('SUY', 'SUB')
        lst[4] = lst[4].replace('SUBI', 'SUB')
        lst[4] = lst[4].replace('SUBJ', 'SUB')
        lst[4] = lst[4].replace('INJ', 'IN')
        lst[4] = lst[4].replace('INJ,TR', 'IN,TR')
        lst[4] = lst[4].replace('AY', 'AX')
        lst[4] = lst[4].replace('DE', 'DF')
        lst[4] = lst[4].replace('NE', 'NC')
        lst[4] = lst[4].replace('LY', 'LE')
        lst[4] = lst[4].replace('DFF', 'DEF')
        lst[4] = lst[4].replace('EF', iff + "E")
        lst[4] = lst[4].replace('IF', "MP")
        lst[4] = lst[4].replace('AE', '&E')
        lst[4] = lst[4].replace('CE', '&E')
