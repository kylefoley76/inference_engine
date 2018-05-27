
from settings import *


def check_grammar(list1):

    str1 = adj_wrong_place(list1)


    return str1


def adj_wrong_place(list1):
    b = -1
    for k, v in adj_to_pred_complement.items():
        b += 1
        if list1[k] != None and \
            list1[relational_positions[b]] not in ["is", "are"] and \
            list1[v] == None:

            return f"Ungrammatical: the adjective {list1[k]} does not modify a noun"


    return ""