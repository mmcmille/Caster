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
        "snake": R(Key("left/1") + Text("_")),

        "<sentence_punc>": R(Key("backspace/1") + Text("%(sentence_punc)s") + Key("space/1")),

        #ambiguous :"<dict>] <sentence_punc>": R(Text("%(dict)s ") + Key("left/1") + Text("%(sentence_punc)s") + Key("right/1")),
        "sheet function": R(Key("home, equals, end")+ Text("()") + Key("left")),
        #goes last in mapping order
        "[dictate] <dict>": R(Text("%(dict)s ")),




    }
    extras = [
        Choice("sentence_punc", {
                "break": ",",
                "period": ".",
                "(exclamation point | !)": "!",
                "(question mark | ?)": "?",
                "deaf": ":",
        }),
        Dictation("dict"),
    ]
    defaults = {"dict": ""}

def get_rule():
    return DictationRule, RuleDetails(name="dictation")
