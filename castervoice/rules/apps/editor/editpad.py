from dragonfly import Repeat, Dictation, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key, Text, Mouse

from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class EditPadRule(MappingRule):

    mapping = {
    "<text> {weight=1000}": R(Text("%(text)s ")),

        "go [to] line <n>":
            R(Key("c-g/10") + Text("%(n)s") + Key("enter")),
    }
    #weight = 2
    extras = [
        Dictation("text"),
        ShortIntegerRef("n", 1, 1000),
        ShortIntegerRef("n2", 1, 10),
    ]
    defaults = {"n": 1}


def get_rule():
    return EditPadRule, RuleDetails(name="edit pad", executable="editpadLite8")
