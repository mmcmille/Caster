from dragonfly import MappingRule, Function, Repeat, Pause, Choice, ShortIntegerRef

from castervoice.lib import utilities
from castervoice.lib import virtual_desktops
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.rules.core.navigation_rules import navigation_support
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class HomeWindowManagementRule(MappingRule):
    window_scale = 120 #system wide scale
    mapping = {

        #app switching via control clicks area on vertical taskbar
        "(open|switch|window|show) <app_n>":
            R(Key("control:down") +
              Mouse("".join(["[30,","%(app_n)s", "], left"])) +
              Key("control:up/20") +
              Pause("200")+
              Mouse("(0.5, 0.5)")
              ),
    }

    extras = [
        Choice("app_n", {
         	"(1|web)": 60,
            "(2|files)": 110,
            "(3|commands)": 160,
            "(4|commands)": 210,
            "5": 280,#255,
            "6": 350,#300,
            "7":  400,#350, #files implemented directly, along with freeplane (maps)
            "8": 440,#400,
            "9": 490,#440,
            "10": 540,#490,
            "11": 590,#540,
            "12": 640, #590,
            "13": 690, #640,
            "14": 740, #690,
            "15": 800, #740,
            "16": 850, #780,
            "17": 900, #820,
            "18": 950, #860,
            "19": 1000, #920,
            "20": 1050, #960
        }),
    ]


def get_rule():
    details = RuleDetails(name="home computer rule")
    return HomeWindowManagementRule, details
