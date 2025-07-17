'''
Michael McMillen
'''


from dragonfly import Repeat, MappingRule, Choice, Pause, ShortIntegerRef, Dictation
from castervoice.lib.actions import Key, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

#double commander
class OneCommanderRule(MappingRule):
    mapping = {

        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s/10")),
        #tab navigation
        "(next | right | down) tab [<n>]":
            R(Key("c-tab/20"))*Repeat(extra="n"),
        "(prior | left | up ) tab [<n>]":
            R(Key("cs-tab/20"))*Repeat(extra="n"),

        "rename <new_name>": R(Key('f2/20, %(new_name)s, enter')),
        "out [<n>]": R(Key('a-up/20') * Repeat(extra='n')),
        "search text": R(Key("a-f7") + Pause("100") + Key("tab/10") * Repeat(extra=5)  + Key("space")),
        #"open T Drive": R(Key("c-p") + Text("t:/") + Key("enter")),
        "<dict>": R(Text("%(dict)s")),

    }
    extras = [
        ShortIntegerRef("n", 1, 100),
        ShortIntegerRef("m", 1, 10),
        Dictation("dict"),
        Choice("new_name", {
			"Q": "q.csv",
		}),
		Choice("key_rule", {
            "restore tab": "cs-t",
            "(focus|switch) [frame]": "a-f",
            "transfer": "a-m",
            "duplicate": "a-c",
            "open": "c-p",
            "open with": "apps,h",
            "extract [all]": "escape, apps,t,enter",
            "extract here": "escape, apps/40,down:5/20,enter",
            "Favorites": "c-d",
            "last": "a-left",
            "link": "cs-c, a-tab",
            "(get|copy|web) link": "apps/80,v/20,up:2/20,enter",
            "get filename": 'cs-n/20, a-tab',
            "get path": "cs-c, a-tab",
            "find [in] files": 'a-f7',
            "search": "a-f7",
            "properties": "apps,up,enter",
            "find [in] files": 'a-f7',
            "view": 'f3',
            "address [bar]": 'a-d',
            "move": 'f6',
            "new (directory | folder)": "cs-n",
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
            "new folder": "cs-n",
            "rename": 'f2',
            "multi rename": 'c-m',
            "display thumbnails": 'cs-f1',
            "display list": 'c-f1',
            "display details": 'c-f2',
            "display file tree": 'c-f8',
		}),

    ]
    defaults = {"n": 1, "m":"",
        "nth": "",
        "dict": "",
    }


def get_rule():
    return OneCommanderRule, RuleDetails(name="one commander", executable="onecommander")
