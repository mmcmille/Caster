'''
Michael McMillen
'''


from dragonfly import Repeat, Pause, Function, Choice, MappingRule, ShortIntegerRef
from castervoice.lib.actions import Key, Mouse, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R
from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve

class SpiritRule(MappingRule):
	mapping = {
		#generic key rule
		"<key_rule>": R(Key("%(key_rule)s/60")),
		#show/hide columns: move item under mouse to display
        "this": R(Mouse("left") + Pause("10") + Key("tab/10, space")),

		# table and button navigation
		"[open] <item>": R(Mouse("(%(item)s)/50, left")),
		#table filtering
		"filter": R(Mouse("left:down, [0, 20], left:up")),
		#query menu
		"<spirit_trait>":R( Text("%(spirit_trait)s", pause = 0.1)+Key("tab/40,equals")),
		#"<key_rule>": R(Key("%(key_rule)s/40")),

		#"close frame": R(Mouse("(0.998, 38), left")),#R(Key("a-f/40,enter")),
		#row and column right-click menu commands
		#uses menu, assthe es mouse is resting on row
		"<rc_item>": R(Mouse("left/40,right/40") +Key("%(rc_item)s,enter")),



		#mouse commands
		"(drag over|pull over| bring over| apply profile | apply this)": R(Mouse("left:down/60, <-800, 0>, left:down/80, left:up")),
		"pull up": R(Mouse("left:down/60, <0, -30>, left:up")),
		"pull down": R(Mouse("left:down/60, <0, 60>, left:up")),

		#menu control
		"<menu_title> [menu]": R(Key("alt/40, %(menu_title)s/40")),
		"frame [<m>]": R(Key("alt/40, w/40, %(m)s/40")),
	}
	extras = [
		Choice("menu_title", { #press alt...
			"file": "f",
			"close (frame|grid)": "f, enter",
			"logout": "f, up:2,enter",
			"import": "f,down:2,right,enter",
			"export": "f,down:3/40,right/40,enter",
			"export containers": "f,down:3/40,right/40,down/40,enter",


			"edit menu": "e",
			"view": "v",
			"reports": "r",

			"window|switch": "w",

			"help": "h",




		}),

		Choice("spirit_trait", {
			"plot prefix":"EXT:PLTPR",
			"plot status":"",
			"(material ID|mad ID)":"MAT:MATID",
			"trial ID":"EXT:TRLID",
			"line code":"MAT:LINE:LINCD",

			"login person code":"LOGIN:PERSN:CODE",

			#Traits
			"trait code":"UDTRT:UDTCD",



		}),
		Choice("item", {
			#assumes menu layout is:
			#Standard
			#Tools (Icons)
			#Query|Save, Print, etc.
			"query": "741,140",

			"people":"1073,81",
			"crop logins":"1105,81",


			"material management":"87, 130",
			"materials":"82, 160",
			"(trial|experiment) management":"87, 654",

			"lines": "87,66",
			"experiments": "87, 234",
			"plots":"87, 280",
			"trials":"87, 285",



			"advanced sort":"396, 70",

			"cell 1":"190, 135",
			"get table":"180, 128",
			"(last row|row last|row end)": "180, 1269",
			"row 1":"180, 145",

			"Entries ":"357, 214",
			"design":"427, 212",


		}),
		Choice("rc_item", {
				"view associated": "v",
				"view [associated] materials": "v/40, m/40",
				"view [associated] (parent materials|parents)": "v/40, p/40",
				"view [associated] subplots": "v/40, right/40, up:2",
				"view [associated] plots": "v/40, right/40, p/40",
				"view [associated] progeny": "v/40, right/40, up:4/40",
				"view [associated] (trial|trials)": "v/40, t/40",
				"(add|make) subplots": "a/40:2",

				"plant (trial|trials)":"p/40:3",
				"sort [down]":"up:8/10,right/10,down/10",
				"sort up":"up:8/10,right/10,down:2/10",

				#Favorites
				"set default profile":"up:2/40,right/40,down/40",
				"(new|save) profile":"up:2/40,right/40,up:2/40",
				"create new grouping":"up:2/40,right/40,up/40",

				"(edit|add|remove|change) (columns|profile)":"up:4/40",

				"remove":"r/10",
				"paste down":"p/10:2",
				"properties":"up/40",

		}),
		Choice("key_rule", {
			#query
			"next": "tab",
			"run query": "a-q",
			"append":"a-a",
			"close query": "a-s",
			"remove": "apps,r",
			"like": "l",

			#other commands
			"(okay|OK)":"a-o",
			"edit": "f2",
			"refresh": "f5/20",

			#Show Hide Columns
			"transfer":"tab,space,s-tab",
			"move":"s-tab:3",

		}),


		ShortIntegerRef("k", 1, 1000),
		ShortIntegerRef("n", 1, 100),
		ShortIntegerRef("m", 1, 10)

	]
	defaults = {"n": 1, "k": 1, "m":1, "nth": ""}


def get_rule():

	#return SpiritRule, RuleDetails(name="spirit", executable="SPIRITShell") #Local version
	return SpiritRule, RuleDetails(name="spirit", executable="appstreamclient") #Appstream
