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

        "[dictate] <dict> {weight=1000}": R(Text("%(dict)s ")),
    }
    extras = [
        Dictation("dict"),
    ]
    defaults = {"dict": ""}

def get_rule():
    return DictationRule, RuleDetails(name="dictation")
