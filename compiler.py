import argparse
from lexer import Lexer
from pyparser import Parser 

if __name__=='__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-m', '--mode', action='store', help='select compilator mod: lexer | parser')
    argparser.add_argument('-f', '--file', action='store', help='specify the path to the file')

    flags = argparser.parse_args()
    # BEGIN DEBUG (Can run without command line parameters)
    # flags.mode      = "parser"
    # flags.file      = "tests/request/def"
    # END DEBUG
    match flags.mode:
        case "lexer":
            lex = Lexer(flags.file)
            state = None
            while state != Lexer.EOF:
                print(lex.get_next_token())
                state = lex.state
        case "parser":
            pars = Parser(Lexer(flags.file))
            tree = pars.parse()
            tree.show()
        case _:
            print("Missing paramenter -m (--mode). Select compiler mode (-m parser | -m lexer)")
    if not flags.file:
        print("Missing paramenter -f (--file). Select input file (-f FILE)")