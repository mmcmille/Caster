from dragonfly import MappingRule, Function, Repeat, Pause, Choice

from castervoice.lib import utilities
from castervoice.lib import virtual_desktops
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.rules.core.navigation_rules import navigation_support
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class HomeWindowManagementRule(MappingRule):
    mapping = {

        #app switching via control clicks area on vertical taskbar
        "(show|open|switch|window) <app_n>":
            R(Key("control:down") +
              Mouse("".join(["[30,","%(app_n)s", "], left"])) +
              Key("control:up/20") +
              Pause("200")+
              Mouse("(0.5, 0.5)")
              ),
    }

    extras = [
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
