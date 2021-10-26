import pytest
from lexer import Lexer
from pyparser import Parser

def test_list_1():
    pars = Parser(Lexer("tests/parser tests/request/list_1.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/list_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_2():
    pars = Parser(Lexer("tests/parser tests/request/list_2.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/list_2.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_3():
    pars = Parser(Lexer("tests/parser tests/request/list_3.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/list_3.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_4():
    pars = Parser(Lexer("tests/parser tests/request/list_4.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/list_4.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_5():
    pars = Parser(Lexer("tests/parser tests/request/list_5.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/list_5.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_6():
    pars = Parser(Lexer("tests/parser tests/request/list_6.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/list_6.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_7():
    pars = Parser(Lexer("tests/parser tests/request/list_7.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/list_7.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_8():
    pars = Parser(Lexer("tests/parser tests/request/list_8.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/list_8.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

if __name__ == '__main__':
    pytest.main()