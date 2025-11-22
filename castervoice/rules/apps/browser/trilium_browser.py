
'''
Michael McMillen
'''
from dragonfly import Repeat, Pause, Function, Choice, MappingRule, ShortIntegerRef, Dictation

from castervoice.lib.actions import Key, Mouse, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve

class TriliumRule(MappingRule):

    mapping = {
        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s/20")),
        #navigate tabs
        "<direction> note [<n>]":
	        R(Key("c-%(direction)s/10"))*Repeat(extra="n"),

        #Formattin
        "(normal text|clear formatting)": "a-h,l,up:2,enter",
        "bullet (this|text)":
            R(Key("home,minus/20,space,end")),
        "number (this|text)":
            R(Key("home/40,one/20,dot,space,end")),
        "checkbox [this|text]":
            R(Key("home/40,[,],space,end")),
        "complete (this|text)":
            R(Key("home/40,[,x,],space,end")),
        "heading <heading_n> {weight=1000}": #corresponds to Heading 2-6, but uses 1-5 for simplicity
	            R(Key("home/20,#, #:%(heading_n)s/10,space,end")),
    }
    extras = [
        Dictation("dict"),
        ShortIntegerRef("n",1,10),
        ShortIntegerRef("heading_n", 1, 5),
        Choice("direction", {
            "left":"[",
            "right":"]",
        }),
        Choice("key_rule", {
            "jump note":"c-j",
            "commands":"cs-j",
            "search":"c-s",
            "search subtree":"cs-s",
            "find":"c-f",
            "full-page":"f9",
            "reload":"f5",

            #Notes
            "close note":"ca-w",
            "(reopen|restore) note":"ca-t",
            "child note":"c-p",
            "sibling note":"c-o",
            "split note":"cs-n",
            "(show|hide) attributes":"a-a",
            "jump in":"a-h",
            "jump out":"a-u",
        }),
    ]
    defaults = {"n": 1}

def get_rule():
    return TriliumRule, RuleDetails(name="Trillium", title="Trilium Notes")
