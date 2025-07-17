'''
Michael McMillen
'''

from dragonfly import Repeat, Pause, Function, Choice, MappingRule, ShortIntegerRef
#from dragonfly.windows.clipboard import Clipboard
from castervoice.lib.actions import Key, Mouse, Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R
from castervoice.lib import github_automation
from castervoice.lib.temporary import Store, Retrieve

class SpiritRule(MappingRule):
	#temporary = Clipboard({Clipboard.format_unicode: u"\\Client\C$\"temp\SpiritTemp\Spirit_temp_export.xlsx"})
	#temporary.copy_to_system()

	mapping = {
		#generic key rule
		"<key_rule>": R(Key("%(key_rule)s/60")),
		#show/hide columns: move item under mouse to display
        "this": R(Mouse("left") + Pause("10") + Key("tab/10, space")),

		# table and button navigation, by mouse clicking
		"[open] <item>": R(Mouse("(%(item)s)/50, left")),
		#table filtering
		"filter": R(Mouse("left:down, [0, 20], left:up")),
		#query menu
		"<spirit_trait>":R( Text("%(spirit_trait)s", pause = 0.1)+Key("right/40, i/40, tab/40")),#"tab/40,equals")),

		"<spirit_part_trait>":R( Text("%(spirit_part_trait)s")),#"tab/40,equals")),

		"export": R(Key("alt/40,f,down:3/40,right/40,enter")
			+ Pause("100")
			+ Key("tab:2/20")
		#Citrix Path
		#+ Text("\\") + Text("\Client\C$", pause = 0.01) + Text("\\temp\Spirit_temp_export.xlsx", pause = 0.01)), #+Key("s-tab")),
		#Local Path
		+ Text("C:", pause = 0.01) + Text("\\temp\DefaultExport.xlsx", pause = 0.01) + Pause("50") + Key("s-tab")),

		"temp": R(Text("\\") + Text("\Client\C$", pause = 0.01) + Text("\\temp\DefaultExport.xlsx", pause = 0.01)), #+Key("s-tab")),

		#servers
		"<server_name> server": R(Key("end/20,s-home")+Text("%(server_name)s")+Key("tab")),
		#row and column right-click menu commands
		#uses menu key, where the mouse is resting on row
		"<rc_item>": R(Key("apps/80, %(rc_item)s/40,enter")), #Mouse("left/40,right/40") +
		"view associated":R(Key("apps/80, v")), #Mouse("left/40,right/40") +"v",
		#mouse commands
		"(drag over|pull over| bring over| apply profile | apply this)": R(Mouse("left:down/60, <-800, 0>, left:down/80, left:up")),
		"pull up": R(Mouse("left:down/10, <0, -30>") + Pause("50") + Mouse("left:up")),
		"pull down": R(Mouse("left:down/10, <0, 60>") + Pause("50") + Mouse("left:up")),

		#menu control
		"<menu_title> [menu]": R(Key("alt/40, %(menu_title)s/40")),
		"frame [<m>]": R(Key("alt/40, w/40, %(m)s/40")),
		#grid (window) switching
		"window" : R(Key("alt, w/40")),
		"grid [<m>]": R(Key("alt, w/40") + Key("%(m)s/40")),
	}
	extras = [
		Choice("server_name",{
			"global": "SPR-GDB-P-1.NAFTA.SYNGENTA.ORG",
			"stage": "SPR-USRDB-S-1.NAFTA.SYNGENTA.ORG",
			"EU|european|production|main": "SPR-EURDB-P-1.NAFTA.SYNGENTA.ORG",
		}),
		Choice("menu_title", { #press alt...
			"file": "f",
			"close (frame|grid|it)": "f, enter",
			"logout": "f, up:2,enter",
			"import": "f,down:2,right,enter",

			"export containers": "f,down:3/40,right/40,down/40,enter",

			"edit menu": "e",
			"view": "v",
			"reports": "r",

			"help": "h",
		}),

		Choice("spirit_trait", {
			#full Spirit trait chains

			"plot prefix":"EXT:PLTPR",
			"plot status":"",
			#Material
			"(Matt|material) ID":"MAT:MATID",
			"(Matt|material) (BE|entity)":"MAT:MMT:BEBID",
			"[Matt|material] generation code":"MAT:GENCD",
			"[Matt|material] identity generation code ": "MAT:MMT:IGENCD",
			"(Matt|material) line code":"MAT:LINE:LINCD",
			"(Matt|material) batch bid":"MAT:MMT:BID",
			"(Matt|material) LBG": "MAT:MMT:",


			#Line
			"line line code":"LINE:LINCD",
			"line incident number":"LINE:INCNO",

			"person code":"PERSN:CODE",
			"experiment number":"EXP:EXTNO",
			"research station code":"LOC:RST:RSTCD",
			"trial ID":"EXT:TRLID",
			#VH
			"stable variety code":"VH:STBVC",
			"variety name":"VH:VHNM",
			"variety number":"VH:VHNO",
			#People
			#location
			"location code":"LOC:LOCCD",
			#Trait Definitions
			"trait code":"UDTRT:UDTCD",
		}),
		Choice("spirit_part_trait", {
			#partial trait chains

			#line
			"line":"LINE:",
			"default material": "DMAT:",
			#material
			"[biological] entity":"MMT:BEBID",
			"material":"MAT:",
			"female parent":"F",
			"male parent":"MPARM:",
			"batch":"MMT:BID",
			"identity generation code": "MMT:IGENCD",
			"pedigree":"PDGRE",
			"identity pedigree":"MMT:BPDGRE",

		}),

		Choice("item", {
			#assumes menu layout is:
			#Standard
			#Tools (Icons)
			#Query|Save, Print, etc.
			"query": "785,66",

			"people":"1073,81",
			"crop logins":"1105,81",


			#"material management":"87, 130",
			"materials":"82, 160",
			"(trial|experiment) management":"87, 654",

			"lines": "87,66",
			"experiments": "87, 234",
			"plots":"87, 280",
			"trials":"87, 285",



			"advanced sort":"386, 70",

			"cell 1":"190, 135",
			"get table":"180, 128",
			"(last row|row last|row end)": "180, 1269",
			"row 1":"180, 145",

			"Entries ":"357, 214",
			"design":"427, 212",


		}),
		Choice("rc_item", {
				"view [associated] (affiliations|GNA)": "v/40, g",
				"view [associated] (locations|line|lines)": "v/40, l",
				"view [associated] materials [created]": "v/40, m",
				"view [associated] (parent materials|parents)": "v/40, p",
				"view [associated] subplots": "v/40, right/40, up:2",
				"view [associated] plots": "v/40, right/40, p",
				"view [associated] progeny": "v/40, right/40, up:4",
				"view [associated] pollinations": "v/40, right/40, up",
				"view [associated] (trial|trials)": "v/40, t",
				"view [associated] variety": "v/40, v",
				"append [existing] [flex] traits": "a:3",
				"(add|make) subplots": "a:2",

				"check quantity": "c:3",
				"plant (trial|trials)":"p/40:3",
				"sort [down]":"up:8/10,right/10,down",
				"sort up":"up:8/10,right/10,down:2",

				#Favorites
				"set default profile":"up:2/40,right/40,down",
				"(new|save) profile":"up:2/40,right/40,up:2",
				"[create] (new|save) grouping":"up:2/40,right/40,up",

				"(edit|add|remove|change|show) (columns|profile)":"up:4",

				"remove [record|records]":"r",
				"delete (record|records)":"d",
				"properties":"up",


		}),
		Choice("key_rule", {
			#close window
			"close window":"",

			#crops
			"broccoli":"b",
			"Brussels sprouts":"b:2",
			"cabbage":"c",
			"cauliflower":"c:3",
			"cucumber":"c:7",
			"lettuce":"l",
			"peppers":"p:2",
			"sweetcorn":"s:6",
			"tomato":"t",
			"watermelon":"w",


			#query
			"next [field]": "tab",
			"run query": "a-q",
			"clear query": "a-c",
			"append":"a-a",
			"replace":"a-r",
			"close query": "a-s",
			#"remove": "apps,r",
			"like": "l",
			"in":"i",

			#Show Hide Columns
			"transfer":"tab,space,s-tab",
			"move":"s-tab:3",

			#other commands
			"(okay|OK)":"a-o",
			"edit": "f2",
			"refresh (grid|frame)": "f5",
			"paste down":"apps/20, down:4/10, enter",

			#Cell text
			"submit":"s,u,tab",
			"complete":"c,tab",


		}),


		ShortIntegerRef("k", 1, 1000),
		ShortIntegerRef("n", 1, 100),
		ShortIntegerRef("m", 1, 10),

	]
	defaults = {"n": 1, "k": 1, "nth": ""}


def get_rule():
	#return SpiritRule, RuleDetails(name="spirit", title="Spirit Application")#title=window title
	#return SpiritRule, RuleDetails(name="spirit", executable="wfica32") #Citrix version
	return SpiritRule, RuleDetails(name="spirit", executable="SPIRITShell") #Local version
	#return SpiritRule, RuleDetails(name="spirit", executable="appstreamclient") #Appstream