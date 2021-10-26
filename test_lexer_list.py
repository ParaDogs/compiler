import pytest
from lexer import Lexer

def test_list_1():
    lex = Lexer("tests/lexer tests/request/list_1.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/list_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_2():
    lex = Lexer("tests/lexer tests/request/list_2.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/list_2.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_3():
    lex = Lexer("tests/lexer tests/request/list_3.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/list_3.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_4():
    lex = Lexer("tests/lexer tests/request/list_4.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/list_4.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_5():
    lex = Lexer("tests/lexer tests/request/list_5.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/list_5.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_6():
    lex = Lexer("tests/lexer tests/request/list_6.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/list_6.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_7():
    lex = Lexer("tests/lexer tests/request/list_7.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/list_7.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_list_8():
    lex = Lexer("tests/lexer tests/request/list_8.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/list_8.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

if __name__ == '__main__':
    pytest.main()