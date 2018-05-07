import pickle, re
import json

get_words_used = 0

cond_r = chr(8835)
consist = "\u2102"  # consistency
top = chr(8868)
bottom = chr(8869)
neg = chr(172)
idd = chr(8781)  # translation symbol
iff = chr(8801)
mini_c = chr(8658)
mini_e = chr(8703)
implies = chr(8866)
conditional = chr(8594)
cond_conn = [conditional, implies]
refers = chr(8701)
nonseq = chr(8876)
xorr = chr(8891)
idisj = chr(8744)
cj = chr(8896)
aid = chr(8776)
jiff = chr(10231) # justified biconditional
cond_conn = [iff, jiff]
disj = chr(8855)
equi = chr(8660)
ne = "\u2260"  # not equal

l1 = "\u2081"
l2 = "\u2082"
l3 = "\u2083"
l4 = "\u2084"
l5 = "\u2085"
l6 = "\u2086"
l7 = "\u2087"
ua = "\u1d43"
ub = "\u1d47"
uc = "\u1d9c"
ud = "\u1d48"
ue = "\u1d49"
uf = "\u1da0"
ug = "\u1d4d"
ui = "\u2071"
uk = "\u1d4f"
um = "\u1d50"
un = "\u207f"
uo = "\u1d52"
up = "\u1d56"
ut = "\u1d57"
uv = "\u1d5b"
uu = "\u1d58"
uw = "\u02b7"
uy = "\u02b8"
uj = "\u02B2"
ul = "\u02E1"
ur = "\u02b3"
us = "\u02e2"
uh = "\u02b0"


superscripts = [ua, ub, uc, ud, ue, uf, ug, ui, uj, uk, ul, um, un, uo,
                up, ur, us, ut, uu, uw, uv, uy, uh]

superscript_dict = {
ua:"a",
ub:"b",
uc:"c",
ud:"d",
ue:"e",
uf:"f",
ug:"g",
uh:"h",
ui:"i",
uj:"j",
uk:"k",
ul:"l",
um:"m",
un:"n",
uo:"o",
up:"p",
ur:"r",
us:"s",
ut:"t",
uu:"u",
uv:"v",
uw:"w",
uy:"y"}

subscripts = [l1, l2, l3, l4]
alpha = chr(945)
beta = chr(946)
delta = chr(948)

parts_of_speech_dict = {
    'd': 'determiner',
    'm': 'negator',
    'n': 'noun',
    'a': "adjective",
    'o': 'possessor',
    's': 'possessor',
    'u': 'relative pronoun',
    'y': 'relative pronoun',
    'c': 'and coordinator',
    'r': 'relation',
    'p': 'noun',
}




name_slots = {
    8: "sent abbrev",
    9: "mini e",
    149: "negation of 61",
    61: "det of 10",
    134: "possessor of 10",
    76: "adj of 10",
    10: "sub",
    91: "instance of 10",
    106: "relative pronoun of 10",
    132: "coordinator of 11",
    150: "negation of 62",
    62: "det of 11",
    135: "possessor of 11",
    77: "adj of 11",
    11: "sub2",
    92: "instance of 11",
    107: "relative pro of 11",
    12: "neg",
    13: "rel",
    151: "negation of 63",
    63: "det of 14 ",
    136: "possessor of 14",
    78: "adj of 14",
    14: "obj",
    93: "instance of 14",
    108: "relative pro of 14",
    133: "coordinator of 15",
    152: "negation of 64",
    64: "det of 15",
    137: "possessor of 15",
    79: "adj of 15",
    15: "obj2",
    94: "instance of 15",
    109: "relative pro of 15",
    16: "obj3",
    17: "obj4",
    18: "obj5",
    19: "obj 6",
    121: "negation of 20",
    20: "rel 2",
    153: "negation of 65",
    65: "det of 21",
    138: "possessor of 21",
    80: "adj of 21",
    21: "obj of 2",
    95: "instance of 21",
    110: "relative pro of 21",
    122: "negation of 22",
    22: "rel 3",
    154: "negation of 66",
    66: "det of 23",
    139: "possessor of 23",
    81: "adj of 23",
    22: "obj of 3",
    96: "instance of 23",
    111: "relative pro of 23",
    123: "negation of 24",
    24: "rel 4",
    155: "negation of 67",
    67: "det of 25",
    140: "possessor of 25",
    82: "adj of 25",
    25: "obj of 4",
    97: "instance of 25",
    112: "relative pro of 25",
    124: "negation of 26",
    26: "rel 5",
    156: "negation of 68",
    68: "det of 27",
    141: "possessor of 27",
    83: "adj of 27",
    27: "obj of 5",
    98: "instance of 27",
    113: "relative pro of 27",
    125: "negation of 28",
    28: "rel 6",
    157: "negation of 69",
    69: "det of 29",
    142: "possessor of 29",
    84: "adj of 29",
    29: "obj of 6",
    99: "instance of 29",
    114: "relative pro of 29",
    126: "negation of 30",
    30: "rel 7",
    158: "negation of 70",
    70: "det of 31",
    143: "possessor of 31",
    85: "adj of 31",
    31: "obj of 7",
    100: "instance of 31",
    115: "relative pro of 31",
    127: "negation of 32",
    32: "rel 8",
    159: "negation of 71",
    71: "det of 33",
    144: "possessor of 33",
    86: "adj of 33",
    33: "obj of 8",
    101: "instance of 33",
    116: "relative pro of 33",
    128: "negation of 34",
    34: "rel 9",
    160: "negation of 72",
    72: "det of 35",
    145: "possessor of 35",
    87: "adj of 35",
    35: "obj of 9",
    102: "instance of 35",
    117: "relative pro of 35",
    129: "negation of 36",
    36: "rel 10",
    161: "negation of 73",
    73: "det of 37",
    146: "possessor of 37",
    88: "adj of 37",
    37: "obj of 10",
    103: "instance of 37",
    118: "relative pro of 37",
    130: "negation of 38",
    38: "rel 11",
    162: "negation of 74",
    74: "det of 39",
    147: "possessor of 39",
    89: "adj of 39",
    39: "obj of 11",
    104: "instance of 39",
    119: "relative pro of 39",
    131: "negation of 40",
    40: "rel 12",
    163: "negation of 75",
    75: "det of 41",
    148: "possessor of 41",
    90: "adj of 41",
    41: "obj of 12",
    105: "instance of 41",
    120: "relative pro of 41",
}

hypo_counter = 0

nine_blanks = [""] * 9

not_blank = lambda x: x != None and x != "" and x != " "

build_contradiction2 = lambda x: x + " & ~" + x

remove_duplicates_sd = lambda x: list(set(x))

strip_sent = lambda x: re.sub(r'[()~ ]', "", x)

name_sent = lambda x, y: y[strip_sent(x)]

one_sentence = lambda x: not re.search(xorr + "|" + implies + "|" + iff + "|" + idisj
                                       + "|" + jiff +
                                       conditional + "|&|#", x)

# x and y are the same in the following:
nbuild_sent = lambda x, y: "(" + " ".join(list(map(lambda x: y[x], y[54]))) + ")"

# the second one is used when we want to build a sentence stripped of its negation sign
nbuild_sent2 = lambda x, y, z: "(" + " ".join(list(map(lambda x: y[x], z))) + ")"

build_connection = lambda x, y, z: x + " " + y + " " + z

build_conjunction = lambda x: "(" + " & ".join(x) + ")"

build_lemma = lambda x, y: x + "." + y

pos_counterpart = lambda x, y, z: x[y.index(z)]

decimal_numbers2 = lambda x: str("{0:.2f}".format(x))

decimal_numbers5 = lambda x: str("{0:.5f}".format(x))

decimal_numbers3 = lambda x: str("{0:.3f}".format(x))

hprop = lambda x: len(x) > 1 and x[0] in ['H', "W"] and x[1].islower()

is_concept = lambda x, y, z: z.get(y) if x in ["I", "J", "V"] else None

pair = lambda x, y, z: z.join(sorted([x, y]))

isrelat = lambda x: x.isupper() or x in ["\\", "/", "+", "-", "=", refers]

standard_nouns = [8, 10, 11, 14, 15, 16, 17, 18, 19, 21, 23, 25, 27, 29,
                  31, 33, 35, 37, 39, 41]

greek_nouns = [chr(946 + x) for x in range(len(standard_nouns))]

sent_pos_name = {10: "s", 11: "t", 14: "o", 15: "b", 16: "c", 17: "d",
              18: "e", 19: "f", 21: "g", 8: "p"}

modifiable_nouns = [10, 11, 14, 15, 21, 23, 25, 27, 29,
                    31, 33, 35, 37, 39, 41]

negative_positions = [12] + [x for x in range(121, 132)]

relational_positions = [13] + [x for x in range(20, 41, 2)]

adjective_positions = [x for x in range(76, 91)]

adj_to_pred_complement = {78:14, 79:15, 80:21, 81:23}

determinative_positions = [x for x in range(61, 76)]

determiner_dict = {61: 10, 63: 14, 64:15, 65: 21, 66: 23}

instantial_nouns = [x for x in range(91, 106)]

possessor_positions = [x for x in range(134, 148)]

relational_positions2 = [x for x in range(20, 41, 2)]

relative_pronoun_positions = [x for x in range(106, 121)]

slot_order = list(name_slots.keys())

determ_and_adj = determinative_positions + adjective_positions

the_is_of_group = ["I", "is" + ug, "are" + ug, "be" + ug, "was" + ug, "were" + ug,
                   "am" + ug]

the_is_of_adjective = ["J", "is" + ua, "be" + ua, "are" + ua, "was" + ua,
                       "am" + ua, "were" + ua]

spec_rel = the_is_of_adjective + the_is_of_group

special_connectives = [iff, conditional, xorr, idisj, "#"]

all_connectives = special_connectives + [implies, nonseq, "&"]

conditionals = [conditional, iff, "#"]

