import sys
from lexer import Lexer

class Node:
    def __init__(self, pattern, value = None, childrens = []):
        self.pattern = pattern
        self.value = value
        self.childrens = childrens

    def show(self, level=0):
        if self.value != None:
            print(f"{Parser.PRESENTATION[self.pattern]} : {self.value}")
        else:
            print(Parser.PRESENTATION[self.pattern])
        if self.childrens != []:
            for children in self.childrens:
                print('|   '*level,end='')
                print("|+-", end='')
                if children.childrens != []:
                    children.show(level+1)
                else:
                    children.show(level)
            
            
class Parser:
    # patterns
    PROGRAM, ZEROBLOCK, LIST, STATEMENT, MODIFICATION, FORMULA, VARIABLE, FORMALPARAMETERS, FACTPARAMETERS,\
    ADD, SUB, SET, LESS, GREATER, MUL, DIV, REM,\
    IFCONSTRUCTION, ELIFCONSTRUCTION, ELSECONSTRUCTION, WHILECONSTRUCTION, FORCONSTRUCTION, DEFCONSTRUCTION, BLOCK,\
    INTNUMBER, FLOATNUMBER, STRING = range(27)

    PRESENTATION = {
        PROGRAM             : "PROGRAM",
        ZEROBLOCK           : "ZEROBLOCK",
        LIST                : "LIST",
        STATEMENT           : "STATEMENT",
        MODIFICATION        : "MODIFICATION",
        FORMULA             : "FORMULA",
        VARIABLE            : "VARIABLE",
        FORMALPARAMETERS    : "FORMALPARAMETERS",
        FACTPARAMETERS      : "FACTPARAMETERS",
        ADD                 : "ADD",
        SUB                 : "SUB",
        SET                 : "SET",
        MUL                 : "MUL",
        DIV                 : "DIV",
        REM                 : "REM",
        LESS                : "LESS",
        GREATER             : "GREATER",
        IFCONSTRUCTION      : "IFCONSTRUCTION",
        ELIFCONSTRUCTION    : "ELIFCONSTRUCTION",
        ELSECONSTRUCTION    : "ELSECONSTRUCTION",
        WHILECONSTRUCTION   : "WHILECONSTRUCTION",
        FORCONSTRUCTION     : "FORCONSTRUCTION",
        DEFCONSTRUCTION     : "DEFCONSTRUCTION",
        BLOCK               : "BLOCK",
        INTNUMBER           : "INTNUMBER",
        FLOATNUMBER         : "FLOATNUMBER",
        STRING              : "STRING",
    }

    def __init__(self, lex=Lexer()):
        self.lex = lex
    
    def error(self, message):
        print("Parser error:", message, f"in possition {self.lex.row,self.lex.col}")
        sys.exit(1)

    def list(self):
        node = Node(Parser.LIST)
        # self.lex.get_next_token()
        while self.lex.state != Lexer.RSBRACKET:
            node.childrens += [self.formula()]
            self.lex.get_next_token()
            if self.lex.state == Lexer.COMMA:
                self.lex.get_next_token()
        if self.lex.state == Lexer.RSBRACKET:
            self.lex.get_next_token()
        else:
            self.error("Expected ']'")
        # node.show()
        return node

    def term(self):
        token = self.lex.state
        value = self.lex.value
        # self.lex.get_next_token()
        
        if token == Lexer.LSBRACKET:
            return self.list()
        if token == Lexer.IDENTIFIER:
            return Node(Parser.VARIABLE, value, [])
        if token == Lexer.INTNUMBER:
            return Node(Parser.INTNUMBER, value, [])
        if token == Lexer.FLOATNUMBER:
            return Node(Parser.FLOATNUMBER, value, [])
        if token == Lexer.STRING:
            return Node(Parser.STRING, value, [])
        if token == Lexer.LRBRACKET:
            self.lex.get_next_token() #?
            node = Node(Parser.FORMULA)
            formula = self.formula()
            node.childrens = formula.childrens # ?????
            if self.lex.state != Lexer.RRBRACKET:
                self.error("Expected ')'")
            self.lex.get_next_token()
            return node
        else:
            self.error(f"Unexpected symbol")

    def sum(self):
        # left = self.product()
        # if self.lex.state == Lexer.PLUS:
        #     self.lex.get_next_token()
        #     right = self.sum()
        #     return Node(Parser.ADD, childrens=[left, right])
        # if self.lex.state == Lexer.MINUS:
        #     while self.lex.state == Lexer.MINUS:
        #         self.lex.get_next_token()
        #         right = self.product()
        #         left = Node(Parser.SUB, childrens=[left, right])
        #     return left
        # else:
        #     return left
        left = self.product()
        match self.lex.state:
            case Lexer.PLUS:
                self.lex.get_next_token()
                right = self.sum()
                return Node(Parser.ADD, childrens=[left, right])
            case Lexer.MINUS: # некоммутативная операция
                while self.lex.state == Lexer.MINUS:
                    self.lex.get_next_token()
                    right = self.product()
                    left = Node(Parser.SUB, childrens=[left, right])
                return left
            case _:
                return left

    def product(self):
        left = self.term()
        match self.lex.state:
            case Lexer.MULTIPLY:
                self.lex.get_next_token()
                right = self.product()
                return Node(Parser.MUL, childrens=[left, right])
            case Lexer.DIVISION: # некоммутативная операция
                while self.lex.state == Lexer.DIVISION:
                    self.lex.get_next_token()
                    right = self.term()
                    left = Node(Parser.DIV, childrens=[left, right])
                return left
            case Lexer.REMAINDER: # некоммутативная операция
                while self.lex.state == Lexer.REMAINDER:
                    self.lex.get_next_token()
                    right = self.term()
                    left = Node(Parser.REM, childrens=[left, right])
                return left
            case _:
                return left

    def formula(self):
        # left = self.sum()
        # if self.lex.state == Lexer.LESS:
        #     self.lex.get_next_token()
        #     right = self.formula()
        #     return Node(Parser.LESS, childrens=[left, right])
        # elif self.lex.state == Lexer.GREATER:
        #     self.lex.get_next_token()
        #     right = self.formula()
        #     return Node(Parser.GREATER, childrens=[left, right])
        # else:
        #     return left
        match self.lex.state:
            case Lexer.LESS:
                self.lex.get_next_token()
                return Node(Parser.LESS, childrens=[self.sum(), self.formula()])
            case Lexer.GREATER:
                self.lex.get_next_token()
                return Node(Parser.GREATER, childrens=[self.sum(), self.formula()])
            case _:
                return self.sum()

    def factparameters(self):
        # if self.lex.state == Lexer.LRBRACKET:
        #     node = Node(Parser.FACTPARAMETERS)
        #     # self.lex.get_next_token()
        #     while self.lex.state != Lexer.RRBRACKET:
        #         node.childrens += [self.formula()]
        #         self.lex.get_next_token()
        #         if self.lex.state == Lexer.COMMA:
        #             self.lex.get_next_token()
        #     if self.lex.state == Lexer.RRBRACKET:
        #         self.lex.get_next_token()
        #     else:
        #         self.error("Expected ')'")
        # else:
        #     self.error("Expected '('")
        # return node
        node = Node(Parser.FACTPARAMETERS)
        print(self.lex.value)
        while self.lex.state != Lexer.RRBRACKET: 
            # print(self.lex.state)
            node.childrens += [self.formula()]
            self.lex.get_next_token()
            if self.lex.state == Lexer.COMMA:
                self.lex.get_next_token()
        return node

    def formalparameters(self):
        if self.lex.state == Lexer.LRBRACKET:
            node = Node(Parser.FORMALPARAMETERS)
            self.lex.get_next_token()
            while self.lex.state == Lexer.IDENTIFIER:
                node.childrens += [Node(Parser.VARIABLE, self.lex.value)]
                self.lex.get_next_token()
                if self.lex.state == Lexer.COMMA:
                    self.lex.get_next_token()
            if self.lex.state == Lexer.RRBRACKET:
                self.lex.get_next_token()
            else:
                self.error("Expected ')'")
        else:
            self.error("Expected '('")
        return node

    def block(self):
        if self.lex.state == Lexer.TABULATION:
            node = Node(Parser.BLOCK)
            while self.lex.state == Lexer.TABULATION:
                self.lex.get_next_token()
                node.childrens += [self.zeroblock()]
                self.lex.get_next_token()
        else:
            self.error("Expected indent")
        return node

    def zeroblock(self): # TODO можно начинать с elif?
        match self.lex.state:
            # IF pattern
            case Lexer.IF:
                node = Node(Parser.IFCONSTRUCTION)
                self.lex.get_next_token()
                statement = self.formula()
                if self.lex.state == Lexer.COLON:
                    self.lex.get_next_token()
                    if self.lex.state == Lexer.NEWLINE:
                        block = self.block()
                    else:
                        self.error("Expected new line")
                else:
                    self.error("Expected ':'")
                node.childrens = [statement, block]
            # ELIF pattern
            case Lexer.ELIF:
                node = Node(Parser.ELIFCONSTRUCTION)
                self.lex.get_next_token()
                statement = self.formula()
                if self.lex.state == Lexer.COLON:
                    self.lex.get_next_token()
                    if self.lex.state == Lexer.NEWLINE:
                        block = self.block()
                    else:
                        self.error("Expected new line")
                else:
                    self.error("Expected ':'")
                node.childrens = [statement, block]
            # ELSE pattern
            case Lexer.ELSE:
                node = Node(Parser.ELSECONSTRUCTION)
                self.lex.get_next_token()
                if self.lex.state == Lexer.COLON:
                    self.lex.get_next_token()
                    if self.lex.state == Lexer.NEWLINE:
                        block = self.block()
                    else:
                        self.error("Expected new line")
                else:
                    self.error("Expected ':'")
                node.childrens = [block]
            # WHILE pattern
            case Lexer.WHILE:
                node = Node(Parser.WHILECONSTRUCTION)
                self.lex.get_next_token()
                statement = self.formula()
                self.lex.get_next_token()
                if self.lex.state == Lexer.COLON:
                    self.lex.get_next_token()
                    if self.lex.state == Lexer.NEWLINE:
                        block = self.block()
                    else:
                        self.error("Expected new line")
                else:
                    self.error("Expected ':'")
                node.childrens = [statement, block]
            # FOR construction
            case Lexer.FOR:
                node = Node(Parser.FORCONSTRUCTION)
                self.lex.get_next_token()
                if self.lex.state == Lexer.IDENTIFIER:
                    identifier = Node(Parser.VARIABLE, self.lex.value, [])
                    self.lex.get_next_token()
                    if self.lex.state == Lexer.IN:
                        self.lex.get_next_token()
                        formula = self.formula()
                        self.lex.get_next_token()
                        if self.lex.state == Lexer.COLON:
                            self.lex.get_next_token()
                            if self.lex.state == Lexer.NEWLINE:
                                self.lex.get_next_token()
                                block = self.block()
                            else:
                                self.error("Expected new line")
                        else:
                            self.error("Expected ':'")
                    else:
                        self.error("Expected 'in'")
                else:
                    self.error("Expected identifier")
                node.childrens = [identifier, formula, block]
            # DEF construction (def ID in FORMULA: \n BLOCK)
            case Lexer.DEF:
                node = Node(Parser.DEFCONSTRUCTION)
                self.lex.get_next_token()
                if self.lex.state == Lexer.IDENTIFIER:
                    identifier = self.lex.value
                    self.lex.get_next_token()
                    formalparameters = self.formalparameters()
                    self.lex.get_next_token()
                    if self.lex.state == Lexer.COLON:
                        self.lex.get_next_token()
                        if self.lex.state == Lexer.NEWLINE:
                            block = self.block()
                        else:
                            self.error("Expected new line")
                    else:
                        self.error("Expected ':'")
                else:
                    self.error("Expected function identifier")
                node.childrens = [identifier, formalparameters, block]
            # MODIFICATION (ID = FORMULA)
            case Lexer.IDENTIFIER:
                identifier = Node(Parser.VARIABLE, self.lex.value, [])
                self.lex.get_next_token()
                if self.lex.state == Lexer.SET:
                    node = Node(Parser.MODIFICATION, self.lex.value)
                    self.lex.get_next_token()
                    formula = self.formula()
                    node.childrens = [identifier, formula]
                    self.lex.get_next_token() # newline skip
            case _: # изолированных формул не будет
                self.error(f"Unexpected syntax")
        return node

    # program is zeroblocks (instructions) list
    def program(self):
        zeroblocks = []
        while self.lex.state != Lexer.EOF:
            zeroblocks += [self.zeroblock()]
            self.lex.get_next_token()
        return Node(Parser.PROGRAM, childrens=zeroblocks)

    def parse(self):
        self.lex.get_next_token()
        node = self.program()
        # if (self.lex.state != Lexer.EOF):
        #     self.error("Invalid statement syntax")
        return node