'''
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

        #switches the position of the center window with either the left or right window
        "switch [window] left":
            R(Mouse("[601, 13], left")+
            Key("a-tab/20")+
            Pause("50")+
            Key("w-left")+
            #Pause("200")+
            Key("a-tab/20")+
            Pause("50")+
            Key("w-right")+
            Mouse("( 0.5, 0.5 )")),
        "switch [window] right":
            R(Mouse("[3000, 14], left")+
            Key("a-tab/20")+
            Pause("50")+
            Key("w-right")+
            #Pause("200")+
            Key("a-tab/20")+
            Pause("50")+
            Key("w-left")+
            Mouse("( 0.5, 0.5 )")),

        #app switching by listed number
        "(show|window) <n> [<close_choice>]":
            R(
                Key("w-t:%(n)s/5") +
                Key("enter") +
                Pause("50") +
                Mouse("(0.5, 0.5)") +
                Key("%(close_choice)s")
            ),

        #app switching via application name - Windows number , 1-10
        "show <app_name> [<close_choice>]":
            R(
                Key("cw-%(app_name)s/20") +
                Pause("50") +
                Mouse("(0.5, 0.5)") +
                Key("%(close_choice)s")
            ),
        #switches to last displayed app
        "show":
            R(
                Key("a-tab") +
                Pause("50") +
                Mouse("(0.5, 0.5)")
            ),
        #app switching via Fluent Search (change shortcut in app)
        "show <text>": R(Key("ca-w/60")+Text("%(text)s")),



        #transfers clipboard to Windows number , 1-10
        "copy <app_name>":
            R(
                Key("c-c") +
                Key("cw-%(app_name)s")
                #Mouse("(0.5, 0.5)")
            ),

        # get mouse coordinates
        "get mouse coordinates":R(Key("cw-m")),

        "snip window ":
            R(Key("ws-s")),
        "(max|maximize) (win|window)":
            R(Function(utilities.maximize_window)),
        "(minimize|hide) (win|window)":
            R(Function(utilities.minimize_window)),
	    "swap (win|window)":
            R(Key("ws-right")),
        "resize (win|window)":
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
        ShortIntegerRef("n_1_9", 1, 9),
        Dictation("text"),

        ShortIntegerRef("n", 1, 30, default=1),
        Choice("close_choice",{
            "close":"a-f4",
            "":"",
        }),
        Choice("app_name", {#can open individual programs through BringMe (opener), but it doesn't work for every program, save first if needed (do this for freeplane )
            "(web|chrome)": 1,
            "(email|mail|outlook)": 2,
            "(commands)": 3,
            "(files)": 4,
            "(copilot)": 5,
            "(Excel|notes)": 6,
            "(teams|chat|AI)": 7,
            "copilot": 8,
            "(spirit)": 9,
            #"(10)": 0,
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
        Choice("key_rule", {
            #Windows voice recognition,
            "Dictate":"w-h",
            "start menu": "win",
            "system tray": "w-t/20,tab/5,space",
            "show desktop": "w-d",
            "window isolate":"w-d/150, a-tab",
            "(pin|unpin) window":"wc-t", #uses power toys
            "(window close|close window )": "a-f4",
            "track": "f10", #command for Enable Viacam head tracking
            "click": "csa-m",#puts letters on the screen for navigation using Fluent Search
            "snippet": "ws-s",#uses snipping tool
            "[show|open] clipboard": "w-v",
            "drop clipboard": "w-v/80,enter",
            #uses power toys
            "get text": "ws-t",
            "screen ruler":"ws-m",
            #open window panes configuration, need to set in fancy zones
            "window ( zones | panes)":"ws-`",
            "two pains":"wca-2",
            "three pains":"wca-3",
        }),

    ]


def get_rule():
    details = RuleDetails(name="home computer rule")
    return HomeWindowManagementRule, details
