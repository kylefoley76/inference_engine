from main_loop import get_result
import sys
from lemmas import *

arguments = sys.argv

start = 85
stop = 86
kind = 0
end = 243
print_type = 2
get_words_used = 0
size = "large"
do_not_argue = [28]
order = []

# in 85.13 the ancestor should be 10 not 11

if len(arguments) > 1:

    if arguments[1] == "j":
        print_type = 2
    elif arguments[1] in ["mm", "dc", "mm2"]:
        kind = arguments[1]
        if len(arguments) > 2: print_type = arguments[2]

        if kind == 'dc':
            size = 'small' if len(arguments) > 2 else 'large'

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
    determine_class("", size)

if print_type == 2:
    print_sent(output, order, print_type)
elif print_type == 1:

    print_sent(output, order, print_type)

