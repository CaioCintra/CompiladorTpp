import tppsemantic
import tppparser
from llvmlite import ir
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

    temp = ir.GlobalVariable(module, _type, name)
    temp.initializer = ir.Constant(_type, 0)
    temp.align = 4

    return temp

def varDeclare(name: str, _type: ir.Type, module) -> ir.AllocaInstr:
    global bloco

    temp = bloco.alloca(_type, name=name)

    temp.align = 4
    constant = ir.Constant(_type, 0)
    bloco.store(constant, temp)

    return temp

def treeTravel(root, module):
    global builder
    for node in root.children:
        if(node.label == 'declaracao_variaveis'):                       #Declaração de variável
            name = node.children[1].label
            Type = Type = ir.IntType(32)
            if(node.children[0].label == 'flutuante'):
                Type = Type = ir.FloatType()
            if(node.parent.label == 'programa'):
                globalVar(name,Type,module) 
            # else:
            #     varDeclare(name,Type,module)  

            if(node.label == 'acao' and len(node.children) > 1):            #Atribuição
                if(node.children[1].label == ':='):    
                    value1 = node.children[0].label
                    value2 = node.children[2].label
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

                retorno = builder.alloca(ir.IntType(32), name='retorno')

                retorno.align = 4

                returnValue = 0
                returnValue = node.children[2].children[1].children[0].children[0].label
                value32 = ir.Constant(ir.IntType(32), returnValue)              #retornando o nome da variável

                builder.store(value32, retorno) 
                builder.branch(endBasicBlock)

                builder.position_at_end(endBasicBlock)

                returnVal_temp = builder.load(retorno, name='ret_temp', align=4)
                builder.ret(returnVal_temp)
                

            

        listNode = treeTravel(node,module) 

def main():
    tree = tppsemantic.main()
    print(tree)
    module = moduleCreate()
    treeTravel(tree,module)
    moduleSave(module)

if __name__ == "__main__":
    main()