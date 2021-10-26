import pytest
from lexer import Lexer

def test_for_1():
    lex = Lexer("tests/lexer tests/request/for_1.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/for_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_for_2():
    lex = Lexer("tests/lexer tests/request/for_2.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/for_2.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_for_3():
    lex = Lexer("tests/lexer tests/request/for_3.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/for_3.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

if __name__ == '__main__':
    pytest.main()