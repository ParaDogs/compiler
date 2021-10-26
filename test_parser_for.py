import pytest
from lexer import Lexer
from pyparser import Parser

def test_for_1():
    pars = Parser(Lexer("tests/parser tests/request/for_1.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/for_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_for_2():
    pars = Parser(Lexer("tests/parser tests/request/for_2.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/for_2.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_for_3():
    pars = Parser(Lexer("tests/parser tests/request/for_3.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/for_3.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

if __name__ == '__main__':
    pytest.main()