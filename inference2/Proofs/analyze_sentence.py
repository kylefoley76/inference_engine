import copy

try:
    from settings import *
    from general_functions import *
    from classes import *
except:
    from .settings import *
    from .general_functions import *
    from .classes import *

#
#
# from settings import *
# from general_functions import *
# from classes import *





def replace_w_greek(sentence, result):
    j = 947
    list1 = [x for x in sentence]
    erase_next_parent = False
    keep_next_mini = False
    embed_dict = {}
    for i, letter in enumerate(list1):
        if letter == neg:
            bb = 8
        try:
            next5 = "".join(list1[i + 1:i+6]).replace(" ","")
        except:
            next5 = ""

        if next5.startswith(mini_e + "((") and not keep_next_mini:
            j += 1
            english = list1[i]
            list1[i] = chr(j)
            keep_next_mini = True
            embed_dict.update({english: chr(j)})

        elif next5[:2] == mini_e + "(" and (next5[3].isupper() or next5[3] == neg):
            print (f"in {sentence} you cannot have a single open paren follow {mini_e}")
            raise Exception

        elif letter == mini_e and keep_next_mini:
            keep_next_mini = False

        elif i > 0 and list1[i - 1] == "(" and (letter.islower() or letter == "~" or letter == neg):
            j += 1
            list1[i] = chr(j)
            list1[i - 1] = " "
            erase_next_parent = True
        elif erase_next_parent and letter == ")":
            list1[i] = " "
            erase_next_parent = False
        elif letter not in ["(", ")", "&", conditional, xorr, iff, idisj, "#", "|"]:
            list1[i] = " "

    sent = "".join(list1)
    result[10] = embed_dict

    return sent

def get_evar(sentence, idx):
    while True:
        idx -= 1
        if sentence[idx] in subscripts:
            var = sentence[idx-1:idx+1]
            assert var[0].islower()
            assert var[1] in subscripts
            return var
        elif sentence[idx].islower():
            return sentence[idx]


def find_sentences(sentence, definiendum="", embed=False, paren=False):
    if sentence == None:
        raise Exception("\n missing word in dictionary \n")

    if one_sentence(sentence):
        if definiendum != "":
            # raise Exception("\n you cannot reduce this word: " + "\n" + definiendum + "\n")
            raise ErrorWithCode(f"\n you cannot reduce {definiendum} \n  in {sentence} \n")
        else:
            raise ErrorWithCode(f"\n you cannot reduce {definiendum} \n  in {sentence} \n")
            # raise Exception("\n you cannot reduce this word: " + "\n" + sentence + "\n")
    bad_paren = False
    if sentence.count('(') != sentence.count(')'):
        print("( paren = " + str(sentence.count("(")))
        print(") paren = " + str(sentence.count(")")))
        print (f" too many parentheses in {definiendum}")
        bad_paren = True

    if definiendum == 'BTP':
        bb = 8

    if not paren:
        paren_count = 1
    if not bad_paren:
        sentence = remove_extra_paren(sentence, embed)
    result = [None] * 11
    tilde = False
    if "~(" in sentence:
        tilde = True
        sentence = sentence.replace("~(", "(~")
    sentences = []
    greek_sent = replace_w_greek(sentence, result)
    greek_sentences = []
    greek_sentences.append(greek_sent)
    assert len(greek_sent) == len(sentence)
    mainc = []
    num_to_conn = {}
    sent_numbers = []
    add_sibling = False
    gen = 1
    gener = ['1']
    sentences.append(sentence)
    sent_numbers.append("1")
    idx_dict = {}
    size_index = [0]
    off = False
    embed = False
    embed2 = False
    ignore_cparen = False
    ecount = 0
    embed_dict = {}

    for idx, letter in enumerate(sentence):
        if idx == 56:
            bb = 8

        if letter in all_connectives:
            sent_num2 = ".".join(gener[:-1])
            num_to_conn.update({sent_num2: letter})

        # if letter.islower() and off:
        #     print (f" in {definiendum} a missing oparen was found")
        #     sentence  = sentence[:idx] + "(" + sentence[idx:]
        #     result[7] = sentence
        #     return result, True
        #
        #
        # if letter in all_connectives and not off:
        #     print (f" in {definiendum} a missing cparen was found")
        #     sentence = sentence[:idx] + ")" + sentence[idx:]
        #     result[7] = sentence
        #     return result, True

        elif letter == mini_e:
            embed = True
            embed2 = True

        elif letter == "(" and embed:
            embed = False
            embed2 = True
            ecount = 1
            evar = get_evar(sentence, idx)
            idx_dict.update({sent_num: idx})

        elif letter == "(" and not embed:
            off = False
            if add_sibling:
                del gener[-1]
                gen += 1
            else:
                gen = 1

            gener.append(str(gen))
            sent_num = ".".join(gener)
            idx_dict.update({sent_num: idx})
            add_sibling = False
            if embed2: ecount += 1

        elif letter == ")" and ignore_cparen:
            ignore_cparen = False

        elif letter == ")":
            if embed2: ecount -= 1
            off = True
            if add_sibling:
                del gener[-1]
                sent_num = ".".join(gener)
                list1 = sent_num.split(".")
                gen = int(list1[-1])
            num_periods = sent_num.count(".")
            begin = idx_dict.get(sent_num)
            add_sibling = True

            if sent_num == '1.2.3':
                bb = 8

            if len(sent_num) >= len(sent_numbers[-1]):
                sent_numbers.append(sent_num)
                sentences.append(sentence[begin: idx + 1])
                greek_sentences.append(greek_sent[begin: idx + 1])
                size_index.append(num_periods)
                b = len(sentences) - 1
            else:
                b = get_sent_position(size_index, num_periods)
                sent_numbers.insert(b, sent_num)
                size_index.insert(b, num_periods)
                sentences.insert(b, sentence[begin: idx + 1])
                greek_sentences.insert(b, greek_sent[begin: idx + 1])

            if embed2 and ecount == 0:
                embed2 = False
                ignore_cparen = True
                embed_dict.update(({evar: greek_sentences[b]}))

        elif letter.islower() and embed:
            embed2 = False
            embed = False

    for sent_number in sent_numbers:
        if sent_number not in num_to_conn.keys():
            num_to_conn.update({sent_number: ""})
        mainc.append([sent_number, num_to_conn.get(sent_number)])

    if bad_paren:
        paren_count += 1
        new_sent, replacements = fix_bad_paren(sentences, sent_numbers)
        result, _ = find_sentences(new_sent, definiendum, False, True)
        # check_that_paren_in_right_order(result, definiendum, paren)
        if replacements != []:
            result[7] = result[3][0]
            result[8] = replacements
    else:

        result[0] = num_to_conn
        result[1] = split_numbers(sent_numbers, bad_paren, sentences, definiendum)
        result[2] = sent_numbers
        result[3] = sentences
        result[4] = mainc
        result[6] = adjust_greek_sent(greek_sentences)
        result[5] = greek_sentences[0]
        result[9] = embed_dict

        check_that_paren_in_right_order(result, definiendum, paren)


    if tilde:
        for e, sent in enumerate(sentences):
            sent = sent.replace("(~", "~(")
            sentences[e] = sent


    return result, False





def fix_missing_paren(idx, sentences, sentence, open):

    chunk = sentence[idx + 1: idx + 5]
    if open:
        for e, sent in enumerate(sentences):
            if sent.startswith(chunk):
                sentences[e] = "(" + sent
    else:
        for e, sent in enumerate(sentences):
            if sent.endswith(chunk):
                sentences[e] = sent + ")"

    return


def fix_bad_paren(sentences, sent_numbers):
    b = sentences[0].count("(") - sentences[0].count(")")
    new_sent = []
    replacements = []
    for sent in reversed(sentences):
        if sent.startswith("(((m"):
            bb = 8
        oparen = sent.count("(")
        cparen = sent.count(")")
        if oparen != cparen:
            if oparen - cparen == b and new_sent == []:
                fix_bad_parent2(sent, sentences, new_sent)
                break
            elif new_sent != "" and sent not in new_sent:
                fix_bad_parent2(sent, sentences, new_sent)
        elif oparen > 1 and one_sentence(sent):
            old_sent = sent
            new_sent3 =remove_extra_paren(sent)
            sentences[0] = sentences[0].replace(old_sent, new_sent3)
            replacements.append([old_sent, new_sent])

    return sentences[0], replacements


def fix_bad_parent2(sent, sentences, new_sent):
    oparen = sent.count("(")
    cparen = sent.count(")")
    b = oparen - cparen
    if oparen < cparen:
        b = abs(b)
        c = "(" * b
        new_sent2 = c + sent
    else:
        c = ")" * b
        if sent[-1] == "|":
            temp = sent[-1]
            new_sent2 = temp + c + "|"
        else:
            new_sent2 = sent + c
    new_sent2 = remove_extra_paren(new_sent2)
    new_sent.append(new_sent2)
    sentences[0] = sentences[0].replace(sent, new_sent2)
    return


def get_sent_position(size_index, num_periods):
    j = 0
    while True:
        if size_index[j] > num_periods:
            return j
        j += 1
    raise Exception


def split_numbers(sent_number, bad_paren, sentences, definiendum):
    list1 = []
    for num in sent_number:
        list2 = num.split(".")
        list1.append(list2)

    if bad_paren:
        for i in range(len(list1) - 1, 1, -1):
            lst = list1[i]
            str1 = sentences[i]
            lst3 = lst[:-1]
            if lst3 not in list1:
                raise Exception(f" {str1} needs a brother in {definiendum}")

    return list1


def check_that_paren_in_right_order(output, definiendum, paren):
    if not paren:
        cond_found = False
        j = 0
        for lst4, lst2, lst3, lst1 in zip(output[4], output[2], output[3], output[1]):
            if j == 0 and lst4[1] == "&":
                is_conjunctive = True

            elif j == 0:
                is_conjunctive = False
            if j > 0:
                if j == 7:
                    bb = 8

                if len(lst1) > 2:
                    idx = output[4][output[2].index(".".join(lst1[:-1]))]
                    parent_conn = idx[1]
                    if parent_conn in [conditional, iff] and lst1[-1] == '3':
                        print_all(output[3])
                        raise Exception(f""" in {definiendum} you have placed your parentheses 
                                        incorrectly in the following sentence """ + lst3)

                if is_conjunctive and len(lst1) == 2 and lst4[1] in [conditional, iff]:
                    cond_found = True
                if is_conjunctive and len(lst1) == 2 and lst4[1] == "&":
                    raise Exception


            j += 1

        if not cond_found and is_conjunctive:
            print_all(output[3])
            raise Exception(f"""in {definiendum} the main connective of the 
                                must be a conditional or a biconditional conjuncts, the
                                following sentence does not have that """ + output[3][0])

    return


def print_all(lst):
    for sent in lst:
        print (sent)


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


def period_elimination(def_info2, definition, word):
    if "." not in definition:
        return def_info2, definition
    hypo_conn = [iff, idisj, xorr, conditional]
    i = -1
    if len(def_info2) > 1:
        raise Exception

    for e, def_info in enumerate(def_info2):
        while i < len(def_info[3]) - 1:
            i += 1
            sent = def_info[3][i]
            if "." in sent and one_sentence(sent):
                # if the sentence is the sole sentence on one side of a hypothetical
                # then we have to add additional parentheses
                paren_num = ".".join(def_info[1][i][:-1])
                g = findposinmd(paren_num, def_info[4], 0)
                paren_conn = def_info[4][g][1]
                assert paren_conn != ""
                per_pos = sent.find(".")
                new_sentences = get_sent_from_period(sent, per_pos)
                new_conjunct = " & ".join(new_sentences)
                if paren_conn in hypo_conn:
                    new_conjunct = "(" + new_conjunct + ')'
                    def_info[4][i][1] = "&"
                    def_info[3][i] = new_conjunct

                definition = definition.replace(sent, new_conjunct)
                def_info, _ = find_sentences(definition, word)
                def_info2[e] = def_info

    return def_info2, definition
