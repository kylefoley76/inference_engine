

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
        if self.kind == None and self.word not in [None, "."]:
            print (f"you forgot to give {self.word} a sort category")
        if self.popular == None and self.word not in [None, "."]:
            print (f"you forgot to state whether {self.word} is popular")

def fill_group(word, dictionary, sec_let, rw, str1):
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
    else:
        str1 = str1.strip()
        if rw.pos[0] == 'n' and sec_let == 'd':
            pass
        elif rw.pos[0] in ['n','r','a'] and word != str1:
            dictionary.groups.update({word: str1})


class relata:

    def __init__(self, worksheet, i, dictionary, rw, sec_let):
        self.subject = worksheet.cell(row=i, column=9).value
        self.object = worksheet.cell(row=i, column=10).value
        self.object2 = worksheet.cell(row=i, column=11).value
        self.object3 = worksheet.cell(row=i, column=12).value
        self.object4 = worksheet.cell(row=i, column=13).value

        if rw.abbrev_relat == None and rw.pos[0] == "r" and sec_let != "s":
            print (f"you forgot to give the abbreviation for {rw.word}")
            raise Exception


        if rw.pos.startswith("r") and sec_let != "s":
            fill_group(rw.abbrev_relat + "s", dictionary, sec_let, rw, self.subject)
            fill_group(rw.abbrev_relat + "o", dictionary, sec_let, rw, self.object)
            fill_group(rw.abbrev_relat + "b", dictionary, sec_let, rw, self.object2)
            fill_group(rw.abbrev_relat + "c", dictionary, sec_let, rw, self.object3)
            fill_group(rw.abbrev_relat + "d", dictionary, sec_let, rw, self.object4)

        else:
            fill_group(rw.word, dictionary, sec_let, rw, self.subject)

        if self.subject == 'thing;c': self.subject = 'thing'
        if self.object == 'thing;c': self.object = 'thing'


        if rw.pos.startswith("r") and sec_let != "s":
            dictionary.relata.update({rw.abbrev_relat: self})
        else:
            dictionary.relata.update({rw.word: self})



        if rw.pos[0] in ["n", "a", "e", "r"] and self.subject == None and \
            sec_let not in ["s", "d"]:
            if self.object2 != 'postponed':
                print (f"you forgot to categorize {rw.word}")
        elif sec_let in ['h','w'] and self.subject == None:
            print (f"{rw.word} does not yet belong to a category")





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

        self.atomic = []
        self.ambiguous = []
        self.bad_paren = {}
        self.basic_definitions = {}
        self.basic_output = {}
        self.categorized_sent = {}
        self.categorized_simple = {}
        self.conjunctive_definitions = {}
        self.connected_definitions = set()
        self.biconditional_words = []
        self.definitions = {}
        self.decision_procedure = {}
        self.def_constants = {}
        self.disjunctive = {}
        self.doubles = {}
        self.entailments = {}
        self.groups = {}
        self.impossible = {}
        self.kind = {} # individual, concept, property, relation
        self.level = {}
        self.ontology = []
        self.negative_definitions = set()
        self.necessary = {}
        self.necessary_predicates = {}
        self.non_spatio_temporal_relations = []
        self.pos = {}
        self.popular = []
        self.period_definitions = {}
        self.possible = {}
        self.predicates = []
        self.prepositional_relations = []
        self.past_participles = []
        self.quadruples = {}
        self.relata = {}
        self.rel_abbrev = {}
        self.read_entail = {}
        self.synonyms = {}
        self.spatio_temporal_relations = []
        self.triples = {}
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
