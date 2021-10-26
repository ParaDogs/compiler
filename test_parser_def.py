import pytest
from lexer import Lexer
from pyparser import Parser

def test_def_1():
    pars = Parser(Lexer("tests/parser tests/request/def_1.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/def_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_def_2():
    pars = Parser(Lexer("tests/parser tests/request/def_2.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/def_2.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_def_3():
    pars = Parser(Lexer("tests/parser tests/request/def_3.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/def_3.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

if __name__ == '__main__':
    pytest.main()