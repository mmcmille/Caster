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

        #"<text>": R(Text("%(text)s ")),
        "scratch":R(Key("w-7")),
        "Open Cisco":
            R(BringApp(r"C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpnui.exe")),
        "open process [explorer]":
            R(BringApp(r"C:\Users\u581917\Apps Local\Utility\ProcessExplorer\procexp.exe")),
	   # "open citrix":
        #    R(BringApp(r"C:\Program Files (x86)\Citrix\ICA Client\SelfServicePlugin\SelfService.exe")),
        #"open spirit": R(BringApp(r"C:\Program Files (
        "[my] username": R(Text("u581917")+ Key("tab")),


        #hotstrings
        "password":R(Text("Q1w1e1rk")+ Pause("20") + Key("enter")),
        "my Syngenta email": R(Text("michael.mcmillen@syngenta.com")),

        #app switching via control clicks area on vertical taskbar
        " [<close_choice>] (show|open|switch|window) <app_n>":
            R(Key("control:down") +
              Mouse("".join(["[30,","%(app_n)s", "], left"])) +
              Key("control:up/20") +
              Pause("100")+
              Mouse("(0.5, 0.5)") +
              Key("%(close_choice)s")
              ),

        #"open <app_name> ":R(Key("alt:down,ctrl:down,ctrl:up,alt:up") + Pause("50") + Text("edge") + Key("tab") + Text("%(app_name)s") + Key("enter")),
    }

    extras = [
        Dictation("text"),
        Choice("app_name", {
            "email": "email",
        }),
        Choice("close_choice",{
            "close":"a-f4",
            "":"",
        }),
        Choice("app_n", {
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
