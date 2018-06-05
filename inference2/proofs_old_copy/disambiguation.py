
# try:
from general_functions import *
# except:
#     from .general_functions import *



def disam_is(sent, num, dictionary, abbreviations):
    idx = sent[54].index(num)
    a_found = False
    aidx = 0
    for e, num2 in enumerate(sent[54]):
        if e > idx:
            word2 = sent[num2]
            if isvariable(word2):
                word2 = abbreviations.get(word2)
                pos = dictionary.pos.get(word2)
                isconcept = True if dictionary.kind.get(word2) == 'c' else False
            else:
                pos = dictionary.pos.get(word2, "xx")
                isconcept = True if dictionary.kind.get(word2) == 'c' else False

            if word2 == 'a':
                a_found = True
                aidx = num2

            if num2 in standard_nouns and isconcept:
                sent[num] = 'I'
                sent[aidx] = None
                sent[54].remove(aidx)
                j = findposinmd(aidx, sent[45], 0)
                assert j != -1
                del sent[45][j]
                return sent

            elif pos[0] == 'n' and dictionary.kind.get(word2) == 'i':
                sent[num] == '='
                assert not a_found
                return sent

            elif pos[0] == 'a' and not a_found:
                new_num = adj_to_pred_complement.get(num2)
                sent[new_num] = sent[num2]
                sent[num] = "J"
                sent[num2] = None
                j = findposinmd(num2, sent[45], 0)
                assert j != -1
                del sent[45][j]
                idx = sent[54].index(num2)
                sent[54][idx] = new_num

                return sent
    return




def disambiguate_sentence(output, inferences, dictionary):
    for m, sent in enumerate(output.all_sent):
        ant_sent = sent[0]
        ant_sentp = sent[3] + sent[2]
        replacement_made = False

        for num in sent[54]:
            if sent[num] in dictionary.ambiguous:
                replacement_made = True
                word = sent[num]
                if word == "IS":
                    sent = disam_is(sent, num, dictionary, output.abbreviations)
                    rule = "DIS IS"
                    output.all_sent[m] = sent

        if replacement_made:
            direct_equivalence(output, ant_sent, ant_sentp, output.all_sent[m], rule)
            inferences.append([output.all_sent[m][1], output.all_sent[m][2], output.all_sent[m][3], "EF", ant_sentp,
                               output.tindex, is_standard(output.all_sent[m])])

    return