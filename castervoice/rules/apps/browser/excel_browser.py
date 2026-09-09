"""
Michael McMillen
Edited:
source: excel_lo
"""

# this function takes a dictionary and returns a dictionary whose keys are sequences of keys of the original dictionary
# and whose values our the corresponding sequences of values of the original dictionary
from dragonfly import Repeat, Dictation, Choice, MappingRule, Repetition, Pause, Function, ShortIntegerRef
from castervoice.rules.core.alphabet_rules import alphabet_support  # Manually change in port in if in user directory
from castervoice.lib.actions import Text, Key, Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

class ExcelBrowserRule(MappingRule): #MappingRule
    mapping = {


        #scrolling
        "scroll (here|this)" : R(Mouse("middle")),
        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s")),
        #temporary rule for transferring
        "transfer": R(Key("c-c/10, a-tab") + Pause("100") + Key("c-v/10, enter")),
        #menu control
        "[<menu_title>] menu": R(Key("alt/30, %(menu_title)s/10")),

        #Right-Click menu
        "<rc_item>": R( Key("apps/10, %(rc_item)s")), #

        #Sheet Action
        "[<sheet_action>] sheet": R(Key("c-f6/10") + Key("%(sheet_action)s")),

        #Locates email with subject of selected cell in outlook, assumes outlook is Win #2
        "(search|find e-mail)": R(Key("c-c/10, cw-2") + Pause("100") + Key("a-q/10, s-home, delete, \", c-v, \", enter")),
        "(search|find notes)": R(Key("c-c/10, cw-5") + Pause("100") + Key("c-e/10, delete, \", c-v, \"/40, enter")),

        "right sheet [<n>]":
                R(Key("c-pgdown"))*Repeat(extra='n'),
        "left sheet [<n>]":
                R(Key("c-pgup"))*Repeat(extra='n'),
        "select <column_1> <row_1> through <column_2> <row_2>":
                R(Key("c-g") + Text("%(column_1)s%(row_1)s:%(column_2)s%(row_2)s") + Key("enter")),

    	#navigation
    	"left file":
    		R(Key("cs-tab/10")),
    	"right file":
    		R(Key("c-tab/10")),

        "left file <n>":
            R(Key("cs-tab/10"))*Repeat(extra='n'),
        "right file <n>":
            R(Key("c-tab/10"))*Repeat(extra='n'),


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

        "function <function>": R(Text("=%(function)s")),
        "<function>": R(Text("%(function)s")),

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
        Choice("direction", {
			"up": "up",
			"down": "down",
			"left": "left",
			"right": "right",
		}),
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
			"help": "y,1",
		}),
        Choice("rc_item", {
            "trash [this]": "d",
            "move this":"m",
            "insert here":"e",



        }),
        Choice("sheet_action", {
            "open":"space",
            "new":"tab/10,enter",
            "rename":"apps/10,r",
            "move":"apps/10,m",
            #"copy":"apps/10,m/10,a-c/10,s-tab:2/10,a-down",
            "link":"apps/10,l",
            "delete":"apps/10,d",
        }),
        Choice("key_rule", {
            "function":"equals",
            "edit": "f2",
            "locket":"f4",
            "fit [width]": "alt/10,h/10,o,i",
            #links
            "get link":"alt/10,z,s,l",
            "edit link": "c-k",
            "open link": "apps/10,o,o,enter",
            "remove link": "apps/10,r",
            #Home
            "wrap text": "alt/10,h/10, w",
            "[fill] color": "alt/10,h/10, h",
            "text color": "alt/10,h/10, fc",
            "style": "alt/10,h/10, j",
            "style bad": "alt/10,h/10, j/40, right:1,enter",
            "style good": "alt/10,h/10, j/40, right:2/10,enter",
            "style input": "alt/10,h/10, j/40, down:1, right:5/10,enter",
            "style neutral": "alt/10,h/10, j/40, right:3/10,enter",
            "style note": "alt/10,h/10, j/40, down:3/10, right/10,enter",
            #Formulas
            "calculate sheet": "s-f9",
            "calculate (workbook|now|file)": "f9",
            "manual calculation":"alt/10,m,x,m",
            "automatic calculation":"alt/10,m,x,a",

            #Data
            "data validation":"alt/10,a/10,v,v",
            "refresh all":"alt/10,a/10,r,a",
            "remove duplicates":"alt/10,a/10,m/80,s-tab:2",

            # View
            "(switch modes|midnight)":"alt/10,w/40,m,1",
            "new window":"alt/10,w/40,n",
            "hide": "apps/10,h",
            "unhide": "apps/10,u",
            "hide ribbon": "c-f1",

            "(read|edit) mode": "cs-m",
            "get block": "cs-down/10,cs-right/10",
            "( search | find)": "c-f",
            "find all": "alt/10,i",
            "find next": "alt/10,f",
            "replace": "c-h",
            "replace all": "alt/10,a",
            "freeze top row": "alt/10,w/10,f,r", #lo "alt/10,v/40,c,r",
            "merge":"alt/10,h,m,m",
            "unmerge":"alt/10,h,m,u",
            # filtering
            "(add|remove) filter": "escape, cs-l",
        	"filter": "alt/10,h/10,s,t",
            "(update|apply|re-) filter": "escape, c-up:2/10, alt/10,down/10, down:8/10, enter",
            "filter this": "apps/60,down,right,enter", #using header: "c-c/10, c-up:2/10, alt/10,down/10, down:8/40, c-v/10, enter",
            "(clear filter| filter off)": "alt/10,h,s,c", #using header:"c-up/2, alt/10,down/40, c/10",

            #sorting
            "sort [down]": "escape, c-up:3/10,a-down/40, s",#-tab, space, enter",
        	"sort up": "escape, c-up:3/10, a-down/40, o", #s-tab, space, down, enter",
            "(custom|advanced) sort": "alt/10,h/10,s,u",
            #"fill down": "c-d",
            "get unique values": "alt/10, a, 2, u/40, enter",
        	"save [file] as": "a-f/40, a/60,o",

            #pasting
            "fill right": "c-c, right, c-down, left, cs-up, c-v", #fills down based on adjacent right column
            "fill left": "c-c, left, c-down, right, cs-up, c-v",
            "fill down": "c-c, down, cs-down, c-v",
            "(drop|insert) date":"c-semicolon,enter",
            "(drop|insert) time":"c-colon,enter",
            "(drop|insert) date time":"c-semicolon/10 ,tab/10, c-colon,enter",
            "(drop|paste) special": "ca-v",
            "drop values": "ca-v/10,v,enter",
            "okay":"a-o, enter",
            "transpose":"apps/10,t,enter",
            "insert cut cells" : "apps/10, e",

            #selecting
            "next field":"tab",
            "last field": "s-tab",
            "(open|activate) sheet":"f6/10,s-tab/10,apps",
            "(trash|delete) [cell|cells]": "apps,d",

            #row
            "[get] row": "s-space",
            #"copy row": "s-space/40,c-c",
            "(trash|delete) row": "s-space, apps,d",
            "(add|insert) (row|rows) ": "escape, s-space,apps,i,enter",
            "fit (row|rows)": "s-space, a-h,o,i",
            #column
            "[get] (call|column)": "c-space",
            "copy (call|column) ": "c-space, c-c",
            "(add|insert) (call|column) ": "escape/10, c-space, apps, i/10", #c, a-o,
            "(trash|delete) (call|column) ": "c-space, apps,d",
            "fit (call|column) [width]": "c-space,a-h,o,i",

            #comments
            "show comments": "a-r/10,h,1",
            "[new|insert] comment": "a-r/10,c",
            "[new|insert] note": "s-f2",
            "fly under": "up, c-down, down",

            #Writer
            "check spelling": "f7",

            #Menus
            #Home
            "clear (format|formats|formatting)":"a-h,e,f",
            "normal text":"a-h,e,f",
            "font up":"a-h,f,g",
            "font down":"a-h,f,k",

            #Macros
            "generate|update [sort]":"c-g",#for hierarchy viewer macro, #for Task Manager
            #saving
            "don't save":"a-n",



        }),
        Choice("name", {
            "darin": "Darryn",
            "mel": "Mel",
            "veronica": "Veronica",
            "drew": "Drew",
            "yvette": "Yvette",
            "leo": "Leo",
        }),
        Choice("function", { #Excel functions
            "join": "TEXTJOIN(\";\",TRUE,",
            "[V] look up": "VLOOKUP(",
            "char":"CHAR(",
            "length":"LEN(",
            "count": "COUNTIF(",
            "index": "INDEX(",
            "match":"MATCH(",


        }),
    ]
    defaults = {"n": 1, "dict": "", "menu":"", "sheet":""}

def get_rule():
    return ExcelBrowserRule, RuleDetails(name="excel browser", title="xlsx")
