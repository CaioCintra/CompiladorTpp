import tppparser
import pandas as pd

global dataFrameVar 
dataFrameVar = pd.DataFrame(data = [], columns = ['TOKEN', 'LEXEMA', 'TIPO', 'DIM','TAM_DIM', 'INIT'])
global dataFrameFunc 
dataFrameFunc = pd.DataFrame(data = [], columns = ['TOKEN', 'LEXEMA', 'QTD_PARAM', 'PARAMETROS', 'TIPO', 'RETORNO'])

def treeTravel(root):
    global dataFrameVar 
    global dataFrameFunc
    listNode = ''
    for node in root.children:
        parametros = [ ]
        if (node.label == 'declaracao_variaveis'):
            token = node.children[2].children[0].children[0].label
            lexema = node.children[2].children[0].children[0].children[0].label
            tipo = node.children[0].children[0].label
            if(len(node.children[2].children[0].children)>1):
                dim = 1
                tam_dim = node.children[2].children[0].children[1].children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].label
            else:
                dim = 0
                tam_dim = 0
            dataFrameVar = dataFrameVar.append({'TOKEN' : token, 'LEXEMA' : lexema, 'TIPO' : tipo, 'DIM': dim, 'TAM_DIM': tam_dim, 'INIT': 'N'}, ignore_index=True)

        if (node.label == 'atribuicao'):
          for ind in dataFrameVar.index:
            if(dataFrameVar['LEXEMA'][ind] == node.children[0].children[0].children[0].label):
                dataFrameVar['INIT'][ind] = node.children[2].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].label
                              
        if (node.label == 'declaracao_funcao'):
            tipo = node.children[0].children[0].label
            token = node.children[1].children[0].label
            lexema = node.children[1].children[0].children[0].label
            retorno = 'vazio'
            qtd_param = 0
            
            if (node.children[1].children[2].label == 'lista_parametros'):
                if (node.children[1].children[2].children[0].label != 'vazio'):
                    if (node.children[1].children[2].children[0].label == 'lista_parametros'):
                        if (node.children[1].children[2].children[0].children[0].children[2].children[0].label != None):
                            id = node.children[1].children[2].children[0].children[0].children[2].children[0].label
                            a = id+' '
                            parametros.append(a)
                            qtd_param = qtd_param + 1 
                            son = len(node.children[1].children[2].children)
                            for i in range (2,son,2):
                                id = node.children[1].children[2].children[i].children[2].children[0].label
                                a = id+' '
                                parametros.append(a)
                                qtd_param = qtd_param + 1 
                    else:
                        if (node.children[1].children[2].children[0].children[2].children[0].label != None):
                            id = node.children[1].children[2].children[0].children[2].children[0].label
                            a = id+' '
                            parametros.append(a)
                            qtd_param = qtd_param + 1 
                            
                else:
                    parametros = 'vazio'
                
            if(node.children[1].children[4].children[1].children[0].label == 'retorna'):
                if(node.children[1].children[4].children[1].children[0].children[1].label == 'ABRE_PARENTESE'):
                    retorno = node.children[1].children[4].children[1].children[0].children[2].label
            dataFrameFunc = dataFrameFunc.append({'TOKEN' : token, 'LEXEMA' : lexema,'QTD_PARAM': qtd_param, 'PARAMETROS' : parametros, 'TIPO' : tipo, 'RETORNO' : retorno}, ignore_index=True)
        
        if (node.label == 'chamada_funcao'):
            funcCalled = node.children[0].children[0].label
            funcExists = 0
            for ind in dataFrameFunc.index:
                if(dataFrameFunc['LEXEMA'][ind] == funcCalled):
                    funcExists = 1
            if(funcExists == 0):
                print('\nErro: Chamada a função',funcCalled,'que não foi declarada')
            else:
                funcParam = ((len(node.children[2].children)-1)/2)+1
                for ind in dataFrameFunc.index:
                    if(dataFrameFunc['LEXEMA'][ind] == funcCalled):
                        if(int(dataFrameFunc['QTD_PARAM'][ind]) > funcParam):
                            print('\nErro: Chamada à função ',funcCalled,' com número de parâmetros menor que o declarado')
                        if(int(dataFrameFunc['QTD_PARAM'][ind]) < funcParam):
                            print(funcParam)
                            print('\nErro: Chamada à função ',funcCalled,' com número de parâmetros maior que o declarado')

        listNode = treeTravel(node)       

    return listNode

def main():
    print ('\n\n')
    tree = tppparser.main()
    treeCall = treeTravel(tree)
    global dataFrameVar
    global dataFrameFunc
    for ind in dataFrameVar.index:
        if(dataFrameVar['INIT'][ind] == 'N'):
            print('\nAviso: Variável',dataFrameVar['LEXEMA'][ind],'declarada e não utilizada')
        if(dataFrameVar['TAM_DIM'][ind] != 0 and float(dataFrameVar['TAM_DIM'][ind]) % 1 != '0'):
            print('\nErro: índice de array',dataFrameVar['LEXEMA'][ind],'não inteiro')
    for ind in dataFrameFunc.index:
        if(dataFrameFunc['RETORNO'][ind] == 'vazio'):
            print('\nErro: Função',dataFrameFunc['LEXEMA'][ind],'deveria retornar',dataFrameFunc['TIPO'][ind],', mas retorna vazio')
    if (len(dataFrameFunc) == 0):
        print('\nErro: Função principal não declarada')

    if (len(dataFrameVar) != 0):
        print ('\nTabela de Símbolos')
        print (dataFrameVar)
        print ('\n')

    if (len(dataFrameFunc) != 0):
        print ('\nTabela de Funções')
        print (dataFrameFunc)
        print ('\n')

    print ('\n')
if __name__ == "__main__":
    main()