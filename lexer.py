import sys

class Lexem:
    def __init__(self, row, col, type, value):
        self.row, self.col, self.type, self.value = row, col, type, value
    
    def __repr__(self):
        return f"({self.row}, {self.col})\t{Lexer.PRESENTATION[self.type]}\t{self.value}"

class Lexer:
    def __init__(self, file=sys.stdin, debug=False):
        self.file = open(file, 'r') if file != sys.stdin else sys.stdin
        self.state = None
        self.debug = debug

    # types of lexemes
    INTNUMBER, FLOATNUMBER, IDENTIFIER, STRING,\
    IF, ELIF, ELSE, WHILE, FOR, DEF, IN, RETURN,\
    PRINT, RANGE, TRUE, FALSE,\
    SET, PLUS, MINUS, MULTIPLY, DIVISION, REMAINDER,\
    LRBRACKET, RRBRACKET, LSBRACKET, RSBRACKET,\
    TABULATION, COMMA, COLON, LESS, GREATER, QUOTE1, QUOTE2, DECIMALPOINT, NEWLINE, EOF = range(36)

    # alphabet = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789()[]\'\""
    PRESENTATION = {
        INTNUMBER   : "integer",
        FLOATNUMBER : "float",
        IDENTIFIER  : "id",
        STRING      : "string",
        IF          : "if",
        ELIF        : "elif",
        ELSE        : "else",
        WHILE       : "while",
        FOR         : "for",
        DEF         : "def",
        IN          : "in",
        RETURN      : "return",
        PRINT       : "print",
        RANGE       : "range",
        TRUE        : "True",
        FALSE       : "False",
        SET         : "set",
        PLUS        : "plus",
        MINUS       : "minus",
        MULTIPLY    : "mult",
        DIVISION    : "div",
        REMAINDER   : "rem",
        LRBRACKET   : "lrbrack",
        RRBRACKET   : "rrbrack",
        LSBRACKET   : "lsbrack",
        RSBRACKET   : "rsbrack",
        TABULATION  : "tab",
        COMMA       : "comma",
        COLON       : "colon",
        LESS        : "less",
        GREATER     : "greater",
        QUOTE1      : "quote1",
        QUOTE2      : "quote2",
        DECIMALPOINT: "point",
        NEWLINE     : "newline",
        EOF         : "EOF",
    }

    KEYWORDS = {
        'if'        : IF,
        'elif'      : ELIF,
        'else'      : ELSE,
        'while'     : WHILE,
        'for'       : FOR,
        'def'       : DEF,
        'in'        : IN,
        'return'    : RETURN,
    }

    RESERVEDNAMES = {
        'print'     : PRINT,
        'range'     : RANGE,
        'True'      : TRUE,
        'False'     : FALSE, 
    }

    SYMBOLS = {
        '='         : SET,
        '+'         : PLUS,
        '-'         : MINUS,
        '*'         : MULTIPLY,
        '/'         : DIVISION,
        '%'         : REMAINDER,
        '('         : LRBRACKET,
        ')'         : RRBRACKET,
        '['         : LSBRACKET,
        ']'         : RSBRACKET,
        '    '      : TABULATION,
        ','         : COMMA,
        ':'         : COLON,
        '<'         : LESS,
        '>'         : GREATER,
        "'"         : QUOTE1,
        '"'         : QUOTE2,
        '.'         : DECIMALPOINT,
        '\n'        : NEWLINE,
    }

    current_char = None
    row, col = 1,0

    def error(self, message):
        print("Lexer error:", message)
        sys.exit(1)

    def get_next_char(self):
        if self.current_char == '\n':
            self.row += 1
            self.col = 0
        self.current_char = self.file.read(1)
        self.col += 1

    def get_next_token(self):
        self.state = None
        self.value = None
        while self.state == None:
            if self.current_char == None:
                self.get_next_char()

            # end of file
            if len(self.current_char) == 0:
                # row, col = self.row, self.col
                self.state = Lexer.EOF
            # comment
            elif self.current_char == '#':
                while self.current_char not in ['\n', '']:
                    self.get_next_char()
            # whitespaces and tabulation
            elif self.current_char == ' ':
                tabulation = ""
                # row,col = self.row,self.col
                while self.current_char == ' ':
                    tabulation += self.current_char
                    self.get_next_char()
                    if len(tabulation) == 4 and col == 1: # if new line
                        self.state = Lexer.SYMBOLS[tabulation]
                        self.value = tabulation
                        break
                if len(tabulation) != 4 and len(tabulation) > 1: # if new line
                    if col == 1:
                        self.error(f'Incorrect indent in position {row,col}')
            # string quote1
            elif self.current_char == "'":
                # row,col = self.row,self.col
                self.state = Lexer.STRING
                self.value = ""
                self.get_next_char()
                while self.current_char != "'":
                    self.value += self.current_char
                    self.get_next_char()
                self.get_next_char()
            # string quote2
            elif self.current_char == '"':
                # row,col = self.row,self.col
                self.state = Lexer.STRING
                self.value = ""
                self.get_next_char()
                while self.current_char != '"':
                    self.value += self.current_char
                    self.get_next_char()
                self.get_next_char()
            # symbols
            elif self.current_char in Lexer.SYMBOLS:
                # row,col = self.row,self.col
                # if self.current_char == '\n':
                #     self.row += 1
                #     self.col = 0              
                self.state = Lexer.SYMBOLS[self.current_char]
                self.value = self.current_char #?
                self.get_next_char() #?
            # numbers float and integer
            elif self.current_char.isdigit():
                # row,col = self.row,self.col
                number = 0
                while self.current_char.isdigit():
                    number = number*10 + int(self.current_char)
                    self.get_next_char()
                if self.current_char.isalpha() or self.current_char == "_":
                    self.error(f'Invalid identifier in position {self.row,self.col}')
                if self.current_char == '.':
                    number = str(number)
                    number += '.'
                    self.get_next_char()
                    while self.current_char.isdigit():
                        number += self.current_char
                        self.get_next_char()
                    self.state = Lexer.FLOATNUMBER
                else:
                    self.state = Lexer.INTNUMBER
                self.value = str(number)
            # identifiers, keywords and reserved names
            elif self.current_char.isalpha() or self.current_char == '_':
                # row,col = self.row,self.col
                identifier = ""
                while self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_':
                    identifier += self.current_char
                    self.get_next_char()
                if identifier in Lexer.KEYWORDS:
                    self.state = Lexer.KEYWORDS[identifier]
                    self.value = identifier #?
                elif identifier in Lexer.RESERVEDNAMES:
                    self.state = Lexer.RESERVEDNAMES[identifier]
                    self.value = identifier #?
                else:
                    self.state = Lexer.IDENTIFIER
                    self.value = identifier
            else:
                self.error(f'Unexpected symbol: {self.current_char} in position {self.row,self.col}')
        # return {"state" : self.state, "value" : self.value}
        lexem = Lexem(self.row, self.col, self.state, self.value)
        if self.debug: print(lexem)
        return lexem