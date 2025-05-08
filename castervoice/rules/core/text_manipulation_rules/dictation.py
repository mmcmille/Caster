"""
Michael McMillen
"""
from dragonfly import Dictation, Choice, MappingRule

from castervoice.lib.actions import Text, Key, Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.const import CCRType
from castervoice.lib.merge.state.short import R


class DictationRule(MappingRule):

    mapping = {
        #"<sentence_punc> {weight=1000}": R(Key("backspace/1") + Text("%(sentence_punc)s")),

        #ambiguous :"<dict>] <sentence_punc>": R(Text("%(dict)s ") + Key("left/1") + Text("%(sentence_punc)s") + Key("right/1")),

        #goes last in mapping order
        "<dict>": R(Text("%(dict)s ",pause=0.01,use_hardware=True)),#<dict> {weight=1000}


    }
    extras = [
        Dictation("dict"),
    ]
    defaults = {"dict": ""}

def get_rule():
    #return DictationRule, RuleDetails(name="edit")
    return DictationRule, RuleDetails(name="dictation")
