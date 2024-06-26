'''
Michael McMillen
'''

from dragonfly import Dictation, MappingRule, Function, Repeat, Pause, Choice, BringApp, ShortIntegerRef, RunCommand
from castervoice.lib import utilities
from castervoice.lib import virtual_desktops
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.rules.core.navigation_rules import navigation_support
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

#work window management
class WorkWindowManagementRule(MappingRule):
    x_pos = 60
    offset = 50
    mapping = {

        # Application Launching
        #"edit text": R(RunApp("notepad")),
        #"edit text": R(BringApp(r"C:\Users\u581917\OneDrive - Syngenta\Apps\npp.8.3.1.portable.x64\notepad++.exe")),
        #"edit everything": R(Key("c-a, c-x") + BringApp(r"C:\Users\u581917\OneDrive - Syngenta\Apps\npp.8.3.1.portable.x64\notepad++.exe") + Key("c-v")),
        #"edit region": R(Key("c-x") + R(BringApp(r"C:\Users\u581917\OneDrive - Syngenta\Apps\npp.8.3.1.portable.x64\notepad++.exe") + Key("c-v")),


        "scratch":R(Key("w-7")),
        "show desktop":R(Key("w-d")),
        "Open Cisco":
            R(BringApp(r"C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpnui.exe")),
        "open process [explorer]":
            R(BringApp(r"C:\Users\u581917\Apps Local\Utility\ProcessExplorer\procexp.exe")),
	   # "open citrix":
        #    R(BringApp(r"C:\Program Files (x86)\Citrix\ICA Client\SelfServicePlugin\SelfService.exe")),
        #"open spirit": R(BringApp(r"C:\Program Files (


        #app switching via Windows number , 1-10
        "[<close_choice>] (show|open|window) <app_n_key>":
            R(
                Key("cw-%(app_n_key)s") +
                Pause("100") +
                Key("%(close_choice)s")
            ),


        "[<close_choice>] (show|open|window) <app_n_11>": #<app_n>":
            R(
                Key("w-t/20, down:9") +
                Key("down:%(app_n_11)s, enter") +
                #Key("control:down") +
              #Mouse("".join(["[30,","%(app_n)s", "], left"])) +
              #Key("control:up/20") +
                Pause("100")+
                Key("%(close_choice)s")),

        #app switching via fluent search
        "switch [<text>]": R(Key("csa-p") + Pause( "100") + Text("%(text)s ")),
        #"taskbar <n>": R(Key("w-%(n)s")),

    }

    extras = [
        ShortIntegerRef("n_1_9", 1, 9),
        Dictation("text"),
        Choice("close_choice",{
            "close":"a-f4",
            "":"",
        }),
        Choice("app_n_key", {
            "(1|email)": 1,
            "(2|planner)": 2,
            "(3|edge|web)": 3,
            "(4|notes)": 4,
            "(5|commands|rules)": 5,
            "(6|files)": 6,
            "(7|writer)": 7,
            "(8|sheets)": 8,
            "9": 9,
            "10": 0,
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
        Choice("app_n_coord", {
            #100% Scale,
            "(1|email)": 64,#"(1|mail|email)": 64,
            "(2|planner)": 110,
            "(3|edge|web)": 160,
            "(4|notes)": 210,
            "(5|commands|rules)": 255,
            "(6| files)": 300,
            "7": 350, #files implemented directly, along with freeplane (maps)
            "8": 400,
            "9": 440,
            "10": 490,
            "11": 540,
            "12":  590,
            "13":  640,
            "14":  690,
            "15":  740,
            "16":  780,
            "17":  820,
            "18":  860,
            "19":  920,
            "20":  960
        }),
    ]


def get_rule():
    details = RuleDetails(name="work computer rule")
    return WorkWindowManagementRule, details
