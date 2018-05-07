
try:
    from settings import *
except:
    from .settings import *


class mem_reduced_def1(object):
    def __init__(self, tsentences, def_stats1):
        self.sentences = tsentences
        self.disjuncts = []
        self.embeds = {}
        self.def_stats = def_stats1


class def_stats(object):
    def __init__(self, definiendum, num):
        self.def_word = definiendum
        self.def_word_num = definiendum + str(num)
        self.ant_index = []
        self.con_index = []
        self.flat_ant_index = []
        self.flat_con_index = []
        self.ant_comp_const = []
        self.con_comp_const = []
        self.ant_comp_greek = []
        self.con_comp_greek = []
        self.instance = []
        self.entailments = []
        self.embedded_conditionals = {}
        self.arity = []
        self.natural_disjuncts = []
        self.isdisjunctive = []
        self.greek_disjuncts = []
        self.already_instantiated = False
        self.now_disjunctive = False
        self.perfect_disjunct = False
        self.ant_hnum = ""
        self.con_hnum = []
        self.ant_greek = ""
        self.con_greek = ""
        self.tot_greek_sent = ""
        self.concept = ""
        self.connection_type = ""
        self.natural_sent = ""
        self.translated_sent = ""
        self.consequent_disjunct = ""
        self.user = ""
        self.natural_antecedent = ""
        self.detacher = 0
        self.def_number = 0
        self.tot_sent_idx = 0


class disjunction:
    def __init__(self):
        self.index1 = []
        self.flat_index = []
        self.comp_const = []
        self.comp_greek = []
        self.hnum = []
        self.tot_greek = ""


def error_messages(self):
    if self.kind == None and self.word not in [None, "."]:
        print(f"you forgot to give {self.word} a sort category")
    if self.popular == None and self.word not in [None, "."]:
        print(f"you forgot to state whether {self.word} is popular")
    if self.pos != None:
        if self.pos[0] == 'r' and self.superscript == None and self.pronounce == None:
            if self.pronounce != 'variable' and "for calculation" not in self.word:
                print(f" you forgot to state how {self.word} is pronounced")
        elif self.pos[0] == 'n' and self.pronounce == None \
                and self.superscript == None:

            if len(self.pos) > 1 and self.pos[1] not in ['h', 'w'] or \
                len(self.pos) == 1:
                print(f"you forgot to state the plural of {self.word}")


class row_class:
    def __init__(self, worksheet, i):
        self.row_num = i
        self.pos = worksheet.cell(row=i, column=3).value
        self.word = worksheet.cell(row=i, column=4).value
        self.next_word = worksheet.cell(row=i + 1, column=4).value
        self.abbrev_relat = worksheet.cell(row=i, column=5).value
        self.next_relat = worksheet.cell(row=i + 1, column=5).value
        self.defin = worksheet.cell(row=i, column=6).value
        self.kind = worksheet.cell(row=i, column=7).value
        self.popular = worksheet.cell(row=i, column=8).value
        self.next_defin = worksheet.cell(row=i + 1, column=6).value
        self.superscript = worksheet.cell(row=i, column=14).value
        self.pronounce = worksheet.cell(row=i, column=15).value

        error_messages(self)


def fill_group(word, dictionary, rw, str1):
    if str1 == None: return
    if str1 == 'thing':
        dictionary.biconditional_words.append(word)
        dictionary.groups.update({word: 'thing'})
    elif str1 == 'thing;c':
        dictionary.groups.update({word: 'thing'})
    elif ";" in str1:
        st = set(str1.split(";"))
        st = [x.strip() for x in st]
        dictionary.groups.update({word: set(st)})
    elif "," in str1:
        print(f'commas should not appear in the relata for {rw.word}')

    else:
        str1 = str1.strip()
        if rw.pos[0] == 'n' and rw.pos[1] == 'd':
            pass
        elif rw.pos[0] in ['n', 'r', 'a'] and word != str1:
            dictionary.groups.update({word: str1})


def correct_superscripts(list1, list2):
    for word in list1:
        if word[-1] not in list2:
            print(f"the ambiguous word {word} must be superscripted with either n or v")


def get_arity(self, rw, dictionary):
    if self.object == None:
        num = 1
    elif self.object2 == None:
        num = 2
    elif self.object3 == None:
        num = 3
    elif self.object4 == None:
        num = 4
    else:
        num = 5
    dictionary.arity.update({rw.word: num})
    dictionary.arity.update({rw.abbrev_relat: num})




def ambiguous_words(rw, relata, dictionary):
    if relata.subject == None:
        print(f"you forgot to state what {rw.word} is ambiguous between")
    else:
        list1 = relata.subject.split(";")
        list1 = [x.strip() for x in list1]
        dictionary.ambiguous2.update({rw.word: list1})
        if rw.pos[0] == 'y':
            correct_superscripts(list1, [un, uv])
        if rw.pos[0] == 'w' and len(rw.pos) > 2 and rw.pos[2] == 'p':
            list2 = rw.pronounce.split(",")
            list4 = relata.object4.split(",")
            am_dict = {}
            for k in list4:
                list5 = k.split(":")
                word1 = list5[0].strip()
                word2 = list5[1].strip()
                am_dict.update({word1: word2})
            if "," in relata.object:
                list3 = relata.object.split(",")
            else:
                list3 = [relata.object]
            for word in list2:
                word = word.strip()
                dictionary.particles.update({word:list3})
                dictionary.ambiguous3.update({word: am_dict})



class relata:

    def __init__(self, worksheet, i, dictionary, rw):
        self.subject = worksheet.cell(row=i, column=9).value
        self.object = worksheet.cell(row=i, column=10).value
        self.object2 = worksheet.cell(row=i, column=11).value
        self.object3 = worksheet.cell(row=i, column=12).value
        self.object4 = worksheet.cell(row=i, column=13).value

        if rw.abbrev_relat == None and rw.pos[0] == "r" and rw.pos[1] != "s":
            print(f"you forgot to give the abbreviation for {rw.word}")
            # raise Exception

        if rw.pos.startswith("r") and rw.pos[1] != "s":
            fill_group(rw.abbrev_relat + "s", dictionary, rw, self.subject)
            fill_group(rw.abbrev_relat + "o", dictionary, rw, self.object)
            fill_group(rw.abbrev_relat + "b", dictionary, rw, self.object2)
            fill_group(rw.abbrev_relat + "c", dictionary, rw, self.object3)
            fill_group(rw.abbrev_relat + "d", dictionary, rw, self.object4)
            get_arity(self, rw, dictionary)
        elif rw.pos[0] in ['y', 'w']:
            ambiguous_words(rw, self, dictionary)
        else:
            fill_group(rw.word, dictionary, rw, self.subject)

        if self.subject == 'thing;c': self.subject = 'thing'
        if self.object == 'thing;c': self.object = 'thing'

        if rw.pos.startswith("r") and rw.pos[1] != "s":
            dictionary.relata.update({rw.abbrev_relat: self})
        else:
            dictionary.relata.update({rw.word: self})

        if rw.pos[0] in ["n", "a", "e", "r"] and self.subject == None and \
                rw.pos[1] not in ["s", "d"]:
            if self.object2 != 'postponed':
                print(f"you forgot to categorize {rw.word}")
        elif rw.pos[1] in ['h', 'w'] and self.subject == None:
            print(f"{rw.word} does not yet belong to a category")


def get_plurals(self, dictionary):
    self.plurals = []
    self.snouns = []
    for plural, singular in dictionary.plurals.items():
        if plural != singular:
            self.plurals.append(plural)
        else:
            self.snouns.append(plural)


def fill_relations(self, word, pos, dictionary):
    arity = dictionary.arity.get(word)
    if arity == 1:
        self.relations1.append(word)
    elif arity == 2:
        self.relations2.append(word)
    elif arity == 3:
        self.relations3.append(word)



class get_words():
    def __init__(self, dictionary):
        temp_list = []
        for word, pos in dictionary.pos.items():
            if word[-1] not in superscripts \
                    and word[0].islower():
                temp_list.append(word)


        get_plurals(self, dictionary)
        self.adjectivies = []
        self.determiners = []
        self.opronouns = []
        self.pronouns = []
        self.pos_pro = []
        self.people = []
        self.relations1 = []
        self.relations2 = []
        self.relations3 = []
        self.h_relations = []

        for word, pos in dictionary.pos.items():
            if word[-1] not in superscripts and word[0].islower() \
                    and pos[2] != 'r':
                if pos[0] == 'a':
                    self.adjectivies.append({word: pos})
                elif pos[0] == 'r':
                    fill_relations(self, word, pos, dictionary)
                elif pos[:2] == 'dc':
                    self.pos_pro.append(word)
                elif pos[0] == 'd':
                    self.determiners.append(word)
                elif pos[:3] == 'pso':
                    self.opronouns.append(word)
                elif pos[0] == 'p':
                    self.pronouns.append(word)


        self.relations2.remove("is")




class ErrorWithCode(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return repr(self.code)


class get_output:
    def __init__(self):
        self.total_sent = []
        self.all_sent = []
        self.lsent_pos = set()
        self.lsent_neg = set()
        self.lcsent_pos = set()
        self.lcsent_neg = set()
        self.detach_var = {}
        self.gsent = {}
        self.gstats = {}
        self.inferences = []
        self.abbreviations = {}
        self.variables = []
        self.negated_conjunction = []
        self.disj_elim = []
        self.constants = set()
        self.prop_var = []
        self.prop_name = {}
        self.oprop_name = {}
        self.tindex = 0
        self.substitutions = {}
        self.trans_def = {}
        self.near_matches = {}
        self.words_used = set()
        self.lnot_instant = []
        self.lemma_embed = {}
        self.catalogue_num = 0
        self.pred_combos = {}


class get_dictionary:
    def __init__(self):
        self.ambiguous2 = {}
        self.ambiguous3 = {}
        self.arity = {}
        self.bad_paren = {}
        self.by_basicity = ()
        self.categorized_sent = {}
        self.conjunctive_definitions = {}
        self.connected_definitions = set()
        self.constituents = {}
        self.biconditional_words = []
        self.definitions = {}
        self.decision_procedure = {}
        self.def_constants = {}
        self.disjunctive = {}
        self.doubles = set()
        self.entailments = {}
        self.groups = {}
        self.impossible = {}
        self.kind = {}  # individual, concept, property, relation
        self.level = {}
        self.ontology = []
        self.negative_definitions = set()
        self.necessary = {}
        self.necessary_predicates = {}
        self.non_spatio_temporal_relations = []
        self.particles = {}
        self.pos = {}
        self.popular = []
        self.period_definitions = {}
        self.possible = {}
        self.plurals = {}
        self.predicates = []
        self.prepositional_relations = []
        self.past_participles = []
        self.quadruples = set()
        self.quintuples = set()
        self.relata = {}
        self.rel_abbrev = {}
        self.read_entail = {}
        self.sextuples = set()
        self.synonyms = {}
        self.spatio_temporal_relations = []
        self.triples = set()
        self.variable_entail = {}
        self.words_to_row = {}


class implications:
    def __init__(self):
        self.ant_pos = set()
        self.ant_neg = set()
        self.con_pos = set()
        self.con_neg = set()
        self.ant_var = {}
        self.con_var = {}
        self.con_pos_by_var = {}
        self.con_neg_by_var = {}
        self.con_neg_4c = set()
