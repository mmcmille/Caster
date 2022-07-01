'''
Michael McMillen
'''


from dragonfly import Repeat, MappingRule, Choice, Pause, ShortIntegerRef
from castervoice.lib.actions import Key, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

#double commander
class DoubleCommanderRule(MappingRule):
    mapping = {
        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s/40")),

        "rename <new_name>": R(Key('f2/20, %(new_name)s, enter')),
        "out [<n>]": R(Key('a-up/20') * Repeat(extra='n')),
        "search text": R(Key("a-f7") + Pause("100") + Key("tab/10") * Repeat(extra=5)  + Key("space")),
        "open T Drive": R(Key("c-p") + Text("t:/") + Key("enter")),
    }
    extras = [
        ShortIntegerRef("n", 1, 100),
        ShortIntegerRef("m", 1, 10),
        Choice("new_name", {
			"Q": "q.csv",
		}),
		Choice("key_rule", {
            "[switch] frame": "tab",
            "transfer": "escape/20, c-x/20,tab/20,c-v",
            "duplicate": "c-c,tab,c-v",
            "open": "c-p",
            "open with": "apps,h",
            "extract [all]": "escape, apps,t,enter",
            "Favorites": "c-d",
            "last": "a-left",
            "get filename": 'cs-n/20, a-tab',
            "get path": "c-p, c-c, escape/20, a-tab",
            "find [in] files": 'a-f7',
            "search": "a-f7",
            "properties": "apps,up,enter",
            "find [in] files": 'a-f7',
            "view": 'f3',
            "edit": 'f4',
            "move": 'f6',
            "new (directory | folder)": 'f7',
            "wipe": 's-delete',
            "trash it": "delete",
            "FTP": 'c-f',
            "synchronize": 'a-c, y',
            "sort by name": 'c-f3',
            "sort by extension": 'c-f4',
            "sort by date": 'c-f5',
            "sort by size": 'c-f6',
            "file filter": 'c-f12',
            "new tab": 'c-t',
            "rename": 'f2',
            "multi rename": 'c-m',
            "display thumbnails": 'cs-f1',
            "display list": 'c-f1',
            "display details": 'c-f2',
            "display file tree": 'c-f8',
            "link": "apps,s,enter",
		}),

    ]
    defaults = {"n": 1, "m":"", "nth": ""}


def get_rule():
    return DoubleCommanderRule, RuleDetails(name="double commander", executable="doublecmd")
