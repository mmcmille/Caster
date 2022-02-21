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
            "(3|commands)": 210,
            "(4|commands)": 250,
            "5": 280,#255,
            "6": 350,#300,
            "7":  400,#350, #files implemented directly, along with freeplane (maps)
            "8": 440,#400,
            "9": 510,#440,
            "ten": 540,#490,
            "eleven": 590,#540,
            "twelve": 640, #590,
            "thirteen": 690, #640,
            "fourteen": 740, #690,
            "fifteen": 800, #740,
            "sixteen": 850, #780,
            "seventeen": 900, #820,
            "eighteen": 950, #860,
            "nineteen": 1000, #920,
            "twenty": 1050, #960
        }),
    ]


def get_rule():
    details = RuleDetails(name="home computer rule")
    return HomeWindowManagementRule, details
