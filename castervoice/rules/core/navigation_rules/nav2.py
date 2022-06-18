'''
Michael McMillen
'''

from dragonfly import Function, Repeat, Dictation, Choice, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key, Mouse
from castervoice.lib import navigation, utilities
from castervoice.rules.core.navigation_rules import navigation_support

try:  # Try first loading from caster user directory
    from alphabet_rules import alphabet_support
except ImportError:
    from castervoice.rules.core.alphabet_rules import alphabet_support

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.actions import AsynchronousAction
from castervoice.lib.merge.state.short import S, L, R


class NavigationNon(MappingRule):

    pronunciation = "navigation companion"

    mapping = {
        "<direction> <time_in_seconds>":
            AsynchronousAction(
                [L(S(["cancel"], Key("%(direction)s"), consume=False))],
                repetitions=1000,
                blocking=False),
        "erase multi clipboard":
            R(Function(navigation.erase_multi_clipboard)),
        "find":
            R(Key("c-f")),
        "find next [<n>]":
            R(Key("f3"))*Repeat(extra="n"),
        "find prior [<n>]":
            R(Key("s-f3"))*Repeat(extra="n"),
        "find everywhere":
            R(Key("cs-f")),
        "replace":
            R(Key("c-h")),
        "[show] context menu":
            R(Key("s-f10")),
        "lean":
            R(Function(navigation.right_down)),
        "hoist":
            R(Function(navigation.right_up)),
        "kick mid":
            R(Function(navigation.middle_click)),
        "shift right click":
            R(Key("shift:down") + Mouse("right") + Key("shift:up")),
        "mouse <direction> [<direction2>] [<nnavi500>] [<dokick>]":
            R(Function(navigation.curse)),
        #places mouse cursor in position of 3x3 grid, and presses f11 to start tracking if needed
        "mouse <mouse_grid> [<track_choice>]":
            R(Mouse("(%(mouse_grid)s)")+ Key("%(track_choice)s")),
        "[mouse] track": R(Key("f11")),

        "wheel <direction> [<nnavi500>]":
            R(Function(navigation.wheel_scroll)),
        "scree <direction> <time_in_seconds>":
            R(AsynchronousAction(
                [L(S(["cancel"], Function(navigation.wheel_scroll, nnavi500=1)))],
                repetitions=1000,
                blocking=False)),

        "colic":
            R(Key("control:down") + Mouse("left") + Key("control:up")),
        "garb [<nnavi500>]":
            R(Mouse("left") + Mouse("left") + Function(
                navigation.stoosh_keep_clipboard)),
        "drop mouse [<nnavi500>]":
            R(Mouse("left") + Mouse("left") + Function(
                navigation.drop_keep_clipboard,
                capitalization=0,
                spacing=0)),
        #implemented in each app "drop text":R(Key("cs-u")),
        "refresh":
            R(Key("c-r")),
        "maxiwin":
            R(Key("w-up")),
        "move window":
            R(Key("a-space, r, a-space, m")),
        "window (left | lease) [<n>]":
            R(Key("w-left"))*Repeat(extra="n"),
        "window (right | ross) [<n>]":
            R(Key("w-right"))*Repeat(extra="n"),
        "monitor (left | lease) [<n>]":
            R(Key("sw-left"))*Repeat(extra="n"),
        "monitor (right | ross) [<n>]":
            R(Key("sw-right"))*Repeat(extra="n"),
        "(next | prior) window":
            R(Key("ca-tab, enter")),
        "switch (window | windows)":
            R(Key("ca-tab"))*Repeat(extra="n"),
        "(next | right ) tab [<n>]":
            R(Key("c-pgdown/20"))*Repeat(extra="n"),
        "(prior | last | left ) tab [<n>]":
            R(Key("c-pgup/20"))*Repeat(extra="n"),
        "close (tab|it) [<n>]":
            R(Key("c-w/40"))*Repeat(extra="n"),
        "new tab [<n>]":
            R(Key("c-t/20"))*Repeat(extra="n"),
        "elite translation <text>":
            R(Function(alphabet_support.elite_text)),
    }

    extras = [
        Dictation("text"),
        Dictation("mim"),
        ShortIntegerRef("function_key", 1, 13),
        ShortIntegerRef("n", 1, 50),
        ShortIntegerRef("nnavi500", 1, 500),
        Choice("time_in_seconds", {
            "super slow": 5,
            "slow": 2,
            "normal": 0.6,
            "fast": 0.1,
            "superfast": 0.05
        }),
        navigation_support.get_direction_choice("direction"),
        navigation_support.get_direction_choice("direction2"),
        navigation_support.TARGET_CHOICE,
        Choice("dokick", {
            "kick": 1,
            "psychic": 2
        }),
        Choice("wm", {
            "ex": 1,
            "tie": 2
        }),
        Choice("mouse_grid", {
            "top": "0.5, 25",
            "1": "0.17, 0.17",
            "2": "0.5, 0.17",
            "3": "0.83, 0.17",
            "4": "0.17, 0.5",
            "(5|center)": "0.5, 0.5",
            "6": "0.83, 0.5",
            "7": "0.17, 0.83",
            "8": "0.5, 0.83",
            "9": "0.83, 0.83",
        }),
        Choice("track_choice",{
            "track":"f11",
            "":"",
        }),

    ]
    defaults = {
        "n": 1,
        "mim": "",
        "nnavi500": 1,
        "direction2": "",
        "dokick": 0,
        "text": "",
        "wm": 2
    }


def get_rule():
    return NavigationNon, RuleDetails(name="navigation companion")
