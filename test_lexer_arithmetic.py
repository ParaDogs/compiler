import pytest
from lexer import Lexer

def test_arithmetic_1():
    lex = Lexer("tests/lexer tests/request/arithmetic_1.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/arithmetic_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_arithmetic_2():
    lex = Lexer("tests/lexer tests/request/arithmetic_2.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/arithmetic_2.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_arithmetic_3():
    lex = Lexer("tests/lexer tests/request/arithmetic_3.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/arithmetic_3.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_arithmetic_4():
    lex = Lexer("tests/lexer tests/request/arithmetic_4.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/arithmetic_4.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_arithmetic_5():
    lex = Lexer("tests/lexer tests/request/arithmetic_5.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/arithmetic_5.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_arithmetic_6():
    lex = Lexer("tests/lexer tests/request/arithmetic_6.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/arithmetic_6.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

if __name__ == '__main__':
    pytest.main()