
'''
Michael McMillen
'''
from dragonfly import Repeat, Pause, Function, Choice, MappingRule, ShortIntegerRef, Dictation

from castervoice.lib.actions import Key, Mouse, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve

class PhenomeRule(MappingRule):

    mapping = {
        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s/20")),

        #"copy column": R(R(Mouse("right")+ Pause("20") +Key() )


    }
    extras = [
        Dictation("dict"),
        Choice("im_attribute", {
            "material":"Material ID",
            "line":"Stable Line Code",
            "[stable] variety [code]":"Stable Variety Code",
            "BE|be E|entity":"Biological Entity",
            "[batch] pedigree":"Batch Pedigree",
            "batch":"batch",
            "owner":"Owner",
        }),
        Choice("im_crop", {
            "[bush] bean":"bus",
            "broccoli":"bro",
            "Brussels sprouts":"bruss",
            "cabbage":"cab",
            "cauliflower": "cau",
            "Chinese cabbage":"chi",
            "cucumber":"cuc",
            "lettuce": "l",
            "melon":"m",
            "onion": "on",
            "pea":"pea",
            "pepper|peppers":"pep",
            "rootstock":"ro",
            "spinach": "sp",
            "squash": "sq",
            "sunflower": "su",
            "sweetcorn": "sw",
            "tomato":"t",
            "watermelon": "wa",
        }),
        Choice("key_rule", {

           #IM
           "search batch":"f5/80,tab:14",
           "search entity":"f5/80,tab:13/10,down/10,tab",
           "search clipboard":"c-a/20,c-v/60,tab:4/40,space",
           "search it":"tab:4/20,space",
           #Diagrams

        }),
    ]
    defaults = {}

def get_rule():
    return PhenomeRule, RuleDetails(name="Phenome", executable="slimjet", title="Phenome") #executable="edge"
