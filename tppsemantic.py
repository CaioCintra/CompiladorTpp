import tppparser
import pandas as pd

global dataFrameVar 
dataFrameVar = pd.DataFrame(data = [], columns = ['TOKEN', 'LEXEMA', 'TIPO', 'INIT'])
global dataFrameFunc 
dataFrameFunc = pd.DataFrame(data = [], columns = ['TOKEN', 'LEXEMA', 'PARAMETROS', 'TIPO'])

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
            dataFrameVar = dataFrameVar.append({'TOKEN' : token, 'LEXEMA' : lexema, 'TIPO' : tipo, 'INIT': 'N'}, ignore_index=True)

        if (node.label == 'atribuicao'):
          for ind in dataFrameVar.index:
            if(dataFrameVar['LEXEMA'][ind] == node.children[0].children[0].children[0].label):
                dataFrameVar['INIT'][ind] = node.children[2].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].label
                              
        if (node.label == 'declaracao_funcao'):
            tipo = node.children[0].children[0].label
            token = node.children[1].children[0].label
            lexema = node.children[1].children[0].children[0].label
            
            if (node.children[1].children[2].label == 'lista_parametros'):
                if (node.children[1].children[2].children[0].label != 'vazio'):
                    if (node.children[1].children[2].children[0].label == 'lista_parametros'):
                        if (node.children[1].children[2].children[0].children[0].children[2].children[0].label != None):
                            id = node.children[1].children[2].children[0].children[0].children[2].children[0].label
                            a = id+' '
                            parametros.append(a)
                            son = len(node.children[1].children[2].children)
                            for i in range (2,son,2):
                                id = node.children[1].children[2].children[i].children[2].children[0].label
                                a = id+' '
                                parametros.append(a)
                    else:
                        if (node.children[1].children[2].children[0].children[2].children[0].label != None):
                            id = node.children[1].children[2].children[0].children[2].children[0].label
                            a = id+' '
                            parametros.append(a)
                else:
                    parametros = 'vazio'
            
            dataFrameFunc = dataFrameFunc.append({'TOKEN' : token, 'LEXEMA' : lexema, 'PARAMETROS' : parametros, 'TIPO' : tipo}, ignore_index=True)
        listNode = treeTravel(node)       

    return listNode

def main():
    tree = tppparser.main()
    treeCall = treeTravel(tree)
    print ('\nTabela de Símbolos')
    global dataFrameVar
    print (dataFrameVar)
    print ('\n')

    for ind in dataFrameVar.index:
        if(dataFrameVar['INIT'][ind] == 'N'):
            print('Aviso: Variável',dataFrameVar['LEXEMA'][ind],'declarada e não utilizada')

    global dataFrameFunc
    if (len(dataFrameFunc) != 0):
        print ('\nTabela de Funções')
        print (dataFrameFunc)
        print ('\n')
    else:
        print('\nErro: Função principal não declarada\n')

if __name__ == "__main__":
    main()