from radon.raw import analyze
from radon.complexity import cc_rank, cc_visit, cc_visit_ast
import inspect

list1 = ["pickle_dictionary","pickle_claims","general_functions", "natural_language",
        "settings", "change_abbreviations", "standard_order", "use_lemmas",
         "analyze_sentence", "uninstantiable_definitions", "put_words_in_slots",
         "prepare_for_print", "main_loop", "start_and_stop", "search_for_instantiation"]
list2 = ["intermed_code"]

base_directory = "/Users/kylefoley/PycharmProjects/inference_engine2/inference2/Proofs/"
base_directory2 = "/Users/kylefoley/PycharmProjects/inference_engine2/inference2/ancient/"

num_of_functions = 0
large_functions = []
total_lines = 0
total_complexity = 0
bb = 8
for file in list1:
    current_file = base_directory + file + ".py"

    with open(current_file) as f:
        content = f.read()
        loc = analyze(content)
        cc = cc_visit(content)
        num_of_functions += len(cc)
        for func in cc:
            if func.letter == 'C':
                for clas_func in func[4]:
                    total_complexity += clas_func[7]
                    if clas_func[7] > 15:
                        large_functions.append([func[0], func[7]])
            else:
                total_complexity += func[7]
                if func[7] > 15:
                    large_functions.append([func[0], func[7]])
        total_lines += loc[1]

        # ccr = cc_rank(content)

large_functions.sort()
print ("total lines: " + str(total_lines))
lines_per_code = total_lines/num_of_functions
print ("lines per code: " + str(lines_per_code))
print ("number of functions: " + str(num_of_functions))
print ("total complextiy: " + str(total_complexity/num_of_functions))

# for func in large_functions:
#     print (func[0] + " " + str(func[1]))

