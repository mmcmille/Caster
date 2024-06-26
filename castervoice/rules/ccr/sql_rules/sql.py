'''
Michael McMillen
'''

from dragonfly import Function, Choice, Dictation
from castervoice.lib.actions import Text, Key
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R

#SQL and MySQL Workbench
class SQL(MergeRule):
    pronunciation = "sequel"

    mapping = {

        #generic key rule
        "<key_rule>": R(Key("%(key_rule)s")),

        "string <dict>": R(Text("\'") + Text("%(dict)s") + Text("\' ")),
        "<dict>": R(Text("%(dict)s")),
        "<sql_strings>": R(Text("%(sql_strings)s")),


        "between":
            R(Text("BETWEEN ")),
        "lodge and ":
            R(Text(" AND ")),
        "lodge or":
            R(Text(" OR ")),
        "case":
            R(Text("CASE ") + Key("enter/5:2") + Text("END,") + Key("up/5")),
        "in":
            R(Text(" IN ('')") + Key("left/5:2")),
        "equals | equal to":
            R(Text(" = ")),
        "not equal | not equal to":
            R(Text(" <> ")),
        "group by":
            R(Text("GROUP BY ")),
        "order by":
            R(Text("ORDER BY ")),
        "ascending":
            R(Text(" ASC ")),
        "descending":
            R(Text(" DESC ")),
        "left join":
            R(Text("LEFT JOIN ")),
        "inner join":
            R(Text("INNER JOIN ")),
        "right join":
            R(Text("RIGHT JOIN ")),
        "full join":
            R(Text("FULL JOIN ")),
        "join":
            R(Text("JOIN ")),
        "on [columns]":
            R(Text("ON ")),
        "using":
            R(Text("USING () ") + Key("left/5:2")),
        "insert into":
            R(Text("INSERT INTO ")),
        "update":
            R(Text("UPDATE TOKEN SET ")),
        "delete":
            R(Text(" DELETE ")),
        "like":
            R(Text("LIKE '%%'") + Key("left/5:2")),
        "union":
            R(Text("UNION ")),
        "is null":
            R(Text(" IS NULL ")),
        "is not null":
            R(Text(" IS NOT NULL ")),

        "fun max":
            R(Text(" MAX() ") + Key("left/5:2")),
        "fun min":
            R(Text(" MIN() ") + Key("left/5:2")),
        "fun count":
            R(Text(" COUNT() ") + Key("left/5:2")),
        "fun average":
            R(Text(" AVG() ") + Key("left/5:2")),
        "fun some":
            R(Text(" SUM() ") + Key("left/5:2")),
        "over partition by":
            R(Text(" OVER (PARTITION BY ) ") + Key("left/5:2")),
    }

    extras = [
        Dictation("dict"),
        Choice("sql_strings", {
            "as": "AS ",
            "select":" SELECT ",
            "distinct":"DISTINCT ",
            "(all | every)":"* ",
            "from":" FROM ",
            "where":" WHERE ",
            "use":"USE ",
            "not":"NOT ",
            "limit":"LIMIT  ",
            "and":"AND ",
            "with":"WITH ",
            "when":"WHEN ",
            "then":"THEN ",
            "else":"ELSE ",
            "null":"NULL ",
            "comment":"-- ",
        }),
        Choice("key_rule", {
            "run line": "c-enter",
        }),
    ]
    defaults = {
        "dict": ""
    }


def get_rule():
    return SQL, RuleDetails(ccrtype=CCRType.GLOBAL)
