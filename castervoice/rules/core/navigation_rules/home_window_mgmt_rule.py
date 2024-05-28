
from dragonfly import Dictation, MappingRule, Function, Repeat, Pause, Choice, BringApp, ShortIntegerRef, RunCommand
from castervoice.lib import utilities
from castervoice.lib import virtual_desktops
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.rules.core.navigation_rules import navigation_support
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class HomeWindowManagementRule(MappingRule):
    mapping = {
        #command for Enable Viacam head tracking
        "track": R(Key("f10")),
        "letters": R(Key("csa-m")),#puts letters on the screen for navigation using Fluent Search
        "snippet": R(Key("ws-s")),#uses snipping tool


        #app switching via Windows number , 1-10
        "[<close_choice>] (show|open|window) <app_n_key>":
            R(
                Key("cw-%(app_n_key)s") +
                Pause("50") +
                Mouse("(0.5, 0.5)") +
                Key("%(close_choice)s")
            ),

        #app switching for windows 11+
        "[<close_choice>] (show|open|window) <app_n_11>": #<app_n>":
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

        #app switching via fluent search
        #"switch [<text>]": R(Key("csa-p") + Pause( "100") + Text("%(text)s ")),
        #"taskbar <n>": R(Key("w-%(n)s")),

        #transfers clipboard to Windows number , 1-10
        "copy <app_n_key>":
            R(
                Key("c-c") +
                Key("cw-%(app_n_key)s")
                #Mouse("(0.5, 0.5)")
            ),

        # "Open VPN":
        #    R(BringApp("C:\Program Files\Palo Alto Networks\GlobalProtect\PanGPA.exe")),

        "open process [explorer]":
            R(BringApp(r"C:\Users\u581917\Apps Local\Utility\ProcessExplorer\procexp.exe")),

    }

    extras = [
        ShortIntegerRef("n_1_9", 1, 9),
        Dictation("text"),
        Choice("close_choice",{
            "close":"a-f4",
            "":"",
        }),
        Choice("app_n_key", {#can open individual programs through BringMe (opener), but it doesn't work for every program, save first if needed (do this for freeplane )
            "(1|web)": 1,
            "(2|email|outlook)": 2,
            "(3|commands)": 3,
            "(4|files)": 4,
            "(5|spreadsheet|Calc)": 5,
            "(6|notes|one note)": 6,
            "(7|timer|tracker)": 7,
            "(8|teams)": 8,
            "(9|map)": 9,
            "(10|log)": 0,
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
    ]


def get_rule():
    details = RuleDetails(name="home computer rule")
    return HomeWindowManagementRule, details
