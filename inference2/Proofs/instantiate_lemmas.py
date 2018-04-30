



def prepare_output(word, greek_dict):
    reduced_def = get_word_info(dictionary, word, "")
    sent = []
    ant_sent = []
    vars = {}
    vars2 = set()
    cvars = set()
    output = get_output()
    for z, cls in enumerate(reduced_def):
        sentences = cls.sentences
        adjust_ant_index(ant_sent, cls, sent, sentences, vars, vars2, greek_dict)
        adjust_con_index(cls, cvars, output, sent, sentences)
    output.prop_var = get_prop_var()
    output.prop_name = defaultdict(lambda: output.prop_var.pop(), {})
    for tsent in sent:
        tsent[2] = name_sent(tsent[1], output.prop_name)
        output.oprop_name[tsent[2]] = tsent[1]

    output.main_var = vars
    output.all_sent = sent
    output.abbreviations = json.loads(json.dumps(dictionary.def_constants.get(word, {})))
    output.variables = get_variables()
    output.user = ""

    for k in output.abbreviations.keys(): output.variables.remove(k)
    for var in vars2 | cvars:
        if var in output.variables: output.variables.remove(var)

    return output, vars, reduced_def


def adjust_ant_index(ant_sent, cls, sent, sentences, vars, vars2, greek_dict):
    kind = dictionary.kind.get(word)

    for num in cls.def_stats.ant_index:
        if isinstance(num, int):
            ant_sent.append(sentences[num])
            for noun in sentences[num][42]:
                if kind in ['c', 'i', 'p'] and sentences[num][13] in ["I", "J", "="] and noun == 14:
                    pass
                else:
                    if sentences[num][noun] not in vars.keys():
                        vars.update({sentences[num][noun]: noun})
                        vars2.add(sentences[num][noun])

            try:
                idx = findposinmd(sentences[num][0], sent, 0)
            except:
                idx = -1
            if idx == -1 and sentences[num][56] == "c":
                sentences[num][7] = sentences[num][56]
                sentences[num][43] = 'do not define'
                sent.append(sentences[num])
        else:
            for cnum in num:
                for noun in sentences[cnum][42]:
                    vars.update({sentences[num][noun]: noun})
                    vars2.add(sentences[cnum][noun])
                    greek_dict[sentences[num][noun]]
                ant_sent.append(sentences[cnum])
                sentences[cnum][7] = sentences[cnum][56]


def adjust_con_index(cls, cvars, output, sent, sentences):
    for num in cls.def_stats.con_index:
        cons_count = 0
        if isinstance(num, int):
            sentences[num][7] = 'c'
            if sentences[num][3] == "~":
                dictionary.negative_definitions.add(word)

            sent.append(sentences[num])
            for noun in sentences[num][42]: cvars.add(sentences[num][noun])
        else:
            tnum = cls.def_stats.con_hnum[cons_count]
            embed = cls.embeds.get(tnum)
            embed.sentences = sentences
            sub_word = embed.def_stats.def_word_num
            add_to_gsent([embed], output)
            output.trans_def.update({sub_word: embed})
            cons_count += 1
            for cnum in num:
                dictionary.connected_definitions.add(word)
                if sentences[cnum][3] == "~":
                    dictionary.negative_definitions.add(word)
                sent.append(sentences[cnum])
                for noun in sentences[cnum][42]: cvars.add(sentences[cnum][noun])


########################
########## perhaps delete


def instantiate_from_lemmas(word, greek_dict):
    output, consistent, reduced = try_instantiation(output, dictionary, "lemmas")
    if not consistent and proof_type == 5:
        output = rearrange("last", output, consistent, "", output.main_var)
        print_sent([output.total_sent], [0], 2)
        print (word)
        raise Exception


def build_basic_definition(output, reduced, word):
    if reduced:
        list2 = dictionary.categorized_sent.get(word)
        nat_ant = list2[0].def_stats.natural_antecedent
        ant_greek = list2[0].def_stats.ant_greek
        conn = iff if list2[0].def_stats.connection_type == 'e' else conditional
        j = 0
        while output.all_sent[0][5] in ant_greek:
            j += 1
            del output.all_sent[0]
            if j > 5: raise Exception

        list1 = list(filter(lambda x: x[0] != 'irrelevant', output.all_sent))
        list1 = [x[0] for x in list1]
        for k, defin in output.trans_def.items():
            if "," in k:
                sentences = defin.sentences
                conn_sent = defin.def_stats.tot_greek_sent
                nant = adjust_sides(defin.def_stats.ant_index, output, sentences)
                ncon = adjust_sides(defin.def_stats.con_index, output, sentences)

                for e, sentence in enumerate(sentences):
                    conn_sent = conn_sent.replace(sentence[5], sentence[0])

                output.lemma_embed.update({k: json.loads(json.dumps([nant, ncon]))})
                list1.append(conn_sent)

        basic_definition = nat_ant + " " + conn + " (" + " & ".join(list1) + ")"
        if output.abbreviations != {}:
            str1 = " & ".join([build_connection("(" + k, "=", v + ")") for k, v in output.abbreviations.items()])
            basic_definition = build_connection(basic_definition, " & ", str1)

        dictionary.basic_definitions.update({word: basic_definition})
    else:
        definition = dictionary.definitions.get(word)
        if definition != None:
            dictionary.basic_definitions.update({word: definition})


def print_to_excel(proof_type):
    if proof_type != 5:
        wb5 = load_workbook('/Users/kylefoley/PycharmProjects/inference_engine2/inference2/Proofs/dictionary5.xlsx')
        w5 = wb5.worksheets[4]
        row_number = 1
        for k, v in dictionary.basic_definitions.items():
            w5.cell(row=row_number, column=1).value = k
            w5.cell(row=row_number, column=2).value = v
            row_number += 1

        wb5.save('/Users/kylefoley/PycharmProjects/inference_engine2/inference2/Proofs/dictionary5.xlsx')


def generate_multiple_possibilities(power_set1, possibilities, new_sets):
    for st in power_set1:
        if len(st) > 1:
            new_sets2 = [new_sets[num] for num in st]
            possibilities2 = [i for i in itertools.product(*new_sets2)]
            for tpl in possibilities2:
                possibilities.append([possibilities[num] for num in tpl])

    for e, itm in enumerate(possibilities):
        if isinstance(itm, tuple):
            possibilities[e] = [possibilities[e]]

    return possibilities


def large_possibilities(xindex, yindex):
    possibilities = [xindex, yindex]
    possibilities = [i for i in itertools.product(*possibilities)]
    max_len = len(xindex) if len(xindex) >= len(yindex) else len(yindex)
    new_sets = []
    sub_sets = []
    for x in range(len(possibilities)):
        if (x + 1) % max_len == 0:
            sub_sets.append(x)
            new_sets.append(json.loads(json.dumps(sub_sets)))
            sub_sets = []
        else:
            sub_sets.append(x)

    power_set1 = list(powerset([x for x in range(len(new_sets))]))

    return generate_multiple_possibilities(power_set1, possibilities, new_sets)


def consistent_classes(xword, yword, lemmata):
    xclass = dictionary.groups.get(xword, {10: "thing", 14: "thing"})
    yclass = dictionary.groups.get(yword, {10: "thing", 14: "thing"})
    xindex = [k for k, y in xclass.items()]
    yindex = [k for k, y in yclass.items()]
    if len(xindex) < 3 and len(yindex) < 3:
        possibilities = [xindex, yindex]
        possibilities = [i for i in itertools.product(*possibilities)]
    else:
        possibilities = large_possibilities(xindex, yindex)

    consistent_classes2(xword, yword, xclass, yclass, possibilities, lemmata)


def consistent_classes2(xword, yword, xclass, yclass, possibilities, lemmata):
    for possibility in possibilities:
        xgroup = xclass.get(possibility[0], 'thing')
        ygroup = yclass.get(possibility[1], 'thing')
        if xgroup == ygroup:
            build_entry(xword, yword, possibility, lemmata, True)
        elif xgroup == 'thing' or ygroup == 'thing':
            build_entry(xword, yword, possibility, lemmata, True)
        else:
            list1 = [xgroup, ygroup]
            list1.sort()
            pair = ".".join(list1)
            tvalue = dictionary.ontology[2].get(pair)
            assert tvalue != None
            if not tvalue:
                build_entry(xword, yword, possibility, lemmata, False)
            else:
                build_entry(xword, yword, possibility, lemmata, True)


def build_entry(xword, yword, possibility, lemmata, tvalue):
    list1 = [xword, yword]
    list1.sort()
    str1 = list1[0] + "." + list1[1]
    for num in possibility:
        str1 += "." + str(num)
    lemmata.update({str1: tvalue})
    return


def modify_abbreviations(youtput, xoutput, xvar, abbrev_dict):
    xabbrev = xoutput.abbreviations
    for k, v in youtput.abbreviations.items():
        if v in xabbrev.values():
            new_var = get_key(xabbrev, v)
            abbrev_dict.update({k: new_var})
        elif k not in xvar:
            new_var = xvar[0]
            abbrev_dict.update({k: new_var})
            del xvar[0]


def modify_variables(youtput, xoutput):
    xvars = xoutput.variables
    yvars = youtput.variables
    xprop_name = xoutput.prop_name
    xoprop_name = xoutput.oprop_name

    tvars = list(set(xvars) | set(yvars))
    abbrev_dict = {}
    modify_abbreviations(youtput, xoutput, xvars, abbrev_dict)

    for sentence in youtput.all_sent:
        changed = False
        for pos in sentence[42]:
            yvar = sentence[pos]
            value = abbrev_dict.get(yvar)
            if value != None:
                changed = True
                sentence[pos] = value
            elif yvar in youtput.main_var:
                pass
            elif yvar not in xvars:
                changed = True
                new_var = tvars[0]
                sentence[pos] = new_var
                abbrev_dict.update({yvar: new_var})
                del tvars[0]
        if changed:
            name_and_build(xoutput, sentence)
        else:
            sentence[2] = name_sent(sentence[1], xprop_name)
            xoprop_name[sentence[2]] = sentence[1]

    return


def get_basic_sent(tword):
    with open("basic/" + tword + ".json", "r") as fp:
        return json.load(fp)


def reload_sentences(output, anc):
    for k, v in output.trans_def.items():
        list2 = []
        list1 = output.lemma_embed.get(k)
        v.def_stats.ant_index = list1[0]
        v.def_stats.con_index = list1[1]
        v.def_stats.tot_sent_idx = anc

        for e, idx in enumerate(list1[0] + list1[1]):
            list2.append(output.all_sent[idx])
        v.sentences = json.loads(json.dumps(list2))

    return


def quick_contradiction(xoutput, youtput):
    xlist = list(filter(lambda x: x[7] == 'c', xoutput.all_sent))
    ylist = list(filter(lambda x: x[7] == 'c', youtput.all_sent))
    xvar = set(map(lambda x: x[2], xlist))
    yvar = set(map(lambda x: x[2], ylist))
    for var in xvar & yvar:
        xtvalue = find_counterpart_inlist(var, xoutput.all_sent, 2, 3)
        ytvalue = find_counterpart_inlist(var, youtput.all_sent, 2, 3)
        if xtvalue != ytvalue:
            return False
    return True


def name_xsent(xoutput):
    for sentence in xoutput.all_sent:
        sentence[2] = name_sent(sentence[1], xoutput.prop_name)
        xoutput.oprop_name.update({sentence[2]: sentence[1]})


def adjust_index2(output, new_sent, list1):
    sentences = output.all_sent
    new_index = []
    for e, num in enumerate(list1):
        if isinstance(num, int):
            new_sent.append(sentences[num])
            new_index.append(len(new_sent) - 1)
        else:
            list2 = []
            for f, cnum in enumerate(num):
                new_sent.append(sentences[cnum])
                list2.append(len(new_sent) - 1)
            new_index.append(list2)

    return new_index


def adjust_index(output):
    for k, v in output.trans_def.items():
        new_sent = []
        new_index = adjust_index2(output, new_sent, v.def_stats.ant_index)
        v.def_stats.ant_index = new_index
        new_index = adjust_index2(output, new_sent, v.def_stats.con_index)
        v.def_stats.con_index = new_index
        v.sentences = json.loads(json.dumps(new_sent))


def do_not_instantiate(xoutput, youtput, len_asent):
    output3 = xoutput if youtput == [] else youtput
    for k, v in output3.trans_def.items():
        for e, sent in enumerate(xoutput.all_sent[len_asent:]):
            xoutput.disj_elim.append([e, v.def_stats.def_word_num])


def make_matrix2(xword, yword, lemmata, user):
    kind = consistent_classes(xword, yword, lemmata)
    if kind == 'no definition':
        pass
    else:
        youtput = dictionary.basic_output.get(yword)
        youtput.all_sent = get_basic_sent(yword)
        reload_sentences(youtput, 2)
        xoutput = dictionary.basic_output.get(xword)
        xoutput.all_sent = get_basic_sent(xword)
        xoutput.prop_var = get_prop_var()
        xoutput.prop_name = defaultdict(lambda: xoutput.prop_var.pop(), {})
        name_xsent(xoutput)
        reload_sentences(xoutput, 1)
        modify_variables(youtput, xoutput)
        if not quick_contradiction(xoutput, youtput):
            print ('contradiction found')
        else:
            adjust_index(xoutput)
            adjust_index(youtput)
            do_not_instantiate(xoutput, [], 0)
            len_asent = len(xoutput.all_sent)
            xoutput.all_sent = xoutput.all_sent + youtput.all_sent
            do_not_instantiate(xoutput, youtput, len_asent)
            xoutput.trans_def = {**xoutput.trans_def, **youtput.trans_def}
            for k, v in xoutput.trans_def.items(): add_to_gsent([v], xoutput)
            if xoutput.gsent != []:
                fill_tsent(xoutput, xword, yword, len_asent)
                loop_through_gsent(xoutput, "lemmas2", dictionary)
                consistent = True if xoutput.total_sent[-1][1] == consist else False
                rearrange("last", xoutput, consistent, "lemmas2", xoutput.main_var)

    return


def fill_tsent(xoutput, xword, yword, len_asent):
    xoutput.tindex = 0
    basic_defintion = dictionary.basic_definitions.get(xword)
    add_to_tsent(xoutput, basic_defintion)
    basic_defintion = dictionary.basic_definitions.get(yword)
    add_to_tsent(xoutput, basic_defintion)
    for sent in xoutput.all_sent[:len_asent]:
        if sent[7] == 'c':
            add_to_tsent(xoutput, sent[1], "", sent[3], "&E", 1)
    for sent in xoutput.all_sent[len_asent:]:
        if sent[7] == 'c':
            add_to_tsent(xoutput, sent[1], "", sent[3], "&E", 2)
    for k, v in xoutput.trans_def.items():
        anc1 = v.def_stats.tot_sent_idx
        add_to_tsent(xoutput, v.def_stats.natural_sent, "", "", "&E", anc1)


def adjust_prop_name(output):
    nprop_name = {}
    for k, v in output.prop_name.items():
        s = k.split()
        s = "".join(s)
        nprop_name.update({s: v})

    output.prop_name = nprop_name


def get_from_all_sent(num, output, sentences, list2):
    idx = findposinmd(sentences[num][0], output.all_sent, 0)
    if idx == -1:
        output.all_sent.append(sentences[num])
        list2.append(len(output.all_sent) - 1)
    else:
        list2.append(idx)


def adjust_sides(list1, output, sentences):
    list2 = []
    for e, num in enumerate(list1):
        if isinstance(num, int):
            get_from_all_sent(num, output, sentences, list2)
        else:
            list3 = []
            for cnum in num:
                get_from_all_sent(cnum, output, sentences, list3)
            list2.append(json.loads(json.dumps(list3)))

    return list2


def eliminate_possessive():
    test_lemmas = []
    for e, word in enumerate(words_used):
        if word[-2:] == "'s":
            test_lemmas.append(word[:-2])
        elif word in dictionary.rel_abbrev.keys():
            pass
        else:
            pos = dictionary.pos.get(word)
            if pos != None:
                if pos[0] in ['n', 'a', 'r']:
                    test_lemmas.append(word)

    return test_lemmas


def make_matrix(user):
    global dictionary
    pkl_file = open(user + 'z_dict_words.pkl', 'rb')
    dictionary = pickle.load(pkl_file)
    pkl_file.close()
    lemmata = {}
    word_list = []
    words_used = eliminate_possessive()
    for xword in words_used:
        for yword in words_used:
            if xword[0] != yword[0]:
                list1 = [xword[0], yword[0]]
                list1.sort()
                if list1 != ['o', 'o']:
                    if list1 not in word_list:
                        consistent_classes(xword, yword, lemmata)

    temp = open(user + 'lemmata.pkl', 'wb')
    pickle.dump(lemmata, temp)
    temp.close()

    return