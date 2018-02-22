
from intermed_code import get_result

import types, sys
m = types.ModuleType("m","intermed_code.py")


sys.modules['m'] = m
sys.modules['m']
code = compile("get_result('hey')", "m.py", "exec")
exec in m.__dict__


# from intermed_code import get_result_old
from ast import literal_eval
#
# begin_file = "/Users/kylefoley/PycharmProjects/inference_engine2/inference2/Ancient/intermed_code.py"
# import importlib.machinery
# bb = 8
# loader = importlib.machinery.SourceFileLoader('report', begin_file)
# handle = loader.load_module('report')
#
# handle.getresult_old()



import cProfile, pstats, profile
import re



list1 = ["new_code","pickle_dictionary","pickle_claims","general_functions",
        "settings", "change_abbreviations", "standard_order", "start_and_stop", "use_lemmas",
         "analyze_sentence", "uninstantiable_definitions", 'natural_language',
         "put_words_in_slots", "z_dict_words", "zz_claims", "search_for_instantiation"]




cProfile.run(code, 'data_stats')
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


    # if k[0][:-3] in list1:
    cd = v[3] * 1_000_000

    # if int(v[3] * 10_000_000_000) > 0:

    total_time = int(v[3] * 1_000_000)
    total_number = v[0]
    average = total_time/total_number
    if k[2] == "change_abbrev":
        bb = 8

    if average > 10:
        average = str(int(average))
    else:
        average = str("{0:.3f}".format(total_time/total_number))


    list4.append([int(v[3] * 1_000_000), v[0], average, k[2]])



list4.sort(reverse = True)

for lst in list4:
    print (str(lst[0]) + "   " + str(lst[1]) + "   " + lst[2] + "   " + lst[3])


bb = 8