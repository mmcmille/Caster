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
			"over ": "a-tab",
			"okay":"a-o",
			# "cancel":"a-c", # esc will also cancel

			# menu items
			"preferences": "c-comma",
			"save all": "a-f/10, a",#"a-s",
			"(copy|get) branch": "cs-c",
			"(copy|get) [node] ID": "a-e/10,c,c",# "cs-i",
			"[get] (link|address)": "a-e/10,c,o",

			#format
			"edit styles": "c-f11",

			# navigation
			"last": "a-left",
			"next": "a-right",
			"(jump in|isolate)":"s-escape",
			"jump out":"a-n,m",

			"next":"enter,enter",

			"fold [it]": "space",
			"(fold|collapse) all": "a-home",
			"unfold all": "a-end",
			"outline view": "a-v/10,v,o", #"cs-o",
			"edit styles": "c-f11",

			# filter
			"search": "cs-j",
			"filter": "c-f",
			"clear filter": "a-i,n",#"ca-f",

			#split
			"split here": "a-s",

			"split dot": "ca-dot",
			"split comma": "ca-comma",

			#edit
			"edit": "end",
			"edit dialogue": "a-enter",
			"edit note":"a-e/10,n,e",
			"title it":"ca-c",
			"(capitalize| cap) this":"ca-up",
			"(all caps|title) this":"ca-c",

			#nodes
			"(insert|big bro)": "s-enter",
			"(child|kid)": "tab",
			"(paste|drop) clone": "c-d",
			"summary node": "a-r/10,n,w",

			#links
			"open link": "c-enter",
			"edit link": "c-k",
			"get link": "a-e/10, c, c",

			#view
			"center ( view | node )": "ca-c",
			"new (window|view)": "a-v/10,e",#"ca-v",
			"tool (panel|bar)":"a-v/10,c,o",

			#icons
			"info icon ": "ca-i",
			"school":"",
			"(clear|remove) (icon | icons )": "a-r/10,o,r,e", #"cs-d",
			"project icon": "a-r/10,o,i,o,l",
			"task icon": "a-r/10,o,i,s,m",
			"checked": "a-r,o,i,s,c",#"c-2",
			"unchecked": "a-r/10,o,i,s,u",# "c-1",

		}),
	]
	defaults = {
		"m":1,
	}

def get_rule():
	return FreeplaneRule, RuleDetails(name="freeplane", title="Freeplane")
