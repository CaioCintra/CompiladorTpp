import tppsemantic
import tppparser
from llvmlite import ir
from llvmlite import binding as llvm

global endBasicBlock

global variables
variables = {}

global builder

def moduleCreate():
    module = ir.Module('modulo.bc')
    return module

def moduleSave(module):
    arquivo = open('modulo.ll', 'w')
    arquivo.write(str(module))
    arquivo.close()
    print('\n',module)

def globalVar(name: str, _type: ir.Type, module) -> ir.GlobalValue:
    global variables
    temp = ir.GlobalVariable(module, _type, name)
    temp.initializer = ir.Constant(_type, 0)
    temp.align = 4
    variables[name] = temp
    print(variables)
    

    return temp

def treeTravel(root, module):
    global builder
    global variables
    global endBasicBlock
    for node in root.children:
        if(node.label == 'declaracao_variaveis' and node.parent.label == 'programa'):                       #Declaração de variável
            name = node.children[1].label
            Type = ir.IntType(32)
            if(node.children[0].label == 'flutuante'):
                Type = ir.FloatType()
            globalVar(name,Type,module) 

        if(node.label == 'acao' and len(node.children) > 1):            #Atribuição
            if(node.children[1].label == ':='):    
                value1 = node.children[0].label
                variablesKey = variables.get(value1)
                if(variablesKey != None):
                    value1 = variables[value1]
                value2 = node.children[2].label
                variablesKey = variables.get(value2)
                if(variablesKey != None):
                    value2Var = variables[value2]
                    # carregando value2Var em uma variável temporária
                    value2 = builder.load(value2Var,"")
                    builder.store(value2, value1)  
                else:
                    value2 = int(value2)
                    builder.store(ir.Constant(ir.IntType(32), value2), value1)  

        if(node.label == 'declaracao_funcao'):                          #Declaração de Função
            if(node.children[0].label == 'inteiro'):
                Type = ir.IntType(32)
                funcType = ir.FunctionType(Type, ())

                name = node.children[1].label
                if(name == 'principal'):
                    name = 'main'
                main = ir.Function(module, funcType, name=str(name))

                entryBlock = main.append_basic_block('entry')
                endBasicBlock = main.append_basic_block('exit')

                builder = ir.IRBuilder(entryBlock)

                aux = node.children[2]
                count = 1
                while(len(aux.children) > 0 and aux.children[0].label == 'corpo'):
                    aux = aux.children[0]
                    count = count + 1
                for corpos in range(count):
                    if(len(aux.children)>0 and aux.children[0].children[0].label == 'declaracao_variaveis'):    #Variável Na Função
                        varType = aux.children[0].children[0].children[0].label
                        name = aux.children[0].children[0].children[1].label
                        value = 0
                        if(varType == 'inteiro'):
                            temp = builder.alloca(ir.IntType(32), name=name)
                            temp.align = 4
                            num1 = ir.Constant(ir.IntType(32),0)
                            builder.store(num1, temp)
                            variables[name] = temp
                        else:
                            temp = builder.alloca(ir.FloatType(32), name=name)
                            temp.align = 4
                            num1 = ir.Constant(ir.FloatType(32),0)
                            builder.store(num1, temp)
                            variables[name] = temp
                            print(variables)
                    if(len(aux.children)>1):
                        if(len(aux.children)>1):
                            if(aux.children[1].children[0].label == 'se'):
                                iftrue_1 = main.append_basic_block('iftrue_1')
                                iffalse_1 = main.append_basic_block('iffalse_1')
                                ifend_1 = main.append_basic_block('ifend_1')

                                cmp1 = builder.load(temp, 'cmp1', align=4)
                                cmp2 = builder.load(temp, 'cmp2', align=4)

                                If_1 = builder.icmp_signed('<', cmp1, cmp2, name='if_test_1')
                                builder.cbranch(If_1, iftrue_1, iffalse_1)

                                builder.position_at_end(iftrue_1)
                                builder.store(ir.Constant(ir.IntType(32), 5), temp)
                                builder.branch(ifend_1)

                                builder.position_at_end(iffalse_1)
                                builder.store(ir.Constant(ir.IntType(32), 6), temp)
                                builder.branch(ifend_1)

                                builder.position_at_end(ifend_1)
       
                    aux = aux.parent

        if(node.label == 'retorna'):           

            builder.branch(endBasicBlock)
            builder.position_at_end(endBasicBlock)

            retorno = builder.alloca(ir.IntType(32), name='retorno')

            retorno.align = 4
            returnValue = 0
            value32 = ir.Constant(ir.IntType(32), 0)

            if(len(node.children) == 1):

                returnValue = node.children[0].label
                returnKey = variables.get(returnValue)
                if(returnKey != None):
                    returnVar = variables[returnValue]
                    returnValue = builder.load(returnVar,"")
                else:
                    returnValue = int(returnValue)
                    value32 = ir.Constant(ir.IntType(32), returnValue)

            builder.ret(returnValue)
                

            

        listNode = treeTravel(node,module) 

def main():
    tree = tppsemantic.main()
    print(tree)
    module = moduleCreate()
    treeTravel(tree,module)
    moduleSave(module)

if __name__ == "__main__":
    main()