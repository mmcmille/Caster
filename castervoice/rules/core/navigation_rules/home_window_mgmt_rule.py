'''


#app switching for windows 11+
"[<close_choice>] (open|show|window) <app_n_11>": #<app_n>":
    R(
        Key("w-t/5, right:9") + #down if vertical taskbar, right if horizontal
        Key("right:%(app_n_11)s, enter") +
        Pause("50") +
        Mouse("(0.5, 0.5)") +

        #Key("control:down") +
      #Mouse("".join(["[30,","%(app_n)s", "], left"])) +
      #Key("control:up/20") +
        Pause("100")+
        Key("%(close_choice)s")),
'''


from dragonfly import Dictation, MappingRule, Function, Repeat, Pause, Choice, BringApp, ShortIntegerRef, RunCommand
from castervoice.lib import utilities
from castervoice.lib import virtual_desktops
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.rules.core.navigation_rules import navigation_support
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class HomeWindowManagementRule(MappingRule):
    mapping = {

        #generic key rule
		"<key_rule>": R(Key("%(key_rule)s/5")),

        #moves window to the direction indicated
        "(window|win) <direction> [<n>]":
            R(Key("w-%(direction)s"))*Repeat(extra="n"),
        #stretches window to the left or right
        "(window|win) (span|stretch) <direction> [<n>]":
            R(Key("wca-%(direction)s"))*Repeat(extra="n"),
        "(span|stretch) (window|win) <direction> [<n>]":
            R(Key("wca-%(direction)s"))*Repeat(extra="n"),
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


        #app switching by listed number
        "[<close_choice>] (open|show|window) <n>":
            R(
                Key("w-t:%(n)s/20") +
                Key("enter") +
                Pause("50") +
                Mouse("(0.5, 0.5)") +
                Key("%(close_choice)s")
            ),

        #app switching via Windows number , 1-10
        "[<close_choice>] (open|show|window) <app_n_key>":
            R(
                Key("cw-%(app_n_key)s/10") +
                Pause("50") +
                Mouse("(0.5, 0.5)") +
                Key("%(close_choice)s")
            ),
        #app switching via switcheroo
        "window": R(Key("w-`/20")),
        "window <app_name>": R(Key("w-`/20")+Text("%(app_name)s")+Key("enter")),
        ##"window <text>": R(Key("w-`/20")+Text("%(text)s")),
        #displays Windows to switch to
        "show (window | windows)":
            R(Key("ca-tab"))*Repeat(extra="n"),

        #switches to last displayed app
        "show":
            R(
                Key("a-tab") +
                Pause("50") +
                Mouse("(0.5, 0.5)")
            ),
        #transfers clipboard to Windows number , 1-10
        "copy <app_n_key>":
            R(
                Key("c-c") +
                Key("cw-%(app_n_key)s")
                #Mouse("(0.5, 0.5)")
            ),

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

        #
        "window <text>": R(Key("w-`/20")+Text("%(text)s")),
    }

    extras = [
        navigation_support.get_direction_choice("direction"),
        ShortIntegerRef("n_1_9", 1, 9),
        Dictation("text"),

        ShortIntegerRef("n", 1, 30, default=1),
        Choice("close_choice",{
            "close":"a-f4",
            "":"",
        }),
        Choice("app_n_key", {#can open individual programs through BringMe (opener), but it doesn't work for every program, save first if needed (do this for freeplane )
            "(web)": 1,
            "(calendar|email|outlook)": 2,
            "(commands)": 3,
            "(files)": 4,
            "(notes|one note)": 5,
            "(Excel)": 6,
            "(teams)": 7,
            "(spirit)": 8,
            "(map)": 9,
            #"(10)": 0,
        }),
        Choice("app_name", {
        "email":"Outlook",
        "files":"OneCommander",
        "notes": "onenote",
        "spirit":"spirit",
        }),
        Choice("app_n_11", {
            "11": 1,
            "12":  2,
            "13":  3,
            "14":  4,
            "15":  5,
            "16":  6,
            "17":  7,
            "18":  8,
            "19":  9,
            "20":  10
        }),
        Choice("app_n", {
         	"(1|web)": 64,
            "(2|files)": 111,#+47@100%
            "(3|commands)": 158,
            "(4|notes)": 205,
            "(5|)": 252,
            "6": 299,
            "7": 346,
            "8": 393,
            "9": 440,
            "10": 487,
            "11": 534,
            "12": 581,
            "13": 628,
            "14": 675,
            "15": 722,
            "16": 769,
            "17": 816,
            "18": 863,
            "19": 910,
            "20": 957,
        }),
        Choice("key_rule", {
            "start menu": "win",
            "system tray": "w-t/20,tab/5,space",
            "show desktop": "w-d",
            "window isolate":"w-d/150, a-tab",
            "(pin|unpin) window":"wc-t", #uses power toys
            "(window close|close window )": "a-f4",
            "track": "f10", #command for Enable Viacam head tracking
            "click": "csa-m",#puts letters on the screen for navigation using Fluent Search
            "snippet": "ws-s",#uses snipping tool
            "(show|open) clipboard": "w-v",
            "drop clipboard": "w-v/80,enter",
            #uses power toys
            "get text": "ws-t",
            "screen ruler":"ws-m",
        }),

    ]


def get_rule():
    details = RuleDetails(name="home computer rule")
    return HomeWindowManagementRule, details
