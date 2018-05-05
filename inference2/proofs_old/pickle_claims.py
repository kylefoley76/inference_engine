
from openpyxl import load_workbook
import pickle
import copy
from general_functions import get_last_row



wb = load_workbook('/Users/kylefoley/PycharmProjects/inference_engine2/inference2/Proofs/inference_engine_new.xlsx')
ws = wb.worksheets[0]

test_sent = []
num = 0
last_string = 0
last_row = get_last_row(ws, 2)
set_of_sentences = []
row_num = 0
for row in ws:
    row_num += 1
    str1 = row[2].value

    if str1 != None and "*" not in str(str1):
        if row[3].value == 0: row[2].value = 'pass'

        if row[2].value != None and row[2].value != "":
            set_of_sentences.append(row[2].value)
        last_string = row[2].value

    elif set_of_sentences != []:
        test_sent.append(copy.deepcopy(set_of_sentences))
        set_of_sentences = []

    if row_num > last_row:
        break

if test_sent == []:
    raise Exception ('no sentences')

output = open('zz_claims.pkl', 'wb')
pickle.dump(test_sent, output)
output.close()
