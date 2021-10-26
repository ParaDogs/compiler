import pytest
from lexer import Lexer

def test_id_1():
    lex = Lexer("tests/lexer tests/request/id_1.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/id_1.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_id_2():
    lex = Lexer("tests/lexer tests/request/id_2.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/id_2.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_id_3():
    with pytest.raises(SystemExit) as e:
        lex = Lexer("tests/lexer tests/request/id_3.txt")
        result = ""
        state = None
        while state != Lexer.EOF:
            result += str(lex.get_next_token()) + '\n'
            state = lex.state
        answer_file = open("tests/lexer tests/response/id_3.txt", 'r')
        answer = answer_file.read()
        answer_file.close()
    assert e.type == SystemExit
    assert e.value.code == 1

def test_id_4():
    lex = Lexer("tests/lexer tests/request/id_4.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/id_4.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

def test_id_5():
    lex = Lexer("tests/lexer tests/request/id_5.txt")
    result = ""
    state = None
    while state != Lexer.EOF:
        result += str(lex.get_next_token()) + '\n'
        state = lex.state
    answer_file = open("tests/lexer tests/response/id_5.txt", 'r')
    answer = answer_file.read()
    answer_file.close()
    assert result == answer

if __name__ == '__main__':
    pytest.main()