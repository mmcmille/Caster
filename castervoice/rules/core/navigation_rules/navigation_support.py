'''
Michael McMillen
'''

import dragonfly
from dragonfly import Choice

DIRECTION_STANDARD = {
    "up [E]": "up",
    "down [E]": "down",
    "left [E]": "left",
    "right [E]": "right",
    "back": "left"
}

def get_direction_choice(name):
    global DIRECTION_STANDARD
    return Choice(name, DIRECTION_STANDARD)


 # Insurers comma is recognized consistently with DNS/Natlink
 # if/else statement workaround engines that do not expect punctuation symbol as a command
if hasattr(dragonfly.get_current_engine(), "name"):
    if (dragonfly.get_current_engine().name == 'natlink'):
        comma = "(comma | ,)"
    else:
        comma = "comma"
else:
    comma = "comma"

'''
Target Choice Note: distinct token types were removed because
A) a general purpose fill token is easier to remember than 10 of them, and
B) the user of a programming language will know what they're supposed to get filled with
'''

TARGET_CHOICE = Choice(
    "target", {
        #comma: ",",
        #"period": ".",
        "(pair | parentheses)": "(~)",
        "[square] (bracket | brackets)": "[~]",
        "curly [brace]": "{~}",
        "loop": "for~while",
        "open paren": "(",
        "close paren": ")",
        "openers": "(~[~{",
        "closers": "}~]~)",
        "token": "TOKEN",
    })
