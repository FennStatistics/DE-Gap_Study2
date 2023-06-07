from random import random, seed, choice as random_choice, randint
from otree.api import *
import numpy as np
# import scipy.stats as stats



author = 'Zahra Rahmani'
doc = """
Description Experience Gap with Carbon Externalities
"""


# def truncnorm(lower, upper, mean, std):
#     return stats.truncnorm((lower - mean) / std, (upper - mean) / std, loc=mean, scale=std).rvs()

class C(BaseConstants):
    NAME_IN_URL = 'EDEG'
    PLAYERS_PER_GROUP = None
    ROUNDS_PER_CONDITION = 10
    NUM_ROUNDS = 4
    STARTING_PAYMENT = 1
    PAYRATIO = 200
    MINIMUM_PAYMENT = 0
    MAXIMUM_PAYMENT = 1.10
    TIME_TO_FINISH = 7
    safe_outcome = 2
    high_lottery = 20 # typical outcome of the lottery
    low_lottery = -200 # rare disaster 
    carbonA = 0
    show_feedback = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

#PLAYER FUNCTION 

class Player(BasePlayer):
    choice = models.StringField( choices=[ 'A', 'B'])  # , widget=widgets.RadioSelect)
    outcomeA = models.FloatField()
    outcomeB = models.FloatField()
    round_outcome = models.FloatField()  # This is the outcome of the selected button in each round


# FUNCTIONS
def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        if subsession.round_number == 1:
            player.participant.game_rounds = C.NUM_ROUNDS
            print("passing round numer", C.NUM_ROUNDS)
    print('creating subsession main')

def output_outcome(player: Player):
    #tax = player.tax
    outcomeA = C.safe_outcome
    rnd = random()
    if rnd < 0.90:
        outcomeB = C.high_lottery
    else:
        outcomeB = C.low_lottery
    print('these are the outcomes', outcomeA, outcomeB)
    return outcomeA, outcomeB

def make_choice(player: Player, choiceMade):
    Exp_Con = player.participant.Exp_Con
    reversedbuttons = player.participant.reversedbuttons
    # if player.round_number % C.ROUNDS_PER_CONDITION == 0:
    #     print('we are drawing reveresedbuttons')
    player.choice = choiceMade
    player.outcomeA, player.outcomeB = output_outcome(player)
    if reversedbuttons == True:
        if choiceMade == 'A':
            player.choice = 'B'
        elif choiceMade == 'B':
            player.choice = 'A'
    if player.choice == "A":
        player.round_outcome = player.outcomeA
    if player.choice == "B":
        player.round_outcome = player.outcomeB
    print('in make choice again',  player.round_outcome)

def determine_outcome(player:Player, chosen_round):
            player.participant.chosen_round_outcome = player.in_round(chosen_round).round_outcome
            player.participant.chosen_round_choice = player.in_round(chosen_round).choice
            #player.payoff = player.chosen_round_outcome / C.PAYRATIO
            player.participant.payoff_decimal = 1 + player.participant.chosen_round_outcome/ C.PAYRATIO 
            participant = player.participant
            participant.chosen_round = chosen_round


# ---------------------------------------------------------------
# ------------------- PAGES--------------------------------------
#----------------------------------------------------------------


class Main(Page):
    form_model = 'player'
    form_fields = ['choice']
    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.participant.Exp_Con
        reversedbuttons = player.participant.reversedbuttons
        carbonB = player.participant.outcomeCarbon
        carbonMiles = carbonB * 4
        game_round = (
                player.round_number
                - int((player.round_number - 1) / C.ROUNDS_PER_CONDITION)
                * C.ROUNDS_PER_CONDITION
            )
        return {
                #'game': game,
                'Exp_Con': Exp_Con,
                'game_round': game_round,
                'gamenum': int((player.round_number - 1) / C.ROUNDS_PER_CONDITION) + 1,
                'lastRB': reversedbuttons,
                'carbonB': carbonB,
                'carbonMiles': carbonMiles
            }
    @staticmethod
    def is_displayed(player: Player):
        return (player.participant.reversedbuttons == False)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        print('in before next page function')
        make_choice(player, player.choice)
        print('do you even get here')

class Main_R(Page):
    form_model = 'player'
    form_fields = ['choice']
    @staticmethod
    def vars_for_template(player: Player):
        Exp_Con = player.participant.Exp_Con
        reversedbuttons = player.participant.reversedbuttons
        carbonB = player.participant.outcomeCarbon
        carbonMiles = carbonB * 4
        game_round = (
                player.round_number
                - int((player.round_number - 1) / C.ROUNDS_PER_CONDITION)
                * C.ROUNDS_PER_CONDITION
            )
        return {
                #'game': game,
                'Exp_Con': Exp_Con,
                'game_round': game_round,
                'gamenum': int((player.round_number - 1) / C.ROUNDS_PER_CONDITION) + 1,
                'lastRB': reversedbuttons,
                'carbonB': carbonB,
                'carbonMiles': carbonMiles
            }
    @staticmethod
    def is_displayed(player: Player):
        return (player.participant.reversedbuttons== True)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        print('in before next page function', player.choice)
        make_choice(player, player.choice)
        print('do you even get here')

class Feedback(Page):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number >= C.show_feedback and player.participant.reversedbuttons== False)

    @staticmethod
    def vars_for_template(player: Player):
            previous_choice = player.choice
            previous_outcome = player.round_outcome
            if player.participant.reversedbuttons == True:
                if previous_choice == "A":
                    previous_choice = "B"
                elif previous_choice == "B":
                    previous_choice = "A"
                previous_outcomeA = player.outcomeB
                previous_outcomeB = player.outcomeA
            else:
                previous_outcomeA = player.outcomeA
                previous_outcomeB = player.outcomeB
            #game = player.in_round(player.round_number - 1).tax
            Exp_Con = player.participant.Exp_Con
            reversedbuttons = player.participant.reversedbuttons
            game_round = (
                player.round_number
                - int((player.round_number ) / C.ROUNDS_PER_CONDITION)
                * C.ROUNDS_PER_CONDITION
            )
            print(game_round)
            return {
                'previous_choice': previous_choice,
                'previous_outcome': previous_outcome,
                #'game': game,
                'previous_outcomeA': previous_outcomeA,
                'previous_outcomeB': previous_outcomeB,
                'Exp_Con': Exp_Con,
                'game_round': game_round,
                'gamenum': int((player.round_number - 1) / C.ROUNDS_PER_CONDITION) + 1,
                'lastRB': reversedbuttons,
                'carbonB' : player.participant.outcomeCarbon
            }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if (player.round_number == C.NUM_ROUNDS):
            chosen_round = randint(1,C.NUM_ROUNDS)
            determine_outcome(player,chosen_round)
            print('the chosen round is', chosen_round)
           
class Feedback_R(Page):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return (player.round_number >= C.show_feedback  and player.participant.reversedbuttons == True )

    @staticmethod
    def vars_for_template(player: Player):
            print("player is in round number", player.round_number)
            previous_choice = player.choice
            previous_outcome = player.round_outcome
            if player.participant.reversedbuttons == True:
                if previous_choice == "A":
                    previous_choice = "B"
                elif previous_choice == "B":
                    previous_choice = "A"
                previous_outcomeA = player.outcomeB
                previous_outcomeB = player.outcomeA
            else:
                previous_outcomeA = player.outcomeA
                previous_outcomeB = player.outcomeB
            Exp_Con = player.participant.Exp_Con
            reversedbuttons = player.participant.reversedbuttons
            game_round = (
                player.round_number
                - int((player.round_number ) / C.ROUNDS_PER_CONDITION)
                * C.ROUNDS_PER_CONDITION
            )
            print(game_round)
            return {
                'previous_choice': previous_choice,
                'previous_outcome': previous_outcome,
                #'game': game,
                'previous_outcomeA': previous_outcomeA,
                'previous_outcomeB': previous_outcomeB,
                'Exp_Con': Exp_Con,
                'game_round': game_round,
                'gamenum': int((player.round_number - 1) / C.ROUNDS_PER_CONDITION) + 1,
                'lastRB': reversedbuttons,
                'carbonA' : player.participant.outcomeCarbon,
                'carbonB' : C.carbonA
            }
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if (player.round_number == C.NUM_ROUNDS):
            player.participant.chosen_round = randint(1,C.NUM_ROUNDS)
            determine_outcome(player,player.participant.chosen_round)
            print('the chosen round is', player.participant.chosen_round)
   
class betweenGames(Page):

    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number == C.show_feedback
        )


page_sequence = [
    #betweenGames,
    Main,
    Feedback,
    Main_R,
    Feedback_R
]
