import clr
import System
import os


import lexical

import synttest



pathDLLSort = os.getcwd() + "\\pythonCompile.dll"









pathDLLByte = os.getcwd() + "\\Bytes.dll"



clr.AddReference(pathDLLSort)
clr.AddReference(pathDLLByte)

# Bubble Sort Started

from pythonCompile import BubbleSort

import System

print(BubbleSort)

print('\n')
print('\n')
print('\n')

code_h = '''
using System;
using System.Text;
using pythonCompile;

public class Program {
    public static void Main() {
        int[] arr = [5, 2, 9, 1, 5, 6];
        BubbleSort.Sort(arr);
        Console.WriteLine(arr);
    }
}

'''
arr = [5, 2, 9, 1, 5, 6]
cs_arr = System.Array.CreateInstance(System.Int32, len(arr))
for i, x in enumerate(arr):
    cs_arr[i] = x
BubbleSort.Sort(cs_arr)
for i in range(len(arr)):
    arr[i] = cs_arr[i]

print(arr)

#print(clr.GetClrType(System.Object).Assembly.ImageRuntimeVersion)
# Bubble Sort Ended



#Byte Code Strted

import Bytes

#print(Bytes)

from Bytes import ByteCode

bytes_c = [104, 101, 108, 108, 111]
string = ByteCode.ConvertBytesToString(bytes_c)
#print(string)  # "hello"

bytes_b = [77, 121, 32, 78, 97, 109, 101, 32, 105, 115, 32, 86, 108, 97, 100]
string_2 = ByteCode.ConvertBytesToString(bytes_b)

#print(string_2) #My Name is Vlad ...


# пример кода на C#
csharp_code = '''
using System;

public class Program {
    public static void Main() {
        Console.WriteLine("Enter array length:");
        int n = Convert.ToInt32(Console.ReadLine());
        int[] arr = new int[n];

        Console.WriteLine("Enter array elements:");
        for (int i = 0; i < n; i++) {
            arr[i] = Convert.ToInt32(Console.ReadLine());
        }

        Console.WriteLine("Before sorting:");
        Console.WriteLine(string.Join(", ", arr));

        Sort(arr);

        Console.WriteLine("After sorting:");
        Console.WriteLine(string.Join(", ", arr));
    }

    public static void Sort(int[] arr) {
        int n = arr.Length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
}
'''


byte_code = '''

using System;
using System.Text;

public class Program {
    public static void Main() {
        byte[] bytes = {72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100};
        string result = ConvertBytesToString(bytes);
        Console.WriteLine(result);
    }

    public static string ConvertBytesToString(byte[] bytes) {
        return Encoding.ASCII.GetString(bytes);
    }
}

'''


byte_code_user='''
using System;
using System.Text;

public class Program {
    public static void Main() {
        Console.WriteLine("Введите строку: ");
        string inputString = Console.ReadLine();
        byte[] bytes = Encoding.ASCII.GetBytes(inputString);
        Console.WriteLine("Массив байт:");
        Console.WriteLine(string.Join(", ", bytes));
    }

    public static string ConvertBytesToString(byte[] bytes) {
        return Encoding.ASCII.GetString(bytes);
    }
}
'''


bnr_srch = '''
using System;

public class Program {
    public static void Main() {

        int x = 5;

        x = 3;

        string s = "hello";


        int[] arr = {1, 2, 3, 4, 5, 6};
        int searchValue = 4;
        Console.WriteLine("Array: {0}", string.Join(", ", arr));
        Console.WriteLine("Searching for: {0}", searchValue);

        int result = BinarySearch(arr, searchValue);

        if (result == -1) {
            Console.WriteLine("Value not found");
        } else {
            Console.WriteLine("Value found at index: {0}", result);
        }
    }

    public static int BinarySearch(int[] arr, int value) {
        int left = 0;
        int right = arr.Length - 1;
        while (left <= right) {
            int mid = (left + right) / 2;
            if (arr[mid] == value) {
                return mid;
            } else if (arr[mid] < value) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }
}
'''

code_h = '''
using System;
using System.Collections;

class Program
{
    public static void Main()
    {
        Hashtable hashtable = new Hashtable();
        hashtable.Add("key1", "value1");
        hashtable.Add("key2", "value2");
        hashtable.Add("key3", "value3");

        Console.WriteLine(hashtable["key1"]);
        Console.WriteLine(hashtable["key2"]);
        Console.WriteLine(hashtable["key3"]);
    }
}
'''


code_h2 = '''

using System;

public class HashTable
{
    private int size;
    private string[] keys;
    private string[] values;

    public HashTable(int size)
    {
        this.size = size;
        keys = new string[size];
        values = new string[size];
    }

    private int HashFunction(string key)
    {
        int hash = 0;
        for (int i = 0; i < key.Length; i++)
        {
            hash += key[i];
        }
        return hash % size;
    }

    public void Add(string key, string value)
    {
        int index = HashFunction(key);
        while (keys[index] != null && keys[index] != key)
        {
            index = (index + 1) % size;
        }
        keys[index] = key;
        values[index] = value;
    }

    public string Get(string key)
    {
        int index = HashFunction(key);
        while (keys[index] != null)
        {
            if (keys[index] == key)
            {
                return values[index];
            }
            index = (index + 1) % size;
        }
        return null;
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        HashTable ht = new HashTable(10);

        ht.Add("one", "1");
        ht.Add("two", "2");
        ht.Add("three", "3");

        Console.WriteLine(ht.Get("one"));
        Console.WriteLine(ht.Get("two"));
        Console.WriteLine(ht.Get("three"));
    }
}

'''


def check_undeclared_variables(code):
    # регулярное выражение для поиска необъявленных переменных
    pattern = r'\b([a-zA-Z_]\w*)\b'
    variables = set(re.findall(pattern, code)) # получение списка всех переменных в коде
    declared_variables = {'int', 'float', 'double', 'char', 'string', 'bool'} # список зарезервированных переменных
    undeclared_variables = variables - declared_variables # нахождение необъявленных переменных

    if len(undeclared_variables) > 0:
        raise ValueError('Найдены необъявленные переменные: {}'.format(', '.join(undeclared_variables)))



def check_variable_types(code):
    # регулярное выражение для поиска типов переменных
    pattern = r'\b(int|float|double|char|string|bool)\b\s+([a-zA-Z_]\w*)\s*=?\s*([a-zA-Z_]\w*)?'
    variable_matches = re.findall(pattern, code)

    for match in variable_matches:
        variable_type, variable_name, variable_value = match

        # проверка типа переменной
        if variable_value and variable_type not in variable_value:
            raise TypeError('Переменная {} должна иметь тип {}, а получен тип {}'.format(variable_name, variable_type, type(variable_value).__name__))


def check_unused_variables(code):
    # регулярное выражение для поиска используемых переменных
    pattern = r'\b([a-zA-Z_]\w*)\b'
    used_variables = set(re.findall(pattern, code))

    # регулярное выражение для поиска объявленных переменных
    pattern = r'\b(int|float|double|char|string|bool)\b\s+([a-zA-Z_]\w*)\s*=?'
    declared_variables = set([match[1] for match in re.findall(pattern, code)])

    unused_variables = declared_variables - used_variables

    if len(unused_variables) > 0:
        raise ValueError('Обнаружены неиспользуемые переменные: {}'.format(', '.join(unused_variables)))



import operator

# Доступные операторы и соответствующие им функции
OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

def evaluate_expression(expr):
    # Разбиваем строку на список токенов
    tokens = expr.split()

    # Стек для хранения операндов
    stack = []

    for token in tokens:
        if token.isdigit():
            # Если токен является числом, добавляем его на стек
            stack.append(int(token))
        elif token in OPS:
            # Если токен является оператором, извлекаем два операнда из стека,
            # применяем к ним оператор и добавляем результат на стек
            op2, op1 = stack.pop(), stack.pop()
            result = OPS[token](op1, op2)
            stack.append(result)
        else:
            # Если токен не является ни числом, ни оператором, возбуждаем исключение
            raise ValueError(f"Неизвестный токен: {token}")

    # После обработки всех токенов результат находится на вершине стека
    if len(stack) != 1:
        raise ValueError("Неправильный формат выражения")
    return stack.pop()



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



def check_unimplemented_methods(code):
    # регулярное выражение для поиска объявления интерфейсов
    pattern = r'\binterface\s+(\w+)\s*{([^}]*)}'
    interface_matches = re.findall(pattern, code)

    for interface_match in interface_matches:
        interface_name, interface_body = interface_match


# компиляция и выполнение кода на C#

def run_csharp_code(code: str) -> None:
    # добавление ссылки на mscorlib
    clr.AddReference('mscorlib')

    # компиляция исходного кода на C#
    provider = System.CodeDom.Compiler.CodeDomProvider.CreateProvider('CSharp')
    parameters = System.CodeDom.Compiler.CompilerParameters(['mscorlib.dll'])
    result = provider.CompileAssemblyFromSource(parameters, code)

    # проверка на наличие ошибок при компиляции
    if result.Errors.HasErrors:
        error_messages = []

        for error in result.Errors:
            if hasattr(error, 'Severity') and error.Severity == System.CodeDom.Compiler.CompilerErrorSeverity.Error:
                error_message = f"Ошибка компиляции в строке {error.Line}: {error.ErrorText}"
                error_messages.append(error_message)

            elif hasattr(error, 'ErrorNumber'):
                if error.ErrorNumber == 'CS0029':
                    error_message = f"Ошибка: несоответствие типов данных в строке {error.Line}"
                    error_messages.append(error_message)

                elif error.ErrorNumber == 'CS0019':
                    error_message = f"Ошибка: неправильное использование оператора в строке {error.Line}"
                    error_messages.append(error_message)

                elif error.ErrorNumber == 'CS0103':
                    error_message = f"Ошибка: использование неопределенной переменной или метода в строке {error.Line}"
                    error_messages.append(error_message)

                elif error.ErrorNumber == 'CS1525':
                    error_message = f"Ошибка: неправильный уровень вложенности в строке {error.Line}"
                    error_messages.append(error_message)
                    
                # Проверка на неправильное количество аргументов
                elif error.ErrorNumber == 'CS1501':
                    error_message = f"Ошибка: неправильное количество аргументов в строке {error.Line}"
                    error_messages.append(error_message)
                    
                # Проверка на неправильный тип аргумента
                elif error.ErrorNumber == 'CS1503':
                    error_message = f"Ошибка: неправильный тип аргумента в строке {error.Line}"
                    error_messages.append(error_message)
            print(f"Error: {error.ErrorText}" + f" Line: {error.Line}")
            print('\n')
        raise ValueError('\n'.join(error_messages))



    # получение экземпляра метода Main()
    main_method = result.CompiledAssembly.GetType('Program').GetMethod('Main')

    # вызов метода Main() и получение результата его выполнения
    main_method.Invoke(None, None)


# запуск кода на C#
#run_csharp_code(bnr_srch)