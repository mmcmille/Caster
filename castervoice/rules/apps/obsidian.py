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

class ObsidianRule(MappingRule):
    mapping = {

		#generic key rule
        "<key_rule>": R(Key("%(key_rule)s/40")),
        "<rc_rule>": R(Key("%(key_rule)s/40")),

        #menu control
        "<menu_title> menu": R(Key("alt/20, %(menu_title)s/20")),


		"rename": R(Mouse("right") + Pause("20") + Key("r")),


        "search [for] [<dict>]": R(Key("cs-f") + Pause("10") + Text("%(dict)s")),
        "switch [<dict>]": R(Key("c-o") + Pause("10") + Text("%(dict)s")),
		"(find | search) [on] page [for] [<dict>]": R(Key("c-f") + Pause("10") + Text("%(dict)s")),
		    #text formatting
	    "toggle edit cell":
	            R(Key("f2")),
        #navigate tabs
        "(next | right) tab [<n>]":
	        R(Key("c-pgdown/10"))*Repeat(extra="n"),
	    "(prior | left ) tab [<n>]":
	        R(Key("c-pgup/10"))*Repeat(extra="n"),
        #navigate page
        "(next | down ) page [<n>]": R(Key("cs-pgdown/20"))*Repeat(extra="n"),
	    "(prior | up ) page [<n>]": R(Key("cs-pgup/20"))*Repeat(extra="n"),
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
        # change max to 3 if you want sequences of lentgh three and so on
        Repetition(Choice("alphabet1", alphabet_support.caster_alphabet()), min=1, max=2, name="column_1"),
        Repetition(Choice("alphabet2", alphabet_support.caster_alphabet()), min=1, max=2, name="column_2"),
        Choice("rc_rule", {
            "link page":"l",
        }),
        #Key Rules
        Choice("key_rule", {
            "(read | edit) (this|mode|page|note)":"c-e",
            "source mode":"cs-s",
            "full (page|screen)": "f11",
			"sidebar": "cs-g",
            #tabs
            "new tab": "c-t",
            "close tab":"c-w",
            "new window": "ca-t",
            #"new docked window":"a-w/20,c",
			"new page": "c-n",
			"drop text": "apps,t",
			"drop date":"as-d",
			"open link": "c-enter", #open selected link
			"edit link": "c-k", #edit selected link
			"(get link|link paragraph)":"apps,p", #get link to paragraph
            "remove (tag|tags)": "c-0",
            "checkbox": "c-1",
			"number list": "c-slash",
			"(select|get) branch": "cs-minus",
            #branch is line plus indented lines below it
            "cut branch": "cs-minus/10,c-x",
            "search this": "c-c/10,cs-f/10,c-v/10,enter",
            "search (it|clipboard)": "cs-f/10,c-v/10,enter",
            #Folding and unfolding
            "(fold|collapse) (it|this|branch)":"as-minus",
            "unfold (it|this)":"as-plus",
            "replace":"c-h",

            #Formatting
            "heading":"home,s-3",
			"(normal text|clear formatting)": "ca-c",
            "bullet (this|text)":"c-dot",
            "number (this|text)":"c-slash",

            #Notebook Navigator
            "(show | reveal) folder":"cs-r",
            "navigator":"as-n",

		}),
    ]
    defaults = {"n": 1, "dict": ""}

def get_rule():
    return ObsidianRule, RuleDetails(name="obsidian", executable="obsidian")
