from syntax import Tree

from lexical import tokens


#корректный скоп видимости использования переменной

def check_variable_in_scope(self, var_name):
    curr_scope = self.curr_scope
    while curr_scope is not None:
        if var_n in curr_scope.variables:
            return True
        curr_scope = curr_scope.parent
    return False

#Это правило выполняет оператор присваивания, который состоит из левой и правой частей.

#ошибки выводит с помощью того же метода из lexicpy report_error

def check_assign_correct(self, node):
    var_name = node.left.value
    if not self.check_variable_in_scope(var_name):
        self.report_error(f"Переменная {var_name} не определена", node.pos_start, node.pos_end)
        return None
    var_value = self.execute(node.right)
    if isinstance(var_value, Error):
        return var_value
    self.current_scope.assign_variable(var_name, var_value)
    return var_value

