"""
Michael McMillen

TODO: make some punctuation go back one, and some punctuation not
"""

from dragonfly import Choice, Repeat, ShortIntegerRef, Dictation

from castervoice.lib.actions import Key, Text

try:  # Try  first loading  from caster user directory! !
    from punctuation_support import double_text_punc_dict, text_punc_dict, sentence_punc_dict
except ImportError:
    from castervoice.rules.core.punctuation_rules.punctuation_support import double_text_punc_dict, text_punc_dict, sentence_punc_dict

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class Punctuation(MergeRule):
    pronunciation = "punctuation"

    mapping = {
        #dictation rule, to better mesh with punctuation
        "[dictate] <dict>": R(Text("%(dict)s ")),

        "ace [<npunc100>]":
            R(Text(" "))*Repeat(extra="npunc100"),


        #alternative punctuation rule, relies on a space after words (moves to the left one space)
        "<sentence_punc>": R(Key("left/1") + Text("%(sentence_punc)s") + Key("right/1")),
        #used to place sentence punctuation at cursor
        "drop <sentence_punc>": R(Text("%(sentence_punc)s")),
        "<dict> <sentence_punc>": R(Text("%(dict)s ") + Key("left/1") + Text("%(sentence_punc)s") + Key("right/1")),
        "underscore": R(Key("left/1") + Text("_")),

        "<text_punc>": R(Text("%(text_punc)s")),

        "[<long>] <text_punc> [<npunc>]":
            R(Text("%(long)s" + "%(text_punc)s" + "%(long)s"))*Repeat(extra="npunc"),
        # For some reason, this one doesn't work through the other function
        "[<long>] backslash [<npunc>]":
            R(Text("%(long)s" + "\\" + "%(long)s"))*Repeat(extra="npunc"),
        "<double_text_punc> [<npunc>]":
            R(Text("%(double_text_punc)s") + Key("left"))*Repeat(extra="npunc"),
        "tabby [<npunc>]":
            R(Key("tab"))*Repeat(extra="npunc"),
        "(back | shin) tabby [<npunc>]":
            R(Key("s-tab"))*Repeat(extra="npunc"),
        "boom [<npunc>]":
            R(Text(", "))*Repeat(extra="npunc"),
        "(dot|point) [<npunc>]":
            R(Text("."))*Repeat(extra="npunc"),



    }

    extras = [
        ShortIntegerRef("npunc", 0, 10),
        ShortIntegerRef("npunc100", 0, 100),
        Choice(
            "long", {
                "long": " ",
            }),
        Choice(
            "sentence_punc", sentence_punc_dict()),
        Choice(
            "text_punc", text_punc_dict()),
        Choice(
            "double_text_punc", double_text_punc_dict()),
        Dictation("dict"),
    ]
    defaults = {
        "npunc": 1,
        "npunc100": 1,
        "long": "",
        "dict": "",
    }


def get_rule():
    return Punctuation, RuleDetails(ccrtype=CCRType.GLOBAL)
