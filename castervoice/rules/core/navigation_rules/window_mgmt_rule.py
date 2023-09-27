'''
Michael McMillen
'''
from dragonfly import MappingRule, Function, Repeat, Pause, Choice, ShortIntegerRef, Dictation
from castervoice.lib import utilities
from castervoice.lib import virtual_desktops
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.rules.core.navigation_rules import navigation_support
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class WindowManagementRule(MappingRule):
    mapping = {

        "letters": R(Key("csa-m")),#uses Fluent Search
        "snippet": R(Key("ws-s")),#uses snipping tool

        #Window Manipulation

        #screen zooming by Windows magnifier, note zoom in is w-equals, not w-plus!
        "(zoom screen| screen in)": R(Key("w-equals/20")),
        "(back screen| screen out) ": R(Key("w-minus/20")),
        "full-screen": R(Key("w-minus:4/40")),
        #uses fluent search
        "search <search_tag>":R(Key("alt:down,ctrl:down,ctrl:up,alt:up") + Pause("50") + Text("%(search_tag)s")),
        "search <search_tag> [for] <dict>":R(Key("alt:down,ctrl:down,ctrl:up,alt:up") + Pause("50") + Text("%(search_tag)s") + Key("tab")+ Text("%(dict)s")),
        #uses windows start menu

        #"search apps":R(Key("w-s/20")+ Text("apps: ")),
        #"search web":R(Key("w-s/20")+ Text("web: ")),
        "system tray": R(Key("w-t/20,tab/5,space")),

        "window isolate":
            R(Key("w-d/150, a-tab")),

        "(window close|close window )": R(Key("a-f4")),

        "window <direction> [<n>]":
            R(Key("w-%(direction)s"))*Repeat(extra="n"),
        #switches the position of the center window with either the left or right window
        "window switch left":
            R(Mouse("[601, 13], left")+
            Key("a-tab/20")+
            Pause("50")+
            Key("w-left")+
            #Pause("200")+
            Key("a-tab/20")+
            Pause("50")+
            Key("w-right")+
            Mouse("( 0.5, 0.5 )")),
        "window switch right":
            R(Mouse("[3000, 14], left")+
            Key("a-tab/20")+
            Pause("50")+
            Key("w-right")+
            #Pause("200")+
            Key("a-tab/20")+
            Pause("50")+
            Key("w-left")+
            Mouse("( 0.5, 0.5 )")),

        "window ( far |fly ) <direction> [<n>]":
            R(Key("ws-%(direction)s"))*Repeat(extra="n"),
        "(next | prior) window":
            R(Key("ca-tab, enter")),
        "show": R(Key("a-tab")),
        "show (window | windows)":
            R(Key("ca-tab"))*Repeat(extra="n"),
        #change screen
        #"switch screen": R(Key("w-p/10")),
        "computer <position>": R(Key("w-p/90, down/40:%(position)s, enter/40") + Pause("800") + Key("escape")+ Pause("200")+ Key("c-m")),
        #open window panes configuration, need to set in fancy zones
        "window ( zones | panes)":R(Key("ws-`")),
        # get mouse coordinates
        "get mouse coordinates":R(Key("cw-m")),
        "window snip":
            R(Key("ws-s")),
        "window max":
            R(Function(utilities.maximize_window)),
        "window (min|hide)":
            R(Function(utilities.minimize_window)),
	           "window swap":
            R(Key("ws-right")),
        "window resize":
            R(Mouse("(0.99, 0.99), left")),
        # Workspace management
        "show work [spaces]":
            R(Key("w-tab")),
        "(create | new) work [space]":
            R(Key("wc-d")),
        "close work [space]":
            R(Key("wc-f4")),
        "close all work [spaces]":
            R(Function(virtual_desktops.close_all_workspaces)),
        "next work [space] [<n>]":
            R(Key("wc-right"))*Repeat(extra="n"),
        "(previous | prior) work [space] [<n>]":
            R(Key("wc-left"))*Repeat(extra="n"),

        "go work [space] <n>":
            R(Function(virtual_desktops.go_to_desktop_number)),
        "send work [space] <n>":
            R(Function(virtual_desktops.move_current_window_to_desktop)),
        "move work [space] <n>":
            R(Function(virtual_desktops.move_current_window_to_desktop, follow=True)),
    }

    extras = [
        navigation_support.get_direction_choice("direction"),
        Dictation("dict"),
        Choice("search_tag", {
            "Windows": "",
            "web": "",
            "apps": "apps",
            "Bible": "bible",
        }),
        Choice("position", {
            "sit": 3,
            "stand": 1
        }),
        ShortIntegerRef("n", 1, 20, default=1),
        Choice("app_n", {
         	"1": 60,
            "2": 110,
            "3": 160,
            "4": 210,
            "5": 255,
            "6": 300,
            "7":  350, #files implemented directly, along with freeplane (maps)
            "8": 400,
            "9": 440,
            "10": 490,
            "11": 540,
            "12": 590,
            "13": 640,
            "14": 690,
            "15": 740,
            "16": 780,
            "17": 820,
            "18": 860,
            "19": 920,
            "20": 960
        }),
    ]
    defaults = {"search_tag": "Windows", "dict": ""}

def get_rule():
    details = RuleDetails(name="window management rule")
    return WindowManagementRule, details
