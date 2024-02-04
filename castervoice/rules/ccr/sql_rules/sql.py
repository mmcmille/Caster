'''
Michael McMillen
'''

from dragonfly import Function, Choice, Dictation
from castervoice.lib.actions import Text, Key
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class SQL(MergeRule):
    pronunciation = "sequel"

    mapping = {

        "string <dict>": R(Text("\'") + Text("%(dict)s") + Text("\' ")),
        #"<dict> {weight=1000}": R(Text("%(dict)s ")),
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
        "not equals | not equal to":
            R(Text(" <> ")),
        "group by":
            R(Text(" GROUP BY ")),
        "order by":
            R(Text("ORDER BY ")),
        "ascending":
            R(Text("ASC ")),
        "descending":
            R(Text("DESC ")),
        "left join":
            R(Text(" LEFT JOIN ")),
        "inner join":
            R(Text(" INNER JOIN ")),
        "right join":
            R(Text(" RIGHT JOIN ")),
        "full join":
            R(Text(" FULL JOIN ")),
        "join":
            R(Text(" JOIN ")),
        "on columns":
            R(Text(" ON ")),
        "using":
            R(Text(" USING () ") + Key("left/5:2")),
        "insert into":
            R(Text(" INSERT INTO ")),
        "update":
            R(Text(" UPDATE TOKEN SET ")),
        "delete":
            R(Text(" DELETE ")),
        "like":
            R(Text("LIKE '%%'") + Key("left/5:2")),
        "union":
            R(Text("UNION ")),
        "alias as":
            R(Text(" AS ")),
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
        "over partition by":
            R(Text(" OVER (PARTITION BY ) ") + Key("left/5:2")),
    }

    extras = [
        Dictation("dict"),
        Choice("sql_strings", {
            "select":" SELECT ",
            "distinct":"DISTINCT ",
            "(all | every)":"* ",
            "from":" FROM ",
            "where":" WHERE ",
            "use":"USE ",
            "not":"NOT ",
            "and":"AND ",
            "when":"WHEN ",
            "then":"THEN ",
            "else":"ELSE ",
            "null":"NULL ",
        }),
    ]
    defaults = {
        "dict": ""
    }


def get_rule():
    return SQL, RuleDetails(ccrtype=CCRType.GLOBAL)
