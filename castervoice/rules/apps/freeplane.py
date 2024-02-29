'''
Michael McMillen
search
to do
filter dictation, press escape
'''


from dragonfly import Repeat, Pause, Function, Choice, MappingRule, ShortIntegerRef
from castervoice.lib.actions import Key, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve

class FreeplaneRule(MappingRule):#free plane
	mapping = {
		#generic key rule
		"<key_rule>": R(Key("%(key_rule)s/40")),
		#menu control
		"<menu_title> menu": R(Key("a-%(menu_title)s")),
		#zoom
		"zoom out [<m>]": R(Key("a-down")) * Repeat(extra='m'),
		"zoom in [<m>]": R(Key("a-up")) * Repeat(extra='m'),
		#movement
		"move <direction> [<m>]": R(Key("c-%(direction)s")) * Repeat(extra='m'),

		#"drop text": R(Key("cs-v/20, a-p, enter")),
	}
	extras = [
		ShortIntegerRef("m", 1, 10),
		Choice("menu_title", {
			"file": "f",
			"edit": "e",
			"insert": "r",
			"view": "v",
			"format": "o",
			"navigate": "n",
			"filter": "i",
			"tools": "t",
			"maps": "m",
			"help": "h",
		}),
		Choice("direction", {
			"up": "up",
			"down": "down",
			"left": "left",
			"right": "right",
		}),
		Choice("key_rule", {
			"save all": "a-s",
			"copy (node|single)": "cs-c",
			"copy [node] ID": "cs-i",
			# navigation
			"last": "a-left",
			"next": "a-right",
			"(jump in|isolate)":"s-escape",
			"(jump out|go back)":"escape",

			"next":"enter,enter",

			"fold [it]": "space",
			"(fold|collapse) all": "a-home",
			"unfold all": "a-end",
			"outline view": "cs-o",
			"edit styles": "c-f11",
			# filter
			"find | search": "cs-j",
			"filter": "c-f",
			"clear filter": "ca-f",

			#split
			"split dot": "ca-dot",
			"split here": "a-s",
			#edit
			"edit": "end",
			"edit dialogue": "a-enter",
			"title it":"ca-c",
			"(capitalize| cap) it":"ca-up",

			#nodes
			"(insert|big bro)": "s-enter",
			"(child|kid)": "tab",
			"(paste|drop) clone": "c-d",
			#links
			"open link": "c-enter",
			"edit link": "c-k",
			"get link": "a-e/20, c, c",
			#view
			"center ( view | node )": "ca-c",
			"new (window|view)": "ca-v",
			#icons
			"info icon ": "ca-i",
			"school":"",
			"remove icons": "cs-d",

		}),
	]
	defaults = {
		"m":1,
	}

def get_rule():
	return FreeplaneRule, RuleDetails(name="freeplane", executable="javaw")
