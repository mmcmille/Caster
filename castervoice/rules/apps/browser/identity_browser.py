
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

        "export": R(Key("tab:8/20,space/10")+Pause("100")+Key("s-tab:6/20,space")+Pause("100")+Key("tab:3/20,space")),

        "<im_crop>": R(Key("tab,space/20,s-tab/40,enter/30")
        + Text("%(im_crop)s")
        + Pause("20")
        + Key("space/10,tab:2/10,space,s-tab:3")

        ),

        "<im_attribute>": R(Key("c-a/20")
            + Text("%(im_attribute)s")
            + Pause("10")
            + Key("enter/10,tab/20,down:7,tab")),

        "[batch] diagram":R(Key("c-c/20,c-t")
            + Text("https://identity.mint.syngentadigitalapps.com/app/batch-details/")
            + Key("c-v")
            + Text("/lineage-diagram")
            + Key("enter")),

    }
    extras = [
        Dictation("dict"),
        Choice("im_attribute", {
            "material":"Material ID",
            "line":"Stable Line Code",
            "[stable] variety [code]":"Stable Variety Code",
            "BE|be E|entity":"Biological Entity",
            "batch pedigree":"Batch Pedigree",
            "batch":"batch",
        }),
        Choice("im_crop", {
            "broccoli":"br",
            "Brussels sprouts":"bruss",
            "cabbage":"cab",
            "cauliflower": "cau",
            "cucumber":"cuc",
            "lettuce": "l",
            "melon":"m",
            "onion": "on",
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
           "search clipboard":"c-a/20,c-v/60,tab:4/30,space",
           "search it":"tab:4/20,space",
           #Diagrams

        }),
    ]
    defaults = {}

def get_rule():
    return IdentityRule, RuleDetails(name="identity management", executable="chrome", title="Identity")
