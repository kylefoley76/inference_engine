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
        self.consequent_disjunct = ""
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


class ErrorWithCode(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(self.code)

