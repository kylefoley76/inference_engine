
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
        self.ant_comp_const = []
        self.con_comp_const = []
        self.ant_comp_greek = []
        self.con_comp_greek = []
        self.instance = []
        self.already_instantiated = False
        self.now_disjunctive = False
        self.ant_hnum = ""
        self.con_hnum = ""
        self.ant_greek = ""
        self.con_greek = ""
        self.tot_greek_sent = ""
        self.concept = ""
        self.connection_type = ""
        self.natural_sent = ""
        self.translated_sent = ""
        self.consequent_disjunct = ""
        self.user = ""
        self.natural_disjuncts = []
        self.greek_disjuncts = []
        self.detacher = 0
        self.def_number = 0
        self.tot_sent_idx = 0



class disjunction:
    def __init__(self):
        self.index1 = []
        self.comp_const = []
        self.comp_greek = []
        self.hnum = []
        self.tot_greek = ""


class row_class:
    def __init__(self):
        self.row_num = 0
        self.pos = ""
        self.word = ""
        self.next_word = ""
        self.abbrev_relat = ""
        self.defin = ""
        self.next_defin = ""
        self.edisj = ""
        self.embed = ""
        self.easy_embed = ""




class ErrorWithCode(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(self.code)


class get_output:
    def __init__(self):
        self.total_sent = []
        self.all_sent = []
        self.lsent_list = []
        self.lsent_dict = {}
        self.gsent = []
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
        self.main_var = set()
        self.lnot_instant = []
        self.lemma_embed = {}


class get_dictionary:
    def __init__(self):
        self.pos = {}
        self.definitions = {}
        self.rel_abbrev = {}
        self.synonyms = {}
        self.doubles = {}
        self.triples = {}
        self.quadruples = {}
        self.kind = {} # individual, concept, property, relation
        self.words_to_row = {}
        self.prepositional_relations = []
        self.categorized_sent = {}
        self.decision_procedure = {}
        self.easy_embed = []
        self.embed_type = {}
        self.spatio_temporal_relations = []
        self.non_spatio_temporal_relations = []
        self.conjunctive_definitions = {}
        self.past_participles = []
        self.def_constants = {}
        self.basic_definitions = {}
        self.basic_output = {}
        self.groups = {}