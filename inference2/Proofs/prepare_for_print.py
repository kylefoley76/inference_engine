from general_functions import *
import copy
import collections
import operator

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


def rearrange_subst_sent(new_numbers, pn, sub_dict, remainder, temp_total_sent):
    sub_sentences = []
    uninstant_conn = []
    for k, v in substitutions.items():
        if k == 'personhood':
            bb = 8
        put_in_stan_premise = True
        rule_counter = collections.Counter([x[4] for x in v])
        conj_number = dictionary[16].get(k, 0)
        subi_count = rule_counter.get('SUBI', 0)
        subj_count = rule_counter.get('SUBJ', 0)

        kind = 0
        if k[:2] == "qu":
            bb = 8
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
            pos = findposinmd(anc1, total_sent, 0)
            orig_subi = total_sent[pos]
            if k[0] in ['1','2','3','4', '5']:
                subj_counter = 1
                sub_sentences.append(orig_subi)

        for j, lst in enumerate(v):

            if j == 0:
                odef_name = lst[4]
                if kind == 1:
                    def_num = lst[0]
                    orig_def = lst

            if lst[4] not in ['SUBI', 'SUBJ', 'AY IDT'] and kind != 3:
                pn += 1
                new_numbers.update({lst[0]: pn})
                lst[0] = pn

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

    add_heading("REMAINDER", temp_total_sent)
    remainder.sort()
    for sent in remainder: temp_total_sent.append(copy.deepcopy(sent))
    add_heading("SUBSTITUTIONS", temp_total_sent)
    for sent in sub_sentences: temp_total_sent.append(copy.deepcopy(sent))
    for lst in temp_total_sent:
        if lst[1].startswith("SUB"):
            break
        lst[4] = sub_dict.get(lst[0], lst[4])

    return sub_sentences


def rearrange(kind, total_sent2, all_sent2, consistent2, abbreviations2,
              substitutions2, artificial2, prop_name2, oprop_name2):
    global total_sent, substitutions, abbreviations, consistent, all_sent
    global artificial, prop_name, oprop_name

    substitutions = substitutions2
    all_sent = all_sent2
    consistent = consistent2
    total_sent = total_sent2
    artificial = artificial2
    prop_name = prop_name2
    oprop_name = oprop_name2
    abbreviations = abbreviations2
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

    for k, v in substitutions.items():
        if k[:3] == 'qua':
            anc1 = v[1][5]
            line = findposinmd(anc1, total_sent, 0)
            v.insert(0, total_sent[line])

    intro_sent = []
    subst_rules = ["DF", "TR", "LY", "SUB", "SUBI", "SUBJ", "IN", "AX", "CE"]
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

    constan = []
    constant_sent = ""
    if abbreviations != {}:
        for k, v in abbreviations.items():
            sent = build_connection(k, "=", v)
            constan.append("(" + sent + ")")
        constant_sent = build_conjunction(constan)
        constant_sent = constant_sent[1:-1]


    g = findposinmd("ABBREVIATIONS", total_sent, 1)

    for e, lst in enumerate(total_sent):
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
            raise Exception ("you forgot a rule")


    pn = 0
    for lst in intro_sent:
        pn += 1
        new_numbers.update({lst[0]: pn})
        lst[0] = pn
        temp_total_sent.append(lst)

    if constant_sent != "":
        add_heading("ABBREVIATIONS", temp_total_sent)
        old_num = find_counterpart_inlist("ABBREVIATIONS", total_sent, 1, 0)
        pn += 1
        new_numbers.update({old_num: pn})
        constant_list = [pn, constant_sent, "", "", "", "", "", ""]
        temp_total_sent.append(constant_list)



    sub_dict = {}
    standard_premises = []

    if uninstant_prem != [] and not artificial:

        pn = build_temp_total(new_numbers, pn, uninstant_prem, temp_total_sent, sub_dict, "UNINSTANTIABLE PREMISES")

        pn = build_temp_total(new_numbers, pn, uninstant_infer, temp_total_sent, sub_dict, "UNINSTANTIABLE INFERENCES")

        for lst in reversed(temp_total_sent):
            if lst[7] == 'standard' or lst[4] == 'SUBI' or lst[4].startswith("LE"):
                standard_premises.append(lst)
                if kind == "last":
                    lst[7] = ""
            elif kind == 'last':
                lst[7] = ""
            if lst[1].startswith("UNINST"):
                break

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

    remainder = []
    if consistent:
        temp_list = standard_premises + stan_infer_sent
        for x in temp_list:
            if one_sentence(x[1]) and x not in remainder:
                remainder.append(x)



    if substitutions != {}:
        rearrange_subst_sent(new_numbers, pn, sub_dict, remainder, temp_total_sent)



    total_sent = temp_total_sent
    renumber_sentences(new_numbers)
    assert isinstance(total_sent[-1][0], int)
    if kind == 'last':
        rearrange_sent_abbrev()
        rename_rules()

    return total_sent


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
        for lst in all_sent:
            lst[44] = new_numbers.get(lst[44])
            assert lst[44] != None

        for e, lst in enumerate(total_sent):
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


def rearrange_sent_abbrev():
    st_infer_rules = [iff + "E", "MP", "MT", "EN", "&I", "&E", idisj + "E", "ASC",
                      mini_e + "E", "~~E", bottom + "I", consist + "I", xorr + "E",
                      "AE", "IF", "EF", "AY IDT"]

    abbrev_sent = []
    for sent in total_sent:
        if sent[2] != "" and sent[4] not in ['SUY', "SUBI"]:

            list1 = [sent[0], sent[2], "", sent[3], sent[4], sent[5], sent[6], ""]
            if list1 not in abbrev_sent:
                abbrev_sent.append(list1)

    abbrev_sent = sorted(abbrev_sent, key=operator.itemgetter(0))
    list1 = [""] * 8
    list1[1] = "INFERENCES"
    for i, sent in enumerate(abbrev_sent):

        if sent[4] in st_infer_rules:
            abbrev_sent.insert(i, list1)
            abbrev_sent.insert(i, [""] * 8)
            break
        else:
            sent[4] = ""


    total_sent.append([""] * 8)
    sent_names = build_sent_name()
    for sent in sent_names:
        lst = [""] * 8
        lst[1] = sent
        total_sent.append(lst)
    total_sent.append([""] * 8)
    for sent in abbrev_sent: total_sent.append(sent)

    return


def build_sent_name():
    str2 = ''
    list1 = []

    i = 0
    for k, v in oprop_name.items():

        v = remove_outer_paren(v)
        str1 = '(' + k + mini_e + v + ')'
        if len(str2) == 0 and len(str1) > 57:
            list1.append(str1)
        elif (len(str2) + len(str1)) > 57:
            list1.append(str2)
            str2 = str1
            if i + 1 == len(oprop_name):
                list1.append(str2)
        elif (len(str2) + len(str1)) <= 57:
            if len(str2) == 0:
                str2 = str1
            else:
                str2 = str2 + ' ' + str1
            if i + 1 == len(oprop_name):
                list1.append(str2)
        i += 1
    return list1


def obtain_relevant_sentences():

    if not consistent:
        relevant_sentences = [total_sent[-2][5], total_sent[-2][6]]
        i = -1
        while i < len(relevant_sentences) - 1:
            i += 1
            k = findposinmdlistint(relevant_sentences[i], total_sent, 0)
            total_sent[k][8] = "*"

            for j in [5, 6]:
                if total_sent[k][j] != "":
                    if isinstance(total_sent[k][j], str):
                        list1 = total_sent[k][j].split(",")
                        list1 = [int(m) for m in list1]
                        for m in list1:
                            if m not in relevant_sentences:
                                relevant_sentences.append(m)
                    else:
                        if total_sent[k][j] not in relevant_sentences:
                            relevant_sentences.append(total_sent[k][j])
        relevant_sentences.sort()
        rel_sent_str = [str(m) for m in relevant_sentences]
        rel_sent = " ".join(rel_sent_str)
        add_to_total_sent(total_sent, "RELEVANT SENTENCES: " + rel_sent)

    return


def rename_rules():
    for lst in total_sent:

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

