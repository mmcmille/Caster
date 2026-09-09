"""
Michael McMillen
TODO:
add grab direction, holds cs, copies with done
"""

# this function takes a dictionary and returns a dictionary whose keys are sequences of keys of the original dictionary
# and whose values our the corresponding sequences of values of the original dictionary
from dragonfly import Repeat, Dictation, Choice, MappingRule, Repetition, Pause, Function, ShortIntegerRef, StartApp
from castervoice.rules.core.alphabet_rules import alphabet_support  # Manually change in port in if in user directory
from castervoice.lib.actions import Text, Key, Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

class AccessRule(MappingRule): #MappingRule
    number_output_mode = ""#default, options: down,right,off,

    def _number_output_direction():
        #print(LORule.number_output_mode)
        return Key(ExcelRule.number_output_mode).execute() #+Key("%(_input_mode)s"),
    # change the direction of number output, based on the Choice
    def change_number_output_direction(output_number_options):
        ExcelRule.number_output_mode = output_number_options #"down"
        print(ExcelRule.number_output_mode)


    mapping = {
        ##inserts UUID
        "(ID|UID) [<n>]":R(StartApp(r"C:\Users\u581917\OneDrive - Syngenta\Apps\Utility\UUID Generator\uuid.exe") + Pause("40") + Key("c-v/20, down"))*Repeat(extra='n'),
        #scrolling
        "scroll (here|this)" : R(Mouse("middle")),
        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s")),
        #temporary rule for transferring
        "transfer": R(Key("c-c/20, a-tab") + Pause("100") + Key("c-v/20, enter")),
        #menu control
        "<menu_title> menu": R(Key("alt/20, %(menu_title)s/20")),

        #Right-Click menu
        "<rc_item>": R( Key("apps/10, %(rc_item)s")), #

        #Sheet Action
        "<sheet_action> sheet": R(Key("f6:2/20") + Key("%(sheet_action)s")),

        #Locates email with subject of selected cell in outlook, assumes outlook is Win #2
        "(search|find e-mail)": R(Key("c-c/20, cw-2") + Pause("100") + Key("a-q/20, s-home, delete, \", c-v, \", enter")),
        "(search|find notes)": R(Key("c-c/20, cw-5") + Pause("100") + Key("c-e/20, delete, \", c-v, \"/40, enter")),

    # whole number input, move to next cell automatically
    #number input right/down/off
    #def _load_and_refresh(self, _input_mode):
        "<row_1>": R(Text("%(row_1)s")+Function(_number_output_direction)),

        # collect number direction, number= number of cells
        "collect <output_number_options>": R(Function(change_number_output_direction)),
        # show other sheets
        "show right [<n>]":R(Key("c-pgdown"))*Repeat(extra='n'),
        "show left [<n>]":R(Key("c-pgup"))*Repeat(extra='n'),
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

        #Disable Dictation
    #    "<dict>": R(Text("")),



    }
    extras = [
        alphabet_support.get_alphabet_choice("letter"),
	    alphabet_support.get_alphabet_choice("letter_2"),
	    Dictation("dict"),
        ShortIntegerRef("n", 1, 100),
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
			"help": "y",
            "table":"j,t",
		}),
        Choice("rc_item", {
            "trash [this]": "d",
            "move this":"m",
            "insert here":"e",
            "format cells":"f",



        }),
        Choice("sheet_action", {
            "new":"tab/20,enter",
            "rename":"apps/20,r",
            "move":"apps/20,m",
            "copy":"apps/20,m/20,a-c/20,s-tab:2/20,a-down",
            "link":"apps/20,l",
            "delete":"apps/20,d",
        }),
        Choice("key_rule", {
            #tables
            "open table ": "c-o",
            "new table": "c-n",
            "rename table ": "f2",
            "delete table ": "delete",
            "copy table ": "c-c",
            "paste table ": "c-v",
            "design table ": "a-enter",
            "datasheet view": "c-enter",

            #queries
            "new query": "c-q",
            "open query ": "c-o",
            "run query": "a-r",
            "design query": "a-enter",
            "save query": "c-s",
            "delete query ": "delete",

            #forms
            "new form": "a-c, f",
            "open form ": "c-o",
            "design form": "a-enter",
            "save form": "c-s",
            "delete form ": "delete",

            #reports
            "new report": "a-c, r",
            "open report ": "c-o",
            "design report": "a-enter",
            "save report": "c-s",
            "delete report ": "delete",

            #navigation
            "next object": "c-tab",
            "previous object": "cs-tab",
            "close object": "c-w",
            "close all": "c-f4",

            #records
            "new record": "c-plus",
            "delete record": "c-minus",
            "save record": "s-enter",
            "find record": "c-f",
            "replace record": "c-h",
            "sort ascending": "a-a",
            "sort descending": "a-d",

            #fields
            "new field": "a-i",
            "delete field": "delete",
            "rename field": "f2",
            "copy field": "c-c",
            "paste field": "c-v",

            #filters
            "filter by selection": "s-f8",
            "filter by form": "s-f11",
            "toggle filter": "cs-l",
            "clear filter": "a-c, c",

            #views
            "switch to design": "v, d",
            "switch to datasheet": "v, s",
            "switch to form view": "v, f",
            "switch to layout view": "v, l",

            #macros
            "new macro": "a-c, m",
            "run macro": "a-f8",
            "save macro": "c-s",
            "delete macro ": "delete",

            #modules
            "new module": "a-c, m",
            "open module ": "c-o",
            "save module": "c-s",
            "run procedure": "f5",

            #application
            "save database": "c-s",
            "compact and repair": "a-f11",
            "options": "a-f, t",
            "print": "c-p",
            "exit access": "a-f4",

            #object tabs (top of Access window)
            "next tab": "c-tab",
            "previous tab": "cs-tab",
            "close tab": "c-w",
            "close all tabs": "c-f4",

            #tab control (inside forms)
            "next page": "c-tab",
            "previous page": "cs-tab",

            #navigation pane tabs
            "toggle navigation pane": "f11",
            "focus navigation pane": "f11, tab",


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
            "join ,": "TEXTJOIN(\"','\",TRUE,",
            "V look up": "VLOOKUP(",
            "X look up": "XLOOKUP(",
            "if statement":"IF(",
            "char":"CHAR(",
            "length":"LEN(",
            "count if": "COUNTIF(",
            "count many if": "COUNTIF(",
            "index": "INDEX(",
            "match":"MATCH(",
            "Dell":"(DEL)",
            "some":"SUM(",
            "indirect":"INDIRECT(",



        }),
    ]
    defaults = {"n": 1, "dict": ""}

def get_rule():
    return AccessRule, RuleDetails(name="access", executable="access")
