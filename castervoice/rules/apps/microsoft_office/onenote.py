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

class OneNoteRule(MappingRule):
    mapping = {

		#generic key rule
        "<key_rule>": R(Key("%(key_rule)s/40")),
        "<rc_rule>": R(Key("%(key_rule)s/40")),

        #menu control
        "<menu_title> menu": R(Key("alt/20, %(menu_title)s/20")),


		"rename": R(Mouse("right") + Pause("20") + Key("r")),


        "search [for] [<dict>]": R(Key("c-e") + Pause("10") + Text("%(dict)s")),
		"(find | search) [on] page [for] [<dict>]": R(Key("c-f") + Pause("10") + Text("%(dict)s")),
		    #text formatting
		"heading <heading_n> {weight=1000}":
	            R(Key("ca-%(heading_n)s")),
	    "toggle edit cell":
	            R(Key("f2")),
        #navigate section
        "(next | down ) section [<n>]":
	        R(Key("c-tab/10"))*Repeat(extra="n"),
	    "(prior | up ) section [<n>]":
	        R(Key("cs-tab/10"))*Repeat(extra="n"),
        #navigate page
        "(next | down ) page [<n>]":
	        R(Key("c-pgdown/20"))*Repeat(extra="n"),
	    "(prior | up ) page [<n>]":
	        R(Key("c-pgup/20"))*Repeat(extra="n"),
        #moves content in direction
        "move <direction_arrow> [<n>]":
	        R(Key("as-%(direction_arrow)s/10"))*Repeat(extra="n"),

    }
    extras = [
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
		ShortIntegerRef("n", 1, 50),
		Dictation("dict"),
		Choice("direction",{"up":"pgup","down":"pgdown"}),
        Choice("direction_arrow",{"up":"up","down":"down","left":"left","right":"right"}),
        ShortIntegerRef("heading_n", 1, 6),
        # change max to 3 if you want sequences of lentgh three and so on
        Repetition(Choice("alphabet1", alphabet_support.caster_alphabet()), min=1, max=2, name="column_1"),
        Repetition(Choice("alphabet2", alphabet_support.caster_alphabet()), min=1, max=2, name="column_2"),
        Choice("rc_rule", {
            "link page":"l",
        }),
        #Key Rules
        Choice("key_rule", {
			"full (page|screen)": "f11",
			"sidebar": "cs-g, space",
			"new (tab|window)": "c-m",
			"new docked window":"a-w/20,c",
			"new page": "c-n",
			"drop text": "apps,t",
			"drop date":"as-d",
			"open link": "c-enter", #open selected link
			"edit link": "c-k", #edit selected link
<<<<<<< Updated upstream
			"(get link|link paragraph)":"apps,p", #get link to paragraph
=======
			"[get] link":"apps,p", #get link to paragraph
>>>>>>> Stashed changes
            "remove (tag|tags)": "c-0",
            "checkbox": "c-1",
			"number list": "c-slash",
			"(select|get) branch": "cs-minus",
            #branch is line plus indented lines below it
            "cut branch": "cs-minus/10,c-x",
            "search this": "c-c/10,c-e/10,c-v/10,enter",
            #Folding and unfolding
            "(fold|collapse) (it|this|branch)":"as-minus",
            "unfold (it|this)":"as-plus",
            "replace":"c-h",

            #Formatting
			"(normal text|clear formatting)": "a-h,l,up:2,enter",
            "bullet (this|text)":"c-dot",
            "number (this|text)":"c-slash",
            #OneMore
			"navigator":"as-n",

		}),
    ]
    defaults = {"n": 1, "dict": ""}

def get_rule():
    return OneNoteRule, RuleDetails(name="one note", executable="onenote")
