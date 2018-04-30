import shutil, os, sys, argparse
from distutils.dir_util import copy_tree

list1 = ["json_dict", "main_loop","pickle_dictionary","pickle_claims","general_functions",
        "settings", "change_abbreviations", "standard_order", "begin_code", "use_lemmas",
         "analyze_sentence", "uninstantiable_definitions", 'natural_language',
         "put_words_in_slots", "prepare_for_print", "analyze_definition",
         "z_dict_words", "zz_claims", "search_for_instantiation", "classes", "lemmas",
         "words_used", "search_for_instantiation2", "lemmata", "disambiguation",
         "lemmas2", "grammar", "useful_tools"]





list2 = ["json_dict"]
list3 = ["words_used", "lemmata"]

base_directory = "/Users/kylefoley/PycharmProjects/inference_engine2/inference2/Proofs/"
old_directory = "/Users/kylefoley/PycharmProjects/inference_engine2/inference2/proofs_old/"


arguments = sys.argv



if len(arguments) > 1:
    com = arguments[1]
else:
    com = ""

if com == 'print':
    print ("""
    vo = moves new files into old and very old
    mi = make intermediate, moves old files into very old
    """)

if com == 'vo':

    str1 = ''
    old_directory = "/Users/kylefoley/PycharmProjects/inference_engine2/inference2/proofs_very_old/"
    shutil.rmtree(old_directory)
    os.mkdir(old_directory)

elif com == 'mi':
    str1 = ""
    old_directory = "/Users/kylefoley/PycharmProjects/inference_engine2/inference2/Proofs_old/"
    very_old_directory = "/Users/kylefoley/PycharmProjects/inference_engine2/inference2/proofs_very_old/"
    for file1 in os.listdir(old_directory):
        if os.path.isfile(old_directory + file1):
            shutil.copy2(old_directory + file1, very_old_directory + file1)
    sys.exit()


else:
    shutil.rmtree(old_directory)
    os.mkdir(old_directory)
    str1 = ""



    for file1 in list1:
        if file1.startswith("z") or file1 in list3:
            file1 += ".pkl"
            shutil.copy2(base_directory + file1, old_directory + file1)
        elif file1 in list2:
            copy_tree(base_directory + file1, old_directory + file1)
        else:
            file1 += ".py"
            shutil.copy2(base_directory + file1, old_directory + file1)
#
#
#
# for file1 in old_list:
#     full_path = old_directory + file1
#     list1 = []
#     with open(full_path, "r") as old:
#         for lines in old:
#             list1.append(lines)
#
#         for i, lines in enumerate(list1):
#             for k, v in dict1.items():
#                 if k in lines:
#                     list1[i] = list1[i].replace(k,v)
#
#     old.close
#
#     with open(full_path, "w") as old:
#         for lines in list1:
#             old.write(lines)
#
#     old.close
#     bb = 8



