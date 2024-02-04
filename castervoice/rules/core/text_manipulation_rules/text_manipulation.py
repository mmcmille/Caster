'''
Michael McMillen
'''

from dragonfly import Function, Choice, Repetition, Dictation, Key, Repeat, ShortIntegerRef

try:  # Try first loading from caster user directory
    from text_manipulation_rules import text_manipulation_support
except ImportError:
    from castervoice.rules.core.text_manipulation_rules import text_manipulation_support

try:  # Try first loading from caster user directory
    from alphabet_rules import alphabet_support
except ImportError:
    from castervoice.rules.core.alphabet_rules import alphabet_support

try:  # Try first loading from caster user directory
    from punctuation_rules.punctuation_support import double_text_punc_dict, text_punc_dict
except ImportError:
    from castervoice.rules.core.punctuation_rules.punctuation_support import double_text_punc_dict, text_punc_dict
from castervoice.lib.actions import Text
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R
from castervoice.lib.util import recognition_history

_history = recognition_history.get_and_register_history(10)

base_number_dict = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9" }

number_dict = {"numb "+k:base_number_dict[k] for k in base_number_dict}

""" requires a recent version of dragonfly because of recent modification of the Function action
    # I think dragonfly2-0.13.0
    The wait times should be adjusted depending on the application by changing the numbers in copy_pause_time_dict
    and paste_pause_time_dict which are called by the functions text_manipulation_copy and text_manipulation_paste
    in text_manipulation_support.py. The wait times can be further adjusted by adjusting the sleep times in the
    functions that those functions call: lib.context.read_selected_without_altering_clipboard
    and lib.context.paste_string_without_altering_clipboard
    the keypress waittime should possibly be made shorter for these commands, though note that the keypress wait time is
    used by the aforementioned functions and lib.context.
    When these commands are not working in a particular application sometimes the problem is that
    there is not enough time from when control-c is pressed until the contents of the clipboard are passed into the function
    In that case you need to increase the pause time in that application in copy_pause_time_dict

    The functions in text_manipulation_support.py copy text into the clipboard and then return whatever
    you had there before back onto the clipboard. If you are using the multi clipboard (windows-x on Windows 10),
    this might be annoying because you will have some extra junk put on the second (and sometimes third)
    slot on your multi clipboard. If you get the wait times exactly right, in principle
    this problem can be avoided using the functions lib.context.read_selected_without_altering_clipboard
    and lib.context.paste_string_without_altering_clipboard
    In my experience, often times the paste part doesn't add
    any junk to the multi-clipboard although the copy (a.k.a. read) part does.

"""


class TextManipulation(MergeRule):
    pronunciation = "text manipulation"

    def _print_history():
        #if len(_history) !=0:
        print(_history[len(_history)-1])


    mapping = {
        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s/40, shift:up, ctrl:up")),
        "drop <drop_strings>": R(Text("%(drop_strings)s")),
        #prefix with space if the last command was text
        #"<dictation>": R(Text("%(dictation)s")),#+Text("")+Function(_print_history)),
        # PROBLEM: sometimes Dragon thinks the variables are part of dictation.
        #select text
        "get [<direction>] [<n>]": #defaults to left
            R(Key("cs-%(direction)s/1")*Repeat(extra="n")),
        "get <direction> <direction2> [<n>]": #defaults to left
            R(Key("cs-%(direction)s/1") + Key("s-%(direction2)s/1")*Repeat(extra="n")),

        "snag [<n>]": #char
            R(Key("s-left:%(n)s")),
        "snag right [<n>]":
            R(Key("s-right:%(n)s")),

    # replace text or character
        "replace <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation> with <dictation2>":
            R(Function(text_manipulation_support.copypaste_replace_phrase_with_phrase,
                       dict(dictation="replaced_phrase", dictation2="replacement_phrase"), dictation_versus_character="dictation"),
              rdescript="Text Manipulation: replace text to the left or right of the cursor"),
        "replace <direction>  [<number_of_lines_to_search>] [<occurrence_number>] <character> with <character2>":
            R(Function(text_manipulation_support.copypaste_replace_phrase_with_phrase,
                       dict(character="replaced_phrase", character2="replacement_phrase"), dictation_versus_character="character"),
              rdescript="Text Manipulation: replace character to the left of the cursor"),



        # remove text or character
        "clear <line_dir>": R(Key("s-%(line_dir)s, backspace")),
        "strike [<direction>] [<n>]": #defaults to left, say right to strike right
            R(Key("cs-%(direction)s/1")*Repeat(extra="n") + Key("backspace")),

        "remove <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>":
            R(Function(text_manipulation_support.copypaste_remove_phrase_from_text,
                       dict(dictation="phrase"), dictation_versus_character="dictation"),
                        rdescript="Text Manipulation: remove chosen phrase to the left or right of the cursor"),

        "remove <direction> [<number_of_lines_to_search>] [<occurrence_number>] <character>":
            R(Function(text_manipulation_support.copypaste_remove_phrase_from_text,
                       dict(character="phrase"), dictation_versus_character="character"),
              rdescript="Text Manipulation: remove chosen character to the left of the cursor"),

        # remove until text or character
        "remove <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation>":
            R(Function(text_manipulation_support.copypaste_delete_until_phrase,
                       dict(dictation="phrase"), dictation_versus_character="dictation"),
              rdescript="Text Manipulation: delete until chosen phrase"),
        "remove <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <character>":
            R(Function(text_manipulation_support.copypaste_delete_until_phrase,
                       dict(character="phrase"), dictation_versus_character="character"),
              rdescript="Text Manipulation: delete until chosen character"),

        # move cursor
        "back [<n>]": R(Key("c-left:%(n)s/10", use_hardware=True)),
        "jump [<n>]": R(Key("c-right:%(n)s/10")),

        #to do get line n

        #"move <direction> [<number_of_lines_to_search>] [<before_after>] [<occurrence_number>] <dictation>":
        #    R(Function(text_manipulation_support.move_until_phrase,
        #               dict(dictation="phrase"), dictation_versus_character="dictation"),
        #       rdescript="Text Manipulation: move to chosen phrase to the left or right of the cursor"),
        #"move <direction> [<number_of_lines_to_search>] [<before_after>] [<occurrence_number>] <character_sequence> [over]":
        #    Function(lambda direction, before_after, number_of_lines_to_search, occurrence_number, character_sequence:
        #     text_manipulation_support.move_until_phrase(direction, before_after,
        #     "".join(character_sequence), number_of_lines_to_search, occurrence_number, "character")),


        "grab <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>":
            R(Function(text_manipulation_support.select_phrase,
                       dict(dictation="phrase"), dictation_versus_character="dictation"),
                 rdescript="Text Manipulation: select chosen phrase"),
        "grab <direction> [<number_of_lines_to_search>] [<occurrence_number>] <character>":
            R(Function(text_manipulation_support.select_phrase,
                       dict(character="phrase", dictation_versus_character="character")),
            rdescript="Text Manipulation: select chosen character"),

        # select until text or character
        "grab <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation> ":
            R(Function(text_manipulation_support.select_until_phrase,
                       dict(dictation="phrase"), dictation_versus_character="dictation"),
                 rdescript="Text Manipulation: select until chosen phrase"),
        "grab <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <character>":
            R(Function(text_manipulation_support.select_until_phrase,
                       dict(character="phrase"), dictation_versus_character="character"),
            rdescript="Text Manipulation: select until chosen character"),

        # capitalized 1st word of text or character
        "capital <direction> [<number_of_lines_to_search>] [<occurrence_number>] [<letter_size>] <dictation>":
            R(Function(text_manipulation_support.copypaste_change_phrase_capitalization,
                       dict(dictation="phrase"), dictation_versus_character="dictation"),
                 rdescript="Text Manipulation: change capitalization phrase"),
        "capital <direction> [<number_of_lines_to_search>] [<occurrence_number>] [<letter_size>] <character>":
            R(Function(text_manipulation_support.copypaste_change_phrase_capitalization,
                       dict(character="phrase"), dictation_versus_character="character"),
            rdescript="Text Manipulation: change capitalization character"),

    }
    new_text_punc_dict = text_punc_dict()
    new_text_punc_dict.update(alphabet_support.caster_alphabet())
    new_text_punc_dict.update(number_dict)
    character_dict = new_text_punc_dict
    character_choice_object = Choice("character_choice", character_dict)

    extras = [
        Repetition(character_choice_object, min=1, max=3, name="character_sequence"),
        Dictation("dict"),
        Dictation("dictation"),
        Dictation("text"),
        Dictation("dictation2"),
        ShortIntegerRef("n", 1, 100),
        ShortIntegerRef("m", 1, 100),
        ShortIntegerRef("wait_time", 1, 1000),
        ShortIntegerRef("number_of_lines_to_search", 1, 50),


        Choice("character", character_dict),
        Choice("character2", character_dict),
        Choice("single_character", character_dict),

        Choice("direction", {
            "left": "left",
            "right": "right",
            "up": "up",
            "down": "down",
            # note: "sauce" (i.e. "up") will be treated the same as "lease" (i.e. "left") except that
            # the default number_of_lines_to_search will be set to 3
            # in the same way, "dunce" (i.e. "down") will be treated the same as
            # "ross" (i.e. "right")
        }),
        Choice("direction2", {
            "left": "left",
            "right": "right",
            "up": "up",
            "down": "down",
        }),
        Choice("line_dir", {
                "left": "home",
                "right": "end",
        }),
        Choice("before_after", {
            "before": "before",
            "after": "after",
        }),
        Choice("letter_size", {
            "upper": "upper",
            "upward": "upper",
            "lower": "lower",
            "lowered": "lower",
        }),
        Choice("occurrence_number", {
            "first": 1,
            "second": 2,
            "third": 3,
            "fourth": 4,
            "fifth": 5,
            "sixth": 6,
            "seventh": 7,
            "eighth": 8,
            "ninth": 9,
            "tenth": 10,
        }),
        Choice("key_rule", {
            "(select all|get everything)": "c-a",
            "bold text": "c-b",
            "underline text": "c-u",
            "italic text": "c-i",
            #line commands
            "get line":"home, s-end",
            "back line":"home",
        	"jump line": "end",
            "new line": "end,enter",
            #clears text
            "clear line": "end, s-home, backspace",
            "strike line": "end, s-up, s-end, backspace",
            "clear page": "c-a, backspace",
            #copying
            #added release modifiers to work with "select"
            "copy [it|this]": "c-c, shift:up, ctrl:up",
            "get word": "c-left, cs-right, c-c",
            "copy over": "c-c/20, a-tab",
            "cut [it|this]": "c-x, shift:up, ctrl:up",
            "drop it": "c-v",



            "copy line": "end/20, s-home/20, c-c",
            "(copy line over | transfer line)":"end/20, s-home/20, c-c/20, a-tab",
            "cut line": "end/20, s-home/20, c-x",
            "transfer page": "c-a, c-c/20, a-tab",
        }),
        Choice("drop_strings", {
            "email":"mandmmcmillen@gmail.com",
            "school email":"mmcmillen@sbhsd.k12.ca.us",
            "Monterey email":"mmcmillen@csumb.edu",
            "syngenta email":"michael.mcmillen@syngenta.com",
            "syngenta password":"Q1w1e1rt",
            "Outlook email":"Michael.S.McMillen@Outlook.com",
            "my email":"mcmillen.michael.s@gmail.com",
            "password":"Lucydog1",
            "[full] name" : "Michael McMillen",
            "first name": "Michael",
            "last name": "McMillen",
            "birthdate": "07/30/1983",
            "address": "1561 Albright Dr.",
            "(telephone|phone) [number]": "8315248552",
            "Monica's (telephone|phone) [number]": "2096027457",
            "Monica's birthdate": "12/29/1987",
            "zipcode": "95023",
            "student id": "841703494",

        }),
    ]
    defaults = {
        "direction": "left",
        "before_after": None,
        "letter_size": "upper",
        "number_of_lines_to_search": 0, # before changing this default, please read the function deal_with_up_down_directions
        "occurrence_number": 1,} # if direction is up or down, the default number_of_lines_to_search

        # will be 3 instead of zero.
        # This can be changed in the function deal_with_up_down_directions
        # 'number_of_lines_to_search = zero' means you are searching only on the current line


def get_rule():
    return TextManipulation, RuleDetails(ccrtype=CCRType.GLOBAL)
