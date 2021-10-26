import pytest
from lexer import Lexer
from pyparser import Parser

def test_tabulation_1():
    pars = Parser(Lexer("tests/parser tests/request/tabulation_1.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/tabulation_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_tabulation_2():
    pars = Parser(Lexer("tests/parser tests/request/tabulation_1.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/tabulation_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_tabulation_3():
    pars = Parser(Lexer("tests/parser tests/request/tabulation_1.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/tabulation_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

if __name__ == '__main__':
    pytest.main()