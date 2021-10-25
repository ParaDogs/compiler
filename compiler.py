import argparse
from lexer import Lexer
from pyparser import Parser 

if __name__=='__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-l', '--lexemes', action='store_true', help='get a lexemes list of the file')
    argparser.add_argument('-t', '--tree', action='store_true', help='get a syntax tree of the file')
    argparser.add_argument('-c', '--compile', action='store_true', help='get a program by the file')
    argparser.add_argument('-f', '--file', action='store', help='specify the path to the file (default stream: sys.stdin)')

    flags = argparser.parse_args()
    # BEGIN DEBUG
    flags.lexemes   = False
    flags.tree      = True
    flags.file      = "tests\id.txt"
    # END DEBUG
    if flags.file is not None:
        lex = Lexer(flags.file, debug=True)
    else:
        lex = Lexer(debug=True)
    if flags.lexemes:
        if not flags.tree:
            lex.debug = False
            state = None
            while state != Lexer.EOF:
                print(lex.get_next_token())
                state = lex.state 
    else:
        lex.debug = False
    if flags.tree:
        pars = Parser(lex)
        tree = pars.parse()
        tree.show()
    if flags.compile:
        pass
    