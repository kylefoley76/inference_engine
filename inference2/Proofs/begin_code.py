import sys
import pickle


try:
    from main_loop import get_result
    from lemmas import determine_class, print_some_lemmas
    from general_functions import print_sent
    from useful_tools import print_geneology
    from generate_sentences import test_sentences
except:
    from .main_loop import get_result
    from .lemmas import determine_class, print_some_lemmas
    from .general_functions import print_sent
    from .useful_tools import print_geneology
    from .generate_sentences import test_sentences


#
# from main_loop import get_result
# from lemmas import determine_class, print_some_lemmas
# from general_functions import print_sent
# from useful_tools import list_of_exc
# from generate_sentences import test_sentences



arguments = sys.argv
start = 278
stop = 279
kind = "ts"
end = 246
print_type = "20" #if the second digit is 1 then it ignores errors
get_words_used = 0
do_not_argue = [28]
order = []
single_sent = ""
if kind == "0": kind = 'default'

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
    # print_type = "20"
    # single_sent = "0 a spatial description is red"
    single_sent = input("input sentence: ")
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

# print (len(arguments))

if len(arguments) == 1:
    arg1 = ""
    arg2 = ""
    arg3 = ""
    arg4 = ""
elif len(arguments) == 2:
    kind = arguments[1]
    arg2 = ""
    arg3 = ""
    arg4 = ""
    arg5 = ""
elif len(arguments) == 3:
    arg1 = arguments[1]
    arg2 = arguments[2]
    arg3 = ""
    arg4 = ""
    arg5 = ""
elif len(arguments) == 4:
    arg1 = arguments[1]
    arg2 = arguments[2]
    arg3 = arguments[3]
    arg4 = ""
    arg5 = ""
elif len(arguments) == 5:
    kind = arguments[1]
    arg1 = arguments[2]
    arg2 = arguments[3]
    arg3 = arguments[4]
    arg4 = ""


try:
    if isinstance(int(arguments[1]), int):
        kind = 'default'
    else:
        kind = arguments[1]
except:
    pass


if kind == 'default':

    if arg1 != "": start = int(arguments[1])
    if arg2 != "": stop = int(arguments[2])
    if arg3 != "": print_type = arguments[3]
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
    arg2 = 2
    test_sentences(arg1)

elif kind == "os":
    single_sent, print_type, order = get_single_sent(arguments)
    output = get_result(single_sent, "", print_type, order, get_words_used)
    print_sent(output, order, print_type)

elif kind == "pg":
    if "." in arg1:
        arg1 = arg1.replace(".", "|")
    print_geneology(arg1)




    # print type
    # 0 do not print sentence or individual times, stop if false, only
    # interested in success or failure
    # 1 print all sentences to temp.xlsx
    # 2 print to terminal
    # 3 do not print but print the time of each sentence
    # 4 do not print individual times, do not stop if false


# the lemma: leibniz.Hessence is missing
# smell|n does not have a plural
# the prepositional relations can also appear without 'is' preceding




