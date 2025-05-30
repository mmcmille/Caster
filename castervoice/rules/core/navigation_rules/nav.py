'''
Michael McMillen
'''

from dragonfly import Function, Repeat, Dictation, Choice, Pause, Text, ContextAction, ShortIntegerRef
from castervoice.lib.context import AppContext

from castervoice.lib import navigation, context, textformat, text_utils
from castervoice.rules.core.navigation_rules import navigation_support
from dragonfly.actions.action_mimic import Mimic

from castervoice.lib.actions import Key, Mouse
from castervoice.rules.ccr.standard import SymbolSpecs

try:  # Try first loading from caster user directory
    from punctuation_rules.punctuation_support import double_text_punc_dict, text_punc_dict
except ImportError:
    try:  # Try  first loading from caster user directory top level
        from punctuation_support import double_text_punc_dict, text_punc_dict
    except ImportError:
        from castervoice.rules.core.punctuation_rules.punctuation_support import double_text_punc_dict, text_punc_dict

try:
    from keyboard_rules import keyboard_support
except ImportError:
    try:
        from keyboard_support import keyboard_support
    except ImportError:
        from castervoice.rules.core.keyboard_rules import keyboard_support

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.actions import AsynchronousAction, ContextSeeker
from castervoice.lib.merge.state.actions2 import UntilCancelled
from castervoice.lib.merge.state.short import S, L, R

_tpd = text_punc_dict()
_dtpd = double_text_punc_dict()


for key, value in _dtpd.items():
    if len(value) == 2:
        _dtpd[key] = value[0] + "~" + value[1]
    elif len(value) == 4:
        _dtpd[key] = value[0:1] + "~" + value[2:3]
    else:
        msg = "Need to deal with nonstandard pair length in double_text_punc_dict: {}"
        raise Exception(msg.format(str(value)))


class Navigation(MergeRule):
    pronunciation = "navigation"

    mapping = {
        # "periodic" repeats whatever comes next at 1-second intervals until "terminate"
        # or "escape" (or your SymbolSpecs.CANCEL) is spoken or 100 tries occur
        "(repeat | periodic) command ":
            ContextSeeker(forward=[
                L(
                    S(["cancel"], lambda: None),
                    S(["*"],
                      lambda fnparams: UntilCancelled(
                          Mimic(*filter(lambda s: s != "periodic", fnparams)), 1).execute(
                          ),
                      use_spoken=True))
            ]),
        # VoiceCoder-inspired -- these should be done at the IDE level

#        "fill <target>":
#            R(Key("escape, escape, end"), show=False) +
#            AsynchronousAction([L(S(["cancel"], Function(context.fill_within_line)))],
        "go in":
            AsynchronousAction([L(S(["cancel"], context.nav, ["right", "(~[~{~<"]))],
                               time_in_seconds=0.01,
                               repetitions=50),
        "go out":
            AsynchronousAction([L(S(["cancel"], context.nav, ["right", ")~]~}~>"]))],
                               time_in_seconds=0.1,
                               repetitions=50),
        "go back":
            AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))],
                               time_in_seconds=0.1,
                               repetitions=50),
        "go back in":
            AsynchronousAction([L(S(["cancel"], context.nav, ["left", "(~[~{~<"]))],
                               finisher=Key("right"),
                               time_in_seconds=0.1,
                               repetitions=50),

        # keyboard shortcuts
        "ignore body":
            R(Key("c-x")),
        "computer <pc_op>":R( Key("w-x/40,up,up,%(pc_op)s")),
        'save ( file | it )':
            R(Key("c-s"), rspec="save"),
        # implemented in each program 'save as': R(Key("cs-s")),
        'new file':
            R(Key("c-n")),
        'open file':
	    R(Key("c-o")),
        'print file':
            R(Key("c-p")),

        #page
        "search page [for] [<textnv>]":
            R(Key("c-f") + Pause("200") + Text("%(textnv)s")),
        "last page": R(Key("a-left")),
	    "header":
            R(Key("c-home/50")),
        "footer":
            R(Key("c-end/50")),
        #orig
        "shift click":
            R(Key("shift:down") + Mouse("left") + Key("shift:up")),
        #"stoosh [<nnavi500>]":
        #    R(Function(navigation.stoosh_keep_clipboard), rspec="stoosh"),
        "cut [<nnavi500>]":
            R(Function(navigation.cut_keep_clipboard), rspec="cut"),
        "spark [<nnavi500>] [(<capitalization> <spacing> | <capitalization> | <spacing>) [(bow|bowel)]]":
            R(Function(navigation.drop_keep_clipboard), rspec="spark"),
        "splat [<splatdir>] [<nnavi10>]":
            R(Key("c-%(splatdir)s"), rspec="splat")*Repeat(extra="nnavi10"),
        SymbolSpecs.CANCEL:
            R(Key("escape, shift:up, ctrl:up"), rspec="cancel"),
        "shackle":
            R(Key("home/5, s-end"), rspec="shackle"),
        "(tell | tau) <semi>":
            R(Function(navigation.next_line), rspec="tell dock"),
        "(hark | heart) <semi>":
            R(Function(navigation.previous_line), rspec="hark dock"),
        "duple [<nnavi50>]":
            R(Function(navigation.duple_keep_clipboard), rspec="duple"),
        "Kraken":
            R(Key("c-space"), rspec="Kraken"),
        "undo [<nnavi10>]":
            R(Key("c-z"))*Repeat(extra="nnavi10"),
        "redo [<nnavi10>]":
            R(
                ContextAction(default=Key("c-y")*Repeat(extra="nnavi10"),
                              actions=[
                                  (AppContext(executable=["rstudio", "foxitreader"]),
                                   Key("cs-z")*Repeat(extra="nnavi10")),
                              ])),

        # text formatting
        "set [<big>] format (<capitalization> <spacing> | <capitalization> | <spacing>) [(bow|bowel)]":
            R(Function(textformat.set_text_format)),
        "clear castervoice [<big>] formatting":
            R(Function(textformat.clear_text_format)),
        "peek [<big>] format":
            R(Function(textformat.peek_text_format)),

        "(<capitalization> <spacing> | <capitalization> | <spacing>) [(bow|bowel)] <textnv> [brunt]":
            R(Function(textformat.master_format_text)+Text(" ")),
        "[<big>] format <textnv>":
            R(Function(textformat.prior_text_format)),
        "<word_limit> [<big>] format <textnv>":
            R(Function(textformat.partial_format_text)),
        "hug this <enclosure>":
            R(Function(text_utils.enclose_selected)),
        #"dredge [<nnavi10>]": #replaced by "show"
        #    R(Key("alt:down, tab/20:%(nnavi10)d, alt:up"),
        #      rdescript="Core: switch to most recent Windows"),

        # Ccr Mouse (Commands)
        # two main points of control, cursor and pointer
        #"here" refers to the location of the cursor
        "here [<nnavi3>]":
            R(Function(navigation.left_click)+Pause("5"))*Repeat(extra="nnavi3"),
        "menu here | here menu":
            R(Function(navigation.right_click)),
        "drop here":
            R(Function(navigation.right_click)+Pause("5")+ Key("c-v")),
        #"scroll here | here scroll":
            #R(Function(navigation.middle_click)),

        #"this" refers to what is beneath the cursor
        "double tap | this [word] ":
            R(Function(navigation.left_click)*Repeat(2)),
        "(here|this) line":
            R(Function(navigation.left_click)+Pause("20"))*Repeat(3),
        "hold here | here hold":
            R(Function(navigation.left_down)),
        #release implemented in keyboard rule, releases modifiers as well
        "(release (it|this|here))":
            R(Function(navigation.left_up)),

        # special keystroke commands
        #"next line": R(Key("backspace, enter")),
        #"go": R(Key("backspace, c-right")),
        "shave right [<nnavi50>]": R(Key("s-right:%(nnavi50)s, backspace")),
        "(lease wally | latch | back line) [<nnavi10>]":
            R(Key("home:%(nnavi10)s")),
        "(ross wally | ratch | jump line) [<nnavi10>]":
            R(Key("end:%(nnavi10)s")),
        #"sauce wally [<nnavi10>]":
        #    R(Key("c-home:%(nnavi10)s")),
        #"dunce wally [<nnavi10>]":
        #    R(Key("c-end:%(nnavi10)s")),
        #"bird [<nnavi500>]":
        #    R(Key("c-left:%(nnavi500)s")),
        #"firch [<nnavi500>]":
        #    R(Key("c-right:%(nnavi500)s")),
        #"brick [<nnavi500>]":
        #    R(Key("s-left:%(nnavi500)s")),
        #"frick [<nnavi500>]":
        #    R(Key("s-right:%(nnavi500)s")),
        #"blitch [<nnavi500>]":
        #    R(Key("cs-left:%(nnavi500)s")),
        #"flitch [<nnavi500>]":
        #    R(Key("cs-right:%(nnavi500)s")),
        "<button_dictionary_500_no_prefix_no_modifier> [<nnavi500>]":
            R(Key("%(button_dictionary_500_no_prefix_no_modifier)s/1")*Repeat(extra='nnavi500'),
              rdescript="press buttons: %(button_dictionary_500_no_prefix_no_modifier)s %(nnavi500)s"),
        "<modifier> <button_dictionary_500_modifier> [<nnavi500>]": #added delay
            R(Key("%(modifier)s-%(button_dictionary_500_modifier)s/1")*Repeat(extra='nnavi500'),
              rdescript="nav: press modifiers plus buttons from button_dictionary_500_modifier"),
        "<modifier> <button_dictionary_1_modifier>":
            R(Key("%(modifier)s-%(button_dictionary_1_modifier)s/1"),
              rdescript="press modifiers plus buttons from button_dictionary_1_modifier"),
    }

    tell_commands_dict = {"dock": ";", "doc": ";", "sink": "", "com": ",", "deck": ":"}
    tell_commands_dict.update(_tpd)
    button_dictionary_500_no_prefix_no_modifier = {
        "tabby": "tab",
        "shave": "backspace",# shift:up, ctrl:up", #select mod
        "(delete | deli)": "del,  shift:up, ctrl:up",#select mod
        "done": "enter",
        "left": "left",
        "right": "right",
        "up": "up",
        "down": "down",
        "page down": "pgdown",
        "page up": "pgup",
    }
    button_dictionary_500_modifier = {
        key:value for key, value in keyboard_support.button_dictionary_1.items() if value in [
            "backspace", "del", "enter", "left", "right", "up", "down", "pgdown", "pgup"
            ]
    }
    button_dictionary_1_modifier = {
        key:value for key, value in keyboard_support.button_dictionary_1.items() if value in [
            "home", "end"
            ]
    }
    extras = [
        ShortIntegerRef("nnavi10", 1, 11),
        ShortIntegerRef("nnavi3", 1, 4),
        ShortIntegerRef("nnavi50", 1, 50),
        ShortIntegerRef("nnavi500", 1, 500),
        Dictation("textnv"),
        Choice("enclosure", _dtpd),

#    Commands for capitalization:
#    1 yell - ALLCAPS
#    2 tie - TitleCase
#    3 Gerrish - camelCase
#    4 sing - Sentencecase
#    5 laws (default) - alllower

#   Commands for word spacing:
#    0 (default except Gerrish) - words with spaces
#    1 gum (default for Gerrish)  - wordstogether
#    2 spine - words-with-hyphens
#    3 snake - words_with_underscores
#    4 pebble - words.with.fullstops
#    5 incline - words/with/slashes

        Choice("capitalization", {
            "yell": 1,
            "tie": 2,
            "camel": 3,
            "sing": 4,
            "laws": 5,
            "say": 6,
            "cap": 7,
            "slip": 8,
        }),
        Choice(
            "spacing", {
                "gum": 1,
                "gun": 1,
                "spine": 2,
                "snake": 3,
                "pebble": 4,
                "incline": 5,
                "dissent": 6,
                "descent": 6,
            }),
        Choice("semi", tell_commands_dict),
        Choice("word_limit", {
            "single": 1,
            "double": 2,
            "triple": 3,
            "Quadra": 4
        }),
        navigation_support.TARGET_CHOICE,
        Choice("extreme", {
            "Wally": "way",
        }),
        Choice("big", {
            "big": True,
        }),
        Choice("splatdir", {
            "lease": "backspace",
            "ross": "delete",
        }),
        Choice("pc_op", {
         	"sleep": "right,down,enter",
            "restart": "right,up",
            "shutdown": "right,up,up",
        }),

        keyboard_support.modifier_choice_object,
        Choice("button_dictionary_500_no_prefix_no_modifier", button_dictionary_500_no_prefix_no_modifier),
        Choice("button_dictionary_500_modifier", button_dictionary_500_modifier),
        Choice("button_dictionary_1_modifier", button_dictionary_1_modifier)
    ]

    defaults = {
        "nnavi500": 1,
        "nnavi50": 1,
        "nnavi10": 1,
        "nnavi3": 1,
        "textnv": "",
        "capitalization": 0,
        "spacing": 0,
        "extreme": None,
        "big": False,
        "splatdir": "backspace",
    }


def get_rule():
    return Navigation, RuleDetails(ccrtype=CCRType.GLOBAL)
