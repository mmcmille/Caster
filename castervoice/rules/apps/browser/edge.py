
'''
Michael McMillen
independent Windows for tabs
dictation folder
'''
from dragonfly import Repeat, Pause, Function, Choice, MappingRule, Dictation, ShortIntegerRef

from castervoice.lib.actions import Key, Mouse, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve

class EdgeRule(MappingRule):
    mapping = {
        #temporary rule for virtual mint fulfillment ,
        # uses an excel file with source container ids in one column, and envelope container ids in the column to the right
        #"transfer": R(Key("a-tab") + Pause("100") + Key("right, c-c/20, a-tab") + Pause("100")+Key("c-v,enter")),
        #"next": R(Key("cs-n/80") + Text("38") + Key("enter")+ Pause("100") + Key("cs-n/80") + Text("39") + Key("enter, a-tab/20") + Pause("100") + Key("down,left")+ Key("c-c/20, a-tab") + Pause("100") + Key("c-v/20, enter") + Pause("300") + Key("a-tab") + Pause("100") + Key("right, c-c/20, a-tab") + Pause("100")+Key("c-v,enter")),


        #Google Sheets
        #menu control
        "<menu_title> menu": R(Key("as-%(menu_title)s/20")),

        "(next | right) sheet [<n>]":
            R(Key("a-down/20"))*Repeat(extra="n"),
        "(prior | left) sheet [<n>]":
            R(Key("a-up/20"))*Repeat(extra="n"),


        #formative rules
        "score <m>": R(Key("%(m)s/40") + Key("tab:2/20")),#scores for converting to rubric

        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s")),

        "[click] <click_item>": R(Mouse("(%(click_item)s), left")),
        "tab here": R(Key("ctrl:down, shift:down") + Mouse("left") + Key("ctrl:up, shift:up")),

        #gmail,   ...outlook online rules
        #moved to folder
        #"move (it|to) [<dict>]": R(Key("v") + Pause(" 100")+ Text("%(dict)s")),#R(Mouse("(341, 152), left")+ Pause(" 100")+ Text(" %(dict)s")),
        "flag it": R(Mouse("(246, 146), left")),
        "trash it": R(Key("s-3")), #R(Mouse("(443, 148), left")),#510, 158
        "send (it|email)": R(Key("tab:3/20,enter")),
        "discard it": R(Key("tab:4/40")),

        "link":
            R(Key("a-c/50, a-tab")),
        "link <m>": R(Key("a-c/50, w-%(m)s")),
        "link map": R(Key("a-c/50, w-9/1")),#assumes map is output window 9
        "link notes ": R(Key("a-c/50, w-5/1")),#assumes onenote  is output window 6
        "find": R(Key("c-f")),
        "previous": R(Key("a-left")),
	    "duplicate tab":
            R(Key("cs-k")),

       #Plug-ins
       #Midnight
       "midnight":
            R(Key("as-m")),
       #click by voice
       "refresh (buttons | numbers)":
            R(Key("cs-space/100") + Text(":-") + Key("enter")) + Pause("80") +
            R(Key("cs-space/80") + Text(":+") + Key("enter")),
       "show (buttons | numbers)":
            R(Key("cs-space/80") + Text(":+") + Key("enter")),
       "hide (buttons | numbers)":
            R(Key("cs-space/100") + Text(":-") + Key("enter")),
        "<k>": R(Key("cs-space/40") + Text("".join(["%(k)s"])) + Pause("20") + Key("enter")),
        "<voice_action> <k>":
            R(Key("cs-space/20") + Text("".join(["%(k)s", "%(voice_action)s"])) + Pause("20") + Key("enter")),

            #Page scrolling
    	#"scroll [<read_dir>] [<read_speed>]":
    	#	R(Key("escape") + Mouse("".join(["(0.97, 0.5), middle, <0, ","%(read_dir)s", "%(read_speed)s", ">"]))),
        "scroll (here|this|it) [<read_dir>] [<read_speed>]": #current mouse location
            R(Mouse("".join(["middle, <0, ","%(read_dir)s", "%(read_speed)s", ">"]))),
        "scroll right [<read_dir>] [<read_speed>]": #right side
        R(Mouse("".join(["(0.97, 0.5), middle, <0, ","%(read_dir)s", "%(read_speed)s", ">"]))),
        "scroll left [<read_dir>] [<read_speed>]": #left side
            R(Mouse("".join(["(12, 0.5), middle, <0, ","%(read_dir)s", "%(read_speed)s", ">"]))),
        "skip":
    		R(Mouse("<0,60>") + Pause("20") + Mouse("<0,-60>") ),
    	"stop [it]":R(Key("escape")),

        "(new window|win new)":
            R(Key("c-n")),
        "(new incognito window | incognito)":
            R(Key("cs-n")),
        #"new tab [<n>]|tab new [<n>]": R(Key("c-t") * Repeat(extra="n")),
        "search (it|this)": R(Key("c-c/20, c-t, c-v, enter")),
        "restore tab [<n>]|tab reopen [<n>]":
            R(Key("cs-t")) * Repeat(extra="n"),
        #"close tab [<n>]|tab close [<n>]":
        #    R(Key("c-w")) * Repeat(extra='n'),
        "win close|close all tabs":
            R(Key("cs-w")),
        "(next|forward) tab [<n>]|tab (right|sauce) [<n>]":
            R(Key("c-tab/40")) * Repeat(extra="n"),
        "(back|previous) tab [<n>]|tab (left|lease) [<n>]":
            R(Key("cs-tab/40")) * Repeat(extra="n"),
        "new tab that":
            R(Mouse("middle") + Pause("20") + Key("c-tab")),
        "(back|prev|prior|previous) page [<n>]":
            R(Key("a-left/20")) * Repeat(extra="n"),
        "(next|forward) page [<n>]":
            R(Key("a-right/20")) * Repeat(extra="n"),
        "zoom in [<n>]":
            R(Key("c-plus/20")) * Repeat(extra="n"),
        "zoom out [<n>]":
            R(Key("c-minus/20")) * Repeat(extra="n"),
        "zoom reset":
            R(Key("c-0")),
        "(hard refresh|super refresh)":
            R(Key("c-f5")),
        "find (next|forward) [match] [<n>]":
            R(Key("c-g/20")) * Repeat(extra="n"),
        "find (back|prev|prior|previous) [match] [<n>]":
            R(Key("cs-g/20")) * Repeat(extra="n"),
        # requires an extension in some browsers such as chrome
        "[toggle] caret browsing":
            R(Key("f7")),
        "(show|hide) cursor":
            R(Key("")),
        "[show] history":
            R(Key("c-h")),
        "address bar":
            R(Key("c-l")),
        "[show] downloads":
            R(Key("c-j")),
        "[add] bookmark":
            R(Key("c-d")),
        "bookmark all [tabs]":
            R(Key("cs-d")),
       "[show] bookmarks":
            R(Key("cs-o")),
        "[toggle] full screen":
            R(Key("f11")),
        "(show|view) page source":
            R(Key("c-u")),


        "step over":
            R(Key("f10")),
        "step into":
            R(Key("f11")),
        "step out":
            R(Key("s-f11")),
        "(duplicate tab|tab duple)":
            R(Key("a-d,a-c,c-t/15,c-v/15, enter")),
        "(duplicate window|win duple)":
            R(Key("a-d,a-c,c-n/15,c-v/15, enter")),
        "[show] (menu | three dots)":
            R(Key("a-f")),
        "[show] settings":
            R(Key("a-f/5, s")),
        "[show chrome] task manager":
            R(Key("s-escape")),
        "(clear history|clear browsing data)":
            R(Key("cs-del")),
        "[show] developer tools":
            R(Key("cs-i")),
        "checkout [this] pull request [locally]":
            R(Function(github_automation.github_checkoutupdate_pull_request, new=True)),
        "update [this] pull request [locally]":
            R(Function(github_automation.github_checkoutupdate_pull_request, new=False)),
        "IRC identify":
            R(Text("/msg NickServ identify PASSWORD")),
        "tab <m>|<nth> tab":
            R(Key("c-%(m)s%(nth)s")),
        "second last tab":
            R(Key("c-9, cs-tab")),




        "[toggle] bookmark bar":
            R(Key("cs-b")),


        "focus notification":
            R(Key("a-n")),
        "allow notification":
            R(Key("as-a")),
        "deny notification":
            R(Key("as-a")),
        "google that":
            R(Store(remove_cr=True) + Key("c-t") + Retrieve() + Key("enter")),
        "wikipedia that":
            R(Store(space="+", remove_cr=True) + Key("c-t") + Text(
                "https://en.wikipedia.org/w/index.php?search=") + Retrieve() + Key("enter")),
        "[show] (extensions|plugins)":
            R(Key("a-f/20, l, e/15, enter")),
        "more tools":
            R(Key("a-f/5, l")),
    }
    extras = [
        Dictation("dict"),
        Choice("nth", {
                "first": "1",
                "second": "2",
                "third": "3",
                "fourth": "4",
                "fifth": "5",
                "sixth": "6",
                "seventh": "7",
                "eighth": "8",
                "(ninth|last)":"9",
            }),
        Choice("voice_action", {
                "go": "",
                "click on": ":c",
                "tab [on]": ":t",
                "(next | page)": ":b",#tab behind
                "hover": ":h",
                "(get|copy)": ":s",
            }),
        Choice("read_speed", {
		"slow":"20",
		"fast":"80",
		}),
    	Choice("read_dir", {
    		"up":"-",
    		"down":"",
    		}),
	    ShortIntegerRef("k", 0, 10000),
        ShortIntegerRef("n", 1, 100),
        ShortIntegerRef("m", 0, 10),
        Choice("click_item", {
    		"true":"288, 881",
    		"false":"257, 927",
            "submit":"835, 1002",
            "continue":"747, 944",
    		}),
        Choice("menu_title", {
			"file": "f",
			"edit": "e",
			"view": "v",
			"insert": "i",
            "format": "o",
            "sheet": "s",
            "data": "d",
            "tools": "t",
            "window": "w",
			"help": "h",
		}),
        Choice("key_rule", {
            "switch mode": "f7",
            "next": "tab:1",
           #"drop text": "cs-v",

           "out": "a-left",

           # spreadsheet
           "edit": "f2",
           "drop date": "c-semicolon",
           #google slides
           "grid view": "ca-1",
           #"canvas view": "csa-c",#Move to canvas	Ctrl + Alt + Shift + c
           #Google Sheets Shortcuts
           #https://support.google.com/docs/answer/181110?hl=en&co=GENIE.Platform%3DDesktop#zippy=%2Cpc-shortcuts
           "get column":"c-space",
           "get row":"s-space",
           #"right sheet":"a-down",
           #"left sheet":"a-up",
           "delete row":"sa-e/20,d/20,d",
        }),
    ]
    defaults = {"n": 1, "k": 1, "m":"", "nth": "", "read_speed":"40","read_dir" : ""}


def get_rule():
    return EdgeRule, RuleDetails(name="edge", executable="msedge")
