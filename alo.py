import sys
sys.path.append("../semantic_analysis")

# import mytree
import pandas as pd
from anytree.search import findall, find_by_attr, findall_by_attr
import tppsemantic
import tppparser

from llvmlite import ir
from llvmlite import binding as llvm

root = None
func_table = None
var_table = None
module = None
vars_dict = {}
atributions_dict = {}
Zero32 = ir.Constant(ir.IntType(32), 0)
builder = None

def get_type(tpp_type):
    if tpp_type == "INTEIRO":
        return ir.IntType(32)
    elif tpp_type == "FLUTUANTE":
        return ir.FloatType()
    elif tpp_type == "VOID":
        return ir.VoidType()

def create_var_util(var_table_index):
    var_dimension = var_table['dim'][var_table_index]
    var_type = get_type(var_table['Tipo'][var_table_index])
    var_name = var_table['Lexema'][var_table_index]
    var_escope = var_table['escopo'][var_table_index]

    if var_dimension == 1:
        var_type = ir.ArrayType(var_type, var_table['tam_dim1'][var_table_index])
    elif var_dimension == 2:
        var_type0 = ir.ArrayType(var_type, var_table['tam_dim1'][var_table_index])
        var_type = ir.ArrayType(var_type0, var_table['tam_dim2'][var_table_index])

    return var_name, var_type, var_dimension, var_escope

def load_value(var):
    if isinstance(var,int):
        return ir.Constant(ir.IntType(32), var)
    elif isinstance(var,float):
        return ir.Constant(ir.FloatType(), var)
    else :
        return builder.load(vars_dict[var]['alloca'], "")

def atribution_util(eq_list):
    stack = eq_list[::-1]
    op = load_value(stack.pop())
    stack.append(op)

    while len(stack)>1:
        var1 = stack.pop()
        op = stack.pop()
        var2 = stack.pop()

        var1 = load_value(var1)
        var2 = load_value(var2)

        if op == "+":
            add_temp = builder.add(var1, var2, name='temp', flags=())
        elif op == "-":
            add_temp = builder.sub(var1, var2, name='temp', flags=())
        elif op == "*":
            add_temp = builder.mul(var1, var2, name='temp', flags=())
        elif op == "/":
            add_temp = builder.fdiv(var1, var2, name='temp', flags=())

        stack.append(add_temp)

    return stack.pop()

def set_atributions(escope):
    
    atributions_list = atributions_dict[escope]

    for atribution in atributions_list:
        temp = atribution_util(atribution[2:])
        var = vars_dict[atribution[0]]['alloca']
        builder.store(temp,var)
        print()
        print(var)
        print()

def get_atributions():
    functions = findall_by_attr(root, 'cabecalho')
    all_function_atribs = []

    for func in functions:
        func_name = func.child().child().name
        atribs = findall_by_attr(func, 'atribuicao')
        all_function_atribs = all_function_atribs + list(atribs)

        atributions_dict[func_name] = [[leaf.name for leaf in atrib.leaves] for atrib in atribs ]

    global_atribs = list(findall_by_attr(root, 'atribuicao'))    
    global_atribs = list(set(global_atribs) - set(all_function_atribs))

    atributions_dict['global'] = [[leaf.name for leaf in atrib.leaves] for atrib in global_atribs ]


def set_global_variables():
    var_indexes = var_table.index[var_table['escopo'] == "global"].tolist()
    
    if var_indexes:
        for index in var_indexes:
            var_name, var_type, var_dimension, var_escope = create_var_util(index)

            var = ir.GlobalVariable(module, var_type, var_name)
            var.align = 4
            var.linkage = "common"
            var.initializer = ir.Constant(var_type, 0)
            
            vars_dict[var_name] = {'alloca' : var, 'escope': var_escope, 'dim': var_dimension, 'type': var_type }

def set_local_variables(indexes):
    
    for index in indexes:
        var_name, var_type, var_dimension, var_escope = create_var_util(index)

        var = builder.alloca(var_type, name=var_name)
        var.align = 4
        var.linkage = "common"
        var.initializer = ir.Constant(var_type, 0)

        vars_dict[var_name] = {'alloca' : var, 'escope': var_escope, 'dim': var_dimension, 'type': var_type }


def set_functions():
    functions = findall_by_attr(root, 'cabecalho')

    for func in functions:
        func_name = func.child().child().name
        row_index = func_table.index[func_table['Nome'] == func_name].tolist()[0]

        func_type = get_type(func_table['Tipo'][row_index])
        func_params_type_list = [get_type(item[0]) for item in func_table['Parametros'][row_index]]
        func_params_name_list = [item[1] for item in func_table['Parametros'][row_index]]
        func_declaration = ir.FunctionType(func_type,func_params_type_list)

        if func_name == "principal":
            func = ir.Function(module, func_declaration, name='main')
        else:
            func = ir.Function(module, func_declaration, name=func_name)
            
        for arg in func.args:
            arg.name = func_params_name_list[func.args.index(arg)]

        entry_block = func.append_basic_block('entry')
        exit_block = func.append_basic_block('exit')

        global builder
        builder = ir.IRBuilder(entry_block)

        var_indexes = var_table.index[var_table['escopo'] == func_name].tolist()

        if var_indexes:
            set_local_variables(var_indexes)

        set_atributions(func_name)

        builder.branch(exit_block)

        builder.position_at_end(exit_block)

        func_return = func_table['Retorna'][row_index][1]
        if isinstance(func_return,str):
            builder.ret(vars_dict[func_return]['alloca'])
        else:
            builder.ret(load_value(func_return))


  

def generate_code():
    set_global_variables()
    get_atributions()
    print(atributions_dict)
    set_functions()

def main():
    global root,func_table,var_table,module
    arg = sys.argv[1]
    if not arg.endswith('.tpp'):
        raise IOError("Not a tpp file!")
    
    data = open(arg, 'r')    
    data.close()

    tree = tppsemantic.main()

    root = tree.root
    func_table = tree.dataFrameFunc
    var_table = tree.dataFrameVar
   

    llvm.initialize()
    llvm.initialize_all_targets()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    module = ir.Module('meu_modulo.bc')
    module.triple = llvm.get_process_triple()
    target = llvm.Target.from_triple(module.triple)
    target_machine = target.create_target_machine()
    module.data_layout = target_machine.target_data


    generate_code()
    tree.set_atribution_asto()
    tree.export_tree()

    arquivo = open('atribuicao.ll', 'w')
    arquivo.write(str(module))
    arquivo.close()
    print(module)
    llvm.shutdown()


if __name__ == '__main__':
    main()