
'''
Michael McMillen
'''
from dragonfly import Repeat, Pause, Function, Choice, MappingRule, ShortIntegerRef, Dictation

from castervoice.lib.actions import Key, Mouse, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve

class IdentityRule(MappingRule):

    mapping = {
        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s/20")),

        "export": R(Key("tab:6/20,space/10")+Pause("100")+Key("s-tab:4/20,space")+Pause("100")+Key("tab:3/20,space")),

        "<im_crop>": R(Key("tab,space/20,s-tab/40,enter/40")
        + Text("%(im_crop)s")
        + Pause("20")
        + Key("space/40,tab:2/40,space,s-tab:3")

        ),

        "<im_attribute>": R(Key("c-a/20")
            + Text("%(im_attribute)s")
            + Key("enter/10,tab/20,down:7,tab")),
    }
    extras = [
        Dictation("dict"),
        Choice("im_attribute", {
            "material":"Material ID",
            "line":"Stable Line Code",
            "[stable] variety [code]":"Stable Variety Code",
            "BE|be E|entity":"Biological Entity",
            "batch pedigree":"Batch Pedigree",
        }),
        Choice("im_crop", {
            "broccoli":"br",
            "Brussels sprouts":"bruss",
            "cabbage":"cab",
            "cauliflower": "cau",
            "cucumber":"cuc",
            "lettuce": "l",
            "onion": "on",
            "pepper|peppers":"pep",
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
           "search clipboard":"c-a/20,c-v/40,tab:4/20,space",
           "search it":"tab:4/20,space",

        }),
    ]
    defaults = {}

def get_rule():
    return IdentityRule, RuleDetails(name="identity management", title="Identity")
