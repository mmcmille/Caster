from dragonfly import Dictation, MappingRule, ShortIntegerRef, Choice
from castervoice.lib.actions import Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class MSWordRule(MappingRule):
    mapping = {
        "insert image": R(Key("alt, n, p")),
        #menu control
        "<menu_title> menu": R(Key("alt/20, %(menu_title)s/20")),
        "<menu_command>": R(Key("alt/20, %(menu_command)s/20")),
        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s")),

    }
    extras = [
        Dictation("dict"),
        ShortIntegerRef("n", 1, 100),
        Choice("menu_title", {
            "file": "f",
			"home":"h",
			"insert": "n",
            "page layout": "p",
            "formulas": "m",
            "data": "a",
            "review": "r",
            "view": "w",
            "automate": "u",
            "developer": "l",
			"help": "y",
		}),
        Choice("menu_command", {
            "save as":"f,a",
        }),
        Choice("key_rule", {
        "normal text":"a-h/10,l,enter",

        }),
    ]
    defaults = {"n": 1, "dict": "nothing"}


def get_rule():
    details = RuleDetails(name="Microsoft Word", executable="winword")
    return MSWordRule, details
