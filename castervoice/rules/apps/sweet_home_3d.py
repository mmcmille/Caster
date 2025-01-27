'''
Michael McMillen
'''


from dragonfly import Repeat, Pause, Function, Choice, MappingRule, ShortIntegerRef
from castervoice.lib.actions import Key, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve
class SweetHomeRule(MappingRule):#free plane
	mapping = {
		#generic key rule
		"<key_rule>": R(Key("%(key_rule)s/10")),
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
			"furniture": "u",
			"view": "v",
			"plan": "p",
			"3D view": "v",
			"help": "h",
		}),
		Choice("direction", {
			"up": "up",
			"down": "down",
			"left": "left",
			"right": "right",
		}),
		Choice("key_rule", {
			"select [mode]":"c-l",
			"hand|pan":"ca-p",
			"create walls":"cs-w",
			"create rooms":"a-r",
			"(create|add) dimensions":"cs-l",
			# menu items
			"preferences": "c-m",
		}),
	]
	defaults = {
		"m":1,
	}

def get_rule():
	return SweetHomeRule, RuleDetails(name="sweet home", title="Sweet Home")#title=window title
