'''
Michael McMillen
'''


from dragonfly import Repeat, Pause, Function, Choice, MappingRule

from castervoice.lib.actions import Key, Mouse, Text

from castervoice.lib.merge.additions import ShortIntegerRef
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve

class SpiritRule(MappingRule):
	mapping = {

		# table and button navigation
		"[open] <item>": R(Mouse("(%(item)s)/50, left")),
		#table filtering
		"filter": R(Mouse("left:down, [0, 20], left:up")),
		#query menu
		"<spirit_trait>":R( Text("%(spirit_trait)s", pause = 0.1)+Key("tab/20,equals")),
		#"<key_rule>": R(Key("%(key_rule)s/40")),

		"close frame": R(Mouse("(0.998, 38), left")),#R(Key("a-f/40,enter")),
		#row and column right-click menu commands
		#uses menu, assumes mouse is resting on row
		"<rc_item>": R(Mouse("right") + Pause("50")+Key("%(rc_item)s,enter")),
		"remove": R(Mouse("left, right") + Pause("20")+Key("r")),
		"paste down":R(Mouse("right/50") + Key("p/10:2,enter")),
		"properties":R(Mouse("right/50") + Key("up,enter")),
		"okay":R(Mouse("(2141, 1324),left")), #Key("a-o")),
		"(pull over| bring over| apply profile)": R(Mouse("left:down/60, <-200, 0>, left:up")),


		#other commands
		"edit": R(Key("f2")),
		#menu control
		"<menu_title> [menu]":
			R(Key("alt/20, %(menu_title)s/20")),

	}
	extras = [
		Choice("menu_title", {
			"file": "f",
			"edit menu": "e",
			"view": "v",
			"reports": "r",
			"window": "w",
			"help": "h",
			"import": "f,down:2,right,enter",
			"export containers": "f,down:3/40,right/40,down/40,enter",
			#"close frame": "f, enter"
		}),

		Choice("spirit_trait", {
			"plot prefix":"EXT:PLTPR",
			"plot status":"",
			"(material ID|mad ID)":"MAT:MATID",
			"trial ID":"EXT:TRLID",
			"line code":"MAT:LINE:LINCD",


		}),
		Choice("item", {
			"query":"778, 67",
			"material management":"87, 130",
			"materials":"82, 160",
			"(trial|experiment) management":"78, 654",
			"trials":"82, 285",
			"experiments": "81, 234",
			"plots":"87, 280",
			"query":"774, 63",

			"advanced sort":"396, 70",
			#"sort down":"386, 96",
			#"sort up":"408, 94",
			"close spirit":"242, 68",
			#"close frame": "2488, 35",
			"cell 1":"190, 135",
			"get table":"180, 128",
			"(last row|row last|row end)": "180, 1269",
			"row 1":"180, 145",

			"Entries ":"357, 214",
			"design":"427, 212",

		}),
		Choice("rc_item", {
				"view associated": "v/20, right",
				"view [associated] subplots": "v/20, right, up:2",
				"view [associated] plots": "v/20, right, p",
				"view [associated] (trial|trials)": "v/20, t",
				"(add|make) subplots": "a/20:2",

				"plant trial":"p/20:3",
				"sort down":"up:8,right,down",
				"sort up":"up:8,right,down:2",
		}),


		ShortIntegerRef("k", 1, 1000),
		ShortIntegerRef("n", 1, 100),
		ShortIntegerRef("m", 1, 10)

	]
    #defaults = {"n": 1, "k": 1, "m":"", "nth": ""}


def get_rule():

	return SpiritRule, RuleDetails(name="spirit rule", executable="wfica32")#"SPIRITShell")
