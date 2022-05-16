import tppparser
import pandas as pd

global dataFrameVar 
dataFrameVar = pd.DataFrame(data = [], columns = ['TOKEN', 'LEXEMA', 'TIPO'])
global dataFrameFunc 
dataFrameFunc = pd.DataFrame(data = [], columns = ['TOKEN', 'LEXEMA', 'PARAMETROS', 'TIPO'])

def treeTravel(root):
    global dataFrameVar 
    global dataFrameFunc
    listNode = ''
    for node in root.children:
        #print(node.label)
        if (node.label == 'declaracao_variaveis'):
            token = node.children[2].children[0].children[0].label
            lexema = node.children[2].children[0].children[0].children[0].label
            tipo = node.children[0].children[0].label
            dataFrameVar = dataFrameVar.append({'TOKEN' : token, 'LEXEMA' : lexema, 'TIPO' : tipo}, ignore_index=True)

        if (node.label == 'declaracao_funcao'):
            tipo = node.children[0].children[0].label
            token = node.children[1].children[0].label
            lexema = node.children[1].children[0].children[0].label
            parametros = 0
            dataFrameFunc = dataFrameFunc.append({'TOKEN' : token, 'LEXEMA' : lexema, 'PARAMETROS' : parametros, 'TIPO' : tipo}, ignore_index=True)
        listNode = treeTravel(node)
    return listNode

def main():
    tree = tppparser.main()

    treeCall = treeTravel(tree)
    print ('\nTabela de Símbolos')
    print (dataFrameVar)

    print ('\nTabela de Funções')
    print (dataFrameFunc)
    

if __name__ == "__main__":
    main()