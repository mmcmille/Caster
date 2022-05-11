"""
Michael McMillen
TODO:
add grab direction, holds cs, copies with done

"""

# this function takes a dictionary and returns a dictionary whose keys are sequences of keys of the original dictionary
# and whose values our the corresponding sequences of values of the original dictionary
from dragonfly import Repeat, Dictation, Choice, MappingRule, Repetition, Pause, Function, ShortIntegerRef



from castervoice.rules.core.alphabet_rules import alphabet_support  # Manually change in port in if in user directory
from castervoice.lib.actions import Text, Key, Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R



class SpreadsheetsRule(MappingRule):
    number_output_mode = ""#default, options: down,right,off,

    def _number_output_direction():
        #print(SpreadsheetsRule.number_output_mode)
        return Key(SpreadsheetsRule.number_output_mode).execute() #+Key("%(_input_mode)s"),
    # change the direction of number output, based on the Choice
    def change_number_output_direction(output_number_options):
        SpreadsheetsRule.number_output_mode = output_number_options #"down"
        print(SpreadsheetsRule.number_output_mode)


    mapping = {
        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s")),
        #temporary rule for transferring
        "transfer": R(Key("c-c/20, a-tab") + Pause("100") + Key("c-v/20, enter")),
        "grab column": R(Key("c-space/20, shift:down")),
    # whole number input, move to next cell automatically
    #number input right/down/off
    #def _load_and_refresh(self, _input_mode):
        "<row_1>": R(Text("%(row_1)s")+Function(_number_output_direction)),

        # collect number direction, number= number of cells
        "collect <output_number_options>": R(Function(change_number_output_direction)),

        "next sheet [<n>]":
                R(Key("c-pgdown"))*Repeat(extra='n'),
            "(prior | previous) sheet [<n>]":
                R(Key("c-pgup"))*Repeat(extra='n'),
            "[select] cell <column_1> <row_1>":
                R(Key("c-g") + Text("%(column_1)s%(row_1)s") + Key("enter")),
            "select <column_1> <row_1> through <column_2> <row_2>":
                R(Key("c-g") + Text("%(column_1)s%(row_1)s:%(column_2)s%(row_2)s") +
                  Key("enter")),
            "edit":
    		R(Key("f2")),
    	"pasta values":
    		R(Key("cs-v/20")),
    	"delete column":
    		R(Key("apps/20,d/20,c/20")),
    	"delete row":
    		R(Key("apps/20,d/20,r/20")),


    	#navigation
    	"left file":
    		R(Key("cs-tab/20")),
    	"right file":
    		R(Key("c-tab/20")),

        "left file <n>":
            R(Key("cs-tab/20"))*Repeat(extra='n'),
        "right file <n>":
            R(Key("c-tab/20"))*Repeat(extra='n'),
        "close file":
    		R(Key("c-w/20")),
    	"save [file] as":
    		R(Key("alt/20, f/20, a/20, m/20")),

        # menu items
        "manage rules": R(Key("alt, h,4,r")),




    	#navigate to top of column labeled letter
    	"column <letter>": R(Mouse("(35, 170), left") + Pause("20") + Text("%(letter)s1") + Key("enter")), # + Key("c-g")), #35, 175
        "column <letter> <letter_2>": R(Mouse("(35, 170), left")
            + Pause("20") + Text("%(letter)s%(letter_2)s1") + Key("enter")),
        "cell <letter> <row_1>": R(Mouse("(35, 175), left")
            + Pause("20") + Text("%(letter)s%(row_1)s") + Key("enter")),

        #"row <row_1>":  navigate to row number, implemented by copying from name box?

    	"get block":
    		R(Key("cs-down/20,cs-right/20")),

    	"select current column":
                R(Key("c-space")),
        "get row":
            R(Key("cs-space/20")),
        "top of column":
            R(Key("c-up")),
        "beginning of row":
            R(Key("c-left")),
        "insert stuff":
            R(Key("cs-plus")),
        "insert row":
            R(Key("cs-plus/80,down")),
        "insert column":
            R(Key("cs-plus/40, a-c/40, enter")),
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

        # From Mark Lillibridge regarding the edit cell command below:
        # There are at least two modes, edit (blue background) and enter (yellow background).
        # In enter mode for formulas, arrow keys select a
        # cell (range if shifted), whereas in edit mode, they move the cursor
        # inside the formula.  For non-formulas, in enter mode, the arrows
        # finished entering the current cell and move to another cell.
        #
        #  and "edit cell" initially switch to edit mode then
        # toggle thereafter for the given cell.  Typing initially puts you in
        # enter mode.
        #

        # edit cell: always edits directly in cell (blue background)

        #
        # this has the effect of pressing F2 without DNS around.
        #
        # Want "edit directly in cell" option turned off:
        #   Office button->advanced-> turn off allow editing directly in cells
        # (Dragon handles edit in cell directly badly)
        #
        # First time, edits current cell via formula bar.  Unlike with
        # editing directly in a cell, this highlights ranges and cells used.
        "toggle edit cell":
            R(Key("f2")),
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
        Choice("key_rule", {
            "fit column [width]": "a-w",
            "( search | find)": "c-f",
            # filtering
            "add filter": "cs-l",
        	"filter": "a-down/20",
        	"clear filter": "a-down/40, up/20, right/20, tab/20, tab/20, enter",
            #sorting
            "sort down": "a-down/40, up/20,up/20,left/20,enter",
        	"sort up": "a-down/40, up/20,up/20,enter",
            "fill down": "c-d",
            "get unique values": "alt/20, a, 2, u/40, enter",

        }),
    ]
    defaults = {"n": 1, "dict": ""}

def get_rule():
    return SpreadsheetsRule, RuleDetails(name="spreadsheets", executable="et")
