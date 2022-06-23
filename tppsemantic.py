import tppparser
import pandas as pd

global dataFrameVar 
dataFrameVar = pd.DataFrame(data = [], columns = ['TOKEN', 'LEXEMA', 'TIPO', 'DIM','TAM_DIM', 'INIT'])
global dataFrameFunc 
dataFrameFunc = pd.DataFrame(data = [], columns = ['TOKEN', 'LEXEMA', 'QTD_PARAM', 'PARAMETROS', 'TIPO', 'RETORNO'])

def declaredVar(knot):
    global dataFrameVar 
    varExists = -1
    varName = ''
    for node in knot.children:
        if(node.label == 'ID'):
            for ind in range(len(dataFrameFunc)):
                if(node.children[0].label == dataFrameFunc['LEXEMA'][ind]):
                    return
            for ind in range(len(dataFrameVar)):
                if(node.children[0].label == dataFrameVar['LEXEMA'][ind]):
                    varExists = 1
                varName = node.children[0].label

            if(varExists == -1):
                varExists = 0
        declaredVar(node)
    
    if(varExists == 0):
        print('\nErro: Variável',varName,'não declarada')
        return
    return


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
            varFlag = 0
            if(len(node.children[2].children[0].children)>1):
                dim = 1
                tam_dim = node.children[2].children[0].children[1].children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].label
            else:
                dim = 0
                tam_dim = 0
            for f in dataFrameVar.index:
                if(lexema == dataFrameVar['LEXEMA'][f]):
                    varFlag = 1
                    print('\nAviso: Variável',lexema,'já declarada anteriormente')
            if(varFlag == 0):
                dataFrameVar = dataFrameVar.append({'TOKEN' : token, 'LEXEMA' : lexema, 'TIPO' : tipo, 'DIM': dim, 'TAM_DIM': tam_dim, 'INIT': 'N'}, ignore_index=True)

        if (node.label == 'atribuicao'):
            declaredVar(node)

            for ind in dataFrameVar.index:
                if(dataFrameVar['LEXEMA'][ind] == node.children[0].children[0].children[0].label):
                    dataFrameVar['INIT'][ind] = node.children[2].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].label
                    varType = dataFrameVar['TIPO'][ind]
                    for n in dataFrameVar.index:
                        if(dataFrameVar['INIT'][ind] == dataFrameVar['LEXEMA'][n]):
                            if(dataFrameVar['TIPO'][n] != varType):
                                print('\nAviso: Atribuição de tipos distintos',dataFrameVar['LEXEMA'][ind],varType,'e',dataFrameVar['LEXEMA'][n],dataFrameVar['TIPO'][n])  
                    for n in dataFrameFunc.index:
                        if(dataFrameVar['INIT'][ind] == dataFrameFunc['LEXEMA'][n]):
                            if(dataFrameFunc['TIPO'][n] != varType):
                                print('\nAviso: Atribuição de tipos distintos',dataFrameVar['LEXEMA'][ind],varType,'e',dataFrameFunc['LEXEMA'][n],'retorna',dataFrameFunc['TIPO'][n])                    
        if (node.label == 'declaracao_funcao'):
            idx = 1
            tipo = node.children[0].children[0].label
            try: 
                token = node.children[1].children[0].label
                lexema = node.children[1].children[0].children[0].label
            except: 
                token = 'vazio'
                idx = 0
                lexema = node.children[0].children[0].children[0].label
            
            retorno = 'vazio'
            qtd_param = 0
            
            if (node.children[idx].children[2].label == 'lista_parametros'):
                if (node.children[idx].children[2].children[0].label != 'vazio'):
                    if (node.children[idx].children[2].children[0].label == 'lista_parametros'):
                        if (node.children[idx].children[2].children[0].children[0].children[2].children[0].label != None):
                            id = node.children[idx].children[2].children[0].children[0].children[2].children[0].label
                            a = id+' '
                            parametros.append(a)
                            qtd_param = qtd_param + 1 
                            son = len(node.children[idx].children[2].children)
                            for i in range (2,son,2):
                                id = node.children[idx].children[2].children[i].children[2].children[0].label
                                a = id+' '
                                parametros.append(a)
                                qtd_param = qtd_param + 1 
                    else:
                        if (node.children[idx].children[2].children[0].children[2].children[0].label != None):
                            id = node.children[idx].children[2].children[0].children[2].children[0].label
                            a = id+' '
                            parametros.append(a)
                            qtd_param = qtd_param + 1 
                            
                else:
                    parametros = 'vazio'
                
            if(node.children[idx].children[4].children[1].children[0].label == 'retorna'):
                if(node.children[idx].children[4].children[1].children[0].children[1].label == 'ABRE_PARENTESE'):
                    retorno = node.children[idx].children[4].children[1].children[0].children[2].label
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
                            print('\nErro: Chamada à função',funcCalled,'com número de parâmetros menor que o declarado')

        listNode = treeTravel(node)       

    return listNode

def cutTree(knot): #Versão Beta
    blacklist = []
    for node in knot.children:
        print(node.label)
        if(node.label in blacklist):
            node.parent.children = node.children
        cutTree(node)
    return


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
    cutTree(tree)
if __name__ == "__main__":
    main()