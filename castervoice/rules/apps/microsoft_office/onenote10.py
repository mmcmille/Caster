"""
Michael McMillen
"""

# this function takes a dictionary and returns a dictionary whose keys are sequences of keys of the original dictionary
# and whose values our the corresponding sequences of values of the original dictionary
from dragonfly import Repeat, Dictation, Choice, MappingRule, Repetition, Pause, Function, ShortIntegerRef

from castervoice.rules.core.alphabet_rules import alphabet_support  # Manually change in port in if in user directory
from castervoice.lib.actions import Text, Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


editing = True

def editText():
	if editing == True:
		output = str(dict).title()
	else:
		output = ""
	Text(output).execute()
	return
def editOn(editing):
	editing = True
	return
def editOff(editing):
	editing = False
	return
class OneNote10Rule(MappingRule):
    mapping = {

		#generic key rule
        "<key_rule>": R(Key("%(key_rule)s/40")),

	    "(find | search) [<dict>]": R(Key("c-e") + Pause("50") + Text("%(dict)s")),
		"(find | search) [on] page [<dict>]": R(Key("c-f") + Pause("50") + Text("%(dict)s")),
		    #text formatting
		"heading <heading_n>":
	            R(Key("ca-%(heading_n)s")),
	    "normal [text]": R(Key("cs-n")),
	    "toggle edit cell":
	            R(Key("f2")),
	    "(next | down ) page [<n>]":
	        R(Key("c-pgdown/20"))*Repeat(extra="n"),
	    "(prior | up ) page [<n>]":
	        R(Key("c-pgup/20"))*Repeat(extra="n"),



	#swallow dictation to prevent unintentional edits
	#"<dict>":
	#	R(Function(editText)),
	 #"edits on ":
	#	R(Function(editOn)),
	#"edits off":
	#	R(Function(editOn)),
    }
    extras = [
		Choice("key_rule", {
			"full (page|screen)": "f11",
			"new window": "c-m",
			"new page": "c-n",
			#"drop text": "apps/20,tab/20,right/20,down:2/20,space",
			"open link": "c-enter",
			"edit link": "c-k",
			"checkbox": "c-1",
			"number list": "c-slash",
			"select branch": "cs-minus",
		}),

		ShortIntegerRef("n", 1, 50),
		Dictation("dict"),
		Choice("direction",{"up":"pgup","down":"pgdown"}),
        ShortIntegerRef("heading_n", 1, 6),
        # change max to 3 if you want sequences of lentgh three and so on
        Repetition(Choice("alphabet1", alphabet_support.caster_alphabet()), min=1, max=2, name="column_1"),
        Repetition(Choice("alphabet2", alphabet_support.caster_alphabet()), min=1, max=2, name="column_2")
    ]
    defaults = {"n": 1, "dict": ""}

def get_rule():
    return OneNote10Rule, RuleDetails(name="one note 10", executable="ApplicationFrameHost")
