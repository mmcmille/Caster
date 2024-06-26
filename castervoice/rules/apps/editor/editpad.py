from dragonfly import Repeat, Dictation, MappingRule, ShortIntegerRef, Choice

from castervoice.lib.actions import Key, Text, Mouse

from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class EditPadRule(MappingRule):

    mapping = {
    #dictation mode
    "<text> {weight=10}": R(Text("%(text)s ")),

    "hi <name>": R(Text("Hi %(name)s,") + Key("enter")),

        "go [to] line <n>":
            R(Key("c-g/10") + Text("%(n)s") + Key("enter")),
    }
    
    extras = [
        Dictation("text"),
        ShortIntegerRef("n", 1, 1000),
        ShortIntegerRef("n2", 1, 10),
        Choice("name", {
            "darin": "Darryn",
            "mel": "Mel",
            "veronica": "Veronica",
            "drew": "Drew",
            "yvette": "Yvette",
            "leo": "Leo",
        }),
    ]
    defaults = {"n": 1}


def get_rule():
    return EditPadRule, RuleDetails(name="edit pad", executable="editpadLite8")
