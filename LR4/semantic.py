from syntax import Tree

from lexical import tokens


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

#корректный скоп видимости использования переменной

def check_variable_in_scope(self, var_name):
    current_scope = self.current_scope
    while current_scope is not None:
        if var_name in current_scope.variables:
            return True
        current_scope = current_scope.parent
    return False