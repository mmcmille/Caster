
'''
Michael McMillen
independent Windows for tabs
dictation folder
'''
from dragonfly import Repeat, Pause, Function, Choice, MappingRule, ShortIntegerRef, Dictation

from castervoice.lib.actions import Key, Mouse, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve

class ChromeQuickFindRule(MappingRule):

    mapping = {
        #clicks link with text (requires Quick Find plug-in )
        #pauses in case there are multiple links
        "[click] <dict>":
            R(Key("singlequote")+ Pause("10")+ Text("%(dict)s") + Pause("300") +  Key("enter")),
        #select
        "get <dict>":
            R(Key("c-f")+ Pause("50")+ Text("%(dict)s")),
        "open [it]": R(Key("escape,enter")),
        "tab it": R(Key("escape, cs-enter")),
    }
    extras = [
        Dictation("dict"),

    ]
    defaults = {}

def get_rule():
    return ChromeQuickFindRule, RuleDetails(name="quick find", executable="chrome")
