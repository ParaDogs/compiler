import sys
from lexer import Lexer

class Node:
    def __init__(self, pattern, value = None, childrens = []):
        self.pattern = pattern
        self.value = value
        self.childrens = childrens

    def show(self, level=0):
        # print(level, self.value)
        if self.value != None:
            print("{} : {}".format(Parser.PRESENTATION[self.pattern],self.value))
        else:
            print(Parser.PRESENTATION[self.pattern])
        if self.childrens != []:
            for children in self.childrens:
                print('|   '*level,end='')
                print("|+-", end='')
                children.show(level+1)
            
class Parser:
    # patterns
    PROGRAM, ATOM, LIST, FUNCTION, STATEMENT, MODIFICATION, FORMULA, VARIABLE, FORMALPARAMETERS, FACTPARAMETERS,\
    ADD, SUB, SET, LESS, GREATER, MUL, DIV, REM,\
    IFCONSTRUCTION, ELIFCONSTRUCTION, ELSECONSTRUCTION, WHILECONSTRUCTION, FORCONSTRUCTION, DEFCONSTRUCTION, BLOCK,\
    INTNUMBER, FLOATNUMBER, LIST, STRING = range(29)

    PRESENTATION = {
        PROGRAM             : "PROGRAM",
        LIST                : "LIST",
        FUNCTION            : "FUNCTION",
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
        LIST                : "LIST",
        STRING              : "STRING",
    }

    def __init__(self):
        self.lex = Lexer()
    
    def __init__(self, lex):
        self.lex = lex
    
    def error(self, message):
        print("Parser error:", message)
        sys.exit(1)

    def list(self):
        if self.lex.state == Lexer.LSBRACKET:
            node = Node(Parser.LIST)
            self.lex.get_next_token()
            while self.lex.state != Lexer.RSBRACKET:
                node.childrens += [self.formula()]
                self.lex.get_next_token()
                if self.lex.state == Lexer.COMMA:
                    self.lex.get_next_token()
            if self.lex.state == Lexer.RSBRACKET:
                self.lex.get_next_token()
            else:
                self.error("Expected ']")
        else:
            self.error("Expected '['")
        return node

    def term(self):
        token = self.lex.state
        value = self.lex.value
        self.lex.get_next_token()
        
        if token == Lexer.IDENTIFIER:
            return Node(Parser.VARIABLE, value)
        if token == Lexer.INTNUMBER:
            return Node(Parser.INTNUMBER, value)
        if token == Lexer.FLOATNUMBER:
            return Node(Parser.FLOATNUMBER, value)
        if token == Lexer.LSBRACKET:
            return self.list()
        if token == Lexer.STRING:
            return Node(Parser.STRING, value)
        if token == Lexer.LRBRACKET:
            node = Node(Parser.FORMULA)
            formula = self.formula()
            node.childrens = formula.childrens
            if self.lex.state != Lexer.RRBRACKET:
                self.error("Expected ')'")
            self.lex.get_next_token()
            return node
        else:
            self.error(f"Unexpected symbol {self.lex.value} in {self.lex.row,self.lex.col}")

    def sum(self):
        left = self.product()
        if self.lex.state == Lexer.PLUS:
            self.lex.get_next_token()
            right = self.sum()
            return Node(Parser.ADD, childrens=[left, right])
        if self.lex.state == Lexer.MINUS:
            vec = []
            while self.lex.state == Lexer.MINUS:
                self.lex.get_next_token()
                right = self.product()
                left = Node(Parser.SUB, childrens=[left, right])
            return left
        else:
            return left

    def product(self):
        left = self.term()
        token = self.lex.state
        if token == Lexer.MULTIPLY:
            self.lex.get_next_token()
            right = self.product()
            return Node(Parser.MUL, childrens=[left, right])
        elif token == Lexer.DIVISION:
            self.lex.get_next_token()
            right = self.product()
            return Node(Parser.DIV, childrens=[left, right])
        elif token == Lexer.REMAINDER:
            self.lex.get_next_token()
            right = self.product()
            return Node(Parser.REM, childrens=[left, right])
        else:
            return left

    def formula(self):
        left = self.sum()
        token = self.lex.state
        if token == Lexer.LESS:
            self.lex.get_next_token()
            right = self.formula()
            return Node(Parser.LESS, childrens=[left, right])
        elif token == Lexer.GREATER:
            self.lex.get_next_token()
            right = self.formula()
            return Node(Parser.GREATER, childrens=[left, right])
        else:
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
            node = Node(Parser.BLOCK)
            while self.lex.state == Lexer.TABULATION:
                self.lex.get_next_token()
                node.childrens += [self.zeroblock()]
        else:
            self.error("Expected indent")
        return node

    def zeroblock(self):
        # IF pattern
        if self.lex.state == Lexer.IF:
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
        elif self.lex.state == Lexer.ELIF:
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
        elif self.lex.state == Lexer.ELSE:
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
        elif self.lex.state == Lexer.WHILE:
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
        elif self.lex.state == Lexer.FOR:
            node = Node(Parser.FORCONSTRUCTION)
            self.lex.get_next_token()
            if self.lex.state == Lexer.IDENTIFIER:
                identifier = Node(Parser.VARIABLE, self.lex.value)
                self.lex.get_next_token()
                if self.lex.state == Lexer.IN:
                    self.lex.get_next_token()
                    formula = self.formula()
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
        # DEF construction
        elif self.lex.state == Lexer.DEF:
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
        # MODIFICATION or FUNCTION
        elif self.lex.state == Lexer.IDENTIFIER:
            identifier = Node(Parser.VARIABLE, self.lex.value)
            self.lex.get_next_token()
            if self.lex.state == Lexer.LRBRACKET:
                self.lex.get_next_token() #
                node = Node(Parser.FUNCTION)
                node.childrens = [identifier, self.factparameters()]
                if self.lex.state != Lexer.RRBRACKET: #
                    self.error("Expected ')'")
            elif self.lex.state == Lexer.SET:
                node = Node(Parser.MODIFICATION, self.lex.value)
                self.lex.get_next_token()
                formula = self.formula()
                node.childrens = [identifier, formula]
        # FORMULA
        else:
            node = Node(Parser.FORMULA)
            formula = self.formula()
            node.childrens = formula.childrens
        self.lex.get_next_token()
        return node

    # program is zeroblocks list
    def program(self):
        zeroblocks = []
        while self.lex.state != Lexer.EOF:
            zeroblocks += [self.zeroblock()]
            self.lex.get_next_token()
        return zeroblocks

    def parse(self):
        self.lex.get_next_token()
        node = Node(Parser.PROGRAM, childrens=self.program())
        if (self.lex.state != Lexer.EOF):
            self.error("Invalid statement syntax")
        return node