def treeTravel(root, module):
    global builder
    for node in root.children:
        if(node.label == 'declaracao_variaveis' and node.parent.label == 'programa'):                       #Declaração de variável
            name = node.children[1].label
            Type = Type = ir.IntType(32)
            if(node.children[0].label == 'flutuante'):
                Type = Type = ir.FloatType()
            globalVar(name,Type,module) 

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

                aux = node.children[2]
                count = 1
                while(len(aux.children) > 0 and aux.children[0].label == 'corpo'):
                    aux = aux.children[0]
                    count = count + 1
                for corpos in range(count):
                    if(aux.children[0].children[0].label == 'declaracao_variaveis'):    #Variável Na Função
                        varType = aux.children[0].children[0].children[0].label
                        name = aux.children[0].children[0].children[1].label
                        value = 0
                        if(varType == 'inteiro'):
                            temp = builder.alloca(ir.IntType(32), name=name)
                            temp.align = 4
                            num1 = ir.Constant(ir.IntType(32),0)
                            builder.store(num1, temp)
                        else:
                            temp = builder.alloca(ir.FloatType(32), name=name)
                            temp.align = 4
                            num1 = ir.Constant(ir.FloatType(32),0)
                            builder.store(num1, temp)
                    if(len(aux.children[0].children)>1 and aux.children[0].children[1].label == ':='):                      #Atribuição
                        name = aux.children[0].children[0].label
                        value = aux.children[0].children[2].label
                        builder.store(ir.Constant(ir.IntType(32), value), name)
                    if(len(aux.children)>1):
                        if(len(aux.children[1].children)>2 and aux.children[1].children[1].label == ':='):                      #Atribuição
                            name = aux.children[1].children[0].label
                            value = aux.children[1].children[2].label
                            builder.store(ir.Constant(ir.IntType(32), value), name)
                        if(len(aux.children)>1):
                            if(aux.children[1].children[0].label == 'se'):
                                print('Se')
       
                    aux = aux.parent
                    


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