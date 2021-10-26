import pytest
from lexer import Lexer

def test_def_1():
    lex = Lexer("tests/lexer tests/request/def_1.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/def_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_def_2():
    lex = Lexer("tests/lexer tests/request/def_2.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/def_2.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_def_3():
    lex = Lexer("tests/lexer tests/request/def_2.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/def_2.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

if __name__ == '__main__':
    pytest.main()