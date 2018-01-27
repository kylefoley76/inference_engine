from general_functions import mainconn, findposinmd, remove_outer_paren, ErrorWithCode
from settings import *
import copy



def replace_w_greek(sentence):
    j = 947
    list1 = [x for x in sentence]
    erase_next_parent = False
    for i, letter in enumerate(list1):
        if i > 0 and list1[i - 1] == "(" and letter.islower():
            j += 1
            list1[i] = chr(j)
            list1[i - 1] = " "
            erase_next_parent = True
        elif erase_next_parent and letter == ")":
            list1[i] = " "
            erase_next_parent = False
        elif letter not in ["(",")", "&", conditional, xorr, iff, idisj, "|"]:
            list1[i] = " "

    sent = "".join(list1)

    return sent

def find_sentences(sentence, definiendum = ""):
    if sentence == None:
        raise Exception("\n missing word in dictionary \n")
    if one_sentence(sentence):
        if definiendum != "":
            # raise Exception("\n you cannot reduce this word: " + "\n" + definiendum + "\n")
            raise ErrorWithCode(f"\n you cannot reduce {definiendum} \n  in {sentence} \n")
        else:
            raise ErrorWithCode(f"\n you cannot reduce {definiendum} \n  in {sentence} \n")
            # raise Exception("\n you cannot reduce this word: " + "\n" + sentence + "\n")
    if sentence.count('(') != sentence.count(')'):
        print ("( paren = " + str(sentence.count("(")))
        print(") paren = " + str(sentence.count(")")))

        raise Exception(" \nwrong number of parentheses in sentence: " + sentence + "\n ")
    marker = False
    total = -1
    sentences = []
    output = [None] * 9
    sent_number = []
    list1 = mainconn(sentence)
    sentence = sentence.strip()
    if sentence.startswith("(b LFT c)"):
        bb = 8
    greek_sent = replace_w_greek(sentence)
    if sentence.find("~(") > -1:
        sentence = sentence.replace("~(", "(!")

    greek_sentences = []
    greek_sentences.append(greek_sent)
    assert len(greek_sent) == len(sentence)
    main_connect = []
    sent_number.append("1")
    main_connect.append(["1", list1[0]])
    father_number = "1"
    v = 0
    sibling_number = 0
    unenclose_at_end = False
    connectives = ["&", idisj, iff, conditional, nonseq, implies, xorr, "#"]
    sentences.append(sentence)



    j = 0
    n = 0
    for i in range(0, len(sentence)):
        str1 = sentence[i:(i + 1)]
        for o in connectives:
            if str1 == o:
                j += 1

    while n < j + 1:

        l = len(sentence)
        x = -1
        while x < l - 1:
            x += 1

            if sentence[x:x + 1] == "(":
                if not unenclose_at_end:
                    unenclose_at_end = is_natural_language(sentence, x)

                if marker == False:
                    z = x
                    marker = True

                total += 1
            elif sentence[x: x + 1] == ")":
                total -= 1
                if total == -1:
                    marker = False
                    temp_sent = sentence[z: x + 1]
                    temp_greek = greek_sent[z: x+ 1]

                    if (len(sentence) - len(temp_sent)) > 2:
                        if one_sentence(temp_sent): n += 1
                        sibling_number += 1
                        num3 = father_number + "." + str(sibling_number)
                        main_co = mainconn(temp_sent)
                        sentences.append(temp_sent)
                        main_connect.append([num3, main_co[0]])
                        sent_number.append(num3)
                        greek_sentences.append(temp_greek)
                    else:
                        sentence = sentence[1:len(sentence) - 1]
                        greek_sent = greek_sent[1:len(greek_sent) - 1]
                        l = len(sentence)
                        x = -1

        total = -1
        marker = False

        if n < j + 1:
            if len(sentences) > v:
                while v + 1 < len(sentences):
                    v += 1
                    father = sentences[v]
                    greek_father = greek_sentences[v]
                    father_number = sent_number[v]
                    sibling_number = 0
                    if not one_sentence(father):
                        sentence = father
                        greek_sent = greek_father
                        break

    unenclose1(sentences, unenclose_at_end)

    output[1] = split_numbers(sent_number)
    output[2] = sent_number
    output[3] = sentences
    output[4] = main_connect
    output[6] = adjust_greek_sent(greek_sentences)
    output[5] = greek_sentences[0]



    if "," in greek_sent[0]: check_that_paren_in_right_order(output)



    return output

def split_numbers(sent_number):
    list1 = []
    for num in sent_number:
        list2 = num.split(".")
        list1.append(list2)
    return list1

def check_that_paren_in_right_order(output):
    for i, sent in enumerate(output[3]):
        if "," in sent:
            num_periods = output[2][i].count(".")
            str1 = sent[output[4][i][2]:output[4][i][2]+7]
            num_pipe = str1.count(",")
            if num_pipe != 0 and num_pipe - 1 != num_periods:
                print ("\n parentheses are in wrong location in " + output[3][0] + "\n")
                assert num_pipe - 1 == num_periods
            output[3][i] = output[3][i].replace(",", "")

def adjust_greek_sent(greek_sentences):
    connectives = ["&", idisj, iff, conditional, nonseq, implies, xorr, "#"]
    for i, sent in enumerate(greek_sentences):
        sent = sent.replace(" ", "")
        for conn in connectives:
            sent = sent.replace(conn, " " + conn + " ")
        greek_sentences[i] = sent

    return greek_sentences

def get_sent_from_period(sent, per_pos):
    end = sent.find(" ", per_pos)
    if end == -1:
        end = len(sent) - 1
    while True:
        per_pos -= 1
        if sent[per_pos] in [" ", "("]:
            beg = per_pos + 1
            break

    to_be_replaced = sent[beg: end]
    letters = to_be_replaced.split(".")
    new_sentences = []
    for letter in letters:
        new_sent = copy.copy(sent)
        new_sent = new_sent.replace(to_be_replaced, letter)
        new_sentences.append(new_sent)

    return new_sentences

def append_def_info(def_info, greatest_num, new_greek, new_sentences,
                    greek_letter, parent, fam_num):
    k = 0

    for sentence in new_sentences:
        fam_num2 = copy.deepcopy(fam_num)
        greek_letter += 1
        k += 1
        new_num = str(greatest_num + k)
        fam_num2.append(new_num)
        def_info[1].append(fam_num2)
        def_info[3].append(sentence)
        def_info[2].append(parent + "." + new_num)
        def_info[4].append([parent + "." + new_num, ""])
        new_greek.append(chr(greek_letter))
        def_info[6].append(chr(greek_letter))

    return greek_letter

def adjust_def_info(def_info, i, new_sentences, already_conjunctive, greek_letter):
    greek_letter += 1
    new_greek = []
    sent_num = def_info[2][i]
    size = sent_num.count(".")
    parent = ".".join(def_info[1][i][:-1])
    old_greek = def_info[6][i]
    sibling_numbers = []
    if already_conjunctive:
        del def_info[1][i][-1]
        new_greek = [chr(greek_letter)]
        def_info[3][i] = new_sentences[0]
        def_info[6][i] = chr(greek_letter)
        del new_sentences[0]

    if already_conjunctive:
        for j, num in enumerate(def_info[2]):
            if num.startswith(parent + ".") and num.count(".") == size and j != i:
                sibling_numbers.append(int(def_info[1][j][-1]))
        greatest_num = max(sibling_numbers)
    else:
        greatest_num = 0
        parent = sent_num

    greek_letter = append_def_info(def_info, greatest_num, new_greek,
                        new_sentences, greek_letter, parent, def_info[1][i])

    new_greek = " & ".join(new_greek)
    if not already_conjunctive:
        new_greek = "(" + new_greek + ")"

    def_info[5] = def_info[5].replace(old_greek, new_greek)
    for n, lst in enumerate(def_info[6]):
        lst = lst.replace(old_greek, new_greek)
        def_info[6][n] = lst

    return def_info, greek_letter

def period_elimination(def_info2, definition):
    hypo_conn = [iff, idisj, xorr, conditional]
    i = -1
    greek_letter = 999
    for def_info in def_info2:
        while i < len(def_info[3]) - 1:
            i += 1
            sent = def_info[3][i]
            if "." in sent and one_sentence(sent):
                # if the sentence is the sole sentence on one side of a hypothetical
                # then we have to add additional parentheses
                sent_num = def_info[4][i][0]
                paren_num = ".".join(def_info[1][i][:-1])

                # paren_num = sent_num[:-1]
                g = findposinmd(paren_num, def_info[4],0)
                paren_conn = def_info[4][g][1]
                assert paren_conn != ""
                per_pos = sent.find(".")
                new_sentences = get_sent_from_period(sent, per_pos)
                new_conjunct = " & ".join(new_sentences)
                already_conjunctive = True
                if paren_conn in hypo_conn:
                    new_conjunct = "(" + new_conjunct + ')'
                    already_conjunctive = False
                    def_info[4][i][1] = "&"
                    def_info[3][i] = new_conjunct


                definition = definition.replace(sent, new_conjunct)
                for j in range(len(def_info[3])):
                    def_info[3][j] = def_info[3][j].replace(sent, new_conjunct)
                def_info, greek_letter = adjust_def_info(def_info, i, new_sentences,
                                              already_conjunctive, greek_letter)

    return def_info2, definition

def is_set_of_bic_wo_id(def_info):
    # if a definition is composed of a set of conditionals or biconditionals
    # and there is no identity statement within the definition then
    # we do not need to delete anything from the def_info list

    if def_info[4][0][1] == "&":
        for i, lst in enumerate(def_info[2]):
            if len(lst) == 3 and def_info[4][i][1] == "":
                return False
            elif len(lst[0]) > 3:
                return True

    return False

def eliminate_conjuncts_from_definition(def_info):
    # any sentences which are not within either an iff or conditiional
    # are deleted

    # 1. if a definition has some detached conjuncts then these are eliminated
    # and a new greek definition is placed in def_info[5], the def_info
    # list will have one member
    # 2. if a definition is composed of sets of complex sentences then
    # the greek definition remains in def_info[5]
    # the other complex sentences are placed in sets of equivalences
    # and it is written on [45] that they are not yet detached and
    # hence cannot be used in the modus ponens function
    # 3. when we add to the total sent list, we do so by looping through the
    # sets of equivalences list and only adding those that say in [45]
    # 'detached'

    if is_set_of_bic_wo_id(def_info):
        for lst in def_info[4]:
            lst[0] = lst[0][1:]
        def_info = make_sets_of_equivalences(def_info)
        def_info = build_conjunction_of_biconditionals(def_info)
    elif def_info[4][0][1] == "&":
        i = 0
        while i < len(def_info[2]):
            if def_info[2][i].count(".") == 1 and def_info[4][i][1] == "":
                # deletions made to def info

                del def_info[1][i]
                del def_info[2][i]
                del def_info[3][i]
                del def_info[4][i]
                del def_info[6][i]
            elif def_info[2][i].count(".") > 1:
                break
            else:
                i += 1

        def_info = prepare_def_info_list(def_info)
    else:
        def_info = [def_info]

    return def_info

def prepare_def_info_list(def_info):
    connectives = [iff, conditional, idisj, xorr]
    # this removes the first number from the old numbers
    for i in range(len(def_info[2])):
        def_info[2][i] = def_info[2][i][2:]
        def_info[4][i][0] = def_info[2][i]
        del def_info[1][i][0]


    # if the definition was composed of a set of conjunctions then the
    # the greek sentence needs to be amended, otherwise we need
    # the "do not add to total sent list
    if def_info[4][1][1] in connectives and def_info[2][1].count(".") == 0 \
        and def_info[4][2][1] in connectives and def_info[2][2].count(".") == 0:
        def_info = make_sets_of_equivalences(def_info)
        def_info = build_conjunction_of_biconditionals(def_info)
    else:
        # deletions made to def info

        del def_info[1][0]
        del def_info[2][0]
        del def_info[3][0]
        del def_info[4][0]
        del def_info[6][0]
        def_info[6][0] = remove_outer_paren(def_info[6][0])
        def_info[5] = def_info[6][0]
        def_info = [def_info]

    return def_info

def make_sets_of_equivalences(def_info):
    # if a definition is composed of a set of equivalences
    # then this function puts each complex sentence into a list
    # deletions made to def info
    num = [1, 2, 3, 4, 6]
    list2 = []
    for i in range(len(def_info[2])):
        if len(def_info[2][i]) == 1:
            list1 = [""] * 9
            for j in num:
                list1[j] = copy.deepcopy([def_info[j][i]])
            list2.append(list1)
        elif len(def_info[2][i]) > 1:
            list1 = [""] * 9
            for j in num:
                list1[j] = copy.deepcopy(def_info[j][i])
            for m in range(len(list2)):
                if list1[2].startswith(list2[m][2][0]):
                    for k in num:
                        list3 = list2[m][k]
                        list3.append(list1[k])
                        list2[m][k] = list3
                    list2[m][5] = list2[m][6][0]

    def_info = [def_info]
    for lst in list2:
        def_info.append(lst)

    return def_info

def build_conjunction_of_biconditionals(def_info):
    str1 = def_info[1][6][0]
    for i in range(2, len(def_info)):
        str1 += " & " + def_info[i][5]
    def_info[0][5] = str1
    def_info[0][6][0] = str1
    return def_info

#######################
############ possibly delete

def is_natural_language(sentence, i):
    # this determines if the sentence is natural or an abbreviation
    if sentence[i + 1] == "~":
        if sentence[i + 3] in subscripts and sentence[i + 4] == ")":
            return True
        elif sentence[i + 3] == ")":
            return True
    else:
        if sentence[i + 2] in subscripts and sentence[i + 3] == ")":
            return True
        elif sentence[i + 2] == ")":
            return True
    return False

def enclose(str1):
    i = -1
    global subscripts
    while i < len(str1) - 1:
        i += 1
        str2 = str1[i:i + 1]
        str3 = str1[i - 1:i]
        str4 = str1[i + 1:i + 2]
        if str2.islower() and str4 in subscripts:
            if str3 == "~":
                str1 = str1[:i - 1] + "(~" + str2 + str4 + ")" + str1[i + 2:]
            else:
                str1 = str1[:i] + "(" + str2 + str4 + ")" + str1[i + 2:]
            i += 4
        elif str2.islower():
            if str3 == "~":
                str1 = str1[:i - 1] + "(~" + str2 + ")" + str1[i + 1:]
            else:
                str1 = str1[:i] + "(" + str2 + ")" + str1[i + 1:]
            i += 3
    return str1

def unenclose(str1):
    # this removes ( ) from around a sentence abbreviation
    i = -1
    if "(" not in str1:
        return str1

    while i < len(str1) - 1:
        i += 1
        str2 = str1[i:i + 1]
        str3 = str1[i - 1:i]
        str4 = str1[i + 1:i + 2]
        if str2.islower() and str3 != "~" and str4 not in subscripts:
            str1 = str1[:i - 1] + str2 + str1[i + 2:]
        elif str2.islower() and str3 == "~" and str4 not in subscripts:
            str1 = str1[:i - 2] + str3 + str2 + str1[i + 2:]
        if str2.islower() and str3 != "~" and str4 in subscripts:
            str1 = str1[:i - 1] + str2 + str4 + str1[i + 3:]
        elif str2.islower() and str3 == "~" and str4 in subscripts:
            str1 = str1[:i - 2] + str3 + str2 + str4 + str1[i + 3:]

    return str1

def unenclose1(sentences, unenclose_at_end):
    for i in range(len(sentences)):
        temp_string = sentences[i]
        if temp_string.find("(!") > -1:
            sentences[i] = sentences[i].replace("(!", "~(")
    if unenclose_at_end:
        for i in range(len(sentences)):
            sentences[i] = unenclose(sentences[i])