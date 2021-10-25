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
    PROGRAM, LIST, STATEMENT, MODIFICATION, FORMULA, FUNCTION, IDENTIFIER, FORMALPARAMETERS, FACTPARAMETERS,\
    ADD, SUB, SET, LESS, GREATER, MUL, DIV, REM,\
    IFCONSTRUCTION, ELIFCONSTRUCTION, ELSECONSTRUCTION, WHILECONSTRUCTION, FORCONSTRUCTION, DEFCONSTRUCTION, BLOCK,\
    INTNUMBER, FLOATNUMBER, STRING, RETURN, LISTELEMENT = range(29)

    PRESENTATION = {
        PROGRAM             : "PROGRAM",
        LIST                : "LIST",
        STATEMENT           : "STATEMENT",
        MODIFICATION        : "MODIFICATION",
        FORMULA             : "FORMULA",
        FUNCTION            : "FUNCTION",
        IDENTIFIER          : "IDENTIFIER",
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
        RETURN              : "RETURN",
        LISTELEMENT         : "LISTELEMENT"
    }

    def __init__(self, lex):
        self.lex = lex
    
    def error(self, message):
        print("Parser error:", message, f"in possition {self.lex.row,self.lex.col}")
        sys.exit(1)

    def list(self):
        formulas = []
        if self.lex.state == Lexer.LSBRACKET:
            self.lex.get_next_token()
        while self.lex.state != Lexer.RSBRACKET:
            formulas += [self.formula()]
            if self.lex.state == Lexer.COMMA:
                self.lex.get_next_token()
        return Node(Parser.LIST, childrens=formulas)

    def term(self):
        match self.lex.state:        
            case Lexer.LSBRACKET:
                node = self.list()
                if self.lex.state != Lexer.RSBRACKET:
                    self.error("Expected ']'")
                self.lex.get_next_token()
                return node
            case Lexer.IDENTIFIER:
                identifier = Node(Parser.IDENTIFIER, self.lex.value)
                self.lex.get_next_token()
                match self.lex.state:
                    case Lexer.LRBRACKET: # function call
                        factparameters = self.factparameters()
                        return Node(Parser.FUNCTION, childrens=[identifier,factparameters])
                    case Lexer.LSBRACKET: # list element
                        self.lex.get_next_token()
                        index = self.formula()
                        if self.lex.state != Lexer.RSBRACKET:
                            self.error("Expected ']'")
                        self.lex.get_next_token()
                        return Node(Parser.LISTELEMENT, childrens=[identifier,index])                            
                    case _: # identifier
                        return identifier
            case Lexer.INTNUMBER:
                node = Node(Parser.INTNUMBER, self.lex.value)
                self.lex.get_next_token()
                return node
            case Lexer.FLOATNUMBER:
                node = Node(Parser.FLOATNUMBER, self.lex.value)
                self.lex.get_next_token()
                return node
            case Lexer.STRING:
                node = Node(Parser.STRING, self.lex.value)
                self.lex.get_next_token()
                return node
            case Lexer.LRBRACKET:
                self.lex.get_next_token()
                formula = self.formula()
                if self.lex.state != Lexer.RRBRACKET:
                    self.error("Expected ')'")
                self.lex.get_next_token()
                return formula
            case _:
                self.error(f"Unexpected symbol")

    def sum(self):
        left = self.product()
        match self.lex.state:
            case Lexer.PLUS:
                self.lex.get_next_token()
                return Node(Parser.ADD, childrens=[left, self.sum()])
            case Lexer.MINUS: # noncommutative operation (1 - 2 - 3 и 1 + 1 - 1 + 1)
                while self.lex.state in [Lexer.MINUS, Lexer.PLUS]:
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
            case (Lexer.DIVISION | Lexer.REMAINDER): # noncommutative operation with same priority
                while self.lex.state in [Lexer.DIVISION, Lexer.MULTIPLY, Lexer.REMAINDER]:
                    match self.lex.state:
                        case Lexer.DIVISION:
                            self.lex.get_next_token()
                            right = self.term()
                            left = Node(Parser.DIV, childrens=[left, right])
                        case Lexer.MULTIPLY:
                            self.lex.get_next_token()
                            right = self.term()
                            left = Node(Parser.MUL, childrens=[left, right])
                        case Lexer.REMAINDER:
                            self.lex.get_next_token()
                            right = self.term()
                            left = Node(Parser.REM, childrens=[left, right])
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
        if self.lex.state == Lexer.LRBRACKET:
            formulas = []
            self.lex.get_next_token()
            while self.lex.state != Lexer.RRBRACKET:
                formulas += [self.formula()]
                if self.lex.state == Lexer.COMMA:
                    self.lex.get_next_token()
            if self.lex.state == Lexer.RRBRACKET:
                self.lex.get_next_token()
            else:
                self.error("Expected ')'")
        else:
            self.error("Expected '('")
        return Node(Parser.FACTPARAMETERS, childrens=formulas)

    def formalparameters(self):
        if self.lex.state == Lexer.LRBRACKET:
            parameters = []
            self.lex.get_next_token()
            while self.lex.state == Lexer.IDENTIFIER:
                parameters += [Node(Parser.IDENTIFIER, self.lex.value)]
                self.lex.get_next_token()
                if self.lex.state == Lexer.COMMA:
                    self.lex.get_next_token()
            if self.lex.state == Lexer.RRBRACKET:
                self.lex.get_next_token()
            else:
                self.error("Expected ')'")
        else:
            self.error("Expected '('")
        return Node(Parser.FORMALPARAMETERS, childrens=parameters)

    def block(self):
        if self.lex.state == Lexer.TABULATION:
            zeroblocks = []
            while self.lex.state == Lexer.TABULATION:
                self.lex.get_next_token()
                zeroblocks += [self.zeroblock()]
        else:
            self.error("Expected indent")
        return Node(Parser.BLOCK, childrens=zeroblocks)

    def zeroblock(self): # TODO можно начинать с elif? (обработать или здесь или в семантическом анализаторе)
        match self.lex.state:
            # IF pattern (if FORMULA: \n BLOCK)
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
            # ELIF pattern (elif FORMULA: \n BLOCK)
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
            # ELSE pattern (else: \n BLOCK)
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
            # WHILE pattern (def ID(FORMALPARAMETERS): \n BLOCK)
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
            # FOR pattern (for ID in FORMULA: \n BLOCK)
            case Lexer.FOR:
                self.lex.get_next_token()
                if self.lex.state == Lexer.IDENTIFIER:
                    identifier = Node(Parser.IDENTIFIER, self.lex.value)
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
                    identifier = Node(Parser.IDENTIFIER, self.lex.value)
                    self.lex.get_next_token()
                    formalparameters = self.formalparameters()
                    if self.lex.state == Lexer.COLON:
                        self.lex.get_next_token()
                        if self.lex.state == Lexer.NEWLINE:
                            self.lex.get_next_token()
                            return Node(Parser.DEFCONSTRUCTION, childrens=[identifier, formalparameters, self.block()])
                        else:
                            self.error("Expected new line")
                    else:
                        self.error("Expected ':'")
                else:
                    self.error("Expected function identifier")
            # MODIFICATION (ID = FORMULA)
            case Lexer.IDENTIFIER:
                identifier = Node(Parser.IDENTIFIER, self.lex.value)
                self.lex.get_next_token()
                if self.lex.state == Lexer.SET:
                    self.lex.get_next_token()
                    formula = self.formula()
                    if self.lex.state == Lexer.NEWLINE:
                        self.lex.get_next_token() # newline skip
                    return Node(Parser.MODIFICATION, childrens=[identifier, formula])                
            # RETURN for DEF-construction
            case Lexer.RETURN:
                self.lex.get_next_token()
                return Node(Parser.RETURN, childrens=[self.formula()])
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