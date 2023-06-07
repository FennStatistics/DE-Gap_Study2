from os import environ


### Action Plan.
# add noise to option and make main reverse, main and feedback and feedback reverse have parameters as points instead of fixed numbers
# add "attention check" how many co2 emissions option entails. 
# randomly draw co2 emissions: have parameters as emissions. 
# try to make quotas for democrats 

SESSION_CONFIGS = [
     dict(
        name='DEG_study2', 
        app_sequence=[ 'Intro','EDEG', 'Scales',], 
        num_demo_participants=5
    ),

    dict(
        name='DEG_study2_EmissionsSalient',
        app_sequence=['Intro', 'EDEG', 'Scales',], 
        num_demo_participants=5,
        Exp_Con=2
    ),
    dict(
        name='DEG_study2_EmissionsDecay',
        app_sequence=[ 'Intro','EDEG', 'Scales',], 
        num_demo_participants=5,
        Exp_Con=3
    ),
    dict(
        name='DEG_study2_Control',
        app_sequence=[ 'Intro','EDEG', 'Scales',], 
        num_demo_participants=5,
        Exp_Con=1,
        doc="""
         Edit the 'num_apples' parameter to change the factor by which
         contributions to the group are multiplied.
         """
    ),


]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'Exp_Con',
    'outcomeCarbon',
    'reversedbuttons',
    'outcomeA',
    'outcomeB',
    'chosen_round',
    'chosen_round_outcome',
    'chosen_round_choice',
    'payoff_decimal',
    'game_rounds', 
    'finished'
]


SESSION_FIELDS = [
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '3153268574945'

INSTALLED_APPS = ['otree']
