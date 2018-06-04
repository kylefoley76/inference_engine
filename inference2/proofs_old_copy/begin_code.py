import sys
import pickle
#
# from main_loop import get_result
# from lemmas import *

#hey man


from main_loop import get_result
from lemmas import determine_class, print_some_lemmas
from general_functions import print_sent



#
# try:
#     from main_loop import get_result
#     from lemmas import determine_class, print_some_lemmas
#     from general_functions import print_sent
# except:
#     from .main_loop import get_result
#     from .lemmas import determine_class, print_some_lemmas
#     from .general_functions import print_sent



arguments = sys.argv
start = 267
stop = 268
kind = "os"
end = 246
print_type = "21"
get_words_used = 0
do_not_argue = [28]
order = []
single_sent = ""


def replace_one_zero(single_sent):
    single_sent = single_sent.strip()
    if single_sent.startswith("0"):
        return "it is contradictory that " + single_sent[2:]
    elif single_sent.startswith("1"):
        return "it is consistent that " + single_sent[2:]
    else:
        return single_sent

def get_single_sent(arguments):
    order = [0]
    if len(arguments) > 2:
        print_type = arguments[2]
        if int(print_type) < 10:
            print_type = print_type + "0"
    else:
        print_type = "20"
    single_sent = "it is consistent that a man is a dog"
    # single_sent = input("input sentence: ")
    if single_sent[-1] == ".":
        single_sent = single_sent[:-1]
    if "." in single_sent:
        single_sent = single_sent.split(".")
        for e, sent in enumerate(single_sent):
            single_sent[e] = [replace_one_zero(sent)]
        order = [x for x in range(len(single_sent))]

    else:
        single_sent = replace_one_zero(single_sent)
        single_sent = [[single_sent]]

    return single_sent, print_type, order


if len(arguments) == 1:
    arg1 = ""
    arg2 = ""
    arg3 = ""
elif len(arguments) == 2:
    kind = arguments[1]
    arg1 = ""
    arg2 = ""
    arg3 = ""
elif len(arguments) == 3:
    kind = arguments[1]
    arg1 = arguments[2]
    arg2 = ""
    arg3 = ""
elif len(arguments) == 4:
    kind = arguments[1]
    arg1 = arguments[2]
    arg2 = arguments[3]
    arg3 = ""
elif len(arguments) == 5:
    kind = arguments[1]
    arg1 = arguments[2]
    arg2 = arguments[3]
    arg3 = arguments[4]

try:
    if isinstance(int(arg1), int):
        kind = 'default'
    else:
        kind = arg1
except:
    pass



if kind == 'default':

    if arg1 != "": start = int(arg1)
    if arg2 != "": stop = int(arg2)
    if arg3 != "": print_type = arg3
    if len(print_type) == 1: print_type += "0"



    if stop == 0: stop = end
    if order == []:
        for x in range(start, stop):
            if x not in do_not_argue: order.append(x)
    output = get_result(single_sent, "", print_type, order, get_words_used)
    print_sent(output, order, print_type)

elif kind == 'le':
    print_some_lemmas(arg1, arg2)

elif kind == 'dc':
    determine_class("")

elif kind == 'ts':
    # list1 = test_sentences()
    pkl_file = open('temp_list.pkl', 'rb')
    list1 = pickle.load(pkl_file)
    pkl_file.close()

    # pkl_file = open('temp_list.pkl', 'wb')
    # pickle.dump(list1, pkl_file)
    # pkl_file.close()

    order = [x for x in range(9)]
    output = get_result(list1, "", "31", order, 0)
    for list2 in output[:9]:
        print (list2[1][1])
        print (list2[len(list2) - 1][1])
        print ("")


elif kind == "os":
    single_sent, print_type, order = get_single_sent(arguments)
    output = get_result(single_sent, "", print_type, order, get_words_used)
    print_sent(output, order, print_type)




    # print type
    # 0 do not print sentence or individual times, stop if false, only
    # interested in success or failure
    # 1 print all sentences to temp.xlsx
    # 2 print to terminal
    # 3 do not print but print the time of each sentence
    # 4 do not print individual times, do not stop if false










# fix disjunctions in definitions
# fix parentheses checker
# build list of 2000 checked predicates
# adjectives must have a J in the definiendum
# set of unnamed adjectives and classes