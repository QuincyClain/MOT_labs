import ply.lex as lex
import ply.yacc as yacc


#класс дерева

class Tree:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def add_child(self, child_node):
        self.children.append(child_node)

    def remove_child(self, del_node):
        self.children = [child for child in self.children if child is not del_node]

    def traverse(self):
        nodes_to_visit = [self]
        while nodes_to_visit:
            current_node = nodes_to_visit.pop()
            print(current_node.value)
            nodes_to_visit += current_node.children

    def repr(self):
        return 'Token(type={type}, value={value}, pos={pos})'.format(
            type=self.type, value=repr(self.value), pos=self.pos)

#получаем список токенов 

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


#повторное отображение для наглядности

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



#некоторый разбор правил для синтаксического анализа PLY

lexer = lex.lex()


#В ОПИСАНИИ ПРАВИЛ ДЛЯ БИБЛИОТЕКИ PLY У МНОГИХ ЯЗЫКОВ ЕСТЬ СХОЖИЕ ПРАВИЛА, ПОЭТОМУ НЕ ЗНАЮ КАК НАПИСАТЬ БЕЗ ПЛАГИАТА

# Синтаксический анализатор
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

def p_statement_assign(p):
    '''statement : IDENTIFIER ASSIGN expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])


def p_statement(p):
    '''statement : expression
                 | assignment'''
    p[0] = p[1]

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = (p[2], p[1], p[3])

#полное описание binop

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = ('neg', p[2])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : INT
                  | FLOAT'''
    p[0] = ('num', p[1])

def p_error(p):
    if p:
        print("Синтаксическая ошибка на '%s'" % p.value)
    else:
        print("Синтаксическая ошибка EOF")

def p_while_statement(p):
    '''while_statement : WHILE LPAREN condition RPAREN block
                       | WHILE LPAREN condition RPAREN line semicolons'''
    p[0] = ('while', [p[3], p[5]])

def p_if_statement(p):
    '''while_statement : IF LPAREN condition RPAREN block
                       | IF LPAREN condition RPAREN line semicolons'''
    p[0] = ('if', [p[3], p[5]])


def p_condition(p):
    '''condition : expr cond_sign expr'''
    p[0] = ('condition', [p[1], p[2], p[3]])



def display_treeNodes(self, level=0):
        indent = " " * level * 4
        print(f"{indent}{self.value}")
        for child in self.children:
            child.pretty_print(level + 1)



#будет дополнено правилами



# <attributes> <return-type> <identifier> ( <formal-parameter-list> ) <body>


#function

def p_function_declaration(p):
    """
    function_declaration : attributes_opt type_specifier IDENTIFIER LPAREN formal_parameters_opt RPAREN block
                          | attributes_opt VOID IDENTIFIER LPAREN formal_parameters_opt RPAREN block
    """
    p[0] = ("function_declaration", p[1], p[2], p[3], p[5], p[7])

def p_attributes_opt(p):
    """
    attributes_opt : attributes
                   | empty
    """
    p[0] = p[1]


def p_function_decl(p):
    """
    function_declaration : attributes_opt type_specifier IDENTIFIER LPAREN formal_parameters_opt RPAREN block
                          | VOID IDENTIFIER LPAREN formal_parameters_opt RPAREN block
    """
    p[0] = ("function_declaration", p[1], p[2], p[3], p[5], p[7])

def p_attributes_opt(p):
    """
    attributes_opt : attributes
                   | empty
    """
    p[0] = p[1]

def p_attributes(p):
    """
    attributes : attribute
               | attributes attribute
    """
    if len(p) == 2:
        p[0] = ("attributes", p[1])
    else:
        p[0] = ("attributes", p[1], p[2])

def p_attribute(p):
    """
    attribute : LBRACKET IDENTIFIER RPAREN
              | LBRACKET IDENTIFIER LPAREN RPAREN RPAREN
              | LBRACKET IDENTIFIER LPAREN IDENTIFIER RPAREN RPAREN
    """
    if len(p) == 4:
        p[0] = ("attribute", p[2])
    elif len(p) == 6:
        p[0] = ("attribute", p[2], p[4])
    else:
        p[0] = ("attribute", p[2], p[4], p[5])

def p_formal_parameters_opt(p):
    """
    formal_parameters_opt : formal_parameters
                          | empty
    """
    p[0] = p[1]



def p_block(p):
    """
    block : LBRACE statements RBRACE
    """
    p[0] = ("block", p[2])


def p_parameter(p):
    """
    parameter : type_specifier IDENTIFIER
              | REF type_specifier IDENTIFIER
    """
    if len(p) == 3:
        p[0] = ("parameter", p[1], p[2])
    else:
        p[0] = ("parameter", p[1], p[2], p[3])


def main():

    #тест дерева
    root = TreeNode("Root")
    child1 = TreeNode("Child 1")
    subchild1 = TreeNode("Subchild 1")
    child1.add_child(subchild1)
    root.add_child(child1)
    root.display_treeNodes()



parser = yacc.yacc()







