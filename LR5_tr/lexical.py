import re

import functools


import ply.yacc as yacc
from prettytable import PrettyTable
import sys
# Определение регулярных выражений для лексического анализа
keyword_pattern = re.compile(
    r'^(abstract|as|base|break|case|catch|checked|class|'
    r'const|continue|default|delegate|do|double|else|enum|event|'
    r'explicit|extern|false|finally|fixed|for|foreach|goto|if|implicit|'
    r'in|interface|internal|is|lock|long|namespace|new|null|object|operator|'
    r'out|override|params|private|protected|public|readonly|ref|return|sbyte|'
    r'sealed|sizeof|stackalloc|static|struct|switch|this|throw|'
    r'true|try|typeof|unchecked|unsafe|using|virtual|void|'
    r'volatile|while|Console.WriteLine|Convert.ToInt32|Console.ReadLine|Length)\b')

datatype_pattern = re.compile(r'^(bool|double|float|char|string|byte|short|ushort|ulong|uint|decimal|var)\b')

operator_pattern = re.compile(
    r'^(\+|\-|\*|\/|\%|\=|\+=|\-=|\*=|\/=|\%=|\+\+|\-\-|\&|\&&|\|\||\!|\=|'
    r'\==|\!=|\>|\<|\>=|\<=|\?|\:|\|)')

punctuation_pattern = re.compile(r'^(\{|\}|\(|\)|\[|\]|\;|\,|\:|\.)$')

identifier_pattern = re.compile(r'\b[a-zA-Z_$][a-zA-Z_$0-9]*(?:\.[a-zA-Z_$][a-zA-Z_$0-9]*)*\b')

number_pattern = re.compile(r'^(\+|\-)?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?')

string_pattern = re.compile(r'^\$?\".*?\"|\$?\'.*?\'|\$?\$\".*?\"|\$?\$\'.*?\'|\$?\$@\".*?\"')


# Определение класса для лексемы
class Token:
    def __init__(self, type, value, pos):
        self.type = type
        self.value = value
        self.pos = pos

    def __lt__(self, other):
        return self.value < other.value

    def repr(self):
        return 'Token(type={type}, value={value}, pos={pos})'.format(
            type=self.type, value=repr(self.value), pos=self.pos)

    def token_cmp(a, b):
        if isinstance(a, Token) and isinstance(b, Token):
            return a.type < b.type
        elif isinstance(a, Token):
            return True
        elif isinstance(b, Token):
            return False
        else:
            return a < b


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.lst_type = None
        self.lst_data_type = None
        self.stack = []
        self.open_skob = 0;
        self.open_curly = 0;
        self.closed_curly = 0;
        self.open_squ = 0;
        self.closed_squ = 0;

    def error(self):
        raise Exception('Invalid character at position ' + str(self.pos))

    def report_error(self, message):
        line_num = self.text.count('\n', 0, self.pos) + 1
        line_start = self.text.rfind('\n', 0, self.pos) + 1
        line_end = self.text.find('\n', self.pos)
        if line_end == -1:
            line_end = len(self.text)
        line = self.text[line_start:line_end]
        col_num = self.pos - line_start + 1
        print('Lexical error: {} at line {}, column {}:\n{}\n{}^'.format(
            message, line_num, col_num, line, ' ' * (col_num - 1)))

    def get_next_token(self):

        if self.pos >= len(self.text):
            if self.stack:
                self.report_error('bracket error')
                sys.exit()
            if self.open_curly > self.closed_curly:
                print('Unbalanced open curly brackets in your code!')
                sys.exit()
            elif self.open_curly < self.closed_curly:
                print('Unbalanced closed curly brackets in your code!')
                sys.exit()
            if self.open_squ > self.closed_squ:
                print('Unbalanced open square brackets in your code!')
                sys.exit()
            elif self.open_squ < self.closed_squ:
                print('Unbalanced closed square brackets in your code!')
                sys.exit()
            return Token('EOF', '', self.pos)

        current_char = self.text[self.pos]

        # установка начальной позиции
        pos_start = self.pos


        if current_char == '/':
            if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '/':
                self.pos += 1
                while self.pos < len(self.text) and self.text[self.pos] not in '\r\n':
                    self.pos += 1
                return self.get_next_token()
            elif self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '*':
                self.pos += 2
                while self.pos + 1 < len(self.text) and not (self.text[self.pos] == '*' and self.text[self.pos + 1] == '/'):
                    self.pos += 1
                if self.pos + 1 < len(self.text):
                    self.pos += 2
                else:
                    self.report_error('unclosed comment')
                    sys.exit()
                return self.get_next_token()
            else: 
                self.report_error('incorrect comment assignment')
                sys.exit()

        # Определение типа лексемы

        if current_char == ' ' or current_char == '\t':
            self.pos += 1
            return self.get_next_token()
        elif current_char == '\n':
            self.pos += 1
            return Token('NEWLINE', '\n', pos_start)
        elif keyword_pattern.match(self.text[self.pos:]):
            if self.lst_type == 'IDENTIFIER':
                self.pos -= 14
                self.report_error('unexpected IDENTIFIER')
                sys.exit()
            match = keyword_pattern.match(self.text[self.pos:])
            self.lst_type='KEYWORD'
            self.pos += match.end()
            return Token('KEYWORD', match.group(), pos_start)
        elif re.match(r'^int\b', self.text[self.pos:]):
            if self.lst_type == 'TYPE_INT':
                self.report_error('two types in a row')
                sys.exit()
            if self.lst_type == 'IDENTIFIER':
                self.pos -=14
                self.report_error('lexic error identifier')
                sys.exit()
            if self.lst_type != 'PUNCTUATION' and self.lst_type != 'KEYWORD':
                self.report_error('expected PUNCTUATION or KEYWORD before TYPE')
                sys.exit()
            match = re.match(r'^int\b', self.text[self.pos:])
            self.lst_type='TYPE_INT'
            self.lst_data_type='TYPE_INT'
            self.pos += match.end()
            return Token('TYPE_INT', match.group(), pos_start)
        elif datatype_pattern.match(self.text[self.pos:]):
            concreteType = ((datatype_pattern.match(self.text[self.pos:])).group()).upper()
            bool_reg = re.compile(r'^(true|false|1|0)$')
            if self.lst_type == f'TYPE_{concreteType}':
                self.report_error('Two types in a row')
                sys.exit()
            if self.lst_type == 'IDENTIFIER':
                self.pos -= 14
                self.report_error('lexic error identifier')
                sys.exit()
            if self.lst_type != 'PUNCTUATION' and self.lst_type != 'KEYWORD':
                self.pos -= 5
                self.report_error('expected ; before TYPE')
                sys.exit()
            self.lst_type=f'TYPE_{concreteType}'
            self.lst_data_type =f'TYPE_{concreteType}'
            '''if self.lst_data_type == 'TYPE_BOOL':
                print(bool_reg.match(self.text[self.pos:]))
                if not bool_reg.match(self.text[self.pos:]):
                    self.pos +=9
                    self.report_error('datatype error');
                    sys.exit()'''
            match = datatype_pattern.match(self.text[self.pos:])
            self.pos += match.end()
            return Token(f'TYPE_{concreteType}', match.group(), pos_start)
        elif operator_pattern.match(current_char):
            if current_char == '+':
                if self.text[self.pos+1:self.pos+3] == '++':
                    self.report_error('Invalid use of operator "++"')
                    self.pos += 2
                    sys.exit()
            if current_char == '-':
                if self.text[self.pos+1:self.pos+3] == '--':
                    self.report_error('Invalid use of operator "--"')
                    self.pos += 2
                    sys.exit()
            if current_char == '=':
                if self.text[self.pos+1:self.pos+3] == '+=':
                    self.report_error('Invalid use of operator "+="')
                    self.pos += 2
                    sys.exit()
            if current_char == '=':
                if self.text[self.pos+1:self.pos+3] == '%=':
                    self.report_error('Invalid use of operator "%="')
                    self.pos += 2
                    sys.exit()
            if current_char == '=':
                if self.text[self.pos+1:self.pos+3] == '*=':
                    self.report_error('Invalid use of operator "*="')
                    self.pos += 2
                    sys.exit()
            if current_char == '=':
                if self.text[self.pos+1:self.pos+3] == '==':
                    self.report_error('Invalid use of operator "=="')
                    self.pos += 2
                    sys.exit()
            self.lst_type = 'OPERATOR'
            self.pos += 1
            return Token('OPERATOR', current_char, pos_start)
        elif punctuation_pattern.match(current_char):
            if_condition_regex = re.compile(r'^\(.+\)\s*(?:(?:and|or)\s+\(.+\)\s*)*(?:(?:==|!=|>=|<=|>|<)\s*\(.+\)\s*)*$')
            n = 0;
            if current_char == '{':
                self.open_curly += 1
            elif current_char == '}':
                self.closed_curly += 1
            elif current_char == '[':
                self.open_squ += 1
            elif current_char == ']':
                self.closed_squ += 1
            elif current_char == '(':
                self.stack.append('(')
                self.open_skob = self.pos
            elif current_char == ')':
                if not self.stack:
                    self.report_error('Unmatched closing bracket')
                    sys.exit()
                self.stack.pop()
            elif current_char == ';':
                if self.text[self.pos+1] == ';':
                    self.report_error('two ; in a row')
                    self.pos += 2
                    sys.exit()
                if self.text[self.pos+1] == '.':
                    self.report_error('unexpected .')
                    self.pos += 2
                    sys.exit()
                if self.text[self.pos+1] == ',':
                    self.report_error('unexpected ,')
                    self.pos += 2
                    sys.exit()
            elif current_char == ',':
                if self.text[self.pos+1] == ',':
                    self.report_error('two , in a row')
                    self.pos += 2
                    sys.exit()
            elif current_char == '.':
                if self.text[self.pos+1] == '.':
                    self.report_error('two . in a row')
                    self.pos += 2
                    sys.exit()
            elif self.lst_type == 'IDENTIFIER' and re.match(if_condition_regex, self.text[self.pos:]):
                print(re.match(if_condition_regex, self.text[self.pos:]))
                self.report_error('incorrect keyword before condition')
                sys.exit()
            elif current_char == '[':
                ...
            elif current_char == ']':
                ...
            elif self.stack:
                #n = self.pos - self.open_skob
                #self.pos = self.pos - n
                self.pos-=5
                self.report_error('Unmatched opening bracket')
                sys.exit()

            self.lst_type = 'PUNCTUATION'
            self.pos += 1
            return Token('PUNCTUATION', current_char, pos_start)
        elif number_pattern.match(self.text[self.pos:]):
            match = number_pattern.match(self.text[self.pos:])
            self.lst_type = 'NUMBER'
            if self.lst_type == 'NUMBER':
                num = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
                if self.text[self.pos+1:self.pos+2] != ';' and self.text[self.pos+1:self.pos+2] != ')' and self.text[self.pos+1:self.pos+2] != '(' and self.text[self.pos+1:self.pos+2] != ']' and self.text[self.pos+1:self.pos+2] != '.' and self.text[self.pos+1:self.pos+2] != '||' and self.text[self.pos+1:self.pos+2] != '&&' and self.text[self.pos+1:self.pos+2] != ' ' and self.text[self.pos+1:self.pos+2] not in set(num):
                    self.report_error('expected ;')
                    sys.exit()
            self.pos += match.end()
            return Token('NUMBER', match.group(), pos_start)
        elif identifier_pattern.match(self.text[self.pos:]):
            if self.lst_type == 'IDENTIFIER':
                self.report_error('Two IDENTIFIERs in a row')
                sys.exit()
            match = identifier_pattern.match(self.text[self.pos:])
            if match.group() in keyword_pattern.findall(self.text):
                self.report_error('Identifier cannot be a keyword')
                sys.exit()
            self.lst_type = 'IDENTIFIER'
            self.pos += match.end()
            return Token('IDENTIFIER', match.group(), pos_start)
        elif string_pattern.match(self.text[self.pos:]):
            if self.lst_data_type != 'TYPE_STRING' and self.lst_type != 'PUNCTUATION' and self.lst_data_type != 'TYPE_BOOL':
                self.report_error('incorrect datatype assignment')
                sys.exit()
            match = string_pattern.match(self.text[self.pos:])
            if match is None:
                self.report_error('Invalid string format')
                sys.exit()
                return self.get_next_token()
            self.lst_type = 'STRING'
            self.pos += match.end()
            return Token('STRING', match.group(), pos_start)
        else:
            self.report_error('Invalid character: ' + current_char)
            self.pos += 1
            sys.exit()
            return self.get_next_token()


filename = 'Program.cs'
with open(filename, 'r', encoding='utf-8-sig') as f:
    text = f.read()
    f.close()


lexer = Lexer(text)


tokens = []

while True:
    token = lexer.get_next_token()
    tokens.append(token)
    if token.type == 'EOF':
        break


def display_tokens(tokens):
    token_types = sorted(list(set(token.type for token in tokens if token.type != "NEWLINE")))
    for token_type in token_types:
        unique_values = sorted(set(token.value for token in tokens if token.type == token_type))
        table = PrettyTable(['Value', 'Position', 'Count'])
        for value in unique_values:
            positions = [token.pos for token in tokens if token.type == token_type and token.value == value]
            positions.sort()  # sort positions
            count = len(positions)
            table.add_row([value, positions, count])
        print(f'Type: {token_type}')
        print(table)
        print()

display_tokens(tokens)



from ply.lex import LexToken
from ply import yacc


sorted_tokens = sorted(tokens, key=functools.cmp_to_key(Token.token_cmp))


