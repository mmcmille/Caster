'''
Michael McMillen
'''


from dragonfly import Repeat, Pause, Function, Choice, MappingRule, ShortIntegerRef
from castervoice.lib.actions import Key, Mouse, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R
from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve

class MySQLWBRule(MappingRule):
	mapping = {
		#generic key rule
        "<key_rule>": R(Key("%(key_rule)s")),
		#menu control
		"<menu_title> [menu]": R(Key("alt/20, %(menu_title)s/20")),

	}
	extras = [
		Choice("key_rule", {
            "run it": "cs-enter",
		}),
		Choice("menu_title", {
			"file": "f",
			"edit menu": "e",
			"view": "v",
			"reports": "r",
			"window": "w",
			"help": "h",

			"import": "f,down:2,right,enter",

		}),
		ShortIntegerRef("k", 1, 1000),
		ShortIntegerRef("n", 1, 100),
		ShortIntegerRef("m", 1, 10)

	]
	defaults = {"n": 1, "k": 1, "m":1, "nth": ""}


def get_rule():

	return MySQLWBRule, RuleDetails(name="MySQL workbench", executable="MySQLWorkbench")
