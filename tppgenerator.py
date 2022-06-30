import tppsemantic
import tppparser
from llvmlite import ir
from llvmlite import binding as llvm

global endBasicBlock

global variables
variables = {}

global builder

def moduleCreate():
    global escrevaInteiro, escrevaFlutuante, leiaInteiro, leiaFlutuante
    module = ir.Module('modulo.bc')
    escrevaInteiro = ir.Function(module, ir.FunctionType(ir.VoidType(), [ir.IntType(32)]), name="escrevaInteiro")
    leiaInteiro = ir.Function(module, ir.FunctionType(ir.IntType(32), []), name="leiaInteiro")
    escrevaFlutuante = ir.Function(module, ir.FunctionType(ir.VoidType(), [ir.FloatType()]), name="escrevaFlutuante")
    leiaFlutuante = ir.Function(module, ir.FunctionType(ir.FloatType(), []), name="leiaFlutuante")
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
    

    return temp

def treeTravel(root, module):
    global builder
    global variables
    global endBasicBlock
    global ifSe
    global ifSe2
    global main
    global ifRepita
    global listEnd
    global loop
    global validate
    global escrevaInteiro, escrevaFlutuante, leiaInteiro, leiaFlutuante
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

                if(len(node.children)>3):
                    var1 = node.children[2].label
                    var2 = node.children[4].label
                    op = node.children[3].label
                    var1 = variables.get(var1)
                    if(op == '+'):
                        var2 = variables.get(var2)
                        operation = builder.add(builder.load(var1),builder.load(var2),name='add')
                    else:
                        var2 = ir.Constant(ir.IntType(32),int(var2))
                        operation = builder.sub(builder.load(var1),var2,name='sub')
                    builder.store(operation,value1)
                else:
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
                    if(len(aux.children)>1):
                        if(len(aux.children)>1):
                            if(aux.children[1].children[0].label == 'se' and aux.children[1].children[0].children[0].label == 'corpo'):
                                if(not ifSe):

                                    pass
                                elif(aux.children[1].children[0].label == 'fim'):
                                    if(aux.children[1].children[0].parent.label == 'se'):
                                        pass
                                        
                            elif(aux.children[1].children[0].label == 'se' and aux.children[1].children[0].children[1].label == 'corpo'):
                                if(ifSe):
                                    pass
       
                    aux = aux.parent

        if(node.label == 'se'):
            if(ifSe == None):
                iftrue_1 = main.append_basic_block('iftrue_1')
                iffalse_1 = main.append_basic_block('iffalse_1')
                listEnd.append(iffalse_1)

                name = node.children[2].label    #a
                signal = node.children[3].label  #>
                name2 = node.children[4].label   #5
                ifSe = True
                nameLoad = variables.get(name)
                nameVar = variables[name]

                name2Key = variables.get(name2)
            
                if(name2Key != None):

                    name2Var = variables[name2]
                    name2 = builder.load(name2Var,"")
                else:
                    name2 = int(name2)
                    name2 = ir.Constant(ir.IntType(32),name2)


                a_cmp = builder.load(nameLoad, 'a_cmp', align=4)
                b_cmp = name2


                If_1 = builder.icmp_signed(signal, a_cmp, b_cmp, name='if_test_1')
                builder.cbranch(If_1, iftrue_1, iffalse_1)

                builder.position_at_end(iftrue_1)
            elif(ifSe2 == None):
                iftrue_1 = main.append_basic_block('iftrue_1')
                iffalse_1 = main.append_basic_block('iffalse_1')
                listEnd.append(iffalse_1)

                name = node.children[2].label    #a
                signal = node.children[3].label  #>
                name2 = node.children[4].label   #5
                ifSe2 = True
                nameLoad = variables.get(name)
                nameVar = variables[name]

                name2Key = variables.get(name2)
            
                if(name2Key != None):

                    name2Var = variables[name2]
                    name2 = builder.load(name2Var,"")
                else:
                    name2 = int(name2)
                    name2 = ir.Constant(ir.IntType(32),name2)


                a_cmp = builder.load(nameLoad, 'a_cmp', align=4)
                b_cmp = name2


                If_1 = builder.icmp_signed(signal, a_cmp, b_cmp, name='if_test_1')
                builder.cbranch(If_1, iftrue_1, iffalse_1)

                builder.position_at_end(iftrue_1)
        if(node.label == 'corpo'):
            if(ifSe2 != None):

                if(ifSe2):
                    ifSe2 = False

                elif(not ifSe2):
                    builder.branch(endBasicBlock)
                    builder.position_at_end(listEnd.pop())
                    ifSe2 = None
            elif(ifSe != None):

                if(ifSe):
                    ifSe = False

                elif(not ifSe):
                    builder.branch(endBasicBlock)
                    builder.position_at_end(listEnd.pop())
                    ifSe = None
        if(node.label == 'repita'):
            ifRepita = True
            validate = main.append_basic_block('validate')
            loop = main.append_basic_block('loop')
            listEnd.append(endBasicBlock)
            builder.branch(loop)
            builder.position_at_end(loop)

            
        if(node.label == 'até'): 
            builder.branch(validate)
            builder.position_at_end(validate)
            name = node.parent.children[2].label    #a
            signal = node.parent.children[3].label  #>
            name2 = node.parent.children[4].label   #5
            nameLoad = variables.get(name)
            nameVar = variables[name]

            name2Key = variables.get(name2)
        
            if(name2Key != None):

                name2Var = variables[name2]
                name2 = builder.load(name2Var,"")
            else:
                name2 = int(name2)
                name2 = ir.Constant(ir.IntType(32),name2)


            a_cmp = builder.load(nameLoad, 'a_cmp', align=4)
            b_cmp = name2

            if(signal == '='):
                signal = '=='
            If_1 = builder.icmp_signed(signal, a_cmp, b_cmp, name='if_test_1')
            returnAte = listEnd.pop()
            builder.cbranch(If_1, returnAte, loop)
            builder.position_at_end(returnAte)

        if(node.label == 'escreva'):
           var1 = node.children[0].label
           var1 = builder.load(variables.get(var1))
           builder.call(escrevaInteiro,[var1]) 

        if(node.label == 'retorna'): 
            if(ifRepita == None):
                builder.branch(endBasicBlock)
            builder.position_at_end(endBasicBlock)

            retorno = builder.alloca(ir.IntType(32), name='retorno')

            retorno.align = 4
            returnValue = 0

            if(len(node.children) == 1):

                returnValue = node.children[0].label
                returnKey = variables.get(returnValue)
                if(returnKey != None):
                    returnVar = variables[returnValue]
                    returnValue = builder.load(returnVar,"")
                else:
                    returnValue = int(returnValue)
                    returnValue = ir.Constant(ir.IntType(32), returnValue)
            builder.ret(returnValue)
            print(str(module))          
                

            

        listNode = treeTravel(node,module) 

def main():
    global ifSe, ifSe2, ifRepita, listEnd, loop, validate
    listEnd = []
    ifSe = None
    ifSe2 = None
    ifRepita = None
    loop = None
    tree = tppsemantic.main()
    print(tree)
    module = moduleCreate()
    treeTravel(tree,module)
    moduleSave(module)

if __name__ == "__main__":
    main()