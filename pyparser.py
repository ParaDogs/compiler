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
        return node

    def term(self):
        match self.lex.state:        
            case Lexer.LSBRACKET:
                return self.list()
            case Lexer.IDENTIFIER:
                node = Node(Parser.VARIABLE, self.lex.value, [])
                self.lex.get_next_token()
                return node
            case Lexer.INTNUMBER:
                node = Node(Parser.INTNUMBER, self.lex.value, [])
                self.lex.get_next_token()
                return node
            case Lexer.FLOATNUMBER:
                node = Node(Parser.FLOATNUMBER, self.lex.value, [])
                self.lex.get_next_token()
                return node
            case Lexer.STRING:
                node = Node(Parser.STRING, self.lex.value, [])
                self.lex.get_next_token()
                return node
            case Lexer.LRBRACKET:
                self.lex.get_next_token() #?
                node = Node(Parser.FORMULA)
                formula = self.formula()
                node.childrens = formula.childrens # ?????
                if self.lex.state != Lexer.RRBRACKET:
                    self.error("Expected ')'")
                self.lex.get_next_token()
                return node
            case _:
                self.error(f"Unexpected symbol")

    def sum(self):
        left = self.product()
        match self.lex.state:
            case Lexer.PLUS:
                self.lex.get_next_token()
                return Node(Parser.ADD, childrens=[left, self.sum()])
            case Lexer.MINUS: # некоммутативная операция
                while self.lex.state == Lexer.MINUS or self.lex.state == Lexer.PLUS:
                    if self.lex.state == Lexer.MINUS:
                        self.lex.get_next_token()
                        right = self.product()
                        left = Node(Parser.SUB, childrens=[left, right])
                    else:
                        self.lex.get_next_token()
                        right = self.product()
                        left = Node(Parser.ADD, childrens=[left, right])
                return left
            case _:
                return left

    def product(self):
        left = self.term()
        match self.lex.state:
            case Lexer.MULTIPLY:
                self.lex.get_next_token()
                return Node(Parser.MUL, childrens=[left, self.product()])
            case Lexer.DIVISION: # некоммутативная операция
                while self.lex.state == Lexer.DIVISION:
                    self.lex.get_next_token()
                    left = Node(Parser.DIV, childrens=[left, self.term()])
                return left
            case Lexer.REMAINDER: # некоммутативная операция
                while self.lex.state == Lexer.REMAINDER:
                    self.lex.get_next_token()
                    left = Node(Parser.REM, childrens=[left, self.term()])
                return left
            case _:
                return left

    def formula(self):
        left = self.sum()
        match self.lex.state:
            case Lexer.LESS:
                self.lex.get_next_token()
                return Node(Parser.LESS, childrens=[left, self.formula()])
            case Lexer.GREATER:
                self.lex.get_next_token()
                return Node(Parser.GREATER, childrens=[left, self.formula()])
            case _:
                return left

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
            zeroblocks = []
            while self.lex.state == Lexer.TABULATION:
                self.lex.get_next_token()
                zeroblocks += [self.zeroblock()]
        else:
            self.error("Expected indent")
        return Node(Parser.BLOCK, childrens=zeroblocks)

    def zeroblock(self): # TODO можно начинать с elif?
        match self.lex.state:
            # IF pattern
            case Lexer.IF:
                self.lex.get_next_token()
                statement = self.formula()
                if self.lex.state == Lexer.COLON:
                    self.lex.get_next_token()
                    if self.lex.state == Lexer.NEWLINE:
                        return Node(Parser.IFCONSTRUCTION, childrens=[statement, self.block()])
                    else:
                        self.error("Expected new line")
                else:
                    self.error("Expected ':'")
            # ELIF pattern
            case Lexer.ELIF:
                self.lex.get_next_token()
                statement = self.formula()
                if self.lex.state == Lexer.COLON:
                    self.lex.get_next_token()
                    if self.lex.state == Lexer.NEWLINE:
                        return Node(Parser.ELIFCONSTRUCTION, childrens=[statement, self.block()])
                    else:
                        self.error("Expected new line")
                else:
                    self.error("Expected ':'")
            # ELSE pattern
            case Lexer.ELSE:
                self.lex.get_next_token()
                if self.lex.state == Lexer.COLON:
                    self.lex.get_next_token()
                    if self.lex.state == Lexer.NEWLINE:
                        return Node(Parser.ELSECONSTRUCTION, childrens=[self.block()])
                    else:
                        self.error("Expected new line")
                else:
                    self.error("Expected ':'")
            # WHILE pattern
            case Lexer.WHILE:
                self.lex.get_next_token()
                statement = self.formula()
                self.lex.get_next_token()
                if self.lex.state == Lexer.COLON:
                    self.lex.get_next_token()
                    if self.lex.state == Lexer.NEWLINE:
                        return Node(Parser.WHILECONSTRUCTION, childrens=[statement, self.block()])
                    else:
                        self.error("Expected new line")
                else:
                    self.error("Expected ':'")
            # FOR construction
            case Lexer.FOR:
                self.lex.get_next_token()
                if self.lex.state == Lexer.IDENTIFIER:
                    identifier = Node(Parser.VARIABLE, self.lex.value, [])
                    self.lex.get_next_token()
                    if self.lex.state == Lexer.IN:
                        self.lex.get_next_token()
                        formula = self.formula()
                        if self.lex.state == Lexer.COLON:
                            self.lex.get_next_token()
                            if self.lex.state == Lexer.NEWLINE:
                                self.lex.get_next_token()
                                return Node(Parser.FORCONSTRUCTION, childrens=[identifier, formula, self.block()])
                            else:
                                self.error("Expected new line")
                        else:
                            self.error("Expected ':'")
                    else:
                        self.error("Expected 'in'")
                else:
                    self.error("Expected identifier")
            # DEF construction (def ID(FORMALPARAMETERS): \n BLOCK)
            case Lexer.DEF:
                self.lex.get_next_token()
                if self.lex.state == Lexer.IDENTIFIER:
                    identifier = self.lex.value
                    self.lex.get_next_token()
                    formalparameters = self.formalparameters()
                    self.lex.get_next_token()
                    if self.lex.state == Lexer.COLON:
                        self.lex.get_next_token()
                        if self.lex.state == Lexer.NEWLINE:
                            return Node(Parser.DEFCONSTRUCTION, childrens=[identifier, formalparameters, self.block()])
                        else:
                            self.error("Expected new line")
                    else:
                        self.error("Expected ':'")
                else:
                    self.error("Expected function identifier")
            # MODIFICATION (ID = FORMULA)
            case Lexer.IDENTIFIER:
                identifier = Node(Parser.VARIABLE, self.lex.value, [])
                self.lex.get_next_token()
                if self.lex.state == Lexer.SET:
                    self.lex.get_next_token()
                    formula = self.formula()
                    if self.lex.state == Lexer.NEWLINE:
                        self.lex.get_next_token() # newline skip
                    return Node(Parser.MODIFICATION, childrens=[identifier, formula])
            case _: # изолированных формул не будет
                self.error(f"Unexpected syntax")

    # program is zeroblocks (instructions) list
    def program(self):
        zeroblocks = []
        while self.lex.state != Lexer.EOF:
            while self.lex.state == Lexer.NEWLINE: # skip empty lines
                self.lex.get_next_token()
            zeroblocks += [self.zeroblock()]
        return Node(Parser.PROGRAM, childrens=zeroblocks)

    def parse(self):
        self.lex.get_next_token()
        return self.program()