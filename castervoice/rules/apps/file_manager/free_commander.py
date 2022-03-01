'''
Michael McMillen
'''

from dragonfly import MappingRule, Choice
from castervoice.lib.actions import Key
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class FreeCommanderRule(MappingRule):
    mapping = {
        #generic key rule
		"<key_rule>": R(Key("%(key_rule)s/40")),


    }
    extras = [
		Choice("key_rule", {
			"save all": "a-s",
			# navigation
	        "get filename": 'c-n',
            "get path": 'c-p',
            "find [in] files": 'a-f7',
            "view": 'f3',
            "edit": 'f4',
            "copy": 'f5',
            "move": 'f6',
            "new (directory | folder)": 'f7',
            "wipe": 's-delete',
            "FTP": 'c-f',
            "synchronize": 'a-c, y',
            "sort by name": 'c-f3',
            "sort by extension": 'c-f4',
            "sort by date": 'c-f5',
            "sort by size": 'c-f6',
            "file filter": 'c-f12',
            "new tab": 'c-t',
            "multi rename": 'c-m',
            "display thumbnails": 'cs-f1',
            "display list": 'c-f1',
            "display details": 'c-f2',
            "display file tree": 'c-f8',
		}),
	]
	#defaults = {
	#}

def get_rule():
    return FreeCommanderRule, RuleDetails(name="free commander", executable="FreeCommander")
