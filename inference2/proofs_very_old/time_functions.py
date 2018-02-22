from new_code_old import get_result
from ast import literal_eval

import cProfile, pstats, profile
import re


list1 = ["new_code","pickle_dictionary","pickle_claims","general_functions",
        "settings", "change_abbreviations", "standard_order", "start_and_stop", "use_lemmas",
         "analyze_sentence", "uninstantiable_definitions", 'natural_language',
         "put_words_in_slots",
         "z_dict_words", "zz_claims", "search_for_instantiation"]



cProfile.run("get_result()", 'data_stats')
p = pstats.Stats('data_stats')
p.strip_dirs().sort_stats(-1).print_stats()
p.sort_stats('name')
list4 = []
for k, v in p.stats.items():
    list2 = k[2].split(",")
    list3 = list1[0].split(".")
    function_name = list2[0][1:]
    if "hypothetical" in k[2]:
        bb = 8

    try:
        if k[0][:-7] in list1:
            if int(v[3] * 1000) > 20:

                total_time = int(v[3] * 1000)
                total_number = v[0]
                average = total_time/total_number
                if k[2] == "change_abbrev":
                    bb = 8

                if average > 100:
                    average = str(int(average))
                else:
                    average = str("{0:.3f}".format(total_time/total_number))


                list4.append([int(v[3] * 1000), v[0], average, k[2]])
    except:
        pass



list4.sort(reverse = True)

for lst in list4:
    print (str(lst[0]) + "   " + str(lst[1]) + "   " + lst[2] + "   " + lst[3])