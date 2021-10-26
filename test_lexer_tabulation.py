import pytest
from lexer import Lexer

def test_tabulation_1():
    lex = Lexer("tests/lexer tests/request/tabulation_1.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/tabulation_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_tabulation_2():
    lex = Lexer("tests/lexer tests/request/tabulation_2.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/tabulation_2.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_tabulation_3():
    lex = Lexer("tests/lexer tests/request/tabulation_3.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/tabulation_3.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

if __name__ == '__main__':
    pytest.main()