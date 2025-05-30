'''
Michael McMillen
Using "Outlook for Web" Shortcuts
'''

from dragonfly import Function, Pause, Repeat, Dictation, Choice, MappingRule, ShortIntegerRef

from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


def capitalize(text):
    output = str(text).title()
    Text(output).execute()


class OutlookRule(MappingRule):
    mapping = {
        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s/20")),

        "scroll here": R(Mouse("middle")),
        "find task": R(Mouse("left:3") + Key("c-c/20, cw-6") + Pause("100") + Key("c-f/50, backspace, c-v/40, enter/20, escape")),

        "signoff": R(Text("Best Regards,") + Key("enter") + Text("Michael")),
        # create new thing
        "new (email|event)": R(Key("n")),
        #"new (appointment | event)": R(Key("sc-a")),
        "new contact": R(Key("cs-c")),
        "new folder": R(Key("cs-e")),
        "advanced (search| find)": R(Key("cs-f")),
        "new office document": R(Key("cs-h")),
        "(inbox | go to inbox)": R(Key("g,i")),#cs-i
        "new journal entry": R(Key("cs-j")),
        "new task": R(Key("cs-k")),
        "new contact group": R(Key("cs-l")),
        "(new message| new mail)": R(Key("c-n")),
        "new note": R(Key("cs-n")),
        "open the new search folder window": R(Key("cs-p")),
        "new meeting request": R(Key("cs-q")),
        "new task request": R(Key("cs-u")),

        # new message window
        "to field": R(Key("a-dot")),
        "c c field": R(Key("a-c")),
        #"subject [field]": R(Key("a-u")),
        #"subject <text>": R(Key("a-u") + Function(capitalize) + Key("tab")),
        "attach file": R(Key("n, a, f")),
        "add to dictionary": R(Key("s-f10/2, a")),
        "send email": R(Key("a-s")),  # be careful
        "find and replace": R(Key("c-h")),
        "check names": R(Key("c-k")),
        "spell check": R(Key("f7")),
        "save as": R(Key("f12")),  # only in mail view

        # folders pane
        "expand [that]": R(Key("asterisk")),
        "collapse [that]": R(Key("minus")),
        #notifications
        "dismiss all": R(Key("a-a")),


        # folders navigation
        # some of these may be user dependent, depends on the order of your folders
        # which you can inspect by pressing control y
        # also I think some of these are built into Dragon
        "[go to] sent mail": R(Key("g,s")),#c-y/10, s, enter")),
        "go to drafts": R(Key("g,d")),#c-y/10, d, enter")),
        "go to trash": R(Key("c-y/10, t, enter")),
        "go to spam": R(Key("c-y/10, s:2, enter")),
        "go to starred": R(Key("c-y/10, s:3, enter")),
        "go to important": R(Key("c-y/10, i:2, enter")),
        "go to outbox": R(Key("cs-o")),
        "inbox": R(Key("cs-i")),

        # center pane
        "sort by [<sort_by>]": R(Key("a-v/5, a, b/5, %(sort_by)s")),
        "reverse sort": R(Key("a-v, r, s")),
        "block sender": R(Key("a-h/3, j/3, b")),
        "search": R(Key("a-q")),#c-e
        "new search": R(Key("a-q/10,s-home,backspace")),#c-e
        "search [for] [<dict>]": R(Key("a-q") + Text("%(dict)s")),
        "(categorize|label) [it] [<dict>]": R(Key("c/10")+Text("%(dict)s")), #"s-f10/40,down:8/10,right/5") + Text("%(dict)s")), #prefix with if needed R(Mouse("left") +
        "(message list | messages)": R(Key("tab:3")),
        "(empty | clear) search [bar]": R(Key("c-e, c-a, del/3, escape")),
        # from the search bar to get the focus into the messages is three tabs
        # pressing escape also seems to work.
        "refresh [mail]": R(Key("f9")),

        # reading pane
        "open attachment": R(Key("s-tab, enter")),
        "[open] attachment menu": R(Key("s-tab, right")),
        "next message [<n>]": R(Key("s-f6/10, down"))*Repeat(extra='n'),
        "(prior | previous) message [<n>]": R(Key("s-f6/20, up"))*Repeat(extra='n'),
        "[select] next link": R(Key("tab")),
        "[select] (previous | prior) link": R(Key("s-tab")),
        "tag email": R(Key("popup/20, t/10, a")),
    #    "archive": R(Key("backspace")),
        "done tagging": R(Key("space/10, enter")),

        # calendar
        "workweek [view]": R(Key("ca-2")),
        "full week [view]": R(Key("ca-3")),
        "month view": R(Key("ca-4")),

        #message shortcuts
        "(new window|read this)":R(Key("s-enter")),
        "flag (it|email)": R(Key("insert")),
        "reply ": R(Key("c-r")),
        "reply all ": R(Key("cs-r")),
        "forward": R(Key("c-f")),
        "Mark as read": R(Key("c-q")),
        "Mark as unread": R(Key("c-u")),
        #folders
        "[(go to|open)] folder": R(Key("c-y")),
        "move (it|to) [<dict>]": R(Key("v") + Pause("50") + Text("%(dict)s")),#cs-v
        #R(Mouse("right, <-5,0>")+ Pause("100") + Key("down:8/5,right/5")),
        "send it": R(Key("c-enter")),
        "trash it": R(Key("delete")),
        # navigation
	    "next pane [<n>]": R(Key("f6"))*Repeat(extra='n'),
        "(un|prior|previous) pane [<n>]": R(Key("s-f6"))*Repeat(extra='n'),
        "email [page]": R(Key("cs-1")),
        "calendar [page]": R(Key("cs-2")),
        "contacts": R(Key("cs-3")),
        "tasks": R(Key("cs-4")),
        "go to notes": R(Key("cs-5")),
        "folder list": R(Key("cs-6")),
        "find contact": R(Key("f11")),
        "address book": R(Key("cs-a")),
        "next open message": R(Key("c-dot")),
        "(prior | previous) open message": R(Key("c-comma")),
        "previous view": R(Key("a-left")),
        "next view": R(Key("a-right")),

        # misc
        "go back": R(Key("a-left")),

        #goes last in mapping order
        #"<dict>": R(Text("%(dict)s ")),
    }
    extras = [
        Dictation("dict"),
        Dictation("text"),
        ShortIntegerRef("n", 1, 100),
        Choice(
            "sort_by", {
                "date": "d",
                "from": "f",
                "to": "t",
                "size": "s",
                "subject": "j",
                "type": "t",
                "attachments": "c",
                "account": "o",
        }),
        Choice("key_rule", {
            "(clear formatting|normal text)":"c-space",
            "remove label":"c/20,down/10,space",

        }),
    ]
    defaults = {"n": 1, "dict": "", "text": "", "sort_by": ""}


def get_rule():
    return OutlookRule, RuleDetails(name="outlook", executable="outlook")
    #return OutlookRule, RuleDetails(name="utlook", title="Outlook")#title=window title