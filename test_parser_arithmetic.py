import pytest
from lexer import Lexer
from pyparser import Parser

def test_arithmetic_1():
    pars = Parser(Lexer("tests/parser tests/request/arithmetic_1.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/arithmetic_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    print(result)
    assert result == answer

def test_arithmetic_2():
    pars = Parser(Lexer("tests/parser tests/request/arithmetic_2.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/arithmetic_2.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_arithmetic_3():
    pars = Parser(Lexer("tests/parser tests/request/arithmetic_3.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/arithmetic_3.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_arithmetic_4():
    pars = Parser(Lexer("tests/parser tests/request/arithmetic_4.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/arithmetic_4.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_arithmetic_5():
    pars = Parser(Lexer("tests/parser tests/request/arithmetic_5.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/arithmetic_5.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_arithmetic_6():
    pars = Parser(Lexer("tests/parser tests/request/arithmetic_6.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/arithmetic_6.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

if __name__ == '__main__':
    pytest.main()