
"""
Command-module for Microsoft Excel
You also can find some good vocola commands for Excel on Mark Lillibridge's Github:
https://github.com/mdbridge/bit-bucket/tree/master/voice/my_commands/commands
Alex Boche 2019
"""

# this function takes a dictionary and returns a dictionary whose keys are sequences of keys of the original dictionary
# and whose values our the corresponding sequences of values of the original dictionary
from dragonfly import Repeat, Dictation, Choice, MappingRule, Repetition, Pause, ShortIntegerRef



from castervoice.rules.core.alphabet_rules import alphabet_support  # Manually change in port in if in user directory
from castervoice.lib.actions import Text, Key, Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

class WriterRule(MappingRule):
    mapping = {
	#"<dict>":R(Text("%(dict)s")),
    #"start typing":

    "next sheet [<n>]":
            R(Key("c-pgdown"))*Repeat(extra='n'),
        "(prior | previous) sheet [<n>]":
            R(Key("c-pgup"))*Repeat(extra='n'),
        "[select] cell <column_1> <row_1>":
            R(Key("c-g") + Text("%(column_1)s%(row_1)s") + Key("enter")),
        "select <column_1> <row_1> through <column_2> <row_2>":
            R(Key("c-g") + Text("%(column_1)s%(row_1)s:%(column_2)s%(row_2)s") +
              Key("enter")),
        "edit":
		R(Key("f2")),
	"pasta values":
		R(Key("cs-v/20")),

    "underline": R(Key("c-u")),

	   #navigation
       "left file":
           R(Key("cs-tab/20")),
       "right file":
           R(Key("c-tab/20")),
       "left file <n>":
           R(Key("cs-tab/20"))*Repeat(extra='n'),
       "right file <n>":
           R(Key("c-tab/20"))*Repeat(extra='n'),
       "close file":
           R(Key("c-w/20")),
       "save [file] as":
           R(Key("a-f/20, a/20, m/20")),
    }
    extras = [
        alphabet_support.get_alphabet_choice("letter"),
	alphabet_support.get_alphabet_choice("letter_2"),
	Dictation("dict"),
        ShortIntegerRef("n", 1, 10),
        ShortIntegerRef("row_1", 1, 9999),
        ShortIntegerRef("row_2", 1, 100),
        # change max to 3 if you want sequences of lentgh three and so on
        Repetition(Choice("alphabet1", alphabet_support.caster_alphabet()), min=1, max=2, name="column_1"),
        Repetition(Choice("alphabet2", alphabet_support.caster_alphabet()), min=1, max=2, name="column_2")
    ]
    defaults = {"n": 1, "dict": ""}

def get_rule():
    return WriterRule, RuleDetails(name="writer", executable="wps")
