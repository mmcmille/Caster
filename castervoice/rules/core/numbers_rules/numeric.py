'''
Michael McMillen
'''
from dragonfly import Choice, Function, ShortIntegerRef

#try:  # Try first loading from caster user directory
#    from numeric_support import word_number, numbers2, numbers3
#except ImportError:
from castervoice.rules.core.numbers_rules.numeric_support import word_number, numbers2, numbers3

from castervoice.lib.actions import Text
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R

class Numbers(MergeRule):
    pronunciation = "numbers"
    mapping = {

        #"word <wn>":
        #    R(Function(word_number, extra="wn")),
        #"[<long>] numb <wnKK>": R(Text("%(long)s") + Function(numbers2, extra="wnKK") + Text("%(long)s"), rspec="Number"),
        #simplified numbers
        "numb <wnKK>": R(Function(numbers2, extra="wnKK")),
        "point <wnKK2>":
            R(Text(".") + Function(numbers3, extra="wnKK2")),
        "[(numb|number)] <wnKK> point <wnKK2>":
            R(Function(numbers2, extra="wnKK") + Text(".") + Function(numbers3, extra="wnKK2")),
        "[numb] zero <wnKK>": R(Text("0") + Function(numbers2, extra="wnKK")),
        "[numb] zero zero <wnKK>": R(Text("00") + Function(numbers2, extra="wnKK")),

    }

    extras = [
        ShortIntegerRef("wn", 0, 10),
        ShortIntegerRef("wnKK", 0, 1000000),
        ShortIntegerRef("wnKK2", 0, 1000000),
        Choice(
            "long", {
                "long": " ",
            }),
    ]

    defaults = {
        "long": "",
    }

def get_rule():
    return Numbers, RuleDetails(ccrtype=CCRType.GLOBAL)
