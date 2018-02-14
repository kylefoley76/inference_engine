import time
import sys
import pickle, json
from natural_language import step_one
from general_functions import parameters
from classes import ErrorWithCode


def calculate_time_statistics(num_proved, total_time):
    total_time = time.time() - total_time
    print("")
    print("average " + str("{0:.4f}".format(total_time / num_proved)))
    print("total " + str("{0:.3f}".format(total_time)))
    print("")
    print (num_proved)


def get_result(one_sent, print_type = 4, order = [0], do_not_argue = [], argue = []):
    total_time = time.time()

    if one_sent == 'a':
        proof_type, print_type, get_words_used, order = parameters()
        pkl_file = open('zz_claims.pkl', 'rb')
        test_sent = pickle.load(pkl_file)
        pkl_file.close()
    elif one_sent != "":
        test_sent = [[one_sent]]
    else:
        if argue != []:
            order = argue
        pkl_file = open('zz_claims.pkl', 'rb')
        test_sent = pickle.load(pkl_file)
        pkl_file.close()


    j = -1
    num_proved = 0
    while j < len(order) - 1:
        j += 1
        k = order[j]

        if test_sent[k][0] != 'pass' and k not in do_not_argue:
            num_proved += 1
            st1 = time.time()

            if k == 225:
                bb = 7
            try:
                consistent, total_sent = step_one(test_sent[k])
                test_sent[k] = json.loads(json.dumps(total_sent))
            except ErrorWithCode:
                print (str(j) + "infinite loop")

            if print_type != 4:
                if not consistent:
                    if print_type == 3:
                        print(str(k) + " - " + str("{0:.3f}".format(time.time() - st1) + " False"))
                    elif print_type == 0:
                        print (str(k) + " - False")
                        sys.exit()
                elif print_type == 3:
                    print(str(k) + " - " + str("{0:.3f}".format(time.time() - st1)))

        elif print_type == 0 and k % 50 == 0:
            print (k)

    if print_type in [0, 2, 3, 4]:
        if print_type == 0:
            print ("success")
        calculate_time_statistics(num_proved, total_time)

    return test_sent






