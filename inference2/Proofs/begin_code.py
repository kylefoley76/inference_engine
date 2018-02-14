from main_loop import get_result
from openpyxl import load_workbook
import sys, re

arguments = sys.argv

start = 120
stop = 121
end = 243
print_type = 2
get_words_used = 0
iff = chr(8801)
implies = chr(8866)
conditional = chr(8594)
xorr = chr(8891)
idisj = chr(8744)
mini_e = chr(8703)
nonseq = chr(8876)
special_connectives = [iff, conditional, xorr, idisj]
all_connectives = special_connectives + [implies, nonseq, "&"]
one_sentence = lambda x: not re.search(xorr + "|" + implies + "|" + iff + "|" + idisj + "|" +
                                   conditional + "|&", x)

do_not_argue = [28]
argue = []
# all arguments fit the relevance rule except for 180
# 80, 178, 233 get caught in infinite loops without relevance rule
#done, 241, 200, 208, 209 - 215, 242

if len(arguments) > 1:

    if arguments[1] == "j":
        print_type = 2
    else:
        start = int(arguments[1])

        if len(arguments) == 2:
            stop = start + 1

        elif len(arguments) < 2:
            stop = 0
        else:
            stop = int(arguments[2])

        print_type = int(arguments[3]) if len(arguments) > 3 else 0
        proof_type = int(arguments[4]) if len(arguments) > 4 else 0

    # print type
    # 0 do not print sentence or individual times, stop if false, only
    # interested in success or failure
    # 1 print all sentences to temp.xlsx
    # 2 print to terminal
    # 3 do not print but print the time of each sentence
    # 4 do not print individual times, do not stop if false
    # 8 print to web page
    # 9 print to test machine

    # proof type
    # 0 break if false sentence
    # 1 ignore false sentence
    # 3 terminal input box
    # 4 test spelling errors


def determine_words_used():
    if get_words_used == 1:
        for i in range(len(words_used)):
            j = dictionary[7].get(words_used[i], 28)
            if j == 28:
                print(words_used[i])
            ws.cell(row=j, column=2).value = 1

def closest_to_max_size(word_str, max_size, sent_type):
    if sent_type == 'sent id' and len(word_str) < max_size:
        for idx in range(max_size, 0, -1):
            if word_str[idx] == ")":
                return idx
    elif one_sentence(word_str[:max_size]):
        for idx in range(max_size, 0, -1):
            if word_str[idx] in " ":
                return idx
    elif word_str.startswith("RELEVANT"):
        return 24

    else:
        for idx in range(max_size, 30, -1):
            if word_str[idx] in all_connectives:
                return idx
        else:
            if word_str[30:max_size].count(")") < 2:
                for idx in range(max_size, 0, -1):
                    if word_str[idx] in " ":
                        return idx
            else:
                raise Exception



def space_sentences(num_str, word_str, largest_rule, space1, rule, sent_type):
    third_column = largest_rule + 4
    max_size = 75 - third_column
    j = 0
    k = 0
    if " ," in word_str: word_str = word_str.replace(" ,",",")
    five_spaces = " " * 5
    # the word_str always starts at position 5, there is always
    # 3 spaces between the rule and the word_str

    while 5 + third_column + len(word_str) > 75:
        k += 1
        if k > 10: raise Exception ("printer caught in infinite loop")
        location = closest_to_max_size(word_str, max_size - 5, sent_type)
        remainder = word_str[location:]
        word_str = word_str[:location]

        if j == 0:
            space2 = 75 - (4 + len(word_str) + largest_rule)
            space2 = " " * space2
            print(num_str + space1 + word_str + space2 + rule)
        else:
            print(five_spaces + word_str)
        j += 1
        word_str = remainder
    else:
        if all(x in ["", " "] for x in word_str) and j > 0:
            pass
        elif j > 0:
            print(five_spaces + word_str)
        else:
            space2 = 75 - (4 + len(word_str) + largest_rule)
            space2 = " " * space2
            print(num_str + space1 + word_str + space2 + rule)

    return

def print_sent(test_sent, order):
    row_number = 1
    largest_rule = 1

    for i in order:
        for j in range(len(test_sent[i])):
            rule = ""
            if test_sent[i][j][5] == "id":
                pass
            elif test_sent[i][j][4] != "":
                rule = test_sent[i][j][4] + " "
                if test_sent[i][j][5] != "":
                    rule += str(test_sent[i][j][5])

                    if test_sent[i][j][6] != "":
                        rule += "," + str(test_sent[i][j][6])

                rule_size = len(rule)
                if rule_size > largest_rule: largest_rule = rule_size

                test_sent[i][j][4] = rule

        for j in range(len(test_sent[i])):
            if print_type == 2:

                size_num = 5 - len(str(test_sent[i][j][0]))
                space1 = " " * size_num
                sent_type = ""
                if test_sent[i][j][5] == 'id':
                    sent_type = 'sent id'
                elif test_sent[i][j][5] == 'natural':
                    sent_type = 'natural'
                word_str = test_sent[i][j][3] + test_sent[i][j][1]
                if test_sent[i][j][1].startswith("(a" + mini_e):
                    bb = 8

                space_sentences(str(test_sent[i][j][0]), word_str,
                    largest_rule, space1, test_sent[i][j][4], sent_type)


            elif print_type == 1:
                w4.cell(row=row_number, column=2).value = test_sent[i][j][0]
                w4.cell(row=row_number, column=3).value = test_sent[i][j][3] + test_sent[i][j][1]
                w4.cell(row=row_number, column=4).value = rule
                if len(test_sent[i][j]) > 8:
                    if test_sent[i][j][8] == "*":
                        xls_cell = w4.cell(row=row_number, column=3)
                        xls_cell.font = xls_cell.font.copy(color='FFFF0000')

            row_number += 1

    return


if stop == 0: stop = end
order = [x for x in range(start, stop)]
# order = [105,106,108,109,121]
output = get_result("", print_type, order, do_not_argue, argue)

if print_type == 2:
    print_sent(output, order)


elif print_type == 1:
    wb4 = load_workbook('/Users/kylefoley/Desktop/inference_engine/temp_proof.xlsx')
    w4 = wb4.worksheets[0]
    print_sent(output, order)
    wb4.save('/Users/kylefoley/Desktop/inference_engine/temp_proof.xlsx')
if get_words_used == 1:
    wb5 = load_workbook('/Users/kylefoley/Desktop/inference_engine/dictionary5.xlsx')
    w5 = wb5.worksheets[0]
    wb5.save('/Users/kylefoley/Desktop/inference engine/dictionary5.xlsx')
