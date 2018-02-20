
from openpyxl import load_workbook
import pickle
# from start_and_stop import info2
import copy



wb = load_workbook('/Users/kylefoley/Desktop/inference_engine/inference engine new.xlsx')
ws = wb.worksheets[0]

test_sent = []
num = 0
last_string = 0
set_of_sentences = []
for row in ws:

    str1 = row[2].value

    if str1 != None and "*" not in str1:
        if row[3].value == 0: row[2].value = 'pass'

        if row[2].value != None and row[2].value != "":
            set_of_sentences.append(row[2].value)
        last_string = row[2].value
        if row[0].value == None:
            break
    elif set_of_sentences != []:
        test_sent.append(copy.deepcopy(set_of_sentences))
        set_of_sentences = []



output = open('zz_claims.pkl', 'wb')
pickle.dump(test_sent, output)
output.close()
