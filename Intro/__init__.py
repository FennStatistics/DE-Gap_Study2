from random import random, seed, choice as random_choice, randint
from otree.api import *
import numpy as np
#import scipy.stats as stats

author = 'Zahra Rahmani'
doc = """
Description Experience Gap with Carbon Externalities
"""

class C(BaseConstants):
    NAME_IN_URL = 'Intro'
    PLAYERS_PER_GROUP = None
    ROUNDS_PER_CONDITION = 1
    NUM_ROUNDS = 1
    safe_outcome = 2
    high_lottery = 20 # typical outcome of the lottery
    low_lottery = -200 # rare disaster 
    carbonB = 25
    carbonA = 0

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    Exp_Con = models.IntegerField()  # This is a between subjects variable, counterbalance of the conditions. 1 is control, 2 is salient experimental, 3 is decay experimental
    reversedbuttons = models.BooleanField()
    dataScience = models.BooleanField(initial=False)
    dataTeach = models.BooleanField(initial=False)
    realEmissions = models.IntegerField(choices=[[1,'True'], [0,'False']], label="Does the decision that will determine your bonus have a real consequence for the environment?")
    attention = models.StringField(max_length=60, blank=True)
    attention2 = models.StringField(max_length=360, blank=True)
    mobileDevice= models.BooleanField(initial=False, blank=True)
    prolificIDMissing= models.BooleanField(initial=False)
    amountEmissionsRisky = models.IntegerField(blank = True, min_length=1)
    amountEmissionsSafe = models.IntegerField(blank = True, min_length=1)
    
# FUNCTIONS

def creating_session(subsession: Subsession):
    import itertools
    conditions = itertools.cycle([1,2,3])
    reverse_display = itertools.cycle([True, False])
    # randomize to treatments
    for player in subsession.get_players():
        if subsession.round_number == 1:
            if 'Exp_Con' in player.session.config:
                player.Exp_Con = player.session.config['Exp_Con']
                player.reversedbuttons = player.session.config['reversedbuttons']
            else:
                player.Exp_Con = next(conditions) # 1 is control, 2 is experimental salient, 3 is experimental with decay
                player.reversedbuttons = next(reverse_display)
            
            player.participant.Exp_Con=player.Exp_Con
            player.participant.reversedbuttons=player.reversedbuttons
            print(player.reversedbuttons)


# ---------------------------------------------------------------
# ------------------- PAGES--------------------------------------
#----------------------------------------------------------------
class Consent(Page):
    form_model = 'player'
    form_fields = ['dataScience', 'dataTeach', 'mobileDevice']
    
    @staticmethod
    def vars_for_template(player: Player):
        # while testing this experiment do not check for prolificID (replace False with commented code)
        player.prolificIDMissing = False # player.participant.label == None
        return {
            "particpantlabel": player.participant.label,
            "nolabel": False # player.participant.label == None
            }
    

class Intro_1(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con
            }

    
class Intro_2(Page):
    form_model = 'player'
    form_fields = ['realEmissions']

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con
            }

    @staticmethod
    def is_displayed(player: Player):
        return player.in_round(1).Exp_Con > 1
    
class Intro_3(Page):
    form_model = 'player'
    form_fields = ['attention']

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con
            }

    
class NotAtt(Page):
    form_model = 'player'
    form_fields = ['attention2']
    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {'num_rounds': player.participant.game_rounds,
                'Exp_Con': Exp_Con}

    @staticmethod
    def is_displayed(player: Player):
        if player.in_round(1).attention is None:
            return True
        else:
            return not("thank" in player.in_round(1).attention.lower())
        

class Preview_Game(Page):
    form_model = 'player'
    form_fields = ['amountEmissionsRisky', 'amountEmissionsSafe']

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con
            }

    @staticmethod
    def is_displayed(player: Player):
        return player.in_round(1).Exp_Con ==3 and player.participant.reversedbuttons == False
    

class Preview_Game_Reverse(Page):
    form_model = 'player'
    form_fields = ['amountEmissionsRisky', 'amountEmissionsSafe']

    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.in_round(1).Exp_Con
        return {
            'num_rounds': player.participant.game_rounds,
            'Exp_Con': Exp_Con
            }

    @staticmethod
    def is_displayed(player: Player):
        return player.in_round(1).Exp_Con ==3 and player.participant.reversedbuttons == True
        

class before_Games(Page):
    form_model = 'player'
    



page_sequence = [
    Consent,
    Intro_1,
    Intro_2,
    Intro_3,
    Preview_Game_Reverse, 
    Preview_Game,
    NotAtt, 
    before_Games
]
