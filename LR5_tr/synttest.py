from lark import Lark, Transformer, v_args
from lark.tree import pydot__tree_to_png

import lexical

    # comment: /[/](2)[a-zA-Z!@#$%^&*(){}[];,._-=+]*/

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

code = """
class Program
{
    static void Swap(ref int current, ref int next)
    {
        
        int temp = current;
        current = next;
        next = temp;
        int s = temp;
        int b;
        b--;

    }
    static int[] BubbleSort(int[] array)
    {
        int len = array.Length;
        for (int i = 1; i < len; i++)
        {
            for (int j = 0; j < len - i; j++)
            {
                if (array[j] == array[j + 1])
                {
                    Swap(ref array[j], ref array[j + 1]);
                }
            }
        }

        return array;
    }

    static void Main(string[] args)
    {
        var parts = Console.ReadLine();
        var array = new int[parts.Length];
        for (int i = 0; i < parts.Length; i++)
        {
            array[i] = Convert.ToInt32(parts[i]);
        }

        Console.ReadLine();
    }
}
"""

code1 = """
class Program
{

    static void Swap(int current, int next)
    {
        
        int temp = current;
        current = next;
        next = temp;
        int s = temp;
        int b;
    }

    static void bubbleSort(string[] args)
    {
        int len = arr;
        for (int i = 1; i < len; i++)
        {
            for (int j = 0; j < len - i; j++)
            {
                if (arrayj == arr)
                {
                    Swap(arrayj, arr + 1);
                }
            }
        }

        return arr;
    }
}
"""


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


#def print_ast(ast, indent=0):
 #   if isinstance(ast, tuple):
  #      node_type = str(ast[0])
   #     node_children = ast[1:]
#
 #       print(' ' * indent + node_type)
#
 #       for child in node_children:
  #          print_ast(child, indent + 4)
   # elif isinstance(ast, list):
    #    for element in ast:
     #       print_ast(element, indent)
    #else:
     #   print(' ' * indent + str(ast))


#
