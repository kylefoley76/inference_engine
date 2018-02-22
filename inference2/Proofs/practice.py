

from radon.raw import analyze
# import natural_language
# import importlib.machinery
import os

temp_directory = '/Users/kylefoley/PycharmProjects/inference_engine2/inference2/ancient/temp.py'

b = os.path.exists(temp_directory)



bb = 8

# from random import choice
# from collections import deque
import collections
from collections import Counter
# import time
# import heapq
# from operator import itemgetter
# from itertools import groupby
# from collections import ChainMap
# from collections import namedtuple
from collections import defaultdict
# import numpy
import copy
import re
import json
from json import JSONEncoder
# import jsonpickle

# import pickle
# import os
# from pprint import pprint
#
# import pandas as pd
#
# from openpyxl import load_workbook
# from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
# from openpyxl.styles import Fill, Color
# # from openpyxl.styles import style
# from openpyxl.styles.colors import RED
# from openpyxl.styles.colors import GREEN


bb = 8
# !/usr/bin/python
class Parent:        # define parent class
   parentAttr = 100
   def __init__(self):
      print ("Calling parent constructor")

   def parentMethod(self):
      print ('Calling parent method')

   def setAttr(self, attr):
      Parent.parentAttr = attr

   def getAttr(self):
      print ("Parent attribute :", Parent.parentAttr)

class Child(Parent): # define child class
   def __init__(self):
      print ("Calling child constructor")

   def childMethod(self):
      print ('Calling child method')

c = Child()          # instance of child
c.childMethod()      # child calls its method
c.parentMethod()     # calls parent's method
c.setAttr(200)       # again call parent's method
c.getAttr()

for x in range(1, 100):
    y = x / 3
    z = x / 5

    if x % 3 == 0 and x % 5   == 0:
        print ('fizzbuzz')



    elif isinstance(y, int):
        print ('buzz')
    elif isinstance(z, int):
        print ('fizz')
    else:
        print (str(x))

bb = 8

# import jsonpickle

class hey:
    x = 1

whats_up = hey()
#
# pickled = jsonpickle.encode(whats_up)
#
# with open("whats_up.json", "w") as fp:
#     json.dump(pickled, fp)
#
# with open("whats_up.json", "r") as fp:
#     hey_man = json.load(fp)
#
# hey_man = jsonpickle.decode(hey_man)
#
# class encoder(JSONEncoder):
#     def default(self, o):
#         return o.__dict__
#
# hey2 = encoder().encode(whats_up)
#
# with open("whats_up.json", "w") as fp:
#     json.dump(hey2, fp)

#
# json.dumps(cls=encoder)
#



bb = 8





def hey(c):

    class c5(object):
        x = []
        x.append(1)

    c5.x.append(c)

    return c5



class c1(object):
    x = []
    x.append(1)


class c6(object):
    def __init__(self, n):
        self.x = []
        self.x.append(n)




d = hey(3)
d.x.append(4)
e = d.x

f = c6(5)
f.g = {}
f.g.update({'h':3})
j = f.g.get('h')
b = c1()
b.x.append(2)
a = c1()
a.x.append(5)
c = c1()
c.x.append(6)


class c7(object):
    a = []
    b = []

    def __init__(self, c, d):
        self.a = c
        self.b = d

g = c7(a, b)
h = c7(a, b)
h.y = 24


d = b.x

b = [1,2,3,4,5]
c = slice(20,32)


####### counter objects can be added

b = collections.Counter([1,2,3,3,4,2,1,])
c = collections.Counter([1,4,5,5,4,2,1,])

d = b + c
bb = 8




########### a study of json

#
# list1 = [[[1,2]], [2,3]]
# list2 = list1
# list3 = [list1, list2]
# list4 = copy.deepcopy(list3)
# list4[0][0][0][0] = 4
# list5 = json.loads(json.dumps(list3))
# list5[0][0][0][0] = 4
#
# # b = list5[0][1][0][0]
# # c = list4[0][1][0][0]
#
# with open('json_dict/list4.json', 'w') as f:
#     json.dump(list4, f)
#
# with open('json_dict/list4.json') as f:
#     list6 = json.load(f)
#
# list6[0][0][0][0] = 7
#
# b = list6[0][0][0][0]
#
# with open('json_dict/list4.json') as f:
#     list7 = json.load(f)
#
# c = list7[0][0][0][0]
#
# print (b)
# print (c)

#####################


c = 8

def fibonacci(n):
    curr = 1
    prev = 0
    counter = 0
    while counter < n:
        yield curr
        prev, curr = curr, prev + curr
        counter += 1


b = next(fibonacci(21))
c = next(fibonacci(21))

#
# cond_r = chr(8835)
# top = chr(8868)
# bottom = chr(8869)
# c = "c"
# cond_r = chr(8835)
# consist = "\u2102"  # consistency
# top = chr(8868)
# bottom = chr(8869)
# neg = chr(172)
# idd = chr(8781)  # translation symbol
# iff = chr(8801)
# mini_c = chr(8658)
# mini_e = chr(8703)
# implies = chr(8866)
# conditional = chr(8594)
# nonseq = chr(8876)
# xorr = chr(8891)
# idisj = chr(8744)
# cj = chr(8896)
# aid = chr(8776)
# disj = chr(8855)
# equi = chr(8660)

################# regular expressions ##############



## the deque method lets you populate a list from the left or the right


def get_lines(list1, functions2, file_name):
    lines = []
    subroutine = file_name
    for i, line in enumerate(list1):

        if line.startswith("def "):

            functions2.update({subroutine: copy.deepcopy(lines)})
            subroutine = line[line.index(" "):line.index("(")]
            subroutine = subroutine.strip()
            lines = []

        lines.append(line)
    functions2.update({subroutine: copy.deepcopy(lines)})
    return



new_functions2 = {}
old_functions2 = {}


all_new_lines = [line for line in ['a', "def hey(m", 'b', 'c']]
all_old_lines = [line for line in ['a',"def hey(m", 'b']]

get_lines(all_new_lines, new_functions2, "new")
get_lines(all_old_lines, old_functions2, "old")


bb = 8



if not re.search(r'\S', "   "):
    bb = 8


if re.search(r'\w', "b"):
    bb = 8

#
# if re.search(cond_r + "|" + chr(8868) + "|&", "bc" + iff):
#     print (True)

#### the ^ denotes that the word must start with that set of characters
if re.search(r'^hey', 'heyz'):
    print (True)

#### the $ denotes that the word must end with that set of characters
if re.search(r'hey$', 'aahey'):
    print (True)

#### the period is a wild card
if re.search(r'he.y', 'hezyz'):
    print (True)

#### use re.I to ignore case
if re.search(r'he','HE', re.I):
    print ("HE")


b = re.sub(r'[()\s]', "","(b R c)")
print (b)


# the star removes any number of characters
# Delete Python-style comments
phone = "2004-959-559 # This is Phone Number"
num = re.sub(r'#.*$', "", phone)
print ("Phone Num : ", num)


#newline. By passing re.DOTALL as the second argument to re.compile(), you can make
# #the dot character match all characters, including the newline character.





b = re.findall(r'(P\w+)', 'Pey Pou man')
print (b)

b = re.findall(r'(Pa(ey){2}\w+)', 'Paeyeyeyrr Paeyeyz Pag Pfg')
# print (b)






# str1 = "ada"
# if one_sentence2(str1):
#     print (True)

one_sentence2 = lambda x: re.search(r'b|c|d', x)
if re.search(chr(8868), 'aP' + chr(8868)):
    print (True)
if re.search(r'e(df)c', 'abf cdd eff'):
    print ('true')

b = re.findall(r'(e|c\w)', 'abf cdd eff')
print (b)



b = re.sub(r'(\w+) (\w+) (\w+)', r'\3 \1 \2',"hey you man")
print (b)
# b = re.sub(r'(\w+)','\\3\\2\\1',"hey you man")

# the following converts YYYY-MM_DD to DD-MM-YYYY
b = re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', "2004-05-16")


b = re.search(r'\d{4}\/\d{0,1}\/\d{0,1}?','www.hey.com/2017/4/15')


str1 = 'hey and |c you what is that youdoing how are you'
list1 = str1.split(" & ")
for c in re.finditer(" and ", str1):
    b = c.start()
    a = c.end()


b = re.search(r'it3', '1udit3 ueen heyght78_')

c = list(b.span())

b = re.findall(r' \b(g)+ \b', '1udit3 ueen heyght78_')

b = re.findall(r'\b(?=\d)\w+ \b', '1uit 3ueen heyght78_')

# the following finds any word containing only letter, numbers and underscores
#this doesn't work
#b = re.findall(r'^[a-zA-Z0-9_]+$', 'ahz2gb_ $f heyght78_')
# c = b.group()
b = re.findall(r'(?<!\S)\w+(?!\S)', 'ahz2gb_ $f heyght78_')

# picks out queen
b = re.findall(r'\b(?=qu)\w{4}n \b', 'quit queen heyght78_')

#b = re.findall(r'^[a-zA-Z0-9_ ]+$', 'ahz2gb_ $f heyght78_')[0].split(' ')

# the following picks out 'tag', 'tag', 'end'
b = re.findall(r"(?<=id\d:)(\b\w*\b)", "begin:id1:tag:id2:tag:id3:end")


b = re.findall(r'\b7\w+\b','7gh ghj 7ui')


# # the following is meant to be false
if re.search(r'^[^z]\w*z[^z]+$','ahzgb heyz'):
    print ('false')
else:
    print ('true')


#
# b = re.findall(r'\w*z\w*','ahzgb hzey 7gh')
# c = b.group()


b = re.search(r'^\w+','ahgb 675')
c = b.group()



b = re.search(r'^[A-Z]+.*_[a-z]+$','A4_dce')
b = b.group()



# Remove anything other than digits
num = re.sub(r'\D', "", phone)
print ("Phone Num : ", num)


bb = 8
b = re.compile( r'^a(b){4}')
c = b.search('abbbb')
c = c.group()

bb = 8

# question 35

b = re.compile( r'[^aeiouAEIOU]')
c = b.findall(' RoboCop eats baby food. BABY FOOD.')



# question 34

b = re.compile( r'\d+\s\w+')
c = b.findall(' 12 drummers, 11 pipers, 10 lords, 9 ladies, 8 maids, 7 swans, 6 geese, 5 rings, 4 birds, 3 hens, 2 doves, 1 partridge')



# question 33

b = re.compile( r'\d\d\d-\d\d\d-\d\d\d\d') # has groups > > >
c = b.findall('Cell: 415-555-9999 Work: 212-555-0000')



# question 32

b = re.compile( r'(\d\d\d)-(\d\d\d)-(\d\d\d\d)') # has groups > > >
c = b.findall('Cell: 415-555-9999 Work: 212-555-0000')



# question 31


c = re.compile(r'(bat(wo){1,4}?man)')
d = c.search('i like batwowoman and batwowowowoman')
b = d.group()
print (b)



# question 30

c = re.compile(r'(bat(wo){1,4}man)')
d = c.search('i like batwowoman')
b = d.group()
bb = 8



# question 29

c = re.compile(r'(bat(wo)+man)')
d = c.search('i like batwowoman')
b = d.group()




# question 28

c = re.compile(r'(bat(wo)*man)')
d = c.search('i like batwowoman')
b = d.group()



# question 26

c = re.compile(r'(bat(wo)?man)')
d = c.search('i like batman')
b = d.group()
bb = 8


phoneNumRegex = re.compile( r'(\(\d\d\d\)) (\d\d\d-\d\d\d\d)')

# question 22

phoneNumRegex = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
c = phoneNumRegex.search(' My number is 415-555-4242.')
b = c.group()


# question 23

phoneNumRegex = re.compile( r'(\d\d\d)-(\d\d\d-\d\d\d\d)')
c = phoneNumRegex.search(' My number is 415-555-4242.')
b = c.groups()
d = c.group(2)


phoneNumRegex = re.compile( r'(\(\d\d\d\)) (\d\d\d-\d\d\d\d)')
b = phoneNumRegex.search(' My phone number is (415) 555-4242.')
c = b.group(1)

# question 24

heroRegex = re.compile (r'Batman|Tina Fey')
b = heroRegex.search(' BatmanandTina Fey.')
c = b.group()

# question 25

batRegex = re.compile( r'Bat(man|mobile|copter|bat)')
mo = batRegex.search(' Batmobile lost a wheel')
b = mo.group()
c = mo.group(1)


b = 'asdf fjdk; afed, fjek,asdf, foo'
a = re.split(r'[;,\s]\s*', b)




b =  re.search(r'\w\w', 'hh')
c = str(b)



lst = [1,2,3,4,5,6,7,8]
low = 2
high = 5
lst1 = list(filter(lambda x: low<=x <high, lst))

bb = 8



# don't understand that point of nums as the second argument in the lambda function
nums = range(2, 50)
for i in range(2, 8):
    nums = filter(lambda x: x == i or x % i, nums)
b = list(nums)
bb = 8


# question 7
a = [1,2,3,5,7,9]
b = [2,3,5,6,7,8]
g = filter(lambda x: x in a, b)  # prints out [2, 3, 5, 7]




# b = input('enter the number: ')
# if b =='1':
#     print ('hey')

#
# sentence = """At eight o'clock on Thursday morning
# ... Arthur didn't feel very good."""
#
# tokens = nltk.word_tokenize(sentence)
#
# mydict = {'a': 1, 'b': 2, 'c': 3}
# output = open('myfile.pkl', 'wb')
# pickle.dump(mydict, output)
# output.close()

list1 = ['a','n','d']





list1 = [[1],[2],[3]]
list2 = [[4],[5]]

list1.append(list2)


list5 = [5] * 8
list4 = [4,5,6] * 4
list3 = [3,4,5,6,7] * 2
list1 = [x for x in range(1,10)]
list6 = list1 + list3 + list4 + list5




#
# list7 = []
# for i in range(1,145):
#     c = choice(list6)
#     list7.append(c)
#
# a = Counter(list7)
bb = 8
#
# def remove_violations(key, value, last_72_numbers, freq_table, add_to_list = False):
#
#     if key == 1 or key == 2 or key == 8 or key == 9:
#         min = 3
#         max = 12
#     elif key == 3 or key == 7:
#         min = 6
#         max = 24
#     elif key == 4 or key == 6:
#         min = 12
#         max = 48
#     elif key == 5:
#         min = 24
#         max = 96
#
#     rule_violated = False
#
#     if value < min:
#         if add_to_list:
#             g = min - value
#             for n in range(1, g + 1):
#                 last_72_numbers.append(key)
#         rule_violated = True
#     elif value > max:
#         if add_to_list:
#             g = value - max
#             for n in range(1, g + 1):
#                 last_72_numbers = list(last_72_numbers)
#                 last_72_numbers.remove(key)
#                 last_72_numbers = deque(last_72_numbers)
#         rule_violated = True
#
#     return rule_violated
#
#
# the_9_digits = [x for x in range(1,10)]
# random_numbers = []
# last_72_numbers= deque(maxlen = 144)
#
#
# for i in range(1,145):
#     random_number = choice(list6)
#     last_72_numbers.append(random_number)
#     random_numbers.append(random_number)
#
#
# frequency_table = Counter(random_numbers)
# last72_list = list(last_72_numbers)
#
# rule_violated = True
# i = 0
# while rule_violated:
#     i += 1
#     for k, v in frequency_table.items():
#         rule_violated = remove_violations(k, v, last_72_numbers, frequency_table, True)
#         if rule_violated:
#             last72_list = list(last_72_numbers)
#             frequency_table = Counter(last72_list)
#             break
#
#
#
# preliminary_last_72 = copy.copy(last_72_numbers)
# random_numbers = []
#
# for z in range(0,300):
#     random_number = choice(the_9_digits)
#     preliminary_last_72.append(random_number)
#     prelim_last_72_list = list(preliminary_last_72)
#     prelim_frequency = Counter(prelim_last_72_list)
#     for k, v in prelim_frequency.items():
#         rule_violated = remove_violations(k, v, last_72_numbers, prelim_frequency, True)
#         if rule_violated:
#             break
#     else:
#         last_72_numbers.append(random_number)
#         random_numbers.append(random_number)
#
#
#
#
# bb = 8
#



#
#
# for z in range(0,6):
#
#
#     list7 = []
#     for i in range(1,300):
#         c = choice(list6)
#         list7.append(c)
#
#     last_num = 0
#     d = {}
#     k = 0
#     for i, j in enumerate(list7):
#         if i > 1:
#             last_num = list7[i - 1]
#             if last_num == j:
#                 k += 1
#             elif k > 1:
#                 d.setdefault(last_num, []).append(k)
#                 k = 0
#             else:
#                 k = 0
#     in_a_row.append(d)
# t = deque(maxlen = 8)
# s = deque(maxlen = 4)
# q = deque(maxlen = 3)
# r = deque(maxlen = 2)
# list3 = []
# list1 = [x for x in range(1,11)]
# for b in range(0,500):
#     c = choice(list1)
#     q.append(c)
#     r.append(c)
#     s.append(c)
#     t.append(c)
#     d = sum(q)
#     e = sum(r)
#     f = sum(s)
#     g = sum(t)
#     if g > 37 and g < 43 and len(t) == 8:
#         list3.append(c)
#     # if e > 7 and e < 14 and len(list1) > 2:
#     #     if d < 19 and d > 12:
#     #         if f < 26 and f > 15:
#     #             list3.append(c)


#
#
# a = Counter(random_numbers)
# a = {key:a[key] for key in sorted(a.keys())}
#
# b = numpy.std(list3,axis=0)
#
# wb4 = load_workbook('/Users/kylefoley/Desktop/inference engine/temp_proof.xlsx')
# w4 = wb4.worksheets[0]
#
# p = 0
# for k, v in a.items():
#     p += 1
#     w4.cell(row=p+1, column=4).value = k
#     w4.cell(row=p + 1, column=5).value = v
#
# wb4.save('/Users/kylefoley/Desktop/inference engine/temp_proof.xlsx')
#
# bb = 8
#

#
# xls_cell = w4['b1']
#
# xls_cell.style = Style(fill=PatternFill(patternType='solid'
#     , fgColor=Color('C4C4C4')))
#
# xls_cell.font = xls_cell.font.copy(color  = 'FFFF0000')
#
# wb4.save('/Users/kylefoley/Desktop/inference engine/temp_proof.xlsx')







# question 27

list2 = [1,2,3]
list1 = [3,4,5]
list1 = list2

list1.append(3)

list1 = [5,4]




def get_right_most_connective(str1):
    split_at_space = False
    if len(str1) > 67:
        j = 67
    else:
        j = len(str1) - 1
    for i in range(j, 15, -1):
        if str1[i] == "":
            return i
        if i == 31:
            split_at_space = True
        if split_at_space and str1[i] == " ":
            return i


def space_sentences(str1, str2):

    b = len(str1)
    c = len(str2)
    j = 0
    list2 = []

    if (b + c) > 70:
        location = get_right_most_connective(str1)
        first = str1[:location]
        second = str1[location:]
        if len(second) > 70:
            j += 1
            list1 = space_sentences(second, str2)
            for sent in list1:


                str2 = ""

        spaces_needed = 65 - (len(second) + len(str2))
        space = " " * spaces_needed
        second = "     " + second + space + str2
    else:
        spaces_needed = 70 - (len(str1) + len(str2))
        space = " " * spaces_needed
        first = str1 + space + str2


    return list2



str1 = '''the longest sentence you can every imagine or even thin about
    that is what i'm talking man and don't mistake anything for everything
    because that it the way things are going to be from now on
    sucka even if you don't like it don't try to pretend like you know something
    because you don't '''

str2 = 'SUB 4,5'





def a(list1):
    list1.append(6)

b = a(list1)

b = list1



bb = 8



#
# # question 21
# a = ['hey','you','beu']
# b = any(c.endswith('u') for c in a)
#
# a = namedtuple('Stock', ['name', 'shares', 'price'])


bb = 8

# import send2trash

b = '11'

#
#
# a = {'x': 1, 'z': 3 }
# b = {'y': 2, 'z': 4 }
# c = ChainMap(a,b)
#
# values = ChainMap()
# values['x'] = 1
# # Add a new mapping
# values = values.new_child()
# values['x'] = 2
# # Add a new mapping
# values = values.new_child()
# values['x'] = 3
#
# ChainMap({'x': 3}, {'x': 2}, {'x': 1})
# b = values['x']
#
# # Discard last mapping
# values = values.parents
# b = values['x']
#
# # Discard last mapping
# values = values.parents
# b = values['x']
# b = values
# ChainMap({'x': 1})
#
#
#
# bb = 8
#
# # question 19
#
# b = {
#        'ACME': 45.23,
#        'AAPL': 612.78,
#        'IBM': 205.55,
#        'HPQ': 37.20,
#        'FB': 10.75}
#
# a = [key for key, value in b.items() if value == 205.55][0]
#
# bb = 8
#
# a = { key:value for key, value in b.items() if value > 200 }
#
#
# dict1 = {
#        'ACME': 45.23,
#        'AAPL': 612.78,
#        'IBM': 205.55,
#        'HPQ': 37.20,
#        'FB': 10.75}
#
#
# obj = {'b': 2}
#
#
# #question 17
# bb = 8
# c = [
#        'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
#        'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
#        'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
#        'my', 'eyes', "you're", 'under']
#
#
# a = Counter(c)
# b = a.most_common(3)
#
#
# # question 18
#
# a = [
#         {'address': '5412 N CLARK', 'date': '07/01/2012'},
#         {'address': '5148 N CLARK', 'date': '07/04/2012'},
#         {'address': '5800 E 58TH', 'date': '07/02/2012'},
#         {'address': '2122 N CLARK', 'date': '07/03/2012'},
#         {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
#         {'address': '1060 W ADDISON', 'date': '07/02/2012'},
#         {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
#         {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},]
#
# a.sort(key=itemgetter('date'))
#
# for date, items in groupby(a, key=itemgetter('date')):
#     print(date)
#     for i in items:
#         print(' ', i)
#
#
# # question 19
#
# c = [date for date, items in groupby(a, key=itemgetter('date'))]
#
#
# a = (1, 4, -5, 10, -7, 2, 3, -1)
#
# b = [n for n in a if n > 0]
#
#
#
# a = {'a':1,"b":2}
#
# a = {k:v for k,v in ([("c",3)]+list(a.items()))}
#
#
#
# #question 16
# a = [1, 5, 2, 1, 9, 1, 5, 10]
# a = list(set(a))
#
#
#
#
# list1 = ['f','g','r']
#
# list2 = []
#
# list2 = [list2.append(x) for x in list1]
#
# for x in list1:
#     list2.append(x)
#
#
#
#
#
# b = [1,2]
# c = [2,3]
#
#
#
# q = deque(maxlen = 3)
# j = [1,2,3,4,5]
# for i in j:
#     q.append(i)
# b = heapq.nlargest(3,j)
# c = heapq.nsmallest(3,j)
#
#
# # question 10
# j = [3,4,2,7,4,9]
# k = sorted(j[1:4])
# m = sorted(j)[1:4]
# b = 88
#
#
# #
# #
# # def search(lines, pattern, history=3):
# #     previous_lines = deque(maxlen=history)
# #     for line in lines:
# #         if pattern in line:
# #             yield line, previous_lines
# #         previous_lines.append(line)
# # #
# # if __name__ == '__main__':
# #     with open('/Users/kylefoley/Desktop/hey.txt') as f:
# #         for line, prevlines in search(f, 'hey', 3):
# #             for pline in prevlines:
# #                 print(pline, end="")
# #             print(line, end="")
# #             print('-'*20)
# #
#
#
#
# jim = {'hey':2,'you':3}
#
#
# names = ['hey','you','there']
# names2 = ['what','are', 'you']
#
#
#
#
#
#
#
# #x = nums
#
# b = [1,2,3,4,5,6,7]
# c = ['hey','you','man','what']
# while c:
#     f = c.pop()
#
#
# # answer to question 1
# g = sum(x*x for x in range(10))
#
#
#
# # f = 7 ms, e = 19 ms
# # don't understand
# def updown(N):
#     for x in range(1, N):
#         yield x
#     for x in range(N, 0, -1):
#         yield x
# #
# # def updown2(N):
# #     yield from range(1, N)
# #     yield from range(N, 0, -1)
# #
# # for i in updown2(3): print(i)
#
#
# for i in updown(3): print(i)
#
# # don't understand
# def frange(start, stop, stride=1.0):
#     while start < stop:
#         yield start
#         start += stride
#
# b = frange(3,6)
#
#
#
#
#
#
#
#
#
# # question 2
# dict1 = {}
# dict1 = dict1.fromkeys('hello',2)
# a = b = c = 0
#
#
# x = 7_000_000
# x += 8
# y = 8
# x,y = y,x
# print('after: x = %d,y = %d' % (x,y))
#
# print('I have %d apples' % (x))
#
# keys = 'guido sarah barry'.split()
#
#
# # don't understand
# hashes = list(map(abs,map(hash,keys)))
#
#
#
#
# # answer to question 4
# y = 9//5
# x = 9/5
#
#
# # answer to question 5
# def fahrenheit(T):
#     return ((float(9)/5)*T + 32)
# def celsius(T):
#     return (float(5)/9)*(T-32)
# temp = (36.5, 37, 37.5,39)
#
#
# F = map(fahrenheit, temp)
# C = map(celsius, F)
# g = list(F)
#
# def plus(x):
#     return x + 2
#
#
# list1 = [1,2,3]
#
# g = list(map(plus,list1))
# x = 1
#
# # answer to question 6
#
# primary_colors = ['red','blue','green']
# colors = ['red','yellow','orange']
#
# def isprimary(str1):
#     if str1 in primary_colors:
#         return True
#     else:
#         return False
#
# g = list(filter(isprimary,colors))
#
#
#
#
# nums = range(2,50)
#
# z = time.time()
#
#
#
# # question 8
# x = 2**3
#
# # question 13
#
#
# d = defaultdict(list)
# d['a'].append(1)
# d['a'].append(2)
# d['b'].append(4)
#
# # question 14
# d = {
#        'ACME': 45.23,
#        'AAPL': 612.78,
#        'IBM': 205.55,
#        'HPQ': 37.20,
#        'FB': 10.75}
#
# x = list(zip(d.values(), d.keys()))
#
# x = max(zip(d.values(), d.keys()))
#
#
# # question 20
#
# b = [
#        {'name':'GOOG', 'shares': 50},
#        {'name':'YHOO', 'shares': 75},
#        {'name':'AOL', 'shares': 20},]
#
#
# a = min(s['shares'] for s in b)
#
# bb = 8
#
#
#
# # question 15
# a={
# 'x' : 1,
# 'y' : 2,
# 'z' : 3 }
#
# b={
# 'w' : 10,
# 'x' : 11,
# 'y' : 2 }
#
# x = a.keys() & b.keys()
# c = a.keys() - b.keys()
#
#
#
#
#
# colors = ['red','gre','yel','green']
# names = ['bob','meg','jess',"jake"]
# # question 11
#
# d = {}
# for color in colors:
#     key = len(color)
#     d.setdefault(key,[]).append(color)
#
#
# # question 12
#
# for color in sorted(colors, reverse = True):
#     print (color)
#
# for color in reversed(sorted(colors)):
#     print (color)
#
#
#
# class FibIterable:
#     """
#     this class is a generates a well known sequence of numbers
#     """
#     def __init__(self,iLast=1,iSecondLast=0,iMax=50):
#         self.iLast = iLast
#         self.iSecondLast = iSecondLast
#         self.iMax = iMax  #cutoff
#     def __iter__(self):
#         return self    # because the object is both the iterable and the itorator
#     def next(self):
#         iNext = self.iLast + self.iSecondLast
#         if iNext > self.iMax:
#             raise StopIteration()
#         self.iSecondLast = self.iLast
#         self.iLast = iNext
#         return iNext
# #
# # o = FibIterable()
# # for i in o:
# #     pass
# #     # print(i)
#
#
#
# import collections
#
# Card = collections.namedtuple('Card', ['rank', 'suit'])
#
# class FrenchDeck:
#     ranks = [str(n) for n in range(2, 11)] + list('JQKA')
#     suits = 'spades diamonds clubs hearts'.split()
#     def __init__(self):
#         self._cards = [Card(rank, suit) for suit in self.suits
#                                         for rank in self.ranks]
#     def __len__(self):
#         return len(self._cards)
#     def __getitem__(self, position):
#         return self._cards[position]
#
#
# deck = FrenchDeck()
# b = choice(deck)
#
# c = Card("Q",'hearts') in deck
#
#
#
# suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
# def spades_high(card):
#     rank_value = FrenchDeck.ranks.index(card.rank)
#     return rank_value * len(suit_values) + suit_values[card.suit]
#
# for card in sorted(deck, key=spades_high): # doctest: +ELLIPSIS ... print(card)
#     b = card
#
bb = 8