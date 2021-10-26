import pytest
from lexer import Lexer
from pyparser import Parser

def test_id_1():
    pars = Parser(Lexer("tests/parser tests/request/id_1.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/id_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_id_2():
    pars = Parser(Lexer("tests/parser tests/request/id_2.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/id_2.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_id_3():
    with pytest.raises(SystemExit) as e:
        pars = Parser(Lexer("tests/parser tests/request/id_3.txt"))
        result = pars.parse().show_str()
        answer_file = open("tests/parser tests/response/id_3.txt", 'r')
        answer = answer_file.read()
        answer_file.close()
    assert e.type == SystemExit
    assert e.value.code == 1

def test_id_4():
    pars = Parser(Lexer("tests/parser tests/request/id_4.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/id_4.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_id_5():
    pars = Parser(Lexer("tests/parser tests/request/id_5.txt"))
    result = pars.parse().show_str()
    answer_file = open("tests/parser tests/response/id_5.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

if __name__ == '__main__':
    pytest.main()