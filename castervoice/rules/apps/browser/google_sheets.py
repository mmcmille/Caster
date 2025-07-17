
'''
Michael McMillen
independent Windows for tabs
dictation folder
'''
from dragonfly import Repeat, Dictation, Choice, MappingRule, Repetition, Pause, Function, ShortIntegerRef
from castervoice.rules.core.alphabet_rules import alphabet_support  # Manually change in port in if in user directory
from castervoice.lib.actions import Text, Key, Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

class GoogleSheetsRule(MappingRule):

    mapping = {



        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s")),
        #temporary rule for transferring
        "transfer": R(Key("c-c/20, a-tab") + Pause("100") + Key("c-v/20, enter")),
        #menu control
        "<menu_title> menu": R(Key("alt/20, %(menu_title)s/20")),

        #Right-Click menu
        "<rc_item>": R(Mouse("left/40,right/40") + Key("%(rc_item)s")), # +

        #Locates email with subject of selected cell in outlook, assumes outlook is Win #2
        "(search|find e-mail)": R(Key("c-c/20, cw-2") + Pause("100") + Key("a-q/20, s-home, delete, \", c-v, \", enter")),
        "(search|find notes)": R(Key("c-c/20, cw-5") + Pause("100") + Key("c-e/20, delete, \", c-v, \"/40, enter")),

        #sheet navigation
        "right sheet [<n>]":
                R(Key("c-pgdown"))*Repeat(extra='n'),
        "left sheet [<n>]":
                R(Key("c-pgup"))*Repeat(extra='n'),
        "select <column_1> <row_1> through <column_2> <row_2>":
                R(Key("c-g") + Text("%(column_1)s%(row_1)s:%(column_2)s%(row_2)s") + Key("enter")),

        #navigation
        "left file":
            R(Key("cs-tab/20")),
        "right file":
            R(Key("c-tab/20")),

        "left file <n>":
            R(Key("cs-tab/20"))*Repeat(extra='n'),
        "right file <n>":
            R(Key("c-tab/20"))*Repeat(extra='n'),


        # menu items
        "manage rules": R(Key("alt, h,4,r")),




        #navigate to top of column labeled letter
        "cell <dict>": R(Key("f5/40, del:2, %(dict)s, enter, f5")),#dict should be characters
        #"column <letter> <letter_2>": R(Mouse("(93, 147), left") + Pause("20") + Text("%(letter)s%(letter_2)s1") + Key("enter")),
        "cell <dict> <row_1>": R(Key("f5/40, del:2, %(dict)s, tab:2/10, del") + Text("%(row_1)s") + Key("enter, f5")),#dict should be characters

        #"row <row_1>":  navigate to row number, implemented by copying from name box?


        "top of column":
            R(Key("c-up")),
        "beginning of row":
            R(Key("c-left")),
        "insert":
            R(Key("cs-plus")),
            #LibreOffice R(Key("cs-plus/80,down:2/10,enter")),
        "insert cell [to the] left":
            R(Key("cs-plus, a-i, enter")),
        "insert cell above":
            R(Key("cs-plus, a-d, enter")),
        "insert pivot table":
            R(Key("a-n, v")),
        "insert pivot chart":
            R(Key("a-n, s, z, c")),
        "add-ins":
            R(Key("a-t, i")),
        "add border":
            R(Key("cs-ampersand")),
        "arrange Windows":
            R(Key("a-w/10, a")),
        "auto sum":
            R(Key("a-equal")),
        "freeze panes":
            R(Key("a-w, f")),

        #dictation mode
        #"<dict> {weight=100}": R(Text("%(dict)s ")),
        "<function> function": R(Text("%(function)s")),

    }
    extras = [
        alphabet_support.get_alphabet_choice("letter"),
        alphabet_support.get_alphabet_choice("letter_2"),
        Dictation("dict"),
        ShortIntegerRef("n", 1, 10),
        ShortIntegerRef("row_1", 1, 9999),
        ShortIntegerRef("row_2", 1, 100),
        # change max to 3 if you want sequences of lentgh three and so on
        Repetition(Choice("alphabet1", alphabet_support.caster_alphabet()), min=1, max=2, name="column_1"),
        Repetition(Choice("alphabet2", alphabet_support.caster_alphabet()), min=1, max=2, name="column_2"),
        Choice("output_number_options", {
            "down": "down",
            "right": "tab",
            "off": ""
        }),
        Choice("menu_title", {
            "file": "f",
            "home":"h",
            "insert": "n",
            "page layout": "p",
            "formulas": "m",
            "data": "a",
            "review": "r",
            "view": "w",
            "automate": "u",
            "developer": "l",
            "help": "y",
        }),
        Choice("rc_item", {
            "delete this": "d",
            "move this":"m",

        }),
        Choice("key_rule", {

            "(drop|insert) date":"c-semicolon",
            "edit": "f2",
            "edit link": "c-k",
            #Home
            "wrap text": "a-h/20, w",
            #Formulas
            "calculate sheet": "s-f9",
            "calculate workbook": "f9",
            #Data
            "refresh all":"a-a/10,r,a",
            # View
            "new window":"a-w/40,n",
            "hide columns":"c-space/10,apps/20,h",
            "hide ribbon": "c-f1",
            "(read|edit) mode": "cs-m",
            "get block": "cs-down/20,cs-right/20",
            "fit column [width]": "sa-right",
            "( search | find)": "c-f",
            "freeze top row": "a-w/20,f,r", #lo "a-v/40,c,r",
            "merge":"a-h,m,m",
            "unmerge":"a-h,m,u",
            # filtering
            "freeze (first|top) row": "a-v/40, c, r",
            "(add|remove) filter": "cs-l",
            "filter": "a-down/20, down:8/20",
            "(clear filter| filter off)": "a-down/40, c/20",
            #sorting
            "sort [down]": "a-down/40, s",#-tab, space, enter",
            "sort up": "a-down/40, o", #s-tab, space, down, enter",
            "(custom|advanced) sort": "a-h/10,s,u",
            "fill down": "c-d",
            "get unique values": "alt/20, a, 2, u/40, enter",
            "save [file] as": "a-f/40, a/20",

            #pasting
            "drop special": "cs-v",
            "okay":"a-o, enter",
            #selecting
            "(select|get) row": "s-space",
            "(select|get) column": "c-space:2/40",
            "delete column": "c-minus/40, a-c, a-o, enter",
            "delete row": "c-minus/40, r, enter",
            "delete (cell|cells)": "apps,d",
            "(add|insert) (column|columns)": "c-space:2/20,cs-equal",#sheets
            "(add|insert) (row|rows)": "s-space:2/20,cs-equal",#sheets
            "insert comment": "ca-c",
            "fly under": "up, c-down, down",
            #Sheet Navigation
            "new sheet": "s-f11",
            "open sheet":"as-k",
            "sheet menu":"as-s",
            "rename sheet":"a-1",
            #Writer
            "check spelling": "f7",

            #Menus
            #Home
            "clear (format|formats|formatting)":"a-h,e,f",
            "normal text":"c-backslash",
            "[keyboard] shortcuts":"c-slash",
            #Macros
            "generate":"c-g",#for hierarchy viewer macro
            #saving
            "don't save":"a-n",



        }),
        Choice("function", {
            "join": "=TEXTJOIN(\";\",TRUE,",
            "look up ": "=VLOOKUP(",
        }),
    ]
    defaults = {"n": 1, "dict": ""}

def get_rule():
    return GoogleSheetsRule, RuleDetails(name="Google sheets", title="Google Sheets")
