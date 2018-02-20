from main_loop import get_result
from openpyxl import load_workbook
import sys, re
from general_functions import print_sent
from lemmas import *

arguments = sys.argv

start = 151
stop = 0
kind = 0
end = 243
print_type = 3
get_words_used = 0
iff = chr(8801)
implies = chr(8866)
conditional = chr(8594)
xorr = chr(8891)
idisj = chr(8744)
mini_e = chr(8703)
nonseq = chr(8876)
bottom = chr(8869)
special_connectives = [iff, conditional, xorr, idisj]
all_connectives = special_connectives + [implies, nonseq, "&"]
one_sentence = lambda x: not re.search(xorr + "|" + implies + "|" + iff + "|" + idisj + "|" +
                                   conditional + "|&", x)

do_not_argue = [28]
order = []

# all arguments fit the relevance rule except for 180
# 80, 178, 233 get caught in infinite loops without relevance rule
#done, 241, 200, 208, 209 - 215, 242

if len(arguments) > 1:

    if arguments[1] == "j":
        print_type = 2
    elif arguments[1] in ["mm", "dc", "mm2"]:
        kind = arguments[1]
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


    # proof type
    # 0 break if false sentence
    # 1 ignore false sentence
    # 3 terminal input box
    # 4 test spelling errors






if stop == 0: stop = end
if order == []:
    for x in range(start, stop):
        if x not in do_not_argue: order.append(x)

if kind == 0:
    output = get_result("", "", print_type, order, get_words_used)
elif kind == "mm":
    make_matrix("")
elif kind == "mm2":
    make_matrix2("")
elif kind == "dc":
    determine_class("")

if print_type == 2:
    print_sent(output, order, print_type)
elif print_type == 1:

    print_sent(output, order)

