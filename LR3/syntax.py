import ply.lex as lex
import ply.yacc as yacc

from lark import Lark, Transformer, v_args


# Описание грамматики языка C# в формате EBNF
grammar = r"""
    start: type_declaration

    type_declaration: class_declaration
                     | struct_declaration
                     | interface_declaration

    class_declaration: "class" NAME "{" [class_member]* "}"
    struct_declaration: "struct" NAME "{" [class_member]* "}"
    interface_declaration: "interface" NAME "{" [interface_member]* "}"

    class_member: method_declaration
                | field_declaration
                | property_declaration

    interface_member: method_declaration
                     | property_declaration

    method_declaration: [static] return_type NAME "(" [parameter_list] ")" [method_body] 
    property_declaration: return_type NAME "{" [property_accessor]* "}"
    field_declaration: [static] type NAME ";"
    
    return_stmt: "return" expression ";"

    static: "static"
    
    parameter_keyword: "ref"
                    |  "out"

    parameter_list: parameter ("," parameter)*
    parameter: [parameter_keyword] type NAME

    method_body: "{" [statement]* "}"

    property_accessor: get_accessor | set_accessor
    get_accessor: "get" "{" [statement]* "}"
    set_accessor: "set" "{" [statement]* "}"

    property_call: NAME "." NAME

    statement: assignment
              | declaration
              | method_call
              | return_stmt
              | for_loop
              | operator_if

    assignment: NAME "=" expression ";"
    declaration: type NAME ["=" expression ]";"
    method_call: NAME "(" [expression_list] ")" ";"

    expression_list: expression ("," expression)*
    expression: term
               | expression "+" expression -> add
               | expression "-" expression -> sub

    term: factor
        | term "*" term -> mul
        | term "/" term -> div

    factor: INT -> int
          | FLOAT -> float
          | STRING -> string
          | "(" expression ")"
          | NAME
          | increment
          | decrement

    increment: NAME "++"
            | "++" NAME
    decrement: NAME "--"
            | "--" NAME

    arr_type: base_type "[]"      

    base_type: "int" -> int_type
        | "float" -> float_type
        | "string" -> string_type

    return_type: "void" -> void_type
                | type

    type: base_type
        | arr_type

    for_loop: "for" "(" for_initializer [for_condition] ";" [for_iterator] ")" method_body
    for_initializer: declaration | assignment | ";"
    for_condition: comparison
    for_iterator: NAME "=" expression
                | increment
                |  decrement

    operator_if: "if" "(" if_condition ")" method_body
    if_condition: comparison          

    comparison: expression "==" expression -> eq
               | expression "!=" expression -> neq
               | expression ">" expression -> gt
               | expression ">=" expression -> gte
               | expression "<" expression -> lt
               | expression "<=" expression -> lte

    comment: "//" /[^\n]*/ "\n"
           | "/*" /(.|\n)/* "*/"

    NAME: /[a-zA-Z_]\w*/
    INT: /[+-]?\d+/
    FLOAT: /[+-]?\d+\.\d+/
    STRING: /"[^"]*"/

    %import common.WS
    %ignore WS
"""


# Класс для преобразования дерева AST в более удобный формат
@v_args(inline=True)
class CSharpTransformer(Transformer):
    def start(self, *args):
        return args[0]

    def type_declaration(self, *args):
        return args[0]

    def class_declaration(self, *args):
        return ('class', args[0], args[1:])

    def struct_declaration(self, *args):
        return ('struct', args[0], args[1:])

    def interface_declaration(self, *args):
        return ('interface', args[0], args[1:])

    def class_member(self, *args):
        return args[0]

    def interface_member(self, *args):
        return args[0]

    def method_declaration(self, *args):
        if args[0]=='static':
            if len(args) == 4:
                return('static method', args[1], args[2], None, args[3])
            return ('static method', args[1], args[2], args[3], args[4])
        if len(args)==3:
            return('method', args[0], args[1], None, args[2])
        return ('method', args[0], args[1], args[2], args[3])
    
    def static(self, *args):
        return 'static'

    def property_declaration(self, *args):
        return ('property', args[0], args[1], args[2:])

    def field_declaration(self, *args):
        if len(args) == 2:
            return ('field', args[0], args[1])
        return ('static field', args[1], args[2])

    def return_stmt(self, *args):
        return list(args)

    def parameter_list(self, *args):
        return list(args)

    def parameter(self, *args):
        if len(args)==3:
            if args[0]==None:
                return (args[1], args[2])
            return (args[0], args[1], args[2])
        return (args[0], args[1])

    def method_body(self, *args):
        return list(args)

    def property_call(self, token):
        return token.value

    def property_accessor(self, *args):
        return args[0]
    
    def expression(self, *args):
        if len(args) == 1:
            return args[0]
        return (args[1], args[0], args[2])
    
    def term(self, *args):
        if len(args) == 1:
            return args[0]
        return (args[1], args[0], args[2])

    def factor(self, *args):
        return args[0]

    def get_accessor(self, *args):
        return 'get'

    def set_accessor(self, *args):
        return 'set'
    
    def for_loop(self, *args):
        return ('for_loop', args[0], args[1], args[2], args[3:])
    
    def for_initializer(self, *args):
        return args[0]
    
    def for_condition(self, *args):
        return args[0]
    
    def for_iterator(self, *args):
        if len(args)==2:
            return ('=', args[0], args[1])
        return args[0]
    
    def operator_if(self, *args):
        return ('if', args[0], args[1])
    
    def if_condition(self, *args):
        return args[0]

    def comparison(self, *args):
        return (args[1], args[0], args[2])

    def statement(self, *args):
        return args[0]

    def assignment(self, *args):
        return ('=', args[0], args[1])

    def declaration(self, *args):
        return ('=', args[1], args[2])

    def method_call(self, *args):
        return (args[0], args[1:])

    def increment(self, *args):
        return ('++', args[0])

    def decrement(self, *args):
        return ('--', args[0])

    def expression_list(self, *args):
        return list(args)

    def expression(self, *args):
        if len(args) == 1:
            return args[0]
        else:
            return tuple(args)

    def base_type(self, *args):
        return args[0]
    
    def arr_type(self, *args):
        return args[0] + "[]"
    
    def type(self, *args):
        return args[0]
    
    def return_type(self, *args):
        return args[0]

    def NAME(self, token):
        return token.value
    
    def add(self, *args):
        return ('add', args[0], args[1])
    
    def sub(self, *args):
        return ('sub', args[0], args[1])
    
    def mul(self, *args):
        return ('mul', args[0], args[1])
    
    def div(self, *args):
        return ('div', args[0], args[1])

    def eq(self, *args):
        return ('eq', args[0], args[1])
    
    def neq(self, *args):
        return ('neq', args[0], args[1])
    
    def gte(self, *args):
        return ('gte', args[0], args[1])
    
    def gt(self, *args):
        return ('gt', args[0], args[1])
    
    def lt(self, *args):
        return ('lt', args[0], args[1])
    
    def lte(self, *args):
        return ('lte', args[0], args[1])

    def int(self, token):
        return int(token)

    def float(self, token):
        return float(token)

    def string(self, token):
        return token[1:-1]  # удаляем кавычки из строки

    def int_type(self, *args):
        return 'int'

    def float_type(self, *args):
        return 'float'

    def string_type(self, *args):
        return 'string'

    def void_type(self, *args):
        return 'void'

def compile_csharp(code):
    parser = Lark(grammar, parser='lalr', transformer=CSharpTransformer())
    ast = parser.parse(code)
    return ast


from anytree import NodeMixin, RenderTree


class AstNode(NodeMixin):
    def __init__(self, name, parent=None, children=None):
        super(AstNode, self).__init__()
        self.name = name
        self.parent = parent
        if children:
            self.children = children

    def __str__(self):
        return self.name

def ast_to_tree(ast):
    if isinstance(ast, tuple):
        node = AstNode(ast[0])
        for sub_ast in ast[1:]:
            child = ast_to_tree(sub_ast)
            child.parent = node
        return node
    elif isinstance(ast, list):
        node = AstNode("list")
        for sub_ast in ast:
            child = ast_to_tree(sub_ast)
            child.parent = node
        return node
    else:
        return AstNode(str(ast))

ast = compile_csharp(code1)

ast_tree = ast_to_tree(ast)
for pre, _, node in RenderTree(ast_tree):
    print(f"{pre}{node.name}")


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







