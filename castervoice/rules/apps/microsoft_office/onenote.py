"""
Michael McMillen
"""

# this function takes a dictionary and returns a dictionary whose keys are sequences of keys of the original dictionary
# and whose values our the corresponding sequences of values of the original dictionary
from dragonfly import Repeat, Dictation, Choice, MappingRule, Repetition, Pause, Function, ShortIntegerRef

from castervoice.rules.core.alphabet_rules import alphabet_support  # Manually change in port in if in user directory
from castervoice.lib.actions import Text, Key, Mouse
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
class OneNoteRule(MappingRule):
    mapping = {

		#generic key rule
        "<key_rule>": R(Key("%(key_rule)s/40")),
		"rename": R(Mouse("right") + Pause("20") + Key("r")),
	    "search [<dict>]": R(Key("c-e") + Pause("50") + Text("%(dict)s")),
		"(find | search) [on] page [<dict>]": R(Key("c-f") + Pause("50") + Text("%(dict)s")),
		    #text formatting
		"heading <heading_n> {weight=1000}":
	            R(Key("ca-%(heading_n)s")),
	    "toggle edit cell":
	            R(Key("f2")),
	    "(next | down ) page [<n>]":
	        R(Key("c-pgdown/20"))*Repeat(extra="n"),
	    "(prior | up ) page [<n>]":
	        R(Key("c-pgup/20"))*Repeat(extra="n"),


    }
    extras = [
		Choice("key_rule", {
			"full (page|screen)": "f11",
			"sidebar": "cs-g, space",
			"new window": "c-m",
			"new docked window":"a-w/20,c",
			"new page": "c-n",
			"drop text": "apps,t",
			"drop date":"as-d",
			"open link": "c-enter", #open selected link
			"edit link": "c-k", #edit selected link
			"link":"apps,p", #get link to paragraph
			"checkbox": "c-1",
			"number list": "c-slash",
			"select branch": "cs-minus",
			#Formatting
			"(normal text|clear formatting)": "cs-n",
			#OneMore
			"navigator":"as-n",

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
    return OneNoteRule, RuleDetails(name="one note", executable="onenote")
