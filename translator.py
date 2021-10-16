# translates syntax tree to JS
from pyparser import Node, Parser

class Translator:
    def __init__(self, node):
        self.node = node

    def translate(self, node):
        match node.pattern:
            case Parser.PROGRAM:
                for child in node.childrens:
                    self.translate(child)
                    print("\n")
            case Parser.IFCONSTRUCTION:
                pass
