
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
    }
    extras = [
        Dictation("dict"),

        Choice("key_rule", {
            #Notes
            "new note":"c-p",
        }),
    ]
    defaults = {}

def get_rule():
    return TriliumRule, RuleDetails(name="Trillium", title="Trilium Notes")
