from dragonfly import ShortIntegerRef
from dragonfly.grammar.elements import Choice
from castervoice.lib import printer


class ShortIntegerRef(ShortIntegerRef):
    """
    Compatibility shim for older grammars that use ShortIntegerRef.
    ShortIntegerRef and Integer Remap has been removed use dragonfly ShortIntegerRef
    """

    def __init__(self, name, min, max, default=None):
        printer.out("\nDetected 'ShortIntegerRef' import in rules/grammars.\nShortIntegerRef and Integer Remap has been removed. \nUpdate your rules to `from dragonfly import ShortIntegerRef` in instead of ShortIntegerRef\n")
        super(ShortIntegerRef, self).__init__(name, min, max, default)


class Boolean(Choice):
    def __init__(self, spec):
        Choice.__init__(self, spec, {spec: True})
