
from main_loop import get_result
from openpyxl import load_workbook
import sys

arguments = sys.argv

start = 221
stop = 222
end = 238
print_type = 3
get_words_used = 0
iff = chr(8801)
implies = chr(8866)
conditional = chr(8594)
xorr = chr(8891)
idisj = chr(8744)

# was at 121

do_not_argue = []



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




def parameters():
    proof_type = 0
    print_type = 2
    get_words_used = 0

    return proof_type, print_type, get_words_used


    # print type
    # 0 do not print sentence or individual times, stop if false, only
    # interested in success or failure
    # 1 print all sentences to temp.xlsx
    # 2 print to terminal
    # 3 do not print but print the time of each sentence
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

def get_right_most_connective(str1):
    split_at_space = False
    if len(str1) > 67:
        j = 67
    else:
        j = len(str1) - 1
    for i in range(j, 15, -1):
        if str1[i] in ["&", conditional, iff, xorr, idisj]:
            return i
        if i == 31:
            split_at_space = True
        if split_at_space and str1[i] == " ":
            return i




def space_sentences(str1, str2):
    b = len(str1)
    c = len(str2)
    j = 0
    second = ""
    third = ""
    if (b + c) > 70:
        location = get_right_most_connective(str1)
        first = str1[:location]
        second = str1[location:]
        if len(second) > 70:
            j += 1
            assert j != 2
            list1 = space_sentences(second, str2)
            second = list1[0]
            third = list1[1]
            str2 = ""

        spaces_needed = 65 - (len(second) + len(str2))
        space = " " * spaces_needed
        second = "     " + second + space + str2
    else:
        spaces_needed = 70 - (len(str1) + len(str2))
        space = " " * spaces_needed
        first = str1 + space + str2

    return [first, second, third]


def print_sent(test_sent, order):
    row_number = 1
    for i in order:
        for j in range(len(test_sent[i])):
            rule = ""
            if test_sent[i][j][4] != "":
                rule = test_sent[i][j][4] + " "
                if test_sent[i][j][5] != "":
                    rule += str(test_sent[i][j][5])

                    if test_sent[i][j][6] != "":
                        rule += "," + str(test_sent[i][j][6])

            if print_type == 2:
                len_sp = 5 - len(str(test_sent[i][j][0]))
                space = " " * len_sp
                list3 = space_sentences(str(test_sent[i][j][0]) + space + test_sent[i][j][3] + \
                                        test_sent[i][j][1], rule)
                for str1 in list3:
                    if str1 != "":
                        print(str1)

            elif print_type == 1:
                w4.cell(row=row_number, column=2).value = test_sent[i][j][0]
                w4.cell(row=row_number, column=3).value = test_sent[i][j][3] + test_sent[i][j][1]
                w4.cell(row=row_number, column=4).value = test_sent[i][j][4]
                if len(test_sent[i][j]) > 8:
                    if test_sent[i][j][8] == "*":
                        xls_cell = w4.cell(row=row_number, column=3)
                        xls_cell.font = xls_cell.font.copy(color='FFFF0000')

            row_number += 1

    return



if stop == 0: stop = end
order = [x for x in range(start, stop)]
# order = [105,106,108,109,121]
output = get_result("", print_type, order, do_not_argue)

if print_type ==  2:
    print_sent(output, order)


elif print_type == 1:
    wb4 = load_workbook('/Users/kylefoley/Desktop/inference_engine/temp_proof.xlsx')
    w4 = wb4.worksheets[0]
    print_sent(output)
    wb4.save('/Users/kylefoley/Desktop/inference_engine/temp_proof.xlsx')
if get_words_used == 1:
    wb5 = load_workbook('/Users/kylefoley/Desktop/inference_engine/dictionary5.xlsx')
    w5 = wb5.worksheets[0]
    wb5.save('/Users/kylefoley/Desktop/inference engine/dictionary5.xlsx')
